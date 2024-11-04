# Author: Toma Oregel-Chaumont
# 
# plotting script for comparison of various measurements to the X-ray energy

# import modules
import numpy as np
import matplotlib.pyplot as plt
import os
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

time = pd.pxst[:-1] # pulse times relative to start of leader/ICC
# excluding last (not stepped-leader pulse)
ydp =  pd.pxre[:-1] # positive flash x-ray energies (MeV)
#ydn = pd.nxre # negative flash x-ray energies (MeV)
#xdp = pd.pxpi # PF current peak (kA)
#xdn = pd.nxpi # NF current peak (kA)
#xdp = np.array(pd.pxpi)/np.array(pd.pxdi) # PF t_mr (us)
#xdn = np.array(pd.nxpi)/np.array(pd.nxdi) # NF t_mr (us)
#xdp = pd.pxdi[:-1] # PF max dI/dt (kA/us)
#xdn = pd.nxdi # NF max dI/dt (kA/us)
xdp = pd.pxde[:-1] # PF E-field change (V/m)
#ydn = pd.nxde # NF E-field change (V/m)
#xdp = [t*0.8 if t!=None else None for t in pd.pxer] # PF EF rise-time (us)
#xdn = [t*0.8 if t!=None else None for t in pd.nxer] # NF EF rise-time (us)

# set up plot
fig = plt.figure()
#ax = fig.add_subplot()

#plt.axis([0, 6, 0, 300]) # XRE vs. Ip lin
#plt.axis([.1, 10, 10, 1e3]) # XRE vs. Ip log
#plt.axis([0, 2.5, 0, 300]) # XRE vs. tm lin
#plt.axis([.01, 10, 10, 1e3]) # XRE vs. tm log
#plt.axis([0, 16, 0, 300]) # XRE vs. dI/dt lin
#plt.axis([1, 100, 10, 1e3]) # XRE vs. dI/dt log
plt.axis([0, 1600, 0, 300]) # XRE vs. dE lin
#plt.axis([1e2, 1e4, 10, 1e3]) # XRE vs. dE log
#plt.axis([0, 25, 0, 300]) # XRE vs. dt lin
#plt.axis([.1, 100, 10, 1e3]) # XRE vs. dt log
#plt.axis([-50, 850, 0, 300]) # XRE vs. time lin

xs = 'linear'
ys = 'linear'
plt.xscale(xs)
plt.yscale(ys)

# ___ vs. XRE plots
plt.ylabel('Energy (keV)')

#plt.title('X-ray Energy -- Peak Current Comparison')
#plt.xlabel('$I_p$ (kA)')

#plt.title('X-ray Energy -- Min Current rise-time Comparison')
#plt.xlabel('$t_{mr}$ ($\mu$s)')

#plt.title('X-ray Energy -- Max Current Derivative Comparison')
#plt.xlabel('$dI/dt$ (kA/$\mu$s)')

plt.title('X-ray Energy -- E-field change Comparison')
plt.xlabel('$\Delta E$ (V/m)')

#plt.title('X-ray Energy -- E-field rise-time Comparison')
#plt.xlabel('$\Delta t_{E,rise}$ ($\mu$s)')

#plt.title('Stepped Leader X-rays')
#plt.xlabel('$t_{SL}$ ($\mu$s)')

# XRE vs. param. plot
plt.scatter(xdp, ydp, c=time, cmap='copper')#, s=np.sqrt(pxd)
            #marker=['o' for pxre[:7]]) # and pxre[9:] else:
           #label='Positive pulses')
# XRE vs. time plot
#plt.scatter(time, ydp, color=colors[1], s=16) # marker size
#           #color options: edge & face
#           label='')

# input actual error from general.py sigmas (might eliminate some data)
# xerr.s: Ip=.05, tm=.02, di=.33, dE=50, dt=.05 (round to these values)
plt.errorbar(xdp, ydp, yerr=.9, xerr=50, zorder=0, # time
             #markersize=4, marker='o', mfc='red', mec='red',
             ecolor='k', elinewidth=.6, # colors[1]
             capsize=4, capthick=.6, ls='')
             #label='Positive pulses')

plt.colorbar(label='$t_{SL}$ ($\mu$s)')

## fit lines
#plt.axhline(y=600, linestyle=':', zorder=0, lw=0.8)

# + pulses
# Min Current rise-time coefficients:
#x = np.linspace(.03, 2.5, 100)
# power-law fit
# 52.0 +/- 17.5 ; -0.492 +/- 0.210 (rss = 31621)
#plt.plot(x, 52*(x**-.49), linewidth=0.8, linestyle=':',
#         color='black', zorder=0, label=r'$XRE= 50 \, t_{mr}^{-.5}$')
# 52.2 ; -0.309 (r^2 = 0.218)
#plt.plot(x, 52*(x**-.31), linewidth=0.8, linestyle=':',
#         color='grey', zorder=0, label=r'$XRE= 50 \, t_{mr}^{-.3}$')
# log fit
# 58.076 +/- 17.614 ; -34.053 +/- 16.951 (rss = 33854, r^2 = 0.268)
#plt.plot(x, 58-34*np.log(x), linewidth=0.8, linestyle=':',
#         color='grey', zorder=0, label=r'$XRE= 50 \, t_{mr}^{-.3}$')

