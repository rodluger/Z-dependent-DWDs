from matplotlib.ticker import AutoMinorLocator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils

'''
Creates plot files with formation efficiency of DWDs. In order to
run this, there must be already-existing LISA band files created with
make_galaxy() at pathtoLband.
    
INPUTS
----------------------
pathtodat [str]: path to folder containing datfiles 
pathtoLband [str]: path to folder containing LISA band files
pathtosave [str]: path to folder to save formation efficiency information to
    
RETURNS
----------------------
No direct function outputs, but saves formation efficiency data for all
DWD types and metallicity bins to files contained in pathtosave.
'''
def formeff(datfiles, pathtodat, label, model):
    lenconv = []
    masslist = []
    for i in range(15):
        if model == 'F50':
            binfrac = 0.5
            ratio = ratio_05
        elif model == 'FZ':
            binfrac = binfracs[i]
            ratio = ratios[i]
        mass_binaries = pd.read_hdf(pathtodat + datfiles[i], key='mass_stars').iloc[-1]
        mass = (1 + ratio) * mass_binaries
        conv = pd.read_hdf(pathtodat + datfiles[i], key='conv')
                            
        masslist.append(mass)
        lenconv.append(len(conv))

    lenconv = np.array(lenconv)
    masslist = np.concatenate(np.array(masslist))
    eff = lenconv / masslist
    return eff

met_arr = np.logspace(np.log10(1e-4), np.log10(0.03), 15)
met_arr = np.round(met_arr, 8)
met_arr = np.append(0.0, met_arr)
Z_sun = 0.02

binfracs = np.array([0.4847, 0.4732, 0.4618, 0.4503, 0.4388, 
                     0.4274, 0.4159, 0.4044, 0.3776, 0.3426, 
                     0.3076, 0.2726, 0.2376, 0.2027, 0.1677])

ratios = np.array([0.68, 0.71, 0.74, 0.78, 0.82, 
                   0.86, 0.9, 0.94, 1.05, 1.22, 
                   1.44, 1.7 , 2.05, 2.51, 3.17])

ratio_05 = 0.64

kstar1_list = ['10', '11', '11', '12']
kstar2_list = ['10', '10', '11', '10_12']
labels = ['10_10', '11_10', '11_11', '12']
pathtodat = "../data/"
eff_var = []
eff_05 = []
for kstar1, kstar2, label in zip(kstar1_list, kstar2_list, labels):
    files, lab = utils.getfiles(kstar1=kstar1, kstar2=kstar2, model="fiducial")
    eff_var.append(formeff(files, pathtodat, label, 'FZ'))
    eff_05.append(formeff(files, pathtodat, label, 'F50'))
    print('finished {}'.format(label))

DWDeff = pd.DataFrame(np.array(eff_var).T, columns=['He', 'COHe', 'CO', 'ONe'])

DWDeff05 = pd.DataFrame(np.array(eff_05).T, columns=['He', 'COHe', 'CO', 'ONe'])
    

effHe = DWDeff.He.values
effCOHe = DWDeff.COHe.values
effCO = DWDeff.CO.values
effONe = DWDeff.ONe.values

effHe05 = DWDeff05.He.values
effCOHe05 = DWDeff05.COHe.values
effCO05 = DWDeff05.CO.values
effONe05 = DWDeff05.ONe.values

fig, ax = plt.subplots(1, 4, figsize=(16, 4.5))
ax[0].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effHe*1e3, 
    color='xkcd:tomato red',
    drawstyle='steps-mid', 
    lw=3, 
    label='FZ', 
    rasterized=True
)

ax[0].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effHe05*1e3, 
    color='xkcd:tomato red',
    ls='--', 
    drawstyle='steps-mid', 
    lw=3, 
    label='F50', 
    rasterized=True
)

ax[1].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effCOHe*1e3, 
    color='xkcd:blurple', 
    drawstyle='steps-mid', 
    lw=3, 
    label='FZ', 
    rasterized=True
)

ax[1].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effCOHe05*1e3, 
    color='xkcd:blurple', 
    ls='--', 
    drawstyle='steps-mid', 
    lw=3, 
    label='F50', 
    rasterized=True
)

ax[2].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effCO*1e3, 
    color='xkcd:pink', 
    drawstyle='steps-mid', 
    lw=3, 
    label='FZ', 
    rasterized=True
)

ax[2].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effCO05*1e3, 
    color='xkcd:pink', 
    ls='--', 
    drawstyle='steps-mid', 
    lw=3, 
    label='F50', 
    rasterized=True
)

ax[3].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effONe*1e3, 
    color='xkcd:light blue', 
    drawstyle='steps-mid', 
    lw=3, 
    label='FZ', 
    rasterized=True
)

ax[3].plot(
    np.log10(met_arr[1:]/Z_sun), 
    effONe05*1e3, 
    color='xkcd:light blue', 
    ls='--', 
    drawstyle='steps-mid', 
    lw=3, 
    label='F50', 
    rasterized=True
)

ax[0].set_ylabel(
    r'$\eta_{\rm{form}}$ [10$^{-3}$ M$_\odot^{-1}$]', 
    fontsize=18
)


labels = ['He + He', "CO + He", 'CO + CO', "ONe + X"]
for i in range(4):
    ax[i].set_xticks([-2, -1.5, -1, -0.5, 0.])
    ax[i].text(0.05, 0.05, labels[i], fontsize=18, transform=ax[i].transAxes)
    ax[i].legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=3, borderaxespad=0, 
               frameon=False, fontsize=15)
    ax[i].set_xlabel('Log$_{10}$(Z/Z$_\odot$)', fontsize=18)
    ax[i].xaxis.set_minor_locator(AutoMinorLocator())
    ax[i].yaxis.set_minor_locator(AutoMinorLocator())
    ax[i].tick_params(labelsize=15)

plt.tight_layout()
plt.subplots_adjust(wspace=0.25)
ax[0].set_yticks(np.arange(0.25, 2.75, 0.5))
ax[1].set_yticks(np.arange(0.75, 4.0, 0.75))
ax[1].set_ylim(top=3.85)
ax[2].set_yticks(np.arange(1,7,1.25))
ax[3].set_yticks(np.arange(0.1, 0.5, 0.1))
ax[3].set_yticklabels(['0.10', '0.20', '0.30', '0.40'])

plt.savefig("form_eff.pdf", dpi=100)
