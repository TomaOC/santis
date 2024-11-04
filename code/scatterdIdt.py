# Author: Toma Oregel-Chaumont
# 
# plotting script for comparison of current measurements

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
ydpx = pd.pxpi # PF current peak (kA)
ydnx = pd.nxpi # NF current peak (kA)
#xdpx = pd.pxdi # PF max dI/dt (kA/us)
#xdnx = pd.nxdi # NF max dI/dt (kA/us)

# pulses w/o x-rays
ydpp = pd.pppi # PF current peak (kA)
ydnp = pd.nppi # NF current peak (kA)
#xdpp = pd.ppdi # PF max dI/dt (kA/us)
#xdnp = pd.npdi # NF max dI/dt (kA/us)

# for Ip vs. tmr plot
xdpx = [va/pd.pxdi[id] if (va and pd.pxdi[id])!=None else None
        for id,va in enumerate(ydpx)]
xdnx = [va/pd.nxdi[id] if (va and pd.nxdi[id])!=None else None
        for id,va in enumerate(ydnx)]
xdpp = [va/pd.ppdi[id] if (va and pd.ppdi[id])!=None else None
        for id,va in enumerate(ydpp)]
xdnp = [va/pd.npdi[id] if (va and pd.npdi[id])!=None else None
        for id,va in enumerate(ydnp)]

# set up plot
fig = plt.figure()
ax = fig.add_subplot()

#plt.axis([1e2, 1e7, 1e-5, 1e-2]) # Imax vs. XRE
#plt.axis([0, 1600, 1, 100]) # dI/dt vs. XRE lin-log

xs = 'linear'
ys = 'linear'
plt.xscale(xs)
plt.yscale(ys)
#print(plt.xscale)
#print(plt.yscale)

# Ip vs. dI/dt plot
#plt.title('Current rise-time comparison '
#          '(circle $\propto \sqrt{\mathrm{XRE}}$)')
#plt.xlabel('$dI/dt$ (kA/$\mu s$)')
#plt.ylabel('$I_{peak}$ (kA)')

# Ip vs. tmr plot
plt.title('Current rate-of-change comparison '
          '(circle $\propto \sqrt{\mathrm{XRE}}$)')
plt.xlabel('$t_{mr}$ ($\mu s$)')
plt.ylabel('$I_{peak}$ (kA)')

# plot
# ADD ERROR BARS (t_mr determined by Ip (+/-0.05 kA) and dI/dt (0.33 kA/us))
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
#x = np.linspace(.4, .9, 100)
# y = m*x+b # m ~ 300 V/m/us
#plt.plot(x, 9*x, linewidth=0.7, linestyle='-',
#         color='grey', zorder=0)
#plt.text(.9, 9, '$dI/dt = 9$ kA/$\mu$s', color='grey', fontsize='small')
#plt.plot(x, (1608.5 - 47.47*x), linewidth=0.8, linestyle='-.',
#         color='grey', zorder=0)
#plt.plot(x, 1000/x, linewidth=0.8, linestyle='-.',
#         color='grey', zorder=0)


# fit lines

# + XRs
#xpx = np.linspace(.16, .48, 100)
#plt.plot(xpx, 287.96/xpx, linewidth=0.8, linestyle=':', color='red')
#plt.axhline(y=1.90, linestyle=':', lw=0.8, color='red')
#plt.text(2, 2.1, '$I_p = 1.90$ kA',
#         color='red', fontsize='small')
#plt.axvline(x=0.28, linestyle=':', lw=0.8, color='red', zorder=0)
#plt.text(.35, 600, '$t_{rise} = 0.28 \mu s$', color='red', fontsize='small')

# + pulses
xpp = np.linspace(.01, 5, 100)
plt.plot(xpp, 2.7*xpp, linewidth=0.8, linestyle='-.', color='red')
#plt.text(0.05, 0.08, '$dI/dt = 2.7$ kA/$\mu s$', color='red', fontsize='small')
plt.text(2, 9, '$dI/dt = 2.7$ kA/$\mu s$', color='red', fontsize='small')
#plt.axvline(x=2.684, linestyle='--', lw=0.8, color='red')
#plt.text(3, 10, '$dI/dt = 2.68$ kA/$\mu s$', color='red', fontsize='small')
#plt.axhline(y=348.44, linestyle='--', lw=0.8, color='red', zorder=0)

# - XRs
#xnx = np.linspace(.2, 1.1, 100)
#plt.plot(xnx, 3.1394/xnx, linewidth=0.8, linestyle=':', color='blue')
#plt.text(.5, 7, '$I_p t_{mr} = 3.139$ mC',
#         color='blue', fontsize='small')
#plt.axhline(y=6.8737, linestyle=':', lw=0.8, color='blue')
#plt.axvline(x=18.1735, linestyle=':', lw=0.8, color='blue')

# - pulses
xnp = np.linspace(1.2, 9, 100)
#plt.plot(xnp, 0.947*xnp, linewidth=0.8, linestyle='--', color='blue')
#plt.text(9, 8, '$t_{mr} = 0.95$ $\mu s$',
#         color='blue', fontsize='small')
#plt.axhline(y=3.057, linestyle='--', lw=0.8, color='blue')
#plt.axvline(x=0.947, linestyle='--', lw=0.8, color='blue')
#plt.text(1, 9, '$t_{mr} = 0.95$ $\mu s$',
#         color='blue', fontsize='small')


#plt.legend(loc='best')
plt.legend(loc='upper center')

#os.chdir()

# save figure
#fig.savefig('pIvXRE_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
#fig.savefig('dIvXRE_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')

#fig.savefig('pIdIdt_all_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
fig.savefig('dIdt_all_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')

# TO DO:

# concat. arrays of like data (neg./pos.; with XR/no XR)
# and recalc. trends.
