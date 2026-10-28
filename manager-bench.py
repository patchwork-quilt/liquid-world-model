#!/usr/bin/env python3
"""manager-bench — the qw manager bench as one re-runnable script.

Any OpenAI-style or Ollama endpoint + a model id -> a full manager arm with
receipts, on the experiment design frozen in rounds 1-2 (QW-MANAGER.md /
QW-REMATCH.md, patchwork-quilt/liquid-world-model):

  - 10 fixed DCSS seeds (101-110), 5 frozen briefs (briefs vendored verbatim
    from qw-rematch/scripts/briefs.json);
  - the manager prompt byte-identical to rounds 1-2 (vendored verbatim from
    qw-rematch/scripts/manager.py, differential-tested against the rig);
  - ONE call per brief at temperature 0 via the endpoint's native API
    (rounds 1-2 used the Oracle farm's raw-completion default, temp 0.7;
    temperature + transport are part of the arm definition, stated in every
    receipt);
  - the rounds 1-2 mechanical validator, vendored verbatim: invalid ->
    stock rc, counted as a fallback, never repaired, never retried;
  - games on the Oracle rig (stock qw @ 8698adc + crawl 0.32.1, the pty
    driver from qw-rematch/scripts), caps 1800 s wall / 200,000 turns;
  - control receipts are round 1's, gated by a determinism spot-check
    (control seed 101 must reproduce round 1 exactly before any arm runs).

Phases (gen and play are separate because the brains and the game usually
live on different boxes — e.g. gen on the Thor next to its resident models,
play on the Oracle next to crawl):

  manager-bench.py selftest
  manager-bench.py gen  --base-url http://localhost:8001 \
                        --model Qwen3-Coder-30B-A3B-Instruct \
                        --dialect openai --arm arm3-coder30b --out DIR
  manager-bench.py gen  --base-url http://localhost:11434 \
                        --model nemotron-3.5-lightning:latest \
                        --dialect ollama --arm arm4-nemotron --out DIR
  manager-bench.py play --arm arm3-coder30b --root DIR [--jobs 2]
                        (Oracle only; writes results-<arm>.json into DIR)

`gen` writes DIR/arms/<arm>/manager-<seed>.json + arm.json.
`play` reads them, writes DIR/runs/<arm>-<seed>/ (rc, logs, morgue) and
DIR/results-<arm>.json including the manager artefacts and the spot-check.

Stdlib only. No retries: a transport error is receipted as that seed's
verdict (valid=false, errors=['transport: ...'], game falls back, counted).
An endpoint that is down produces an arm of transport errors, stated as such.
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

# ---------------------------------------------------------------------------
# Vendored verbatim from qw-rematch/scripts/briefs.json (frozen round 1).
BRIEFS = {
    "seeds": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "briefs": {
        "B1-survival": "Prioritise survival over depth. A long-lived run that dies late and safe beats a fast run that gambles. Avoid optional and dangerous branches, take the safest route to three runes, and value retreat and caution over speed.",
        "B2-rune-rush": "Rush the first rune. Get to the Lair and into a Lair branch as fast as possible and secure a rune early. Momentum and an early rune matter more than fully clearing every level.",
        "B3-orb-sprint": "Play for the Orb, fast. Ignore optional branches entirely, take the shortest three-rune route, and go for the win without detours or shopping trips beyond the essentials.",
        "B4-methodical": "Clear everything methodically. Fully explore each branch you enter before moving on. Steady, complete, unhurried progress matters more than speed.",
        "B5-zealot": "Convert early to a powerful god and lean on divine help for the whole run. Choose one of the strongest gods for the combo and structure the route around worship from the very start."
    },
    "seed_brief": {"101": "B1-survival", "102": "B1-survival",
                   "103": "B2-rune-rush", "104": "B2-rune-rush",
                   "105": "B3-orb-sprint", "106": "B3-orb-sprint",
                   "107": "B4-methodical", "108": "B4-methodical",
                   "109": "B5-zealot", "110": "B5-zealot"}
}

# ---------------------------------------------------------------------------
# Vendored verbatim from qw-rematch/scripts/manager.py (rounds 1-2):
# vocabularies, the prompt, and the mechanical validator. Do not edit here;
# if the rig changes, re-vendor and re-run the differential test.
# --- begin vendored segment: qw-rematch/scripts/manager.py, byte-identical, sha256 578473217881fffbbfa79a0bcf6d068a6b94c167059579adfda4ba1d6caf8db1 ---
COMBOS = ['GrBe.handaxe', 'GrFi.waraxe', 'MiBe.handaxe', 'MiFi.waraxe', 'GrHu']
GODS = ['Beogh', 'Cheibriados', 'Hepliaklqana', 'Lugonu', 'Makhleb', 'Okawaru',
        'Qazlal', 'Ru', 'Trog', 'The Shining One', 'Uskayaw', 'Xom', 'Yredelemnul']
BRANCHES = ['D', 'Lair', 'Orc', 'Elf', 'Vaults', 'Depths', 'Slime', 'Snake',
            'Spider', 'Swamp', 'Shoals', 'Crypt', 'Tomb', 'Zot', 'Abyss', 'Pan',
            'Geh', 'Coc', 'Dis', 'Tar', '1stLairBranch', '2ndLairBranch']
RUNE_BRANCHES = ['Snake', 'Spider', 'Swamp', 'Shoals', 'Slime', 'Vaults',
                 'Abyss', 'Pan', 'Geh', 'Coc', 'Dis', 'Tar', 'Tomb']
SPECIALS = ['Normal', 'Shopping', 'Win', 'Orb', 'Escape', 'Hells', 'Zig']
# Save/Quit are legal qw goals but end a run administratively (no morgue);
# they are invalid in this experiment by stated rule.

PROMPT = """You are the manager of an automated Dungeon Crawl Stone Soup player (the bot qw). You do not play the game. Before the run you set its strategy: its starting combo, its preferred gods, and an ordered goal list. The bot follows your plan exactly.

