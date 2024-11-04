# Author: Toma Oregel-Chaumont
# 
# plotting script for X-ray count histogram

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

pxst = pd.pxst # XR pulse times relative to start of leader/ICC
ppst = pd.ppst # non-XR pulse times relative to start of leader

# set up histogram
fig = plt.figure()
#ax = fig.add_subplot()

plt.axis([0, 800, 0, 25]) # pulse count vs. time lin

#xs = 'linear'
#ys = 'linear'
#plt.xscale(xs)
#plt.yscale(ys)

plt.title('Stepped Leader / ICC Pulses (all UP flashes)')
plt.xlabel('$t_{SL}$ ($\mu$s)')
plt.ylabel('Counts')

tmin = min(min(pxst), min(ppst))
tmax = max(max(pxst), max(ppst))
binsize = 200 # width (in microseconds)
bins = np.linspace(tmin, tmax, num=int(np.ceil((tmax-tmin)/binsize)))

# All pulse counts vs. time (label is what's visible on plot)
plt.hist(ppst+pxst, bins=bins, edgecolor='black', label='No X-rays')
# X-ray pulse counts vs. time
plt.hist(pxst, bins=bins, edgecolor='black', label='With X-rays')

#plt.colorbar(label='$t_{SL}$ ($\mu$s)')

# fit lines
#plt.axhline(y=600, linestyle=':', zorder=0, lw=0.8)

# + pulses

# XRE vs. time
#plt.axvline(x=0, linestyle=':', lw=0.8, color='black')
#x = np.linspace(0, 800, 10000) # 1, 20 log #  lin
# affine: -0.11111 +/- 0.06510 ; 114.77 +/- 28.12 (rss=36586, r^2=0.209)
#plt.plot(x, -.1111*x+114.8, linewidth=0.8, linestyle=':',
#         color='black', zorder=0, label=r'$XRE= -0.11 \, t_{SL} + 115$')


# dashed lines separating data groups ?

plt.legend(loc='best')
#plt.legend(loc='lower right')

#os.chdir()

# save figure
#fig.savefig('XRCvT.pdf', bbox_inches='tight')
fig.savefig('PulseCounts_vT_test.pdf', bbox_inches='tight')
