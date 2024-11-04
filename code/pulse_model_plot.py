# Author: Toma OC
#
# Generates subplots comparing current pulse and fitted function
# to predicted and measured E-field.

import numpy as np
import matplotlib.pyplot as plt
import os
import general as g
#from scipy.signal import butter, filtfilt
from scipy.optimize import curve_fit
from scipy.integrate import cumulative_trapezoid as cumul_trapez
from scipy.constants import pi, epsilon_0, c
from local_extrema import local_extrema
from read_channel_saentis import rcs
from fitfunc import heidler2#, eta
# latex fonts:
from matplotlib import rcParams
rcParams['text.usetex'] = True

# colors
colors = ['#000075', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf', '#B8B8B8', '#eeeeee']

# filter functions
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
    
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# select flash:
#     ['UPa','UP0','UP1','UP2','UN1','UN2','UN3','UN4','UP3','UP4','UN5','UN6',
#      'UN7','UN8']
f=3 # [' 0 ',' 1 ',' 2 ',' 3 ',' 4 ',' 5 ',' 6 ',' 7 ',' 8 ',' 9 ','10 ','11 ',
    #  '12 ','13 ']

# go to current data
os.chdir(g.crdir+g.cds[f])

fsc = 50e6 # current sampling rate (Hz)

End_time = 2.4
data_size_nS = End_time * fsc

# read from channel
bds,tb = rcs('./',1,data_size_nS,fsc) # B-dot data (kA/us, us)

# go to E-field data
os.chdir(g.cfadir+g.rds[f])

# number of samples set on digitizer
XX = 4e7

fsxe = 20e6 # digitiser sampling rate (Hz)

# set up time array
Txe = np.arange(1,XX+1)/fsxe
txe = Txe*1e6 # convert to microsec

## CHANNEL 2    E-field Melope
# Amplifier was set to 10 kV/m before 30.7.2021 and 1 kV/m after 30.7.
# Volts to kV/m conversion cofficient:
KK_ef = (10 * 1 / 0.4) if f<10 else (1 * 1 / 0.4)

fIDe = open('adlink_ch1.bin', 'rb')
Ych1_r = np.fromfile(fIDe, dtype='>d')
Ych1e = KK_ef * Ych1_r

## CHANNEL 3    E-field Flat plate, mostly not working
#fIDf = open('adlink_ch2.bin', 'rb')
#Ych2_r = np.fromfile(fIDf, dtype='>d') #,XX,'double','ieee-be')
#K_flat_plate to calculate

# align current and E-field data

# find peak values
# use B-dot signal to align PEM signal
if f in [2,3,7,10,11,9]: # UP1, UP2, UN4, UN5
    idc = np.argmax(np.abs(bds))
    print(f'B-dot max: {max(bds)} kA/us at {tb[idc]} us')
    idc = np.argmin(bds)
    print(f'B-dot min: {min(bds)} kA/us at {tb[idc]} us')
#if f in [0,1]: # UPa, UP0
if f in [8]: # UP3
    idc = np.argmin(np.abs(tb-959.92532))
# same for EF
if f in [0,1,2,3,8,9]: # UPa, UP0, UP1, UP2, UP3
    Emargin = np.abs(np.mean(Ych1e)) + np.std(Ych1e)*8 # 20,12,9
    ide,vae = next((ide,vae) for ide,vae in enumerate(Ych1e)
                    if np.abs(vae) > Emargin)
    print(f'First E-field step: {vae} kV/m at {txe[ide]} us')
if f in [7,11]: # UN4, UN6
    ide = np.argmax(np.abs(Ych1e))
if f in [10]: # UN5
    ide = np.argmin(Ych1e)
#else:
#    print('INVALID FLASH NUMBER')

tos = txe[ide]-tb[idc] # time offset # -56765.13 us for UP2
print('Radome - Tower time offset:', tos, 'microseconds')

# shift time array accordingly
txes = txe-tos #txe[(ide-i0):(ide+ie)] # in microsec
Yefs = Ych1e

## RAW DATA and adjust units
fbds = bds # in kA
fefs = Yefs*1e3 # to V/m

## FILTER DATA and adjust units # HPF on Bdot?
cutoff = 1e5 # Hz ## also removes EF system oscillations?
#fbds = butter_lowpass_filter(bds, cutoff, fsc) # in kA
#fefs = butter_lowpass_filter(Yefs, cutoff, fsxe)*1e3 # to V/m

print('B-dot avg.: %.7g +/- %.7g kA/us' % (np.mean(fbds), np.std(fbds)))
#print('B-dot range: %.7g (at %.9g us) to %.7g (at %.9g us)' %
#      (np.min(fbds), tb[np.argmin(fbds)], np.max(fbds), tb[np.argmax(fbds)]))
print('E-field avg.: %.7g +/- %.7g V/m' % (np.mean(fefs), np.std(fefs)))
print('E-field range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (np.min(fefs), txes[np.argmin(fefs)],
         np.max(fefs), txes[np.argmax(fefs)]))

