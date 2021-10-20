import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import astropy.units as u

models = ['log_uniform', 'qcflag_4', 'alpha_0.25', 'alpha_5']
model_names = ['fiducial', r'q3', r'$\alpha25$', r'$\alpha5$']
colors = sns.color_palette("mako", n_colors=len(models))

Tobs = 4 * u.yr

def func(x, a, b, c, d, e):
    return a + b*x + c*x**2 + d*x**3 + e*x**4

mosaic = """
AA
AA
BB
"""

fig = plt.figure(figsize=(6, 8))
ax_dict = fig.subplot_mosaic(mosaic)


lisa_ratio = []
n_lisa_F50_list = []

popt_F50_list = []
popt_FZ_list = []

for m in models:
    if m == 'log_uniform':
        n_lisa_F50 = pd.read_hdf('numLISA_30bins_F50.hdf', key='data')
        n_lisa_FZ = pd.read_hdf('numLISA_30bins_FZ.hdf', key='data')
        
        popt_F50 = pd.read_hdf('resolved_DWDs_F50.hdf', key='conf_fit')
        popt_FZ = pd.read_hdf('resolved_DWDs_FZ.hdf', key='conf_fit')
    else:
        n_lisa_F50 = pd.read_hdf('numLISA_30bins_F50_{}.hdf'.format(m), key='data')
        n_lisa_FZ = pd.read_hdf('numLISA_30bins_FZ_{}.hdf'.format(m), key='data')

        print(m, 'resolved_DWDs_F50_{}.hdf'.format(m))        
        popt_F50 = pd.read_hdf('resolved_DWDs_F50_{}.hdf'.format(m), key='conf_fit')
        popt_FZ = pd.read_hdf('resolved_DWDs_FZ_{}.hdf'.format(m), key='conf_fit')

    n_lisa_F50 = np.sum(n_lisa_F50.values.flatten())
    n_lisa_FZ = np.sum(n_lisa_FZ.values.flatten())
    
    lisa_ratio.append(n_lisa_FZ/n_lisa_F50)
    n_lisa_F50_list.append(n_lisa_F50)

    popt_F50 = popt_F50.values.flatten()
    popt_FZ = popt_FZ.values.flatten()
            
    popt_F50_list.append(popt_F50)
    popt_FZ_list.append(popt_FZ)

        
for popt_F50, popt_FZ, ii in zip(popt_F50_list, popt_FZ_list, range(len(popt_FZ_list))):
    conf_fit_FZ = 10**func(
        x=np.log10(np.linspace(1e-4, 1e-1, 100000)), 
        a=popt_FZ[0], b=popt_FZ[1], c=popt_FZ[2], d=popt_FZ[3], e=popt_FZ[4]
    )* Tobs.to(u.s).value
    
    conf_fit_F50 = 10**func(
        x=np.log10(np.linspace(1e-4, 1e-1, 100000)), 
        a=popt_F50[0], b=popt_F50[1], c=popt_F50[2], d=popt_F50[3], e=popt_F50[4]
    )* Tobs.to(u.s).value
    
    ax_dict['A'].plot(
        np.linspace(1e-4, 1e-1, 100000), conf_fit_F50, color=colors[ii], ls='--', lw=2.5, zorder=10-ii
    )
    ax_dict['A'].plot(
        np.linspace(1e-4, 1e-1, 100000), conf_fit_FZ, color=colors[ii], ls='-', lw=2.5, label=model_names[ii]
    )



ax_dict['A'].set_xscale('log')
ax_dict['A'].set_yscale('log')

ax_dict['A'].set_ylabel(r'confusion fit [Hz$^{-1}$]', size=16)
ax_dict['A'].set_xlabel(r'f$_{\rm{GW}}$ [Hz]', size=16)
ax_dict['A'].set_xlim(1e-4, 3.5e-3)
ax_dict['A'].set_ylim(1e-38, 7e-35)


for ii in range(len(lisa_ratio)):
    ax_dict['B'].scatter(n_lisa_F50_list[ii], lisa_ratio[ii], color=colors[ii], marker='s', s=45, label=model_names[ii])
ax_dict['A'].legend(prop={'size' : 12}, frameon=False, loc='upper right')
ax_dict['B'].set_xscale('log')
ax_dict['B'].axhline(0.5, ls='--', color='silver', lw=2, zorder=0)
ax_dict['B'].set_ylim(0.2, 0.8) 
ax_dict['B'].set_xlim(3e5, 1e8)
ax_dict['B'].set_ylabel(r'N$_{\rm{LISA, FZ}}$/N$_{\rm{LISA, F50}}$', size=16)
ax_dict['B'].set_xlabel(r'N$_{\rm{LISA, F50}}$', size=16)
ax_dict['A'].tick_params(labelsize=12)
ax_dict['B'].tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('model_comp.pdf', dpi=100)
