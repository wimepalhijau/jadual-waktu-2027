# Jadual Waktu 2027 — SK Putrajaya Presint 17(1)

Arahan projek untuk Claude Code. Baca keseluruhan fail ini sebelum mula.

## Cara bekerja dengan pengguna

- Pengguna ialah guru (akaun GitHub `wimepalhijau`). **Sentiasa balas dalam Bahasa Melayu**, ringkas dan tanpa istilah teknikal yang tidak perlu.
- **Jangan terjemah atau tukar ke Bahasa Inggeris.** Elakkan perkataan Inggeris dalam jawapan; guna istilah Melayu. Nama butang/menu GitHub yang memang dalam Inggeris boleh disebut, tetapi terangkan dalam Bahasa Melayu.
- Bila pengguna taip **"kemaskini"**: jalankan `python3 tools/build_pages.py`, `python3 tools/semak.py`, kemudian commit dan push ke `main` supaya GitHub Pages dikemas kini. Lapor ringkas apa yang berubah.
- Jangan hantar/salin fail HTML ke desktop pengguna — dia kerja terus dalam talian.
- Jangan teka nama guru untuk sesuatu kelas/subjek. Ambil daripada data (`borang`, `plan.teachers`) atau tanya.
- Bila menukar jadual guru lain (alih pelajaran), minta izin dulu.

## Apa yang ada dalam repo

```
src/jadual-waktu-aktif/index.html   Aplikasi utama (versi claude.ai, ~470 KB, satu fail HTML+JS)
src/borang-opsyen/index.html        Borang Mengajar Ikut Opsyen 2027
src/guru-kelas/index.html           Borang Guru Kelas 2027
src/staffing-guru/index.html        Staffing Guru 2027
data/<app>/<koleksi>/<id>.json      Salinan pangkalan data kongsi setiap aplikasi (dieksport 2026-11-13)
docs/index.html                     Versi GitHub Pages (DIJANA — jangan sunting terus)
tools/build_pages.py                Jana docs/index.html daripada src + data
tools/semak.py                      Semak data terhadap peraturan sekolah
```

Versi asal (sumber kebenaran untuk suntingan bersama guru) berada di claude.ai:

| Aplikasi | URL claude.ai | Koleksi data |
|---|---|---|
| JADUAL WAKTU AKTIF 2027 | https://claude.ai/artifact/U1Yf3T2QfajDJsa2UeNPga | `plan/jadual` (semua data jadual), `borang` (subjek & kelas setiap guru, id = kod guru), `relif`, `versi` |
| Borang Mengajar Ikut Opsyen 2027 | https://claude.ai/artifact/S2wRjQfXAh1XPjLU3kksNP | `borang` (id = nama guru, `rows:[{s,k,m}]`) |
| Guru Kelas 2027 | https://claude.ai/artifact/5cbsvynfMRN8CFMFkh6YNq | `guruKelas` (id = `1-AMBER`, `{guruKelas,pembantu}`) |
| Staffing Guru 2027 | https://claude.ai/artifact/CKywZRiTVDstDFvZEPWEKG | `staffing` |

## Penting: dua dunia data

- Dalam claude.ai, halaman memanggil `window.claude.use('db')` dan menyimpan ke pangkalan data kongsi; semua guru nampak data yang sama.
- **Di luar claude.ai (GitHub Pages, fail tempatan) `window.claude` tiada.** Halaman jatuh balik kepada data tertanam `window.__SNAP={savedAt,data}` + `localStorage` (`jw-data-v4`). Suntingan di sana hanya tinggal dalam pelayar itu. Jadi GitHub Pages = **paparan sahaja**.
- Claude Code **tidak boleh** baca/tulis pangkalan data claude.ai. Untuk dapat data terbaru, pengguna perlu minta di claude.ai: "eksport data jadual ke GitHub" (atau muat turun JSON dan letak di `data/`). Kalau Claude Code mengubah jadual (`data/.../plan/jadual.json`), perubahan itu **tidak** masuk ke claude.ai secara automatik — beritahu pengguna.
- `once` dalam data ialah bendera migrasi sekali-jalan dalam `norm()`; jangan padam.

## Model data `plan/jadual` (`data.data` dalam JSON)

- `classes[i]` `{code,name,guru,pgk,catatan}` — indeks i dipakai dalam pelajaran. 0–1 Prasekolah, kemudian Tahun 1…6.
- `teachers[i]` `{code(3 huruf),name,subs[],pentadbir?,off:["hari,waktu"],habis:"HH:MM",depan:n}`.
- `lessons[]` = `[guru_idx, hari 0–4 (Isnin–Jumaat), waktu 0–11, kod_subjek, [kelas_idx…]]`. Waktu k = 07:40 + 30k minit. `PER` (perhimpunan Isnin waktu 0) dan `BY` (Jumaat waktu 0) bukan mengajar.
- `kur[tahun][subjek]` waktu seminggu; `pola[tahun][subjek]` susunan blok (cth `3+3+2+2+2`).
- `rehat[tahun]` = indeks waktu rehat; `rehatEx` minit tambahan Prasekolah.
- `pairSubs` subjek dua guru serentak (ADM, TAS, PI(q2)); `groups` kumpulan serentak.

