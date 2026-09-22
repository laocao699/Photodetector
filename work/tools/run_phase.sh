#!/usr/bin/env bash
# =============================================================================
# run_phase.sh — DEVSIM 研究项目各 Phase 的端到端复现入口
#
# 用法:
#   bash work/tools/run_phase.sh <phase> [only]
#     phase : 1 | 3 | 4 | 5 | 6
#     only  : 可选，仅跑某个子步骤（关键字匹配，如 equil / gummel / ft / dark）
#
# 行为:
#   - 每个 Phase 在其自身目录下运行（驱动脚本以 phase 目录为 cwd 导入本地包）
#   - stdout/stderr 统一 tee 到 work/logs/<phase>_<step>.log
#   - Phase 3 的扫描产物按官方约定写回 phase3_bjt/*_new.out
#   - 不使用 set -e：单步失败也继续，末尾汇总退出码，便于一次性看全貌
# =============================================================================
set -uo pipefail

TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$(cd "$TOOLS/.." && pwd)"
LOGS="$WORK/logs"
mkdir -p "$LOGS"

PHASE="${1:-}"
ONLY="${2:-}"

ts() { date '+%H:%M:%S'; }

# run <logfile> <cwd> <cmd...>
run() {
  local log="$1"; shift
  local cwd="$1"; shift
  echo "[$(ts)] >>> $* (cwd=$(basename "$cwd")) -> logs/$(basename "$log")"
  ( cd "$cwd" && "$@" ) >"$log" 2>&1
  local rc=$?
  echo "[$(ts)]     exit=$rc"
  return $rc
}

want() { [[ -z "$ONLY" || "$1" == *"$ONLY"* ]]; }

FAILS=0

# ---------------------------------------------------------------------------
phase1() {
  local d="$WORK/phase1_diode"
  for s in diode_1d diode_2d gmsh_diode2d gmsh_diode3d ssac_diode tran_diode analyze_diode; do
    want "$s" || continue
    run "$LOGS/phase1_$s.log" "$d" python3 "$s.py" || FAILS=$((FAILS+1))
  done
}

# ---------------------------------------------------------------------------
phase3() {
  local d="$WORK/phase3_bjt"
  # 1) 平衡态（后续所有 circuit 脚本 load_devices 依赖 bjt_dd_0.msh）
  if want equil || want all || [[ -z "$ONLY" ]]; then
    run "$LOGS/phase3_bjt_dd.log" "$d" python3 bjt_dd.py || FAILS=$((FAILS+1))
  fi
  # 2) Ic-Vce 族 (vb2_<Vb>)：固定 Vb，扫 Vc 0->1.5  -> golden ic_vce_<Vb>
  if want icvce || want vb2 || [[ -z "$ONLY" ]]; then
    for Vb in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
      # Vb=0.1 处于近截止离态(电流~1e-12A 纯噪声)，需放宽容差到 1e-2 才能扫完
      local tol=""
      [[ "$Vb" == "0.1" ]] && tol="1e-2"
      echo "[$(ts)] >>> bjt_circuit2.py $Vb $tol -> vb2_${Vb}_new.out"
      ( cd "$d" && python3 bjt_circuit2.py "$Vb" $tol ) >"$d/vb2_${Vb}_new.out" 2>&1 || FAILS=$((FAILS+1))
    done
  fi
  # 3) 输出特性 (vc_<Vc>)：固定 Vc，扫 Vb 0->1.0
  if want vc || [[ -z "$ONLY" ]]; then
    for Vc in 0.0 0.5; do
      echo "[$(ts)] >>> bjt_circuit3.py $Vc -> vc_${Vc}_new.out"
      ( cd "$d" && python3 bjt_circuit3.py "$Vc" ) >"$d/vc_${Vc}_new.out" 2>&1 || FAILS=$((FAILS+1))
    done
  fi
  # 4) Gummel (ve_<Vcb>)：固定 Vcb，扫 Ve 0->-1.0  -> golden gummel_<Vcb>
  if want gummel || want ve || [[ -z "$ONLY" ]]; then
    for Vc in 0.0 0.1 0.2 0.3 0.4 0.5; do
      echo "[$(ts)] >>> bjt_circuit4.py $Vc -> ve_${Vc}_new.out"
      ( cd "$d" && python3 bjt_circuit4.py "$Vc" ) >"$d/ve_${Vc}_new.out" 2>&1 || FAILS=$((FAILS+1))
    done
  fi
  # 5) fT (ssac -> ft_data)：Vcb=0，Ve 扫，AC 1e3->1e11 Hz，ppd=3
  if want ft || want ssac || [[ -z "$ONLY" ]]; then
    echo "[$(ts)] >>> bjt_circuit5.py 0.0 1000 1e11 3 -> ssac_0.0_new.out"
    ( cd "$d" && python3 bjt_circuit5.py 0.0 1000 1e11 3 ) >"$d/ssac_0.0_new.out" 2>&1 || FAILS=$((FAILS+1))
    ( cd "$d" && grep 'AC: ' ssac_0.0_new.out | sed 's/AC: //' > ft_data_new.out )
  fi
  # 6) 出图
  if want plot || [[ -z "$ONLY" ]]; then
    run "$LOGS/phase3_plot.log" "$d" python3 plot_bjt.py || FAILS=$((FAILS+1))
  fi
}

