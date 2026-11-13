#!/usr/bin/env python3
"""Semak data jadual terhadap peraturan sekolah (tanpa mengubah apa-apa).

Guna:  python3 tools/semak.py [data/jadual-waktu-aktif/plan/jadual.json]

Format pelajaran: [guru_idx, hari(0=Isnin..4=Jumaat), waktu(0..11), kod_subjek, [kelas_idx, ...]]
Waktu k bermula 07:40 + 30*k minit (waktu 0 = 07:40-08:10).
"""
import json, sys, pathlib
from collections import defaultdict, Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/jadual-waktu-aktif/plan/jadual.json"
doc = json.loads(path.read_text(encoding="utf-8"))
D = doc["data"] if "lessons" in doc.get("data", {}) else doc
L, T, C = D["lessons"], D["teachers"], D["classes"]
DAYS = ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat"]
NOTEACH = {"PER", "BY"}           # tidak dikira sebagai mengajar
TRUN, TGAP, TBERAT, TCAP = 3, 2, 33, 7
PJ_END = 640                       # PJ mesti tamat sebelum 10:40
end_min = lambda p: 460 + 30 * (p + 1)

def year(ci):
    c = C[ci]["code"]
    return 0 if c.startswith("PRA") else int(c.split()[0])

issues = defaultdict(list)

# 1. Pertindihan guru dan kelas
tslot, cslot = defaultdict(list), defaultdict(list)
for l in L:
    tslot[(l[0], l[1], l[2])].append(l)
    for c in l[4]:
        cslot[(c, l[1], l[2])].append(l)
for (t, d, p), v in tslot.items():
    if len(v) > 1:
        issues["Guru bertindih"].append(f"{T[t]['code']} {DAYS[d]} waktu {p+1}: " + ", ".join(x[3] for x in v))
for (c, d, p), v in cslot.items():
    subs = {x[3] for x in v}
    if len(v) > 1 and not subs <= set(D.get("pairSubs", [])):
        issues["Kelas bertindih"].append(f"{C[c]['code']} {DAYS[d]} waktu {p+1}: " + ", ".join(sorted(subs)))

# 2. Rehat
for l in L:
    for c in l[4]:
        r = D.get("rehat", {}).get(str(year(c)))
        if r is not None and l[2] == r:
            issues["Pelajaran pada waktu rehat"].append(f"{C[c]['code']} {DAYS[l[1]]} waktu {l[2]+1} {l[3]}")

# 3. Kurikulum (bilangan waktu seminggu)
cnt = defaultdict(Counter)
for l in L:
    for c in l[4]:
        cnt[c][l[3]] += 1
for ci, cl in enumerate(C):
    for sub, want in D.get("kur", {}).get(str(year(ci)), {}).items():
        have = cnt[ci][sub]
        if have != want:
            issues["Kurikulum tidak cukup/lebih"].append(f"{cl['code']} {sub}: {have}/{want}")

# 4. PJ selepas 10:40
for l in L:
    if l[3].startswith("PJ") and end_min(l[2]) > PJ_END:
        issues["PJ tamat selepas 10:40"].append(f"{T[l[0]]['code']} {DAYS[l[1]]} waktu {l[2]+1} {l[3]}")
    if l[3].startswith("PJ") and l[1] == 0:
        issues["PJ pada hari Isnin"].append(f"{T[l[0]]['code']} waktu {l[2]+1} {l[3]} " + ", ".join(C[c]['code'] for c in l[4]))

# 5. Peraturan guru
load = Counter(l[0] for l in L if l[3] != "PER")
for ti, t in enumerate(T):
    gap = 1 if load[ti] >= TBERAT else TGAP
    for d in range(5):
        row = [None] * 12
        for l in L:
            if l[0] == ti and l[1] == d and l[3] not in NOTEACH:
                row[l[2]] = tuple(l[4])
        n = sum(1 for x in row if x is not None)
        if n > TCAP:
            issues["Guru > 7 waktu sehari"].append(f"{t['code']} {DAYS[d]}: {n}")
        run = prev = 0; g = 99
        for p in range(13):
            on = p < 12 and row[p] is not None
            if on:
                if run == 0 and prev >= TRUN and g < gap:
                    issues["Rehat guru selepas 3 waktu"].append(f"{t['code']} {DAYS[d]} waktu {p+1}")
                run += 1
                if run == TRUN + 1:
                    issues["Guru > 3 waktu berturut"].append(f"{t['code']} {DAYS[d]} waktu {p+1}")
            else:
                if run: prev, g = run, 0
                run = 0; g += 1
        for p in range(11):
            a, b = row[p], row[p + 1]
            if a and b and a != b:  # tuple kosong (tugas tanpa kelas) tidak dikira
                issues["Tukar kelas tanpa waktu kosong"].append(f"{t['code']} {DAYS[d]} waktu {p+1}-{p+2}")

if not issues:
    print("Semua peraturan dipatuhi.")
for k, v in issues.items():
    print(f"\n## {k} ({len(v)})")
    for x in v[:40]:
        print("  -", x)
    if len(v) > 40:
        print(f"  ... dan {len(v)-40} lagi")
