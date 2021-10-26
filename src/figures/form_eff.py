from matplotlib.ticker import AutoMinorLocator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

met_arr = np.logspace(np.log10(1e-4), np.log10(0.03), 15)
met_arr = np.round(met_arr, 8)
met_arr = np.append(0.0, met_arr)
Z_sun = 0.02

DWDeff = pd.read_hdf("../data/DWDeff_FZ.hdf", key="data")
effHe = DWDeff.He.values
effCOHe = DWDeff.COHe.values
effCO = DWDeff.CO.values
effONe = DWDeff.ONe.values

DWDeff05 = pd.read_hdf("../data/DWDeff_F50.hdf", key="data")
effHe05 = DWDeff05.He.values
effCOHe05 = DWDeff05.COHe.values
effCO05 = DWDeff05.CO.values
effONe05 = DWDeff05.ONe.values

fig, ax = plt.subplots(1, 4, figsize=(16, 4))
ax[0].plot(
    np.log10(met_arr[1:] / Z_sun),
    effHe * 1e3,
    color="xkcd:tomato red",
    drawstyle="steps-mid",
    lw=3,
    label="FZ",
)
ax[0].plot(
    np.log10(met_arr[1:] / Z_sun),
    effHe05 * 1e3,
    color="xkcd:tomato red",
    ls="--",
    drawstyle="steps-mid",
    lw=3,
    label="F50",
)

ax[1].plot(
    np.log10(met_arr[1:] / Z_sun),
    effCOHe * 1e3,
    color="xkcd:blurple",
    drawstyle="steps-mid",
    lw=3,
    label="FZ",
)
ax[1].plot(
    np.log10(met_arr[1:] / Z_sun),
    effCOHe05 * 1e3,
    color="xkcd:blurple",
    ls="--",
    drawstyle="steps-mid",
    lw=3,
    label="F50",
)

ax[2].plot(
    np.log10(met_arr[1:] / Z_sun),
    effCO * 1e3,
    color="xkcd:pink",
    drawstyle="steps-mid",
    lw=3,
    label="FZ",
)
ax[2].plot(
    np.log10(met_arr[1:] / Z_sun),
    effCO05 * 1e3,
    color="xkcd:pink",
    ls="--",
    drawstyle="steps-mid",
    lw=3,
    label="F50",
)

ax[3].plot(
    np.log10(met_arr[1:] / Z_sun),
    effONe * 1e3,
    color="xkcd:light blue",
    drawstyle="steps-mid",
    lw=3,
    label="FZ",
)
ax[3].plot(
    np.log10(met_arr[1:] / Z_sun),
    effONe05 * 1e3,
    color="xkcd:light blue",
    ls="--",
    drawstyle="steps-mid",
    lw=3,
    label="F50",
)

ax[0].set_ylabel(r"$\eta_{\rm{form}}$ [10$^{-3}$ M$_\odot^{-1}$]", fontsize=18)


labels = ["He + He", "CO + He", "CO + CO", "ONe + X"]
for i in range(4):
    ax[i].set_xticks([-2, -1.5, -1, -0.5, 0.0])
    ax[i].text(0.05, 0.05, labels[i], fontsize=18, transform=ax[i].transAxes)
    ax[i].legend(
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=3,
        borderaxespad=0,
        frameon=False,
        fontsize=15,
    )
    ax[i].set_xlabel("Log$_{10}$(Z/Z$_\odot$)", fontsize=18)
    ax[i].xaxis.set_minor_locator(AutoMinorLocator())
    ax[i].yaxis.set_minor_locator(AutoMinorLocator())
    ax[i].tick_params(labelsize=15)

plt.tight_layout()
plt.savefig("form_eff.pdf", dpi=100)
