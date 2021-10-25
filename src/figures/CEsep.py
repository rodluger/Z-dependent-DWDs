from matplotlib.ticker import AutoMinorLocator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


# Needed for `\langle` and `\rangle` commands
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"


Heinter = pd.read_hdf("../data/10_10_intersep_FZ.hdf", key="data")
COHeinter = pd.read_hdf("../data/11_10_intersep_FZ.hdf", key="data")
COinter = pd.read_hdf("../data/11_11_intersep_FZ.hdf", key="data")
ONeinter = pd.read_hdf("../data/12_intersep_FZ.hdf", key="data")

FIREmin = 0.00015
FIREmax = 13.346
Z_sun = 0.02
num = 30
met_bins = np.logspace(np.log10(FIREmin), np.log10(FIREmax), num)  # *Z_sun
met_mids = (met_bins[1:] + met_bins[:-1]) / 2
whichsep = "CEsep"

Heavgs = []
Hecovs = []
COHeavgs = []
COHecovs = []
COavgs = []
COcovs = []
ONeavgs = []
ONecovs = []
for i in range(num - 1):
    meti = met_bins[i]
    metf = met_bins[i + 1]

    Hebin = Heinter.loc[(Heinter.met >= meti) & (Heinter.met <= metf)]
    if len(Hebin) != 0:
        Heavgs.append(np.mean(Hebin[whichsep].values))
        Hecovs.append(np.std(Hebin[whichsep].values))
    else:
        Heavgs.append(0.0)
        Hecovs.append(0.0)

    COHebin = COHeinter.loc[(COHeinter.met >= meti) & (COHeinter.met <= metf)]
    if len(COHebin) != 0:
        COHeavgs.append(np.mean(COHebin[whichsep].values))
        COHecovs.append(np.std(COHebin[whichsep].values))
    else:
        COHeavgs.append(0.0)
        COHecovs.append(0.0)

    CObin = COinter.loc[(COinter.met >= meti) & (COinter.met <= metf)]
    if len(CObin) != 0:
        COavgs.append(np.mean(CObin[whichsep].values))
        COcovs.append(np.std(CObin[whichsep].values))
    else:
        COavgs.append(0.0)
        COcovs.append(0.0)

    ONebin = ONeinter.loc[(ONeinter.met >= meti) & (ONeinter.met <= metf)]
    if len(ONebin) != 0:
        ONeavgs.append(np.mean(ONebin[whichsep].values))
        ONecovs.append(np.std(ONebin[whichsep].values))
    else:
        ONeavgs.append(0.0)
        ONecovs.append(0.0)

Heavgs = np.array(Heavgs)
Hecovs = np.array(Hecovs)
COHeavgs = np.array(COHeavgs)
COHecovs = np.array(COHecovs)
COavgs = np.array(COavgs)
COcovs = np.array(COcovs)
ONeavgs = np.array(ONeavgs)
ONecovs = np.array(ONecovs)

fig, ax = plt.subplots(1, 4, figsize=(16, 4))
ax[0].plot(
    np.log10(met_mids[Heavgs > 0]),
    Heavgs[Heavgs > 0] / 1e3,
    color="xkcd:tomato red",
    lw=3,
    ls="-",
    label="He + He",
    drawstyle="steps-mid",
)
ax[0].fill_between(
    np.log10(met_mids[Heavgs > 0]),
    (Heavgs[Heavgs > 0] - Hecovs[Heavgs > 0]) / 1e3,
    (Heavgs[Heavgs > 0] + Hecovs[Heavgs > 0]) / 1e3,
    alpha=0.3,
    color="xkcd:tomato red",
    zorder=0,
    step="mid",
    label="$1\sigma$",
)

ax[2].plot(
    np.log10(met_mids[COavgs > 0]),
    COavgs[COavgs > 0] / 1e3,
    color="xkcd:pink",
    lw=3,
    ls="-",
    label="CO + CO",
    drawstyle="steps-mid",
)
ax[2].fill_between(
    np.log10(met_mids[COavgs > 0]),
    (COavgs[COavgs > 0] - COcovs[COavgs > 0]) / 1e3,
    (COavgs[COavgs > 0] + COcovs[COavgs > 0]) / 1e3,
    alpha=0.3,
    color="xkcd:pink",
    zorder=0,
    step="mid",
    label="$1\sigma$",
)

ax[1].plot(
    np.log10(met_mids),
    COHeavgs / 1e3,
    color="xkcd:blurple",
    lw=3,
    ls="-",
    label="CO + He",
    drawstyle="steps-mid",
)
ax[1].fill_between(
    np.log10(met_mids[COHeavgs > 0]),
    (COHeavgs[COHeavgs > 0] - COHecovs[COHeavgs > 0]) / 1e3,
    (COHeavgs[COHeavgs > 0] + COHecovs[COHeavgs > 0]) / 1e3,
    alpha=0.3,
    color="xkcd:blurple",
    zorder=0,
    step="mid",
    label="$1\sigma$",
)

ax[3].plot(
    np.log10(met_mids[ONeavgs > 0]),
    ONeavgs[ONeavgs > 0] / 1e3,
    color="xkcd:light blue",
    lw=3,
    label="ONe + X",
    drawstyle="steps-mid",
)
ax[3].fill_between(
    np.log10(met_mids[ONeavgs > 0]),
    (ONeavgs[ONeavgs > 0] - ONecovs[ONeavgs > 0]) / 1e3,
    (ONeavgs[ONeavgs > 0] + ONecovs[ONeavgs > 0]) / 1e3,
    alpha=0.3,
    color="xkcd:light blue",
    zorder=0,
    step="mid",
    label="$1\sigma$",
)

for i in range(4):
    ax[i].set_xticks([-3.0, -2.0, -1.0, 0.0, 1.0])
    ax[i].tick_params(labelsize=15)
    ax[i].set_xlim(np.log10(met_mids[0]), np.log10(met_mids[-1]))
    ax[i].set_xlabel("Log$_{10}$(Z/Z$_\odot$)", fontsize=18)
    ax[i].legend(
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=2,
        borderaxespad=0,
        frameon=False,
        fontsize=15,
        markerscale=0.5,
    )
    ax[i].xaxis.set_minor_locator(AutoMinorLocator())
    ax[i].yaxis.set_minor_locator(AutoMinorLocator())
ax[0].set_ylabel(r"$\langle a_{\rm{RLOF}}\rangle$ [10$^3$ R$_\odot$]", fontsize=18)

plt.tight_layout()
plt.savefig("CEsep.pdf", dpi=100)
