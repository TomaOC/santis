# Author: Toma Oregel-Chaumont
# 
# plotting script for comparison of electric field measurements

# import modules
import numpy as np
import matplotlib.pyplot as plt
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

# pulses w/ x-rays
pxd = pd.pxre # positive flash x-ray energies (MeV)
nxd = pd.nxre # negative flash x-ray energies (MeV)
ydpx = pd.pxde # PF E-field change (V/m)
ydnx = pd.nxde # NF E-field change (V/m)
xdpx = [t*0.8 if t!=None else None for t in pd.pxer] # PF EF rise-time (us)
xdnx = [t*0.8 if t!=None else None for t in pd.nxer] # NF EF rise-time (us)

# pulses w/o x-rays
ydpp = pd.ppde # PF E-field change (V/m)
ydnp = pd.npde # NF E-field change (V/m)
xdpp = [t*0.8 if t!=None else None for t in pd.pper] # PF EF rise-time (us)
xdnp = [t*0.8 if t!=None else None for t in pd.nper] # NF EF rise-time (us)

# set up plot
fig = plt.figure()
ax = fig.add_subplot()

#plt.axis([0, 50, 0, 4500]) # dE vs. dt lin-lin

xs = 'linear'
ys = 'linear'
plt.xscale(xs)
plt.yscale(ys)
#print(plt.xscale)
#print(plt.yscale)

# dE vs. dt plot
plt.title('E-field rate-of-change comparison '
          '(circle $\propto \sqrt{\mathrm{XRE}}$)')
plt.xlabel('$\Delta t_{E,rise} (\mu s)$')
plt.ylabel('$\Delta E$ (V/m)')

# plot
# ADD ERROR BARS (+/- 0.05 us for Dt, ~45 V/m for DE)
ax.scatter(xdpx, ydpx, s=np.sqrt(pxd),
           color='red', #colors[3]
           label='Positive pulses (with X-ray)')
ax.scatter(xdnx, ydnx, s=np.sqrt(nxd),
           color='blue', #colors[0] # option: edge & face
           label='Negative pulses (with X-ray)')
ax.scatter(xdpp, ydpp, s=9, marker='x',
           color='red', #colors[3]
           label='Positive pulses (no X-ray)')
ax.scatter(xdnp, ydnp, s=9, marker='x',
           color='blue', #colors[0] # option: edge & face
           label='Negative pulses (no X-ray)')

#eb = plt.errorbar(lam5/mu50, rd.Clam[j], yerr=rd.Cleb[j],
#                  marker='o', mec=colors[j],#int(j/2)
#                  mfc=colors[j],#('none' if eos==True else
#                  ecolor=colors[j], elinewidth=.5,
#                  capsize=4, capthick=.5, ls='',
#                  label=rd.names[j])#(None if eos==True else
    

# dashed lines separating data groups
#plt.axhline(y=600, linestyle=':', zorder=0, lw=0.8)
#plt.text(10, 650, '$\Delta E = 600$', fontsize='small')
x = np.linspace(12, 26, 100)
#plt.plot(x, (1608.5 - 47.47*x), linewidth=0.8, linestyle='-.',
#         color='grey', zorder=0)
#plt.plot(x, 14000/x, linewidth=0.8, linestyle='-.',
#         color='grey', zorder=0)
#plt.text(1, 1200, '$\Delta E \Delta t = 14$ mV s/m',
#         color='grey', fontsize='small')


# fit lines

# + XRs
#xpx = np.linspace(.16, .48, 100)
#plt.plot(xpx, 287.96/xpx, linewidth=0.8, linestyle=':', color='red')
#plt.text(.3, 1000, '$\Delta E \Delta t = 288$ $\mu$Vs/m',
#         color='red', fontsize='small')
#plt.axhline(y=712, linestyle=':', lw=0.8, color='red')
#plt.text(24, 740, '$\Delta E = 712$ V/m', color='red', fontsize='small')
#plt.axvline(x=0.28, linestyle=':', lw=0.8, color='red', zorder=0)

# + pulses
#xpp = np.linspace(.08, 1, 100)
#plt.plot(xpp, 2.9077*xpp, linewidth=0.8, linestyle='--', color='red')
#plt.axvline(x=2.9077, linestyle='--', lw=0.8, color='red')
#plt.text(.45, .8, '$dI/dt = 2.908$ kA/$\mu$s', color='red', fontsize='small')
#plt.axhline(y=374, linestyle='--', lw=0.8, color='red', zorder=0)
#plt.text(24, 400, '$\Delta E = 374$ V/m', color='red', fontsize='small')

# - XRs
#xnx = np.linspace(.2, 1.1, 100)
#plt.plot(xnx, 3.1394/xnx, linewidth=0.8, linestyle=':', color='blue')
#plt.text(.5, 7, '$I_p t_{mr} = 3.139$ mC',
#         color='blue', fontsize='small')
#plt.axhline(y=6.8737, linestyle=':', lw=0.8, color='blue')
#plt.axvline(x=18.1735, linestyle=':', lw=0.8, color='blue')

# - pulses
#xnp = np.linspace(1, 8, 100)
#plt.plot(xnp, 1.0930*xnp, linewidth=0.8, linestyle='--', color='blue')
#plt.text(8, 9, '$t_{mr} = 1.09 \mu s$',
#         color='blue', fontsize='small')
#plt.axhline(y=3.057, linestyle='--', lw=0.8, color='blue')
#plt.axvline(x=3.8526, linestyle='--', lw=0.8, color='blue')


plt.legend(loc='best')
#plt.legend(loc='lower right')

#os.chdir()

# save figure
#fig.savefig('dEFvXRE_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
#fig.savefig('dtEvXRE_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')

fig.savefig('dEdt_all_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')

# TO DO:

# concat. arrays of like data (neg./pos.; with XR/no XR)
# and recalc. trends.