## Peraturan sekolah (dari pengguna)

Kelas & kurikulum
- Kelas 2027: Tahun 1 AMBER/CRYSTAL/DIAMOND/EMERALD/OPAL/PEARL/RUBY; Tahun 2 AMBER–EMERALD; Tahun 3 AMBER–PEARL (6); Tahun 4, 5 dan 6 AMBER/CRYSTAL/DIAMOND/EMERALD/OPAL — 32 kelas + 2 Prasekolah.
- BM: Tahun 1 **12** (susunan 3+3+2+2+2), Tahun 2–3 11 (2+2+2+3+2), Tahun 4–6 9 (2+2+2+2+1).
- Tahun 1: BI 8 (2+2+2+2), MT 7 (2+2+3), ADM 4 (dua guru serentak), PJ1 3. Tahun 2–6: MT 2+2+2, BI 2+2+2+3, PJ 1+1 hari berselang.
- Tahun 1 tiada PK, DMZ, PSV, SN, SEJ, RBT. ADM untuk Tahun 1 sahaja. SEJ dan RBT Tahun 4–6.
- PI(q) 3 waktu = PI(q1) 1 waktu (guru PI(j)/PI(u) kelas itu) + PI(q2) 2 waktu berpasangan.
- PJ1–PJ6 mesti tamat sebelum 10:40 (boleh selepas rehat).
- **Tiada PJ pada hari Isnin.**
- TAS kelas yang ada Pendidikan Moral diletak di waktu terakhir sesi.
- Tahun 1–3: tidak lebih 4 subjek berbeza sehari.
- Rehat: Tahun 1 & 4 09:10–09:40; Tahun 2 & 3 09:40–10:10; Tahun 5 & 6 10:10–10:40; Prasekolah 10:00–10:40.

Guru
- Paling banyak 3 waktu berturut; selepas 3 berturut mesti 2 waktu kosong (1 cukup jika beban ≥ 33 waktu seminggu).
- Paling banyak 7 waktu sehari.
- Tukar ke kelas lain perlu sekurang-kurangnya 1 waktu kosong; blok berturut dalam kelas sama dibenarkan.
- Pentadbir: HEZ, DSZ, NFJ, SAM — tiada peranan guru kelas, **tidak pernah diberi relif**.
- Relif statik: bila ramai guru tidak hadir, guru relif kekal dalam satu kelas sehingga 3 waktu berturut, kemudian ke kelas lain.

## Kerja yang belum selesai (setakat 2026-11-13)

- SSA (Syafia): PJ1 1 CRYSTAL, PJ2 2 AMBER & 2 CRYSTAL, PJ3 3 AMBER & 3 PEARL kini sudah ada dalam jadual (disemak 2026-11-13), tetapi SSA masih ada isu rehat selepas 3 waktu. Dalam borang, 3 AMBER/3 PEARL masih ditanda PJ2 — patut PJ3.
- PJ5 5 AMBER (MAM) masih pada Isnin 10:40 — langgar 'tiada PJ Isnin' dan 'tamat sebelum 10:40'. Pengguna pilih **biarkan dulu** (2026-11-13); pagi Selasa/Rabu 5 AMBER penuh, pilihan tukar dengan BM SUW atau BI DSZ ditolak buat masa ini. Cuba semula selepas lebih banyak subjek dimasukkan.
- Selesai 2026-11-13: pertindihan PJ6 MFZ Selasa 09:10 — 6 AMBER & 6 CRYSTAL digabung dalam satu pelajaran (pilihan pengguna). **Belum dibuat di claude.ai.**
- BM 1 DIAMOND (ANU) masih 10/12 — tiada slot Isnin yang ikut peraturan guru.
- Banyak subjek lain belum dijadualkan (lihat `tools/semak.py`). Laporan semak.py ialah anggaran; menu **Semak** dalam aplikasi ialah rujukan utama.
- Guru kelas & pembantu: **sumber betul ialah JADUAL WAKTU AKTIF 2027** (`classes[].guru` dan `classes[].pgk`), bukan Borang Guru Kelas. Keputusan pengguna 2026-11-13. Borang Guru Kelas (15 kelas sahaja diisi) berbeza di 12 tempat dan ada kelas '1 SAPPHIRE' yang tiada dalam jadual — jangan salin borang ke jadual.
- Borang Opsyen: data masuk ke jadual hanya bila pengguna minta.

## GitHub Pages

- Repo: `wimepalhijau/jadual-waktu-2027` (public, cawangan `main`).
- Settings → Pages → Source: *Deploy from a branch* → `main` / `/docs`.
- URL: https://wimepalhijau.github.io/jadual-waktu-2027/
- Repo public bermakna nama guru & jadual boleh dilihat sesiapa; `docs/index.html` diberi `noindex` supaya tidak diindeks enjin carian.
