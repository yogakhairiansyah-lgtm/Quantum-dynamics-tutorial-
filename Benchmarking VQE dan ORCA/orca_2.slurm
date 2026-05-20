#!/bin/bash
#SBATCH --job-name=H2_SCAN
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8GB
#SBATCH --output=slurm-%j.out
#SBATCH --error=error-%j.txt

cd "/mgpfs/home/mkhairiansyah/Benchmarking VQE dan ORCA"

module load nuclear/orca/6.1.1

ORCA=/mgpfs/apps/nuclear/apps/orca/6.1.1/orca
INPUT_DIR=inputs_casscf
MAX_PARALLEL=8

echo "Start = $(date)"
echo "Total input: $(ls ${INPUT_DIR}/*.inp | wc -l) file"
echo "Method     : CASSCF(2,2) / STO-3G  [= FCI untuk H2]"
echo "=============================="

for file in ${INPUT_DIR}/*.inp; do
    out="${file%.inp}.out"
    echo "  → Running: $file"
    $ORCA "$file" > "$out" &

    while [ "$(jobs -rp | wc -l)" -ge "$MAX_PARALLEL" ]; do
        sleep 1
    done
done

wait

echo "=============================="
echo "Finish = $(date)"
echo ""
echo "=== CEK HASIL ==="
OK=0; FAIL=0
for out in ${INPUT_DIR}/*.out; do
    if grep -q "FINAL SINGLE POINT ENERGY" "$out" 2>/dev/null; then
        OK=$((OK + 1))
    else
        FAIL=$((FAIL + 1))
        echo "  ✗ GAGAL: $out"
    fi
done
echo "  ✓ Berhasil : $OK file"
echo "  ✗ Gagal    : $FAIL file"