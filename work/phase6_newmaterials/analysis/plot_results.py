#!/usr/bin/env python3
"""Generate Phase 6 analysis figures from saved driver outputs."""

import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(path):
    path = ROOT / path
    if not path.exists():
        return None
    return np.genfromtxt(path, names=True)


def plot_dark_and_spectral():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    dark = load("regression_planar_dark.dat")
    if dark is not None:
        ax1.semilogy(-dark["V_anode_V"], np.abs(dark["J_anode_Acm2"]), "-o",
                     label="planar dark (ND=3e16)")
    doping_1e18 = load("sweep_nd_1e18_operating_point.dat")
    doping_3e16 = load("sweep_nd_3e16_operating_point.dat")
    if doping_3e16 is not None and doping_1e18 is not None:
        ax1.scatter(
            [2.0, 2.0],
            [abs(doping_3e16["J_dark_Acm2"]), abs(doping_1e18["J_dark_Acm2"])],
            color="C3",
            label="ND sweep @ -2 V",
        )
    ax1.axhline(1e-3, color="k", ls="--", lw=0.8, label="paper dark ~1e-3 A/cm2")
    ax1.set_xlabel("reverse bias (V)")
    ax1.set_ylabel("|J| (A/cm2)")
    ax1.grid(alpha=0.3, which="both")
    ax1.legend(fontsize=7)

    points = []
    for wavelength in (245, 255, 355):
        point = load(f"sweep_wl_{wavelength}_operating_point.dat")
        if point is not None:
            points.append((wavelength, point["R_AW"]))
    if points:
        wavelength, responsivity = zip(*sorted(points))
        ax2.plot(wavelength, responsivity, "o-", color="C0")
    ax2.axvline(255, color="grey", lw=0.8, ls="--")
    ax2.axhline(0.23, color="k", lw=0.8, ls="--", label="paper 0.23 A/W")
    ax2.set_xlabel("wavelength (nm)")
    ax2.set_ylabel("responsivity (A/W)")
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=7)

    fig.tight_layout()
    output = ROOT / "analysis" / "fig_phase6.png"
    fig.savefig(output, dpi=150)
    print("wrote", output)


def main():
    plot_dark_and_spectral()


if __name__ == "__main__":
    main()