# ---------------------------------------------------------------------------
phase4() {
  local d="$WORK/phase4_electrothermal"
  want diode && { run "$LOGS/phase4_diode.log" "$d" python3 diode_1d_electrothermal.py || FAILS=$((FAILS+1)); }
  want bjt   && { run "$LOGS/phase4_bjt.log"   "$d" python3 bjt_electrothermal.py     || FAILS=$((FAILS+1)); }
  want plot  && { run "$LOGS/phase4_plot.log"  "$d" python3 plot_temperature.py        || FAILS=$((FAILS+1)); }
}

# ---------------------------------------------------------------------------
phase5() {
  local d="$WORK/phase5_photodetector"
  want pn1d    && { run "$LOGS/phase5_pn1d.log"    "$d" python3 drivers/pd_pn_1d.py            || FAILS=$((FAILS+1)); }
  want dark20  && { run "$LOGS/phase5_dark20.log"  "$d" python3 drivers/pd_pin_2d_dark.py 20 1e-4  || FAILS=$((FAILS+1)); }
  want dark30  && { run "$LOGS/phase5_dark30.log"  "$d" python3 drivers/pd_pin_2d_dark.py 30 1e-4  || FAILS=$((FAILS+1)); }
  want photo20 && { run "$LOGS/phase5_photo20.log" "$d" python3 drivers/pd_pin_2d_photo.py 20 1e-3 5 || FAILS=$((FAILS+1)); }
  want photo30 && { run "$LOGS/phase5_photo30.log" "$d" python3 drivers/pd_pin_2d_photo.py 30 1e-3 5 || FAILS=$((FAILS+1)); }
  want plot    && { run "$LOGS/phase5_plot.log"    "$d" python3 analysis/plot_results.py       || FAILS=$((FAILS+1)); }
}

# ---------------------------------------------------------------------------
phase6() {
  local d="$WORK/phase6_newmaterials"
  want tests && { run "$LOGS/phase6_tests.log" "$d" python3 -m unittest discover -s tests -v || FAILS=$((FAILS+1)); }
  want a0 && { run "$LOGS/phase6_a0.log" "$d" python3 drivers/a0_material_check.py || FAILS=$((FAILS+1)); }
  want a1 && { run "$LOGS/phase6_a1.log" "$d" python3 drivers/a1_schottky_dark.py  || FAILS=$((FAILS+1)); }
  want a2 && { run "$LOGS/phase6_a2.log" "$d" python3 drivers/a2_planar_photo.py   || FAILS=$((FAILS+1)); }
  # 逐项物理标定变体（opt-in：仅当 only 显式包含 arora/traps 时运行，不入默认全量跑）
  [[ "$ONLY" == *arora* ]] && { run "$LOGS/phase6_a2_arora.log" "$d" python3 drivers/a2_planar_photo.py --arora --tag a2_arora || FAILS=$((FAILS+1)); }
  [[ "$ONLY" == *traps* ]] && { run "$LOGS/phase6_a2_traps.log" "$d" python3 drivers/a2_planar_photo.py --traps --tag a2_traps || FAILS=$((FAILS+1)); }
  want a3 && { run "$LOGS/phase6_a3.log" "$d" python3 drivers/a3_msm_photo.py      || FAILS=$((FAILS+1)); }
  want a4 && { run "$LOGS/phase6_a4.log" "$d" python3 drivers/a4_key_figures.py    || FAILS=$((FAILS+1)); }
  want plot && { run "$LOGS/phase6_plot.log" "$d" python3 analysis/plot_results.py || FAILS=$((FAILS+1)); }
}

# ---------------------------------------------------------------------------
case "$PHASE" in
  1) phase1 ;;
  3) phase3 ;;
  4) phase4 ;;
  5) phase5 ;;
  6) phase6 ;;
  all) phase1; phase3; phase4; phase5; phase6 ;;
  *) echo "用法: run_phase.sh <1|3|4|5|6|all> [only]"; exit 2 ;;
esac

echo "=================================================="
echo "[$(ts)] Phase $PHASE 完成，失败步骤数 = $FAILS"
exit $(( FAILS > 0 ? 1 : 0 ))
