# Author: Toma OC
#
# Generates subplots comparing I, dI/dt, and E as functions of time

import numpy as np
import matplotlib.pyplot as plt
import os
import general as g
from scipy.integrate import cumulative_trapezoid as cumul_trapez
from scipy.signal import butter, filtfilt # argrelextrema,
from read_channel_saentis import rcs
from local_extrema import local_extrema
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
#     ['UPa','UP0','UP1','UP2','UN1','UN2','UN3','UN4','UP3','UP4','UN5',
#      'UN6', 'UN7','UN8']
f=3 # [' 0 ',' 1 ',' 2 ',' 3 ',' 4 ',' 5 ',' 6 ',' 7 ',' 8 ',' 9 ','10 ',
#      '11 ', '12 ','13 ']

# go to current data
os.chdir(g.crdir+g.cds[f])

fsc = 50e6 # current sampling rate (Hz)

End_time = 2.4
data_size_nS = End_time * fsc

# pick current sensor
cs = ['Bdtt','PEMt','ROCb','PEMb']
# 1: B-dot top (dI/dt)
# 2: PEM top (I)
# 3: ROCOIL bottom (I)
# 4: PEM bottom (I)
chp = 4
cha = 3
chb = 1
# read from channel
cur,tc = rcs('./',chp,data_size_nS,fsc) # current data
#dia,ta = rcs('./',cha,data_size_nS,fsc) # ROCb data (for alignment)
bds,tb = rcs('./',chb,data_size_nS,fsc) # B-dot data

# go to ef data
os.chdir(g.cfadir+g.rds[f])

# number of samples set on digitizer
XX = 4e7

fsxe = 20e6 # digitiser sampling rate (Hz)

# set up time array
Txe = np.arange(1,XX+1)/fsxe
txe = Txe*1e3 # convert to ms

## CHANNEL 1 : X-rays

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

# align current/derivative and E-field data

# find peak values
#idc = np.argmax(np.abs(cur))
# use B-dot signal to align PEM signal
if f in [2,3,7,10,11,9]: # UP1, UP2, UN4, UN5
    idc = np.argmax(np.abs(bds))
    #print(f'B-dot max: {max(bds)} kA/us at {tc[idc]} us')
    idc = np.argmin(bds)
    #print(f'B-dot min: {min(bds)} kA/us at {tc[idc]} us')
if f in [0,1]: # UPa, UP0
    idc = np.argmin(dia)
if f in [8]: # UP3
    idc = np.argmin(np.abs(tb-959925.32))
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

tos = txe[ide]-tc[idc] # time offset
print('Radome - Tower time offset:', tos, 'us')

# shift time array accordingly
txes = txe-tos #txe[(ide-i0):(ide+ie)]
Yefs = Ych1e

## RAW DATA and adjust units
#fcur = cur # in kA
fefs = Yefs*1e3 # to V/m

## FILTER DATA and adjust units
cutoff = 1e5 # Hz ## also removes EF system oscillations?
fcur = butter_lowpass_filter(cur, cutoff, fsc) # in kA
#fefs = butter_lowpass_filter(Yefs, cutoff, fsxe)*1e3 # to V/m

print('%s avg.: %.7g +/- %.7g' % (cs[chp-1], np.mean(fcur), np.std(fcur)))
print('%s range: %.7g (at %.9g us) to %.7g (at %.9g us)' % (cs[chp-1],
      np.min(fcur), tc[np.argmin(fcur)], np.max(fcur), tc[np.argmax(fcur)]))
print('E-field avg.: %.7g +/- %.7g' % (np.mean(fefs), np.std(fefs)))
print('E-field range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (np.min(fefs), txes[np.argmin(fefs)],
         np.max(fefs), txes[np.argmax(fefs)]))

# write data to file
os.chdir(g.ppd+g.names[f])

#with open(g.names[f]+'_%s_data_filt.bin'%cs[chp-1], # raw/filt
#          "wb") as file:
#    np.save(file, [tc, fcur])

#with open(g.names[f]+'_EF_data_raw.bin', "wb") as file: # raw/filt
#    np.save(file, [txes, fefs])

#exit()

# leader start time (1st step)
tsl = 959010. # UP2

# zoom times
t1 = 940
t2 = 1100

# find corresponding indices
it1=np.argmin(np.abs(tc-t1)) # starting index (tower)
it2=np.argmin(np.abs(tc-t2)) # ending index (tower)
ir1=np.argmin(np.abs(txes-t1)) # starting index (radome)
ir2=np.argmin(np.abs(txes-t2)) # ending index (radome)

# ID peaks and troughs in time range:
Imin=np.min(fcur[it1:it2])
Imax=np.max(fcur[it1:it2])
Emin=np.min(fefs[ir1:ir2])
Emax=np.max(fefs[ir1:ir2])
print('For the specified time interval (%.7g to %.7g us):' % (t1,t2))
print('Current avg.: %.5g +/- %.5g' %
      (np.mean(fcur[it1:it2]),np.std(fcur[it1:it2])))
print('Current range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (Imin, tc[it1+np.argmin(fcur[it1:it2])],
         Imax, tc[it1+np.argmax(fcur[it1:it2])]))
print('E-field avg.: %.5g +/- %.5g' %
      (np.mean(fefs[ir1:ir2]),np.std(fefs[ir1:ir2])))
print('E-field range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (Emin, txes[ir1+np.argmin(fefs[ir1:ir2])],
         Emax, txes[ir1+np.argmax(fefs[ir1:ir2])]))
      #'deltaE =',(Emax-Emin))

# Find and print local extrema
div=16 # division
#local_extrema(t1, t2, fsc, fsxe, tc, fcur, txes, fefs, div)

