import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

numsFZ = pd.read_hdf("../data/numLISA_30bins_FZ.hdf", key="data")
numsF50 = pd.read_hdf("../data/numLISA_30bins_F50.hdf", key="data")

FIREmin = 0.00015
FIREmax = 13.346
Z_sun = 0.02
num = 30

met_bins = np.logspace(np.log10(FIREmin), np.log10(FIREmax), num) * Z_sun


Henums = numsFZ.He.values
COHenums = numsFZ.COHe.values
COnums = numsFZ.CO.values
ONenums = numsFZ.ONe.values

Henums05 = numsF50.He.values
COHenums05 = numsF50.COHe.values
COnums05 = numsF50.CO.values
ONenums05 = numsF50.ONe.values

fig, ax = plt.subplots(1, 4, figsize=(16, 4))

ax[0].plot(
    np.log10(met_bins[1:] / Z_sun),
    Henums / 1e5,
    drawstyle="steps-mid",
    color="xkcd:tomato red",
    lw=3,
    label="FZ",
)
ax[0].plot(
    np.log10(met_bins[1:] / Z_sun),
    Henums05 / 1e5,
    drawstyle="steps-mid",
    color="xkcd:tomato red",
    ls="--",
    lw=3,
    label="F50",
)
ax[0].text(0.05, 0.85, "He + He", fontsize=18, transform=ax[0].transAxes)

ax[1].plot(
    np.log10(met_bins[1:] / Z_sun),
    COHenums / 1e5,
    drawstyle="steps-mid",
    color="xkcd:blurple",
    lw=3,
    label="FZ",
)
ax[1].plot(
    np.log10(met_bins[1:] / Z_sun),
    COHenums05 / 1e5,
    drawstyle="steps-mid",
    color="xkcd:blurple",
    ls="--",
    lw=3,
    label="F50",
)
ax[1].text(0.05, 0.85, "CO + He", fontsize=18, transform=ax[1].transAxes)

ax[2].plot(
    np.log10(met_bins[1:] / Z_sun),
    COnums / 1e5,
    drawstyle="steps-mid",
    color="xkcd:pink",
    lw=3,
    label="FZ",
)
ax[2].plot(
    np.log10(met_bins[1:] / Z_sun),
    COnums05 / 1e5,
    drawstyle="steps-mid",
    color="xkcd:pink",
    ls="--",
    lw=3,
    label="F50",
)
ax[2].text(0.05, 0.85, "CO + CO", fontsize=18, transform=ax[2].transAxes)

ax[3].plot(
    np.log10(met_bins[1:] / Z_sun),
    ONenums / 1e5,
    drawstyle="steps-mid",
    color="xkcd:light blue",
    lw=3,
    label="FZ",
)
ax[3].plot(
    np.log10(met_bins[1:] / Z_sun),
    ONenums05 / 1e5,
    drawstyle="steps-mid",
    color="xkcd:light blue",
    ls="--",
    lw=3,
    label="F50",
)
ax[3].text(0.05, 0.85, "ONe + X", fontsize=18, transform=ax[3].transAxes)

for i in range(4):
    ax[i].set_xlabel("Log$_{10}$(Z/Z$_\odot$)", fontsize=18)
    ax[i].set_xticks([-3, -2, -1, 0, 1.0])
    ax[i].legend(
        loc="lower left",
        bbox_to_anchor=(-0.02, 1.01),
        ncol=2,
        borderaxespad=0,
        frameon=False,
        fontsize=15,
    )
    ax[i].xaxis.set_minor_locator(AutoMinorLocator())
    ax[i].yaxis.set_minor_locator(AutoMinorLocator())
    ax[i].tick_params(labelsize=15)

ax[0].set_ylabel(r"N$_{f_{\rm{GW}} \geq 10^{-4} \rm{Hz}}$ (Z) [10$^5$]", fontsize=18)
plt.tight_layout()
plt.savefig("lisa_nums.pdf", dpi=100)
