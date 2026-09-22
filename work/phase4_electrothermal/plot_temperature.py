import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_tec(fn):
    varlist = None
    data = []
    with open(fn) as f:
        reading = False
        for line in f:
            if line.startswith("VARIABLES"):
                varlist = re.findall(r'"([^"]+)"', line)
            elif line.startswith("ZONE"):
                m = re.search(r"NODES=(\d+)", line)
                reading = True
                continue
            elif reading:
                data.extend(line.split())
    return varlist, np.array(data, dtype=float), int(m.group(1)) if m else 0


# ---- BJT 2D temperature field ----
vl, d, N = read_tec("bjt_electrothermal")
print("BJOT tecplot: nvar=%d, tokens=%d, NODES=%d" % (len(vl), len(d), N))
ix = vl.index("x"); iy = vl.index("y"); it = vl.index("Temperature")
x = d[ix * N:(ix + 1) * N]
y = d[iy * N:(iy + 1) * N]
T = d[it * N:(it + 1) * N]
print("BJT T: min=%.5f max=%.5f rise=%.5f K" % (T.min(), T.max(), T.max() - 300.0))
# hotspot location
k = np.argmax(T)
print("BJT hotspot at (x,y)=(%.4e, %.4e) cm, T=%.5f K" % (x[k], y[k], T[k]))

fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.scatter(x, y, c=T - 300.0, s=4, cmap="hot")
plt.colorbar(sc, label="T - 300 (K)")
ax.set_xlabel("x (cm)"); ax.set_ylabel("y (cm)")
ax.set_title("BJT electro-thermal: temperature rise field (max %.4f K)" % (T.max() - 300.0))
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("bjt_temperature.png", dpi=110)
print("saved bjt_temperature.png")

# ---- diode 1D temperature profile ----
vl2, d2, N2 = read_tec("diode_1d_electrothermal")
ix = vl2.index("x"); it = vl2.index("Temperature")
x2 = d2[ix * N2:(ix + 1) * N2]
T2 = d2[it * N2:(it + 1) * N2]
print("diode T: min=%.8f max=%.8f rise=%.3e K" % (T2.min(), T2.max(), T2.max() - 300.0))
