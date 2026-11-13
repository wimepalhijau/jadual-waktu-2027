# Jadual Waktu 2027 — SK Putrajaya Presint 17(1)

Aplikasi jadual waktu, jadual guru ganti (relif) dan borang guru untuk tahun 2027.

**Lihat dalam talian:** https://wimepalhijau.github.io/jadual-waktu-2027/ (paparan sahaja)

Suntingan bersama guru dibuat dalam halaman asal di claude.ai.

## Mula di Claude Code

1. Muat naik semua fail dalam pakej ini ke repo `jadual-waktu-2027` (cawangan `main`).
2. Di GitHub: **Settings → Pages → Source: Deploy from a branch → `main` dan folder `/docs` → Save**.
3. Buka repo ini dalam Claude Code. Claude akan membaca `CLAUDE.md` untuk faham projek dan peraturan sekolah.
4. Taip **"kemaskini"** untuk menjana semula laman dan menghantarnya ke GitHub.

## Arahan teknikal

```bash
python3 tools/build_pages.py   # jana docs/index.html daripada src + data
python3 tools/semak.py         # semak peraturan jadual
```

## Fail lama (dimuat naik sebelum ini)

Fail di akar repo ini ialah versi awal dan salinan statik. Ia disimpan untuk rujukan.

| Fail | Keterangan |
|---|---|
| `jadual-waktu-v1-2027.html` | **JADUAL WAKTU AKTIF 2027** — prototaip gaya aSc, dengan Borang Subjek Guru terbina dalam (ketua panitia isi subjek dan kelas setiap guru, banding dengan jadual) dan butang Borang kosong (PDF): Pelajaran, Kelas, Bilik, Guru, Relations, Jadual, Semak, Sekolah; paparan guru/kelas, cetak, kumpulan serentak, jana automatik. 38 kelas (Tahun 1 ada 8 kelas). |
| `jadual-waktu-aktif-2027.html` | Salinan JADUAL WAKTU AKTIF 2027 dengan data terkini tertanam (buka terus dalam Chrome). Salinan statik: tidak bersambung dengan versi Claude. |
| `jadual-waktu-guru-dan-kelas.html` | Jadual Waktu Guru dan Kelas — dijana daripada data aSc (80 guru, 34 kelas), dengan semakan pertindihan. |
| `jadual-guru-ganti-skpp17.html` | Jadual Guru Ganti SKPP17(1) — berdasarkan Jadual Waktu Guru Versi 5.0 (mula 28.9.26), cadangan guru ganti automatik, muat turun CSV. |
| `jadual-relif.html` | Jadual Relif — senarai relif harian untuk telefon guru, salin untuk WhatsApp, rumusan bulanan. |
| `jadual-guru-ganti-papan-notis.html` | Jadual Guru Ganti — gaya lembaran notis bilik guru. |
| `borang-subjek-guru-cetak.pdf` | Borang Subjek Guru — versi cetak kosong, A4 satu muka surat. |
| `borang-subjek-guru-cetak-nama.html` | Borang Subjek Guru — 80 muka surat, nama dan kod setiap guru sudah tercetak. Buka dalam Chrome, tekan Ctrl+P, pilih A4. |
| `e-guru-ganti-prototaip.html` | e-Guru Ganti — prototaip awal dengan data contoh rekaan. |
