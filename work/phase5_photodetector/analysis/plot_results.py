#!/usr/bin/env python3
"""P5.4  --  analysis / plotting for the Si PIN photodiode benchmark.

Reads the .dat files produced by the drivers (run from the phase5 root) and
writes comparison figures into analysis/:

    analysis/fig_spectral.png : responsivity and EQE vs wavelength
    analysis/fig_dark.png     : dark I-V and C-V vs reverse bias

Usage:  python3 analysis/plot_results.py [data_dir] [out_dir]
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_PHASE5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = sys.argv[1] if len(sys.argv) > 1 else _PHASE5
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(_PHASE5, "analysis")
os.makedirs(OUT, exist_ok=True)


def load_photo(tag):
    f = os.path.join(DATA, "pd_pin_2d_photo_%s.dat" % tag)
    return np.genfromtxt(f, names=True) if os.path.exists(f) else None


def load_dark(tag):
    f = os.path.join(DATA, "pd_pin_2d_dark_%s.dat" % tag)
    return np.genfromtxt(f, names=True) if os.path.exists(f) else None


def plot_spectral():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for tag, style in (("20um", "-"), ("30um", "--")):
        d = load_photo(tag)
        if d is None:
            continue
        ax1.plot(d["lambda_nm"], d["R_barc_AW"], style, color="C0",
                 label="%s, BARC" % tag)
        ax1.plot(d["lambda_nm"], d["R_bare_AW"], style, color="C3",
                 label="%s, bare" % tag)
        ax2.plot(d["lambda_nm"], d["EQE_barc"] * 100, style, color="C0",
                 label="%s, BARC" % tag)
        ax2.plot(d["lambda_nm"], d["EQE_bare"] * 100, style, color="C3",
                 label="%s, bare" % tag)
    ax1.axhline(0.63, color="k", lw=0.8, ls=":", label="Roger 2018: 0.63 A/W")
    ax1.axvline(800, color="grey", lw=0.6)
    ax1.set_xlabel("wavelength (nm)")
    ax1.set_ylabel("responsivity (A/W)")
    ax1.set_title("Spectral responsivity")
    ax1.legend(fontsize=7)
    ax1.grid(alpha=0.3)
    ax2.axhline(100, color="k", lw=0.8, ls=":", label="100 %")
    ax2.axvline(750, color="grey", lw=0.6)
    ax2.set_xlabel("wavelength (nm)")
    ax2.set_ylabel("external QE (%)")
    ax2.set_title("External quantum efficiency")
    ax2.legend(fontsize=7)
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    p = os.path.join(OUT, "fig_spectral.png")
    fig.savefig(p, dpi=150)
    print("wrote", p)


def plot_dark():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for tag, style in (("20um", "-o"), ("30um", "--s")):
        d = load_dark(tag)
        if d is None:
            continue
        ax1.semilogy(d["V_cathode_V"], np.abs(d["I_dark_A"]) * 1e12, style,
                     label="%s iEPI" % tag)
        ax2.plot(d["V_cathode_V"], d["C_F"] * 1e12, style,
                 label="%s iEPI" % tag)
    ax1.axhspan(3.5, 10.0, color="green", alpha=0.15,
                label="Roger 2018 leakage 3.5-10 pA")
    ax1.set_xlabel("reverse bias (V)")
    ax1.set_ylabel("dark current (pA)")
    ax1.set_title("Dark leakage")
    ax1.legend(fontsize=7)
    ax1.grid(alpha=0.3, which="both")
    ax2.set_xlabel("reverse bias (V)")
    ax2.set_ylabel("capacitance (pF)")
    ax2.set_title("Junction C-V (SSAC)")
    ax2.legend(fontsize=7)
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    p = os.path.join(OUT, "fig_dark.png")
    fig.savefig(p, dpi=150)
    print("wrote", p)


if __name__ == "__main__":
    plot_spectral()
    plot_dark()