# adjust for offset
for y in (fbds, fefs): y -= np.mean(y)

# change directory
os.chdir(g.ppd+g.names[f])

# leader start time (1st step)
tsl = 959010. # UP2

# zoom times (us)
t1 = tsl-2
t2 = tsl+6
# new indices
it1=np.argmin(np.abs(tb-t1)) # starting index (tower)
it2=np.argmin(np.abs(tb-t2)) # ending index (tower)
ir1=np.argmin(np.abs(txes-t1)) # starting index (radome)
ir2=np.argmin(np.abs(txes-t2)) # ending index (radome)
# new time arrays
tcn = tb[it1:it2]-tsl # adjust to leader start
#print('tcn =',tcn)
# B-dot integration
Ibd = cumul_trapez(fbds[it1:it2], tcn, initial=0) # in kA
#print('Ibd =',Ibd)
# ID peaks and troughs in time range:
Imin=np.min(Ibd)
Imax=np.max(Ibd)
Emin=np.min(fefs[ir1:ir2])
Emax=np.max(fefs[ir1:ir2])
tEmin=txes[ir1+np.argmin(fefs[ir1:ir2])]
tEmax=txes[ir1+np.argmax(fefs[ir1:ir2])]

print('For the specified time interval (%.7g to %.7g us):' % (t1, t2))
print('Current avg.: %.5g +/- %.5g' % (np.mean(Ibd), np.std(Ibd)))
print('Current range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (Imin, tcn[np.argmin(Ibd)],
         Imax, tcn[np.argmax(Ibd)]))
