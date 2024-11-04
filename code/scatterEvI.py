# Author: Toma Oregel-Chaumont
# 
# plotting script for comparison of electric field and current measurements

# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from fitfunc import affine,quadratic
import pulse_data as pd
#import general as g
# latex fonts:
from matplotlib import rcParams
rcParams['text.usetex'] = True

# plot stuff
colors = ['#000075', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf', '#B8B8B8', '#eeeeee']

# import data
# pulse times relative to start of leader/ICC
tpx = pd.pxst[:-1] # w/ XRs
tpp = np.array(pd.ppst[20:]) # no XRs

# pulses w/ x-rays
pxd = pd.pxre[:-1] # positive flash x-ray energies (MeV)
ydpx = pd.pxde[:-1] # PF E-field change (V/m)
xdpx = pd.pxpi[:-1] # PF current peak (kA)

# pulses w/o x-rays
ydpp = pd.ppde # PF E-field change (V/m) # UP0 not included yet
xdpp = pd.pppi # PF current peak (kA)    # UP0 not included yet

#print('dE*Ip (power) =', (np.array(ydpx)+45)*(np.array(xdpx)+.05), 'N/ms')

# set up plot
fig = plt.figure()
ax = fig.add_subplot()

plt.axis([0, 6, 0, 1600]) # dE vs. Ip lin-lin
#plt.axis([.3, 6, 1e2, 2e3]) # dE vs. Ip log-log

xs = 'linear'
ys = 'linear'
plt.xscale(xs)
plt.yscale(ys)

plt.title('Comparison of E-field change and peak current ')
          #r' ($\alpha \propto 1/t$)')

plt.xlabel('$I_{peak}$ (kA)')
plt.ylabel('$\Delta E$ (V/m)')

#plt.xticks(np.arange(0, 6.5, .5))

# plot
# positive pulses
plt.scatter(xdpx, ydpx, s=np.sqrt(pxd),
           c=tpx, cmap='gray', #olor='red', alpha=(1+np.array(tpx))**(-1/3), # #np.sqrt(1/(1+np.array(tpx))),
           label='$\propto \sqrt{\mathrm{XRE}}$') # Positive pulses
ax.scatter(xdpp, ydpp, s=9, marker='x', zorder=0,
           color='gray', alpha=(1+tpp)**(-1/3)) #np.sqrt(1/
           #label='no X-rays') # Positive pulses

plt.errorbar(xdpx, ydpx, xerr=0.05, yerr=45, zorder=0, # kA, V/m
            #fmt='o', markersize=ms_xre, #mec='red', mfc='red', np.sqrt(pxd)
            ecolor='k', elinewidth=.5, capsize=2, capthick=.5,
            ls='')#, #alpha=(1+tpx)**(-1/3), #np.array(
             #label=r'$\propto \sqrt{\mathrm{XRE}}$')
    
plt.colorbar(label='$t_{SL}$ ($\mu$s)')

# fit lines
xp = np.linspace(.3, 6, 100)
# + XRs
# linear (r^2 = 0.0158, RSS=1.41e6)
plt.plot(xp, affine(xp, -36.30641979, 698.55629598), # +/- [82.8, 205]
         lw=0.8, ls='--', label=r'$\Delta E = 699 - 36.3I_p$') #, color=''
# quadratic (r^2 = 0.0160, RSS=1.41e6)
plt.plot(xp,
         quadratic(xp, -2.359558, -23.44556, 684.5997), # +/- [47.7, 274, 353]
         lw=0.8, ls='--', label=r'$\Delta E = 685 - 23.4I_p - 2.36I_p^2$')

# poisson-lognorm?

# means
plt.axhline(y=620, linestyle=':', lw=0.8) # linear
plt.axhline(y=540, linestyle=':', lw=0.8) # log
plt.axvline(x=2.19, linestyle=':', lw=0.8) # linear
plt.axvline(x=1.88, linestyle=':', lw=0.8) # log

# max power line
plt.plot(xp, 3200/xp, linewidth=0.6, ls='-', color='red')
plt.text(2.8, 1200, r'$I_p \Delta E = 3.2$ N/$\mu$s',
         color='red', fontsize='small')

# + pulses
#plt.axvline(x=2.9077, linestyle='--', lw=0.8, color='red')
#plt.text(.45, .8, '$dI/dt = 2.908$ kA/$\mu$s', color='red', fontsize='small')
#plt.axhline(y=374, linestyle='--', lw=0.8, color='red', zorder=0)
#plt.text(24, 400, '$\Delta E = 374$ V/m', color='red', fontsize='small')


legend = plt.legend(loc='best')
#for lh in legend.legendHandles:
#    lh.set_alpha(1) # adjust transparency

# save figure
fig.savefig('dEvIp_pos_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')

# TO DO:
