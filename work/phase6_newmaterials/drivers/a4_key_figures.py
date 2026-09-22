#!/usr/bin/env python3
"""P1 key-figure validation: reproduce Boulahia 2024 trend figures + metrics.

Runs the core parameter sweeps of the planar IZTO/beta-Ga2O3/Al solar-blind
photodetector and writes a comparison summary + figures.  Each sweep uses the
shared build_device from a2_planar_photo (single-variable attribution).
"""

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from devsim import set_parameter  # noqa: E402
from devsim.python_packages.simple_physics import GetContactBiasName  # noqa: E402

import a2_planar_photo as a2  # noqa: E402
from device.ga2o3_schottky import (  # noqa: E402
    DONOR_CONCENTRATION_CM3,
    FILM_THICKNESS_CM,
    PLANAR_CONTACT_WIDTH_CM,
    doping_sweep_values,
)
from materials.ga2o3 import BETA_GA2O3, with_overrides  # noqa: E402
from physics import validation as V  # noqa: E402

ILLUMINATED_AREA_CM2 = PLANAR_CONTACT_WIDTH_CM * 1.0 + 2.0e-4  # width*depth*1
POWER_W_CM2 = 0.1  # incident 100 mW/cm^2


def sweep_iv(device, region, voltages, illuminated=False, wavelength_nm=255.0,
             power_w_cm2=POWER_W_CM2):
    """Return (V, J) arrays for dark or illuminated conditions."""
    if illuminated:
        a2.illuminate_at_operating_point(device, region, wavelength_nm,
                                         power_w_cm2)
    else:
        a2.wbg.set_dark_generation(device, region)
    out = []
    for v in voltages:
        set_parameter(device=device, name=GetContactBiasName("anode"), value=float(v))
        a2.solve_dc()
        j = a2.total_current(device, "anode") / PLANAR_CONTACT_WIDTH_CM
        out.append((v, j))
    return np.asarray(out)


def _safe_point(fn, *args):
    """Run a single sweep point, returning None on non-convergence."""
    try:
        return fn(*args)
    except Exception as exc:  # noqa: BLE001 - record and continue
        print("  [skip] %s" % exc)
        return None


def run():
    results = {}

    # ---- baseline device (used for I-V, PDCR, spectral, power, D*) ----
    dev, reg, geo = a2.build_device()
    voltages = np.arange(0.0, -2.001, -0.1)

    dark = sweep_iv(dev, reg, voltages, illuminated=False)
    illum = sweep_iv(dev, reg, voltages, illuminated=True)
    results["iv_dark"] = dark
    results["iv_illum"] = illum
    dark_floor = np.maximum(np.abs(dark[:, 1]), 1e-9)  # avoid div-by-0 at 0V
    pdcr = np.abs(illum[:, 1] / dark_floor)
    results["pdcr_v"] = np.column_stack([voltages, pdcr])

    # responsivity + EQE + D* at 255 nm operating point (-2 V)
    j_dark = dark[-1, 1]
    j_photo = illum[-1, 1] - j_dark
    # responsivity vs incident power over illuminated area
    R = abs(j_photo) / POWER_W_CM2  # A/W using power density
    eqe = V.eqe_from_responsivity(R, 255.0)
    # RA product from dark J-V slope near 0 V
    djdV = np.gradient(dark[:, 1], voltages)
    ra = 1.0 / abs(np.interp(0.0, voltages, djdV))
    dstar = V.detectivity_jones(R, 255.0, ra)
    results["operating"] = dict(j_dark=j_dark, j_photo=j_photo, R=R, eqe=eqe,
                                ra=ra, dstar=dstar)

    # ---- spectral sweep ----
    spectral = []
    for wl in (220.0, 255.0, 300.0, 400.0, 450.0):
        a2.wbg.set_dark_generation(dev, reg)
        set_parameter(device=dev, name=GetContactBiasName("anode"), value=-2.0)
        a2.solve_dc()
        jdark = a2.total_current(dev, "anode") / PLANAR_CONTACT_WIDTH_CM
        jillum = a2.illuminate_at_operating_point(dev, reg, wl, POWER_W_CM2)
        jph = jillum - jdark
        spectral.append((wl, abs(jph), abs(jph) / POWER_W_CM2))
    results["spectral"] = np.asarray(spectral)

    # ---- power sweep at 255 nm ----
    power = []
    for scale in (1e-2, 1e-1, 0.5, 1.0):
        a2.wbg.set_dark_generation(dev, reg)
        set_parameter(device=dev, name=GetContactBiasName("anode"), value=-2.0)
        a2.solve_dc()
        jdark = a2.total_current(dev, "anode") / PLANAR_CONTACT_WIDTH_CM
        jillum = a2.illuminate_at_operating_point(dev, reg, 255.0,
                                                  0.1 * scale)
        power.append((scale, abs(jillum - jdark)))
    results["power"] = np.asarray(power)

    # ---- doping sweep (rebuild per doping; skip non-converging points) ----
    doping = []
    for nd in (3.0e16, 1.0e17, 1.0e18):
        def _one_doping(nd_):
            d_dev, d_reg, _ = a2.build_device(donor_concentration_cm3=nd_,
                                              name="nd_%.0e" % nd_)
            d = sweep_iv(d_dev, d_reg, np.array([-2.0]), illuminated=False)
            i = sweep_iv(d_dev, d_reg, np.array([-2.0]), illuminated=True)
            return (nd_, d[0, 1], i[0, 1] - d[0, 1])
        r = _safe_point(_one_doping, nd)
        if r is not None:
            doping.append(r)
    results["doping"] = np.asarray(doping)

    # ---- thickness sweep (values are nm; paper range 100-900 nm) ----
    thickness = []
    for t_nm in (100.0, 300.0, 900.0):
        def _one_thickness(t_nm_):
            t_dev, t_reg, _ = a2.build_device(thickness_cm=t_nm_ * 1e-7,
                                              name="th_%.0f" % t_nm_)
            d = sweep_iv(t_dev, t_reg, np.array([-2.0]), illuminated=False)
            i = sweep_iv(t_dev, t_reg, np.array([-2.0]), illuminated=True)
            return (t_nm_, i[0, 1] - d[0, 1])
        r = _safe_point(_one_thickness, t_nm)
        if r is not None:
            thickness.append(r)
    results["thickness"] = np.asarray(thickness)

    return results


