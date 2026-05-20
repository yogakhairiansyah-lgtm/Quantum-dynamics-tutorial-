"""
Generate ORCA input files untuk benchmark VQE vs ORCA
H2 / STO-3G / CASSCF(2,2) — rentang 0.30 s.d. 2.50 Å (step 0.05 Å)
 
Mengapa CASSCF(2,2) dan bukan CCSD/FCI?
  - CCSD  → crash ORCA 6.1.1: "K(C)-AO-direct not implemented for CCSD"
  - FCI   → "UNRECOGNIZED KEYWORD" di simple input line ORCA 6.1.1
  - CASSCF(nel=2, norb=2) = FCI secara matematis untuk H2/STO-3G:
      * Active space mencakup SEMUA elektron (2) dan SEMUA orbital (2)
      * Semua konfigurasi CI disertakan → identik dengan Full CI
      * Menggunakan modul CASSCF (bukan MDCI) → tidak ada bug di atas
  - Basis sama dengan PySCF/VQE → perbandingan apple-to-apple
  - Chemical accuracy: |ΔE_ORCA vs E_FCI_PySCF| ≈ 0
 
Cara pakai:
  python generate_orca_inputs.py
  → Membuat folder 'inputs_casscf/' berisi 45 file .inp
 
Tidak memerlukan library eksternal — hanya menggunakan modul standar Python (os).
"""
 
import os
 
# ── Konfigurasi ──────────────────────────────────────────────
OUTPUT_DIR = "inputs_casscf"  # folder output
R_START    = 30               # 0.30 Å × 100 (integer untuk menghindari float drift)
R_STOP     = 250              # 2.50 Å × 100
R_STEP     = 5                # 0.05 Å × 100
NPROCS     = 1                # jumlah core per job
# ─────────────────────────────────────────────────────────────
 
# Bangun daftar panjang ikatan dengan aritmetika integer
# lalu konversi ke float di akhir → tidak ada floating-point drift
BOND_LENGTHS = [round(i / 100, 2) for i in range(R_START, R_STOP + R_STEP, R_STEP)]
 
# CASSCF(2,2): 2 elektron aktif, 2 orbital aktif = FCI untuk H2/STO-3G
# Modul CASSCF terpisah dari MDCI → tidak terkena bug CCSD/FCI di ORCA 6.1.1
TEMPLATE = """\
! CASSCF STO-3G SP
 
%pal
 nprocs {nprocs}
end
 
%casscf
 nel  2
 norb 2
end
 
* xyz 0 1
H  0.000000  0.000000  0.000000
H  0.000000  0.000000  {R:.6f}
*
"""
 
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
for R in BOND_LENGTHS:
    content  = TEMPLATE.format(R=R, nprocs=NPROCS)
    filename = os.path.join(OUTPUT_DIR, f"h2_{R:.2f}.inp")
    with open(filename, "w") as f:
        f.write(content)
 
print(f"✅ {len(BOND_LENGTHS)} file input berhasil dibuat di folder '{OUTPUT_DIR}/'")
print(f"   Rentang: {BOND_LENGTHS[0]:.2f} – {BOND_LENGTHS[-1]:.2f} Å")
print(f"   Method : CASSCF(2,2) / STO-3G  (≡ FCI untuk H₂)")
print()
print("Jalankan semua job dengan loop bash, contoh:")
print("  for f in inputs_casscf/*.inp; do orca $f > ${f%.inp}.out; done")