# Current derivative coefficients:
#x = np.linspace(0, 16, 100) # 1, 20 log #  lin
# linear fit: 14.0501 +/- 1.82689 (rssr = 140, r^2 = 0.542)
#plt.plot(x, 15*x, linewidth=0.8, linestyle=':',
#         color='black', zorder=0, label=r'$XRE= 15 \frac{dI}{dt}$')
# affine: a*x+b
# 11.5390 +/- 2.7785 ; 18.7000 +/- 15.7690 (rssr = 132, r^2 = 0.590)
# 11.5742            ; 18.5079             (  same , GC r^2 = 0.591)
# arit-geom mean convergence: 11.5566 ; 18.6038 (1 ; 2 steps)
#plt.plot(x, 11.54*x+18.70, linewidth=0.8, linestyle=':',
#         color=colors[2], zorder=0, label=r'$XRE= 12 \, \frac{dI}{dt} + 19$')
#plt.fill_between(x, (11.54+2.78)*x+(18.70+15.77),
#                    (11.54-2.78)*x+(18.70-15.77),
#                    lw=.4, color=colors[2], alpha=.4, zorder=0)
# exponential: con*exp(gam*x)
# 28.4079 +/- 6.2783 ; 0.149661 +/- 0.019123     (rssr = 94  ; r^2 = 0.793)
# 36.4457            ; 0.103151 (GC r^2 = 0.478) (rssr = 124 ; r^2 = 0.637)
# arit-geom mean convergence: 32.3017 ; 0.125325 (3 steps)
#plt.plot(x, 28.41*np.exp(0.1497*x), linewidth=0.8, linestyle=':',
#         color=colors[0], zorder=0, label=r'$XRE= 28 \exp(0.15\frac{dI}{dt})$')
#plt.fill_between(x, (28.41+6.28)*np.exp((0.1497+0.0191)*x),
#                    (28.41-6.28)*np.exp((0.1497-0.0191)*x),
#                    lw=.4, color=colors[0], alpha=.4, zorder=0)
# excluding 250 keV event
# 46.8862 +/- 8.5880 ; 0.03915 +/- 0.03696     (rssr = 66  ; r^2 = 0.0854)
# 43.8            ; 0.0413 (GC r^2 = 0.081) (rssr = 124 ; r^2 = 0.637)
# arit-geom mean convergence: 45. ; 0.04 ( steps)
#plt.plot(x, 46.89*np.exp(0.0391*x), linewidth=0.8, linestyle=':',
#         color=colors[2], zorder=0, label=r'$XRE= 47 \exp(0.04\frac{dI}{dt})$')
#plt.fill_between(x, (46.89+8.59)*np.exp((0.0391+0.0370)*x),
#                    (46.89-8.59)*np.exp((0.0391-0.0370)*x),
#                    lw=.4, color=colors[2], alpha=.4, zorder=0)


# E-field change coefficients:
#x = np.linspace(1, 1600, 10000) #  log # 140, 1520 lin
# linear fit: 0.102927 +/- 0.020336 (rssr = 191, r^2 = 0.144)
#plt.plot(x, x/10, linewidth=0.8, linestyle=':',
#         color='black', zorder=0, label=r'$XRE = \Delta E / 10$')
# affine fit: a*x+b
# 0.0733688 +/- 0.0450839 ; 23.1874 +/- 31.4181 (rssr = 187, r^2 = 0.181) +
# 0.0730368               ; 23.4287             (  same , GC r^2 = 0.179) +
#plt.plot(x, 0.07337*x+23.19, linewidth=0.8, linestyle=':',
#         color=colors[2], zorder=0, label=r'$XRE = 0.073 \, \Delta E + 23$')
#plt.fill_between(x, (0.07337+0.04508)*x+(23.19+31.42),
#                    (0.07337-0.04508)*x+(23.19-31.42),
#                    lw=.4, color=colors[2], alpha=.4, zorder=0)