def make_figures(results, out):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    ax = axes[0, 0]
    ax.semilogy(-results["iv_dark"][:, 0], np.abs(results["iv_dark"][:, 1]),
                "o-", label="dark")
    ax.semilogy(-results["iv_illum"][:, 0], np.abs(results["iv_illum"][:, 1]),
                "s-", label="illum 255nm")
    ax.set_xlabel("reverse bias (V)")
    ax.set_ylabel("|J| (A/cm2)")
    ax.set_title("I-V")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")

    ax = axes[0, 1]
    ax.plot(-results["pdcr_v"][:, 0], results["pdcr_v"][:, 1], "o-")
    ax.set_xlabel("reverse bias (V)")
    ax.set_ylabel("PDCR")
    ax.set_yscale("log")
    ax.set_title("Photo-to-dark current ratio")
    ax.grid(alpha=0.3, which="both")

    ax = axes[0, 2]
    ax.plot(results["spectral"][:, 0], results["spectral"][:, 2], "o-")
    ax.axvline(261, color="r", ls="--", label="cutoff ~261 nm")
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("R (A/W)")
    ax.set_title("Spectral responsivity")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.loglog(results["power"][:, 0], results["power"][:, 1], "o-")
    ax.set_xlabel("power scale")
    ax.set_ylabel("|J_ph| (A/cm2)")
    ax.set_title("Photocurrent vs power")
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    if len(results["doping"]):
        ax.loglog(results["doping"][:, 0], np.abs(results["doping"][:, 1]),
                  "o-", label="dark")
        ax.loglog(results["doping"][:, 0], np.abs(results["doping"][:, 2]),
                  "s-", label="photo")
        ax.set_xlabel("Nd (cm-3)")
        ax.set_ylabel("J (A/cm2)")
        ax.set_title("Doping dependence")
        ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")

    ax = axes[1, 2]
    if len(results["thickness"]):
        ax.plot(results["thickness"][:, 0], np.abs(results["thickness"][:, 1]), "o-")
        ax.set_xlabel("Ga2O3 thickness (nm)")
        ax.set_ylabel("|J_ph| (A/cm2)")
        ax.set_title("Thickness dependence")
        ax.grid(alpha=0.3)

    fig.suptitle("Phase 6A key-figure validation (Boulahia 2024)")
    fig.tight_layout()
    fig.savefig(out, dpi=150)


def main():
    results = run()
    op = results["operating"]
    print("==== Phase 6A key-figure summary (Boulahia 2024) ====")
    print("dark J(-2V)      = %.4e A/cm2   (paper ~1e-3)" % op["j_dark"])
    print("photo J(-2V)     = %.4e A/cm2   (paper ~7e-3 / Fig10c)" % op["j_photo"])
    print("PDCR @ -2V       = %.3e         (paper ~1e2)" % results["pdcr_v"][-1, 1])
    print("PDCR @ 0V        = %.3e         (dark-floor limited; paper ~3e4)" % results["pdcr_v"][0, 1])
    print("R @ 255nm        = %.4f A/W     (paper ~0.23)" % op["R"])
    print("EQE @ 255nm      = %.3f" % op["eqe"])
    print("D* @ 255nm       = %.3e Jones   (paper ~2.5e9)" % op["dstar"])
    print("spectral cutoff  ~ %d nm" % int(
        results["spectral"][np.argmax(results["spectral"][:, 2]), 0]))
    out = ROOT / "analysis" / "fig_key_figures.png"
    make_figures(results, out)
    print("wrote", out)

    # save machine-readable summary
    with open(ROOT / "key_figures_summary.txt", "w") as f:
        f.write(repr(op) + "\n")


if __name__ == "__main__":
    main()