#exit()

# set yaxis offsets to zero
Imax,Imin = (Imax,Imin)-np.mean(fcur)
Emax,Emin = (Emax,Emin)-np.mean(fefs)

for y in (fcur, fefs): y -= np.mean(y) #

dI = Imax-Imin
dE = Emax-Emin

# setup PLOTS
fig, (ax0, ax2) = plt.subplots(2, 1) #

ax0.set_title('Current (%s)' % cs[chp-1])
ax2.set_title('E-field')

# whole flash
#st = -tos if tos<0 else 0 # start time
#et = 2e3-tos if (2e3-tos)<2400 else 2400 # end time
#for ax in (ax0, ax2): ax.set_xlim(st, et)

# zoom
for ax in (ax0, ax2): ax.set_xlim(t1, t2) #

ax0.set_ylim(Imin-.05*dI, Imax+.05*dI) # UP2 (-1.66, 0.28)#SL
#print(Imin-.05*dI, Imax+.05*dI) # UP2 (-0.695, -0.232)#RL (-13.15, 0.45)#MP
ax2.set_ylim(Emin-.05*dE, Emax+.05*dE) # UP2 (-1080, 560)#SL
#print(Emin-.05*dE, Emax+.05*dE) # UP2 (-107, 229)#RL (-216, 502)#MP

ax0.set_ylabel('$I$ (kA)')
ax2.set_ylabel('$E_z$ (V/m)')

plt.xlabel('Time ($\mu$s)')

ax0.plot(tc, fcur, linewidth=0.8, color=colors[0])
ax2.plot(txes, fefs, linewidth=0.8, color=colors[2])

# add space between plots
fig.subplots_adjust(hspace=1/2)#, wspace=1/3)

# add lines
for ax in (ax0, ax2): #
    ax.axhline(y=0, linestyle=':', lw=0.6, color='black')
    #ax.axvline(x=959010., linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=972.2329, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.2737, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.3154, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.3571, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.3987, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.4404, linestyle=':', lw=0.5, color='red')
    ##ax.axvline(x=959.6411, linestyle=':', lw=0.5, color=colors[4])


# shade HSC frame region
# UP2 correction: -0.00625
# UN4 correction: +0.01349

frp = -1*np.array([323,322,321,320,319,318,  # start UNL
                   108,107,106,105,104,103,  # RL branch creat.
                     6,  5,  4,  3,  2,  1]) # RL - MP

fr = -1 #for fr in frp: #
et = 972.4675 + fr/24 # event time (ms) # peak - frames before
cpt = tc[np.argmax(np.abs(fcur))] - 0.00625 # I peak time - correction
ef = round((et-cpt)*24) # event frame (relative to peak)
#print('Event Frame:', ef)
#cof = cpt + ef/24 # center of event frame
#print('Temporal Center of Event Frame (ms):', cof)
#htw = .5/24 # half temporal width
#for ax in (ax0, ax2):
#    ax.axvspan(cof-htw, cof+htw, color='red', alpha=1/3, zorder=0)
#ax0.text(972.234, 1., 'F972', fontsize='small')
#ax0.text(972.275, 1., 'F973', fontsize='x-small')

#fig.savefig(g.names[f]+'_ibxe_whole_raw.pdf', bbox_inches='tight')
#fig.savefig(g.names[f]+'_ibxe_whole_100khzIB.pdf', bbox_inches='tight')
#fig.savefig(g.names[f]+'_ie_zoomMP_F971-976_raw.pdf', bbox_inches='tight')
#fig.savefig(g.names[f]+'_ie_Izoom_100khzI.pdf', bbox_inches='tight')
#fig.savefig(g.names[f]+'_ie_SLzoom_raw.pdf', bbox_inches='tight')
#fig.savefig(g.names[f]+'_ie_zoom_F976_raw.pdf', bbox_inches='tight')

plt.show()

# TO DO:
#  4. Update summary sheet and/or paper appendix.
#  5. ID events using > np.abs(mean+2*sigma) and/or max. DONE.
#  6. Apply low-pass filter for frequencies > 5e6 Hz. DONE.
#     (1 MHz for temporal correlation OK, raw for max)
#  7. Align current and Ef based on 10% rise time.

# Flash (Activity in 1-5s prior?)
# Close field timestamp
# Control room timestamp
# Herisau timestamp

# UP0 (Yes at EUCLID 2021-06-28 23:26:52. Confirm location)
# 2021-06-29_01.27.06,860815048
# 2021-06-29_01.27.30.430286026
# 2021-06-29_01.26.53.611041545

# UP1 (None. EUCLID 2021-07-24 16:06:06 where?)
# 2021-07-24_18.06.15,656520843
# 2021-07-24_18.06.44.769081436
# 2021-07-24_18.06.08.092065811

# UP2 (None. EUCLID 2021-07-24 16:24:00 where?)
# 2021-07-24_18.24.11,515220642
# 2021-07-24_18.24.40.678498596
# 2021-07-24_18.24.03.949035167

# UN4 (None. Flash itself at EUCLID 2021-07-30 15:38:10? If so why not below?)
# 2021-07-30_17.38.21,666766166
# 2021-07-30_17.38.47.073173566
# 2021-07-30_17.38.10.279182434

# UP3 (YES at EUCLID 2021-07-30 18:00:10)
# 2021-07-30_20.00.22,734939098
# 2021-07-30_20.00.47.477396746
# 2021-07-30_20.00.11.270195007

# UP4 (YES at EUCLID 2021-07-30 18:04:53)
# 2021-07-30_20.05.05,753443241
# 2021-07-30_20.05.30.176073566
# 2021-07-30_20.04.54.327002525
