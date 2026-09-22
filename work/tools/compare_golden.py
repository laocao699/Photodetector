#!/usr/bin/env python3
"""compare_golden.py — Phase 3 BJT 复现结果与论文 golden 数据的自动对照。

golden 数据: devsim_bjt_example/data/  (2016 devsim "Beta 0.01" 生成)
本地复现  : work/phase3_bjt/*_new.out (devsim 2.10.0)

数据格式
--------
DC 曲线 6 列: Vb Vc Ve Ib Ic Ie
  - golden gummel_*/ic_vce_* 为 prep.sh 处理后的裸列
  - golden vc_*/ve_*/vb2_* 及本地 *_new.out 含 DEVSIM 日志 + "CURVE: " 前缀行
AC (fT) 13 列: f Vb Vc Ve Ib Ic Ie IRb IIb IRc IIc IRe IIe
  - golden ft_data.out / 本地 ft_data_new.out 均为提取后的裸列

用法
----
  python3 work/tools/compare_golden.py            # 对照全部可配对曲线
  python3 work/tools/compare_golden.py --ic-floor 1e-9
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GOLDEN = os.path.join(REPO, "devsim_bjt_example", "data")
LOCAL = os.path.join(REPO, "work", "phase3_bjt")


def read_rows(path, ncol, prefix=None):
    """从文件中提取 ncol 列浮点数据行，兼容裸列与带前缀(如 'CURVE: ')两种格式。"""
    rows = []
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            if prefix is not None:
                if not s.startswith(prefix):
                    continue
                s = s[len(prefix):].strip()
            parts = s.split()
            if len(parts) < ncol:
                continue
            try:
                vals = [float(p) for p in parts[:ncol]]
            except ValueError:
                continue
            rows.append(vals)
    if not rows:
        return None
    return np.array(rows)


def load_dc(golden_path, local_path):
    """加载一对 DC 曲线；本地优先按 'CURVE: ' 前缀解析，golden 兼容裸列/前缀。"""
    loc = read_rows(local_path, 6, prefix="CURVE:")
    if loc is None:
        loc = read_rows(local_path, 6)
    gold = read_rows(golden_path, 6, prefix="CURVE:")
    if gold is None:
        gold = read_rows(golden_path, 6)
    return gold, loc


def compare_dc(gold, loc, sweep_col, ic_floor, label):
    """按扫描变量插值比对 |Ic|（并附 Ib），返回 (mean%, max%, npts, 描述)。"""
    if gold is None or loc is None:
        return None
    xg, yg = gold[:, sweep_col], np.abs(gold[:, 4])
    xl, yl = loc[:, sweep_col], np.abs(loc[:, 4])
    # 以本地 x 为基准，在 golden 上插值（单调化 x）
    og = np.argsort(xg)
    xg, yg = xg[og], yg[og]
    ol = np.argsort(xl)
    xl, yl = xl[ol], yl[ol]
    # 仅在 golden x 覆盖范围内比较
    mask = (xl >= xg.min()) & (xl <= xg.max()) & (yl > ic_floor)
    if mask.sum() < 2:
        return None
    xlm, ylm = xl[mask], yl[mask]
    ygm = np.interp(xlm, xg, yg)
    valid = ygm > ic_floor
    if valid.sum() < 2:
        return None
    rel = np.abs(ylm[valid] - ygm[valid]) / ygm[valid] * 100.0
    return {
        "label": label,
        "npts": int(valid.sum()),
        "mean": float(rel.mean()),
        "max": float(rel.max()),
        "ic_range": (float(ylm[valid].min()), float(ylm[valid].max())),
    }


def extract_ft(path):
    """用 beta=|ic/ib| 在 log-log 上穿越 1 的频率提取 fT；返回 (peak_ft, ic_at_peak, [(ic,ft)...])。"""
    data = read_rows(path, 13)
    if data is None or len(data) < 3:
        return None
    fmin = data[0, 0]
    blocks, start = [], 0
    for i in range(1, len(data)):
        if data[i, 0] == fmin:
            blocks.append(data[start:i])
            start = i
    blocks.append(data[start:])
    pts = []
    for d in blocks:
        if len(d) < 3:
            continue
        ic = d[:, 9] + 1j * d[:, 10]
        ib = d[:, 7] + 1j * d[:, 8]
        with np.errstate(divide="ignore", invalid="ignore"):
            beta = np.abs(ic / ib)
        if not np.isfinite(beta[0]) or beta[0] <= 1:
            continue
        for j in range(1, len(beta)):
            if beta[j] < 1:
                y1, y0 = np.log(beta[j]), np.log(beta[j - 1])
                x1, x0 = np.log(d[j, 0]), np.log(d[j - 1, 0])
                m = (y1 - y0) / (x1 - x0)
                if m == 0:
                    break
                ft = np.exp(x1 - y1 / m)
                pts.append((float(d[0, 5]), float(ft)))
                break
    if not pts:
        return None
    peak = max(pts, key=lambda t: t[1])
    return {"peak_ft": peak[1], "ic_at_peak": peak[0], "npts": len(pts), "pts": pts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ic-floor", type=float, default=1e-9,
                    help="低于此 |Ic|(A/cm) 的点视为离态噪声，不参与比对")
    args = ap.parse_args()

    print("=" * 78)
    print("Phase 3 BJT — 本地复现 vs 论文 golden 对照 (devsim 2.10.0 vs Beta 0.01)")
    print("=" * 78)

    # (label, golden, local, sweep_col)
    pairs = []
    for vcb in ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5"]:
        pairs.append((f"Gummel  Vcb={vcb} (Ve扫)",
                      os.path.join(GOLDEN, f"gummel_{vcb}.out"),
                      os.path.join(LOCAL, f"ve_{vcb}_new.out"), 2))
    for vb in ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]:
        pairs.append((f"Ic-Vce  Vb={vb} (Vce扫)",
                      os.path.join(GOLDEN, f"ic_vce_{vb}.out"),
                      os.path.join(LOCAL, f"vb2_{vb}_new.out"), 1))
    for vc in ["0.0", "0.5"]:
        lp = os.path.join(LOCAL, f"vc_{vc}_new.out")
        if not os.path.exists(lp):
            lp = os.path.join(LOCAL, f"vc_{vc}.out")
        pairs.append((f"输出特性 Vc={vc} (Vb扫)",
                      os.path.join(GOLDEN, f"vc_{vc}.out"), lp, 0))

    print(f"\n{'曲线':<28}{'点数':>6}{'mean dIc%':>12}{'max dIc%':>12}   判定")
    print("-" * 78)
    results = []
    for label, gpath, lpath, scol in pairs:
        gold, loc = load_dc(gpath, lpath)
        r = compare_dc(gold, loc, scol, args.ic_floor, label)
        if r is None:
            print(f"{label:<28}{'—':>6}{'—':>12}{'—':>12}   [缺数据/无法配对]")
            continue
        verdict = "OK" if r["mean"] <= 3.0 else ("偏大" if r["mean"] <= 10 else "需查")
        print(f"{label:<28}{r['npts']:>6}{r['mean']:>11.2f}%{r['max']:>11.2f}%   {verdict}")
        results.append(r)

    # fT
    print("-" * 78)
    ft_g = extract_ft(os.path.join(GOLDEN, "ft_data.out"))
    ft_l = extract_ft(os.path.join(LOCAL, "ft_data_new.out"))
    if ft_g and ft_l:
        d = (ft_l["peak_ft"] - ft_g["peak_ft"]) / ft_g["peak_ft"] * 100.0
        print("\n截止频率 fT (Vcb=0):")
        print(f"  峰值 fT   本地 {ft_l['peak_ft']:.4e} Hz   golden {ft_g['peak_ft']:.4e} Hz   偏差 {d:+.2f}%")
        print(f"  峰值处 Ic 本地 {ft_l['ic_at_peak']:.4e}      golden {ft_g['ic_at_peak']:.4e} A/cm")
        print(f"  有效工作点数 本地 {ft_l['npts']}  golden {ft_g['npts']}")
        verdict = "OK" if abs(d) <= 5.0 else "需查"
        print(f"  判定: {verdict} (容差 <=5%)")
    else:
        print("\n截止频率 fT: [缺 ft_data / 无法提取]")

    # 汇总
    if results:
        means = [r["mean"] for r in results]
        print("\n" + "=" * 78)
        print(f"DC 曲线汇总: {len(results)} 条配对成功，"
              f"mean dIc% 区间 [{min(means):.2f}, {max(means):.2f}]，"
              f"总体均值 {np.mean(means):.2f}%")
        print("判据: 低注入区系统性 +2~2.8% 属 devsim 版本差异(见 REPORT)，非复现错误。")
        print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
