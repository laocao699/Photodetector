import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def parse_curves(path, sweep_col):
    x, ib, ic = [], [], []
    for line in open(path):
        if line.startswith("CURVE:"):
            v = line.split(": ", 1)[1].split()
            x.append(float(v[sweep_col])); ib.append(float(v[3])); ic.append(float(v[4]))
    return np.array(x), np.array(ib), np.array(ic)

# ---- Figure 1: Gummel plots (Ic, Ib, beta vs Vbe) at different Vcb ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 10), sharex=True)
for vcb in ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5"]:
    x, ib, ic = parse_curves(f"ve_{vcb}_new.out", 2)   # sweep var = Ve (col 2)
    vbe = 0.0 - x  # Vb=0, Ve swept negative
    beta = np.abs(ic / np.where(ib == 0, 1e-300, ib))
    ax1.semilogy(vbe, np.abs(ic), label=f"$I_c$ Vcb={vcb}")
    ax1.semilogy(vbe, np.abs(ib), "--", alpha=0.6)
ax1.set_ylabel(r"$I$ (A/cm)")
ax1.set_title("Gummel plot (Vb=0, Ve swept negative); dashed = Ib")
ax1.legend(loc="upper left")

for vcb in ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5"]:
    x, ib, ic = parse_curves(f"ve_{vcb}_new.out", 2)
    vbe = 0.0 - x
    beta = np.abs(ic / np.where(ib == 0, 1e-300, ib))
    ax2.semilogy(vbe, beta, label=f"Vcb={vcb}")
ax2.set_xlabel(r"$V_{be}$ (V)")
ax2.set_ylabel(r"$\beta = I_c/I_b$")
ax2.set_title("Current gain beta")
ax2.legend(loc="upper left")
plt.tight_layout()
plt.savefig("bjt_gummel_new.png", dpi=110)

# ---- Figure 2: Ic-Vce family at different Vb ----
fig, ax = plt.subplots(figsize=(9, 6))
for vb in ["0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]:
    x, ib, ic = parse_curves(f"vb2_{vb}_new.out", 1)   # sweep var = Vce (col 1)
    ax.semilogy(x, np.abs(ic), label=f"Vb={vb}")
x, ib, ic = parse_curves("vb2_0.1_new.out", 1)
ax.semilogy(x, np.abs(ic), label="Vb=0.1 (loose tol)", ls=":")
ax.set_xlabel(r"$V_{ce}$ (V)")
ax.set_ylabel(r"$|I_c|$ (A/cm)")
ax.set_title("Ic-Vce family (common-emitter output characteristics)")
ax.legend()
plt.tight_layout()
plt.savefig("bjt_icvce_new.png", dpi=110)

# ---- Figure 3: fT vs Ic ----
data = np.loadtxt("ft_data_new.out")
fmin = data[0, 0]; imin = 0
IC, ft = [], []
for i in range(1, len(data)):
    if data[i, 0] == fmin:
        d = data[imin:i]; imin = i
        ic = d[:, 9] + 1j * d[:, 10]
        ib = d[:, 7] + 1j * d[:, 8]
        beta = np.abs(ic / ib)
        if beta[0] > 1:
            for j in range(1, len(beta)):
                if beta[j] < 1:
                    y1 = np.log(beta[j]); y0 = np.log(beta[j - 1])
                    x1 = np.log(d[j, 0]); x0 = np.log(d[j - 1, 0])
                    m = (y1 - y0) / (x1 - x0)
                    ft.append(np.exp(x1 - y1 / m))
                    IC.append(d[0, 5])
                    break
d = data[imin:]
ic = d[:, 9] + 1j * d[:, 10]; ib = d[:, 7] + 1j * d[:, 8]
beta = np.abs(ic / ib)
if beta[0] > 1:
    for j in range(1, len(beta)):
        if beta[j] < 1:
            y1 = np.log(beta[j]); y0 = np.log(beta[j - 1])
            x1 = np.log(d[j, 0]); x0 = np.log(d[j - 1, 0])
            m = (y1 - y0) / (x1 - x0)
            ft.append(np.exp(x1 - y1 / m)); IC.append(d[0, 5]); break
fig, ax = plt.subplots(figsize=(9, 6))
ax.semilogx(IC, ft, "-+")
ax.set_xlabel(r"$I_c$ (A/cm)")
ax.set_ylabel(r"$f_T$ (Hz)")
ax.set_title("Cutoff frequency fT vs collector current (Vcb=0)")
ax.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("bjt_ft_new.png", dpi=110)

print("peak fT = %.3e Hz at Ic = %.3e A/cm" % (max(ft), IC[np.argmax(ft)]))
print("saved: bjt_gummel_new.png, bjt_icvce_new.png, bjt_ft_new.png")