The run uses game seed {seed}. Your strategic brief from the coach:
"{brief}"

Reply with EXACTLY these three lines and nothing else:
COMBO: <one of: GrBe.handaxe, GrFi.waraxe, MiBe.handaxe, MiFi.waraxe, GrHu, STOCK>
GODS: <1 to 3 god names separated by commas, chosen from: Beogh, Cheibriados, Hepliaklqana, Lugonu, Makhleb, Okawaru, Qazlal, Ru, Trog, The Shining One, Uskayaw, Xom, Yredelemnul - or STOCK>
GOALS: <your goal list>

Goal list rules: comma-separated goals, in the order the bot should pursue them. A goal is one of:
- Normal (the bot's proven standard 3-rune route)
- a branch: D, Lair, Orc, Elf, Vaults, Depths, Slime, Snake, Spider, Swamp, Shoals, Crypt, Tomb, Zot - optionally with a level range, e.g. D:1-11 or Vaults:5
- Rune:<branch> to dive straight for that branch's rune, e.g. Rune:Shoals
- God:<god name> to convert to that god at that point in the plan
- Shopping, Win, Orb, Escape, Hells
Example: GOALS: D:1-11, Lair, D:12-15, Orc, Rune:Shoals, Rune:Snake, Vaults:1-4, Depths, Vaults:5, Shopping, Zot:1-4, Win

STOCK for a line means: leave that part at the bot's proven default (combo GrBe.handaxe, gods Trog/Okawaru/Makhleb, goal Normal).

Now write the three lines for seed {seed}. /no_think"""

def canon_branch(tok):
    for b in BRANCHES:
        if tok.lower() == b.lower():
            return b
    return None

def valid_goal_token(tok):
    t = tok.strip()
    if not t:
        return None
    for s in SPECIALS:
        if t.lower() == s.lower():
            return s
    m = re.fullmatch(r'Zig:(\d{1,2})', t, re.I)
    if m and 1 <= int(m.group(1)) <= 27:
        return 'Zig:%d' % int(m.group(1))
    m = re.fullmatch(r'Rune:([A-Za-z]+)', t, re.I)
    if m:
        for b in RUNE_BRANCHES:
            if m.group(1).lower() == b.lower():
                return 'Rune:' + b
        return None
    m = re.fullmatch(r'God:(.+)', t, re.I)
    if m:
        name = m.group(1).strip()
        for g in GODS:
            if name.lower() == g.lower():
                return 'God:' + g
        squashed = {g.replace(' ', '').lower(): g for g in GODS}
        key = name.replace(' ', '').lower()
        for g, full in squashed.items():
            if key in (g[:1], g[:3], g[:4]):
                return 'God:' + full
        if key in ('tso', '1'):
            return 'God:The Shining One'
        if key in ('0', 'none', 'nogod'):
            return 'God:No God'
        return None
    m = re.fullmatch(r'([A-Za-z0-9]+)(?::(\d{1,2})(?:-(\d{1,2}))?)?', t)
    if m:
        b = canon_branch(m.group(1))
        if b is None:
            return None
        if m.group(2) is None:
            return b
        lo = int(m.group(2)); hi = int(m.group(3)) if m.group(3) else lo
        if not (1 <= lo <= hi <= 27):
            return None
        return '%s:%d' % (b, lo) if hi == lo else '%s:%d-%d' % (b, lo, hi)
    return None

def validate(cfg_text):
    """Return (managed_dict, errors). managed_dict None if any error."""
    lines = {}
    for raw in cfg_text.splitlines():
        m = re.match(r'\s*(?:[-*#>]+\s*)?(COMBO|GODS|GOALS)\s*:\s*(.+?)\s*$', raw, re.I)
        if m:
            lines[m.group(1).upper()] = m.group(2).strip()
    errs = []
    if not all(k in lines for k in ('COMBO', 'GODS', 'GOALS')):
        return None, ['missing line(s): have %s' % sorted(lines)]
    combo_raw = lines['COMBO']
    if combo_raw.upper() == 'STOCK':
        combo = 'STOCK'
    else:
        combo = next((c for c in COMBOS if c.lower() == combo_raw.lower()), None)
        if combo is None:
            errs.append('bad COMBO: %r' % combo_raw)
    gods_raw = lines['GODS']
    if gods_raw.upper() == 'STOCK':
        gods = 'STOCK'
    else:
        gods = []
        for part in gods_raw.split(','):
            g = next((x for x in GODS if x.lower() == part.strip().lower()), None)
            if g is None:
                errs.append('bad god: %r' % part.strip())
            else:
                gods.append(g)
        if not (1 <= len(gods) <= 3):
            errs.append('gods count %d not in 1..3' % len(gods))
    goals_raw = lines['GOALS']
    toks = [t.strip() for t in goals_raw.split(',')]
    if not (1 <= len(toks) <= 24):
        errs.append('goals count %d not in 1..24' % len(toks))
    goals = []
    for t in toks:
        v = valid_goal_token(t)
        if v is None:
            errs.append('bad goal token: %r' % t)
        else:
            goals.append(v)
    if errs:
        return None, errs
    return {'combo': combo, 'gods': gods, 'goals': ', '.join(goals)}, []
# --- end vendored segment ---

# ---------------------------------------------------------------------------
# Self-test: the rig's 10 validator cases (from qw-rematch/scripts/
# test_validator.py), vendored so the bench can sanity-check itself anywhere.
SELFTEST_CASES = [
    ("round1-seed101-valid",
     "COMBO: MiFi.waraxe\nGODS: Beogh, Cheibriados, Hepliaklqana\nGOALS: Normal, Rune:Shoals, Vaults:1-4",
     True, None),
    ("runes-plural",
     "COMBO: GrHu\nGODS: Trog\nGOALS: D:1-11, Runes:Shoals, Runes:Snake",
     False, "Runes:Shoals"),
    ("hallucinated-god",
     "COMBO: GrHu\nGODS: Mgazlal\nGOALS: Normal",
     False, "Mgazlal"),
    ("stock-as-god",
     "COMBO: GrHu\nGODS: Beogh, Qazlal, Stock\nGOALS: Runes:Shoals",
     False, "Stock"),
    ("combo-in-goals",
     "COMBO: MiFi.waraxe\nGODS: Trog\nGOALS: Run:GrHu, Normal",
     False, "Run:GrHu"),
    ("normal-with-description",
     "COMBO: STOCK\nGODS: STOCK\nGOALS: Normal (the bot's proven standard 3-rune route)",
     False, "Normal (the bot"),
    ("invented-tokens",
     "COMBO: STOCK\nGODS: STOCK\nGOALS: Shrine, Runestone",
     False, "Shrine"),
    ("all-stock",
     "COMBO: STOCK\nGODS: STOCK\nGOALS: Normal",
     True, None),
    ("god-token-zig-lowercase-rune",
     "COMBO: GrFi.waraxe\nGODS: Okawaru, The Shining One\nGOALS: D:1-11, God:Trog, rune:shoals, Zig:5, Win",
     True, None),
    ("missing-goals-line",
     "COMBO: GrHu\nGODS: Trog",
     False, "missing line"),
]

def selftest():
    fails = 0
    for name, text, want_valid, want_err in SELFTEST_CASES:
        managed, errs = validate(text)
        ok = (managed is not None) == want_valid
        if ok and want_err:
            ok = any(want_err in e for e in errs)
        if ok and want_valid and name == "god-token-zig-lowercase-rune":
            ok = "Rune:Shoals" in managed["goals"] and "God:Trog" in managed["goals"]
        print(("PASS " if ok else "FAIL ") + name)
        fails += 0 if ok else 1
    print("validator selftest: %d/10 passed" % (10 - fails))
    return 1 if fails else 0

# ---------------------------------------------------------------------------
# Transport: one call per brief, temperature 0, the endpoint's native API.
# No retries — a transport error is that seed's verdict, receipted.
MAX_TOKENS = 512  # headroom only; a config needs ~90 tokens. Truncation, if
                  # it ever binds, is visible via finish_reason in the receipt.

def _post_json(url, payload, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def call_openai(base_url, model, prompt, timeout):
    """llama-server / OpenAI-style chat completions."""
    resp = _post_json(base_url.rstrip('/') + '/v1/chat/completions', {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0, 'max_tokens': MAX_TOKENS, 'stream': False}, timeout)
    choice = resp['choices'][0]
    return choice['message']['content'], {
        'finish_reason': choice.get('finish_reason'),
        'usage': resp.get('usage')}

def call_ollama(base_url, model, prompt, timeout):
    """Ollama native chat API."""
    resp = _post_json(base_url.rstrip('/') + '/api/chat', {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'stream': False,
        'options': {'temperature': 0, 'num_predict': MAX_TOKENS}}, timeout)
    return resp['message']['content'], {
        'finish_reason': resp.get('done_reason'),
        'eval_count': resp.get('eval_count'),
        'eval_duration_ns': resp.get('eval_duration'),
        'prompt_eval_count': resp.get('prompt_eval_count')}

DIALECTS = {'openai': call_openai, 'ollama': call_ollama}

def ask_manager_http(seed, brief, base_url, model, dialect, timeout):
    prompt = PROMPT.format(seed=seed, brief=brief)
    t0 = time.time()
    try:
        text, meta = DIALECTS[dialect](base_url, model, prompt, timeout)
        wall = time.time() - t0
        managed, errs = validate(text)
        return {'seed': seed, 'brief': brief, 'prompt': prompt,
                'raw_output': text, 'llm_wall_s': round(wall, 2),
                'call_wall_s': round(wall, 2),
                'valid': managed is not None, 'errors': errs,
                'managed': managed, 'endpoint_meta': meta}
    except Exception as e:  # transport failure IS the receipt (see docstring)
        wall = time.time() - t0
        return {'seed': seed, 'brief': brief, 'prompt': prompt,
                'raw_output': '', 'llm_wall_s': round(wall, 2),
                'call_wall_s': round(wall, 2),
                'valid': False, 'errors': ['transport: %r' % (e,)],
                'managed': None, 'endpoint_meta': None}

def cmd_gen(args):
    arm_dir = os.path.join(args.out, 'arms', args.arm)
    os.makedirs(arm_dir, exist_ok=True)
    arm_meta = {'arm': args.arm, 'base_url': args.base_url,
                'model': args.model, 'dialect': args.dialect,
                'temperature': 0, 'max_tokens': MAX_TOKENS,
                'gen_host': os.uname().nodename,
                'gen_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    json.dump(arm_meta, open(os.path.join(arm_dir, 'arm.json'), 'w'), indent=1)
    total = 0.0
    for seed in BRIEFS['seeds']:
        bid = BRIEFS['seed_brief'][str(seed)]
        art = ask_manager_http(seed, BRIEFS['briefs'][bid], args.base_url,
                               args.model, args.dialect, args.timeout)
        art['brief_id'] = bid
        art['arm'] = args.arm
        json.dump(art, open(os.path.join(arm_dir, 'manager-%d.json' % seed),
                            'w'), indent=1)
        total += art['call_wall_s']
        print('seed %d (%s): %s wall=%.2fs %s' % (
            seed, bid,
            'VALID' if art['valid'] else 'FALLBACK',
            art['call_wall_s'],
            json.dumps(art['managed']) if art['valid'] else art['errors']),
            flush=True)
    print('arm %s: manager phase total wall %.1fs -> %s' % (args.arm, total,
                                                           arm_dir))
    return 0

# ---------------------------------------------------------------------------
# Play phase — Oracle only. Vendored from qw-rematch/scripts/run_rematch.py
# (parse_xlog / parse_morgue / run_game), with rig paths pointed at the
# round-2 tree (shared by symlink there) and run dirs under the bench root.
RIG = '/home/ubuntu/qw-rematch'
RIG_BIN = RIG + '/crawl-032/crawl-ref/source/crawl'
R1_RESULTS_CANDIDATES = ['/home/ubuntu/qw-manager/results.json',
                         '/home/ubuntu/qw-rematch/results.json']
WALL_CAP = 1800
TURN_CAP = 200000  # stated cap; post-hoc receipt check (round 1 design)

def _load_r1_controls():
    for path in R1_RESULTS_CANDIDATES:
        if os.path.exists(path):
            d = json.load(open(path))
            if 'runs' in d:
                return {r['seed']: r for r in d['runs']
                        if r['arm'] == 'control'}, path
            if 'control_round1' in d:
                return {int(s): r for s, r in
                        d['control_round1'].items()}, path
    raise SystemExit('round 1 control receipts not found on this host')

def parse_xlog(path):
    if not os.path.exists(path):
        return None
    lines = [l for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        return None
    fields = {}
    for part in lines[-1].split(':'):
        if '=' in part:
            k, v = part.split('=', 1)
            fields[k] = v
    return fields

def parse_morgue(path):
    txt = open(path).read()
    out = {}
    m = re.search(r'You visited (\d+) branch', txt)
    out['branches_visited'] = int(m.group(1)) if m else None
    m = re.search(r'saw (\d+) of its levels', txt)
    out['levels_seen'] = int(m.group(1)) if m else None
    mb = re.search(r'Branches:\n(.*?)\n\n', txt, re.S)
    reached = {}
    if mb:
        for name, got in re.findall(r'([A-Za-z]+) \((\d+)/\d+\)', mb.group(1)):
            reached[name] = int(got)
    out['branch_reached'] = reached
    out['runes_found'] = len(set(re.findall(r'Found the (\w+) rune of Zot', txt)))
    out['won'] = ('scaped with the Orb' in txt) or ('Escaped the dungeon' in txt)
    return out

def run_game(root, arm, seed, rc_text):
    sys.path.insert(0, RIG + '/scripts')
    rid = '%s-%d' % (arm, seed)
    rdir = os.path.join(root, 'runs', rid)
    os.makedirs(os.path.join(rdir, 'morgue'), exist_ok=True)
    rcpath = os.path.join(rdir, 'rc.txt')
    open(rcpath, 'w').write(rc_text)
    cmd = ['nice', '-n', '10', 'python3', RIG + '/scripts/drive.py',
           os.path.join(rdir, 'output.log'), os.path.join(rdir, 'driver.log'),
           str(WALL_CAP), RIG_BIN, '-lua-max-memory', '128', '-no-throttle',
           '-rc', rcpath, '-rcdir', RIG + '/qw',
           '-dir', rdir, '-morgue', os.path.join(rdir, 'morgue'),
           '-seed', str(seed)]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True,
                       timeout=WALL_CAP + 300)
    wall = time.time() - t0
    morgues = sorted(f for f in os.listdir(os.path.join(rdir, 'morgue'))
                     if f.startswith('morgue-') and f.endswith('.txt'))
    xlog = parse_xlog(os.path.join(rdir, 'saves', 'logfile-seeded'))
    morgue = parse_morgue(os.path.join(rdir, 'morgue', morgues[-1])) \
        if morgues else {}
    res = {'arm': arm, 'seed': seed, 'run_dir': rdir,
           'wall_s': round(wall, 1),
           'driver_tail': r.stdout.strip().splitlines()[-1]
           if r.stdout.strip() else '',
           'morgue_file': morgues[-1] if morgues else None}
    if xlog:
        res.update({'score': int(xlog.get('sc', 0)),
                    'xl': int(xlog.get('xl', 0)),
                    'turns': int(xlog.get('turn', 0)),
                    'absdepth': int(xlog.get('absdepth', 0)),
                    'place': xlog.get('place'), 'god': xlog.get('god'),
                    'char': xlog.get('char'), 'ktyp': xlog.get('ktyp'),
                    'killer': xlog.get('killer'),
                    'gold': int(xlog.get('gold', 0)),
                    'kills': int(xlog.get('kills', 0))})
        res['outcome'] = 'WIN' if morgue.get('won') else 'DIED'
    else:
        res['outcome'] = 'CAP-NO-MORGUE'
    res['morgue_parse'] = morgue
    res['turn_cap_exceeded'] = bool(
        xlog and int(xlog.get('turn', 0)) > TURN_CAP)
    return res

def cmd_play(args):
    sys.path.insert(0, RIG + '/scripts')
    from mkrc import make_rc
    root = os.path.abspath(args.root)
    arm_dir = os.path.join(root, 'arms', args.arm)
    arm_meta = json.load(open(os.path.join(arm_dir, 'arm.json')))
    r1_control, r1_src = _load_r1_controls()
    # Determinism spot-check, once per bench root (round 1/2 discipline).
    sc_path = os.path.join(root, 'spotcheck.json')
    if os.path.exists(sc_path):
        spot = json.load(open(sc_path))
        print('spot-check on file: match=%s' % spot['match'], flush=True)
    else:
        sc = run_game(root, 'control', 101, make_rc(None))
        ref = r1_control[101]
        match = all(sc.get(k) == ref.get(k)
                    for k in ('score', 'xl', 'turns', 'killer'))
        spot = {'seed': 101, 'fields': ['score', 'xl', 'turns', 'killer'],
                'bench': {k: sc.get(k) for k in
                          ('score', 'xl', 'turns', 'killer')},
                'round1': {k: ref.get(k) for k in
                           ('score', 'xl', 'turns', 'killer')},
                'match': match, 'control_run': sc,
                'consequence': ('round 1 control receipts reused' if match
                                else 'MISMATCH - full control arm re-run')}
        json.dump(spot, open(sc_path, 'w'), indent=1)
        print('spot-check control 101: %s (%s vs round1 %s)' % (
            'MATCH' if match else 'MISMATCH', spot['bench'], spot['round1']),
            flush=True)
    results = {'config': {'wall_cap_s': WALL_CAP, 'turn_cap': TURN_CAP,
                          'crawl': '0.32.1 (source build)',
                          'qw': '8698adc (stock)', 'binary': RIG_BIN,
                          'rig': RIG},
               'arm': arm_meta, 'manager': {}, 'runs': [],
               'determinism_spotcheck': spot,
               'control_source': r1_src,
               'control_round1': {str(s): r1_control[s]
                                  for s in BRIEFS['seeds']}}
    arts = {}
    for seed in BRIEFS['seeds']:
        art = json.load(open(os.path.join(arm_dir, 'manager-%d.json' % seed)))
        arts[seed] = art
        results['manager'][str(seed)] = {
            'brief_id': art['brief_id'], 'valid': art['valid'],
            'errors': art['errors'], 'managed': art['managed'],
            'llm_wall_s': art['llm_wall_s'],
            'call_wall_s': art['call_wall_s'],
            'raw_output': art['raw_output']}
    jobs = []
    if not spot['match']:
        for seed in BRIEFS['seeds']:
            if seed != 101:
                jobs.append(('control', seed, make_rc(None)))
            else:
                results['runs'].append(spot['control_run'])
    for seed in BRIEFS['seeds']:
        art = arts[seed]
        rc = make_rc(art['managed']) if art['valid'] else make_rc(None)
        jobs.append((args.arm, seed, rc))

    def _play(job):
        arm, seed, rc = job
        res = run_game(root, arm, seed, rc)
        if arm == args.arm:
            res['manager_valid'] = arts[seed]['valid']
        print('%s %d: %s score=%s xl=%s turns=%s depth=%s wall=%ss' % (
            arm, seed, res['outcome'], res.get('score'), res.get('xl'),
            res.get('turns'), res.get('absdepth'), res['wall_s']), flush=True)
        return res

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        results['runs'].extend(ex.map(_play, jobs))
    results['runs'].sort(key=lambda r: (r['arm'], r['seed']))
    out = os.path.join(root, 'results-%s.json' % args.arm)
    json.dump(results, open(out, 'w'), indent=1)
    json.dump(results, open(os.path.join(
        arm_dir, 'results.json'), 'w'), indent=1)
    print('ALL DONE -> %s' % out)
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('selftest')
    g = sub.add_parser('gen')
    g.add_argument('--base-url', required=True)
    g.add_argument('--model', required=True)
    g.add_argument('--dialect', choices=sorted(DIALECTS), required=True)
    g.add_argument('--arm', required=True)
    g.add_argument('--out', required=True)
    g.add_argument('--timeout', type=int, default=300)
    p = sub.add_parser('play')
    p.add_argument('--arm', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--jobs', type=int, default=2)
    args = ap.parse_args()
    if args.cmd == 'selftest':
        return selftest()
    if args.cmd == 'gen':
        return cmd_gen(args)
    if args.cmd == 'play':
        return cmd_play(args)
    return 2

if __name__ == '__main__':
    sys.exit(main())