# log fit: a + b*ln(x)
# -211.467 +/- 172.634 ; 44.4862 +/- 27.3247 (rssr = 187, r^2 = 0.181) +
# -209.594             ; 44.1982             (  same , GC r^2 = 0.180) +
# arit-geom mean convergence: -210.53 ; 44.342 (1 step)
#plt.plot(x, -211.5+44.49*np.log(x), linewidth=0.8, linestyle=':',
#         color=colors[4], zorder=0, label=r'$XRE = 44 \, \ln(\Delta E)-211$')
#plt.fill_between(x, (-211.5+172.6)+(44.49+27.32)*np.log(x),
#                    (-211.5-172.6)+(44.49-27.32)*np.log(x),
#                    lw=.4, color=colors[4], alpha=.4, zorder=0)
# excluding 250 keV event
# -26.3351 +/- 66.2091 ; 12.8902 +/- 10.5631 (rssr = 65, r^2 = 0.119)
# -25.7068             ; 12.7922             ( same , GC r^2 = 0.118)
# arit-geom mean convergence: -26.02 ; 12.84 (1 step)
#plt.plot(x, -26.33+12.89*np.log(x), linewidth=0.8, linestyle=':',
#         color=colors[3], zorder=0, label=r'$XRE = 13 \, \ln(\Delta E)-26$')
#plt.fill_between(x, (-26.33+66.21)+(12.89+10.56)*np.log(x),
#                    (-26.33-66.21)+(12.89-10.56)*np.log(x),
#                    lw=.4, color=colors[3], alpha=.4, zorder=0)


# E-field rise-time coefficients:
#x = np.linspace(.1, 30, 1000)
# power-law fit:
# 86.37 +/- 18.36 ; -0.1559 +/- 0.1146 (rss = 39807)
#plt.plot(x, 86*(x**(-.16)), linewidth=0.8, linestyle=':',
#         color='black', zorder=0, label=r'$XRE = 90 \, t_{Er}^{-1/6}$')
# 67.68 ; -0.0885 (r^2 = 0.072)
# log fit: 89.2626 +/- 19.8561 ; -12.0306 +/- 9.2051 (rss=40055, r^2=0.134)
#plt.plot(x, 89.3-12.0*np.log(x), linewidth=0.8, linestyle=':',
#         color='black', zorder=0, label=r'$XRE = 89 - 12 \ln(t_{Er})$')


# XRE vs. time
#plt.axvline(x=0, linestyle=':', lw=0.8, color='black', zorder=0)
#x = np.linspace(0, 850, 10000) # 1, 20 log #  lin
# including 250 keV outlier
# affine: -0.102414+/-0.058688 ; 103.496+/-24.542 (rssr=185, r^2=0.202 gc same)
#plt.plot(x, -.1024*x+103.5, linewidth=0.8, linestyle=':',
#         color=colors[2], zorder=0, label=r'$XRE= -0.102 \, t_{SL} + 103$')
#plt.fill_between(x, (-.1024+0.0587)*x+(103.5+24.5),
#                    (-.1024-0.0587)*x+(103.5-24.5),
#                    lw=.4, color=colors[2], alpha=.4, zorder=0)

# exponential: a*(b**x)
# 134.575 +/- 32.794 ; 0.997321 +/- .001237 (rssr = 174) # r^2 = 0.290
#plt.plot(x, 134.6*(0.9973**x), linewidth=0.8, linestyle='--',
#        color=colors[1], zorder=0, label=r'$XRE= 135 \times 0.997^{t_{SL}}$')
# equivalently: con*exp(gam*x)
# 134.562 +/- 32.790 ; -2.68189e-3 +/- 1.24020e-3 (rssr = 174) # r^2 = 0.290
#plt.plot(x, 134.6*np.exp(-0.002682*x), linewidth=0.8, linestyle='--',
#         color=colors[0], zorder=0, label=r'$XRE= 135 \exp(-t_{SL}/373\mu s)$')
#plt.fill_between(x, (134.6+32.8)*np.exp((-.002682+.001240)*x),
#                    (134.6-32.8)*np.exp((-.002682-.001240)*x),
#                    lw=.4, color=colors[0], alpha=.4, zorder=0)

# excluding 250 keV event
# affine: -0.022285+/-0.024140 ; 62.361+/-10.476 (rssr=67, r^2=0.072 gc same)
#plt.plot(x, -.0223*x+62.4, linewidth=0.8, linestyle='--',
#         color=colors[2], zorder=0, label=r'$XRE= -0.022 \, t_{SL} + 62$')
#plt.fill_between(x, (-.0223+0.0241)*x+(62.4+10.5),
#                    (-.0223-0.0241)*x+(62.4-10.5),
#                    lw=.4, color=colors[0], alpha=.4, zorder=0)

# average

#plt.legend(loc='best')
#plt.legend(loc='lower right')

os.chdir('../scatterplots/')

# save figure
#fig.savefig('XRvIp_pos_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
#fig.savefig('XRvtm_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
#fig.savefig('XRvdI_pos_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
fig.savefig('XRvdE_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
#fig.savefig('XRvdt_%s%s.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')
#fig.savefig('XREvT_%s%s_aff1.pdf'%(xs[:3],ys[:3]), bbox_inches='tight')


# TO DO:
# Add XRE vs. dE/dt & Ip*tmr
