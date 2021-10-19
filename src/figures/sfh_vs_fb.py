"""
Generate figure 1 of the paper based on galaxy m12i and the Moe+19 metallicity-dependent binary fraction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import get_binfrac_of_Z, get_FeH_from_Z


FIRE = pd.read_hdf('FIRE.h5')
fig, ax = plt.subplots()
plt.grid(lw=0.25, which='both')
bins = np.append(met_arr[1:-1]/Z_sun, FIRE.met.max())
bins = np.append(FIRE.met.min(), bins)
bins = np.log10(bins)
ax2 = ax.twinx()
h, bins, _ = ax2.hist(np.log10(FIRE.met), bins=bins, histtype='step', lw=2, 
                      color='xkcd:tomato red', label='Latte m12i')
ax2.set_yscale('log')
ax2.legend(loc='lower left', bbox_to_anchor= (0.6, 1.01), ncol=4, borderaxespad=0, frameon=False, 
           fontsize=20)
ax.scatter(np.log10(met_arr[1:]/Z_sun), get_binfrac_of_Z(met_arr[1:]), color='k', s=15, zorder=2, 
           label='COSMIC Z grid')
met_plot = np.linspace(FIRE.met.min()*Z_sun, FIRE.met.max()*Z_sun, 10000)
ax.plot(np.log10(met_plot/Z_sun), get_binfrac_of_Z(met_plot), color='k', label='FZ')
ax.set_xlim(bins[1]-0.17693008, bins[-2] + 2 * 0.17693008)
ax.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=4, borderaxespad=0, frameon=False, 
          fontsize=20, markerscale=3)
ax.set_zorder(ax2.get_zorder()+1)
ax.patch.set_visible(False)
ax.set_xlabel('Log$_{10}$(Z/Z$_\odot$)')
ax.set_ylabel('Binary Fraction')
ax2.set_ylabel(r'M$_{\rm{stars}}$ per Z bin (M$_\odot$)')
ax2.set_yticks([1e4, 1e5, 1e6, 1e7]);
ax2.set_yticklabels(['7e7', '7e8', '7e9', '7e10']);
plt.savefig('SFH_vs_fb.png', dpi=250)