print('EF avg.: %.5g +/- %.5g'%(np.mean(fefs[ir1:ir2]),np.std(fefs[ir1:ir2])))
print('E-field range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (Emin, tEmin, Emax, tEmax))
      #'deltaE =',(Emax-Emin))

# Find and print local extrema
div=16 # division
#local_extrema(t1, t2, fsc, fsxe, tcn, Ibd, txes, fefs, div)

#exit()

# set yaxis offsets to zero (already done above?)
#Imax,Imin = (Imax,Imin)-np.mean(Ibd)
#Emax,Emin = (Emax,Emin)-np.mean(fefs)

dI = Imax-Imin
dE = Emax-Emin

# fit Heidler function sum to current pulse
bounds=([-np.inf,0,0,0, -np.inf,0,0,0], np.inf) # taus & n > 0
#popt,pcov = curve_fit(heidler2, tcn, Ibd,
#                      p0=[-1.,1.,1.,2., -1.,1.,1.,2.],
#                      bounds=bounds, maxfev=200*len(tcn)) # guesses
#print('popt =', popt)
#perr = np.sqrt(np.diag(pcov))
#print('perr =', perr)
#I1,tau11,tau12,n1, I2,tau21,tau22,n2 = popt
#Imod = heidler2(tcn, I1,tau11,tau12,n1, I2,tau21,tau22,n2)
#Qmod = cumul_trapez(Imod, tcn, initial=0) # charge (mC)

# plug in to E-field equation:
#ht, rs = 126, 20 # metres # Emod off by ~2 OoM (2nd slightly better)
Hl, ht = 137, 124 # leader tip and tower heights (metres)
tl = 0.5 # (us) estim. leader growth time
vl = (Hl-ht)/tl
Hlt = Hl # ht+vl*tcn # leader finishes growing at 0.5 us
#Em1 = -((Hlt**-2 - ht**-2)*Qmod/2e3 +
#        (1/Hlt - 1/ht)*Imod*1e3/c)/(pi*epsilon_0)
#Emod = ((rs**2/(4*Hl**4) - Hl**-2 + 3/(4*rs**2))*Qmod/1e3 +
#       (rs**2/(3*Hl**3) - 2/Hl + 5/(3*rs))*Imod*1e3/c)/(2*pi*epsilon_0)
#Em2 =
#print('EF model 1 range: %.7g (at %.9g us) to %.7g (at %.9g us)'
#      % (np.min(Em1), tcn[np.argmin(Em1)],
#         np.max(Em1), tcn[np.argmax(Em1)]))
#print('EF model 2 range: %.7g (at %.9g us) to %.7g (at %.9g us)'
#      % (np.min(Em2), tcn[np.argmin(Em2)],
#         np.max(Em2), tcn[np.argmax(Em2)]))

# calc E-field near leader tip
zp = np.linspace(ht-2, Hl+1, 100) # observation height
# change to cmapped lines over time
iEmin=np.argmin(np.abs(tcn-(tEmin-t1)))
#print('Leader height at Emin:', Hlt[iEmin])
#ElEmn = (((zp-Hlt)**-2 - (zp-ht)**-2)*Qmod[iEmin]/2e3 + # [iEmin]
#         (1/(zp-Hlt) - 1/(zp-ht))*Imod[iEmin]*1e3/c)/(2*pi*epsilon_0)
iEmax=np.argmin(np.abs(tcn-(tEmax-t1)))
#print('Leader height at Emax:', Hlt[iEmax])
#ElEmx = (((zp-Hlt)**-2 - (zp-ht)**-2)*Qmod[iEmax]/2e3 + # [iEmax]
#         (1/(zp-Hlt) - 1/(zp-ht))*Imod[iEmax]*1e3/c)/(2*pi*epsilon_0)


### setup PLOTS ###
fig, (ax1, ax2) = plt.subplots(2, 1) #ax0,

ax1.set_title('Current (Integ. B-dot)')
ax2.set_title('Electric field')
#ax0.set_title('E-field in leader')

# zoom
#ax0.set_xlim(ht-2, Hl+1)
for ax in (ax1, ax2): ax.set_xlim(t1-tsl, t2-tsl) #
ax1.set_ylim(Imin-.05*dI, Imax+.05*dI)
ax2.set_ylim(Emin-.05*dE, Emax+.05*dE)
#ax0.set_ylim(-20, 20)

#ax0.set_xlabel('$z$ (m)')
#ax0.set_ylabel('$E_z$ (MV/m)')

ax1.set_ylabel('$I$ (kA)')
ax2.set_ylabel('$E_z$ (V/m)')

plt.xlabel('Time ($\mu$s)')

# measurements
ax1.plot(tcn, Ibd, linewidth=0.8, color=colors[0])
ax2.plot(txes-tsl, fefs, linewidth=0.8, color=colors[2])

# modeled fits
# current
#ax1.plot(tcn, Imod, linewidth=0.8, color=colors[1])
#ax1.plot(tcn, Qmod, linewidth=0.7, color=colors[4]) # charge
# E-field
#ax2.plot(tcn, Em1, linewidth=0.7, color=colors[3],
#label=r'$\frac{1}{2\pi\epsilon_0}[(\frac{1}{h^2}-\frac{1}{H^2})Q(t)$'
#      r'$+\frac{2}{c}(\frac{1}{h}-\frac{1}{H})I(t)]$')
#ax2.plot(tcn, Em2, linewidth=0.7, color=colors[5])

# plot E-field in leader as function of height at chosen time
# cmapped lines over time
#ax0.plot(zp, ElEmn/1e6, linewidth=0.8, color=colors[5], label=r'$t_{min}$')
#ax0.plot(zp, ElEmx/1e6, linewidth=0.8, color=colors[6], label=r'$t_{max}$')

# add space between plots
fig.subplots_adjust(hspace=2/3)#, wspace=1/3)

# add lines
for ax in (ax1, ax2):
    ax.axhline(y=0, linestyle=':', lw=0.6, color='black')
    ax.axvline(x=959056.4-tsl, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959277.6-tsl, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.0898, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.1558, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.2036, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.2123, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=1041.521, linestyle=':', lw=0.5, color=colors[4])

#ax0.legend(loc='best')
ax2.legend(loc='best')

#plt.show()


#fig.savefig(g.names[f]+'_ie_modelfit_zoom_Step1_zoom.pdf', bbox_inches='tight')
fig.savefig(g.names[f]+'_ie_MP_zoom.pdf', bbox_inches='tight')


# TO DO:
#  1. Integrate B-dot signal for higher-resolution current.
#  4. Update summary sheet and/or paper appendix.
#  7. Align current and Ef based on 10% rise time.(?)
