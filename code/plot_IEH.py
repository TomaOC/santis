# Author: Toma OC
#
# Generates subplots comparing I, dI/dt, and E as functions of time

import numpy as np
import matplotlib.pyplot as plt
import os
import general as g
from scipy.signal import butter, filtfilt # argrelextrema,
from read_channel_saentis import rcs
from read_field import read_field
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

# go to Tower data
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

# go to Radome data
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

# go to Herisau data
os.chdir(g.hdir+g.hds[f])

## Parameter Setting & Sampling Issue
SampleRate = 10000000.0
Start_time = 0
End_time = 6000
## Intervals & Undersampling & Reading
data_size_nS = (End_time - Start_time) * (0.001) * (SampleRate)
offset_nS = Start_time * (0.001) * (SampleRate)
FU = 0
FU = 2 * FU
ajuste_datos = FU / 4 + 1
data_size = np.round(data_size_nS / ajuste_datos)
Y_ch1,Time,__ = read_field('./', 1, FU, data_size_nS, offset_nS, SampleRate)
KK_flat_plate_herisau = 40
Y_ch1 = KK_flat_plate_herisau * Y_ch1

# Ensure Time and Y_ch1 have the same length
min_length = min(len(Time), len(Y_ch1))
Time = Time[:min_length] * 1000.0 # convert to ms
Y_ch1 = Y_ch1[:min_length]

# align current/derivative and E-field data

# find peak values
#idc = np.argmax(np.abs(cur))
# use B-dot signal to alignment
if f in [2,3,7,10,11,9]: # UP1, UP2, UN4, UN5
    #idc = np.argmax(bds)
    #print(f'B-dot max: {max(bds)} kA/us at {tc[idc]} ms')
    idc = np.argmin(bds)
    print(f'B-dot min: {min(bds)} kA/us at {tc[idc]} ms')
if f in [0,1]: # UPa, UP0
    idc = np.argmin(dia)
if f in [8]: # UP3
    idc = np.argmin(np.abs(tb-959925.32))
# same for EF
if f in [0,1,2,3,8,9]: # UPa, UP0, UP1, UP2, UP3
    Emargin = np.abs(np.mean(Ych1e)) + np.std(Ych1e)*8 # 20,12,9
    ide,vae = next((ide,vae) for ide,vae in enumerate(Ych1e)
                    if np.abs(vae) > Emargin)
    print(f'First E-field step: {vae} kV/m at {txe[ide]} ms')
if f in [7,11]: # UN4, UN6
    ide = np.argmax(Ych1e)
    print(f'EF max: {max(Ych1e)} kV/m at {txe[ide]} ms')
    idh = np.argmax(np.abs(Y_ch1))
if f in [10]: # UN5
    ide = np.argmin(Ych1e)
    print(f'EF min: {min(Ych1e)} kV/m at {txe[ide]} ms')
#else:
#    print('INVALID FLASH NUMBER')

tos = txe[ide]-tc[idc] # time offset
print('Radome - Tower time offset:', tos, 'ms')
#hos = Time[idh]-tc[idc] # Herisau offset
#print('Herisau - Tower time offset:', hos, 'ms')

# shift time array accordingly
txes = txe-tos #txe[(ide-i0):(ide+ie)]
thes = Time-1747.937 # UP2 Herisau offset
#thes = Time-hos # UN4 Herisau offset

## RAW DATA and adjust units
fcur = cur # in kA
fefs = Ych1e*1e3 # to V/m
fhes = Y_ch1

## FILTER DATA and adjust units
cutoff = 1e5 # Hz ## also removes EF system oscillations?
#fcur = butter_lowpass_filter(cur, cutoff, fsc) # in kA
#fefs = butter_lowpass_filter(Ych1e, cutoff, fsxe)*1e3 # to V/m
#fhes = butter_lowpass_filter(Y_ch1, cutoff, SampleRate)

print('%s avg.: %.7g +/- %.7g' % (cs[chp-1], np.mean(fcur), np.std(fcur)))
print('%s range: %.7g (at %.9g ms) to %.7g (at %.9g ms)' % (cs[chp-1],
      np.min(fcur), tc[np.argmin(fcur)], np.max(fcur), tc[np.argmax(fcur)]))
print('Radome EF avg.: %.7g +/- %.7g' % (np.mean(fefs), np.std(fefs)))
print('Radome EF range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (np.min(fefs), txes[np.argmin(fefs)],
         np.max(fefs), txes[np.argmax(fefs)]))
print('Herisau EF avg.: %.7g +/- %.7g' % (np.mean(fhes), np.std(fhes)))
print('Herisau EF range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (np.min(fhes), thes[np.argmin(fhes)],
         np.max(fhes), thes[np.argmax(fhes)]))

# write data to file
os.chdir(g.ppd+g.names[f])

#with open(g.names[f]+'_%s_data_filt.bin'%cs[chp-1], # raw/filt
#          "wb") as file:
#    np.save(file, [tc, fcur])

#with open(g.names[f]+'_EF_data_raw.bin', "wb") as file: # raw/filt
#    np.save(file, [txes, fefs])

#exit()

# leader start time (1st step)
tsl = 959.010 # UP2

# whole flash times
#t1 = -tos if tos<0 else 0 # start time
#t2 = 2e3-tos if (2e3-tos)<2400 else 2400 # end time

# zoom times
t1 = 972.34
t2 = 972.50

# find corresponding indices (start, end)
it1, it2 = np.argmin(np.abs(tc-t1)), np.argmin(np.abs(tc-t2)) # (tower)
ir1, ir2 = np.argmin(np.abs(txes-t1)), np.argmin(np.abs(txes-t2)) # (radome)
ih1, ih2 = np.argmin(np.abs(thes-t1)), np.argmin(np.abs(thes-t2)) # (herisau)

# ID peaks and troughs in time range:
Imin, Imax = np.min(fcur[it1:it2]), np.max(fcur[it1:it2])
Emin, Emax = np.min(fefs[ir1:ir2]), np.max(fefs[ir1:ir2])
Hmin, Hmax = np.min(fhes[ih1:ih2]), np.max(fhes[ih1:ih2])

print('For the specified time interval (%.7g to %.7g ms):' % (t1,t2))
print('Current avg.: %.5g +/- %.5g' %
      (np.mean(fcur[it1:it2]),np.std(fcur[it1:it2])))
print('Current range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (Imin, tc[it1+np.argmin(fcur[it1:it2])],
         Imax, tc[it1+np.argmax(fcur[it1:it2])]))
print('Radome EF avg.: %.5g +/- %.5g' %
      (np.mean(fefs[ir1:ir2]),np.std(fefs[ir1:ir2])))
print('Radome EF range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (Emin, txes[ir1+np.argmin(fefs[ir1:ir2])],
         Emax, txes[ir1+np.argmax(fefs[ir1:ir2])]))
print('Herisau EF avg.: %.5g +/- %.5g' %
      (np.mean(fhes[ih1:ih2]),np.std(fhes[ih1:ih2])))
print('Herisau EF range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (Hmin, thes[ih1+np.argmin(fhes[ih1:ih2])],
         Hmax, thes[ih1+np.argmax(fhes[ih1:ih2])]))

# Find and print local extrema
div=16 # division
#local_extrema(t1, t2, fsc, fsxe, tc, fcur, txes, fefs, div)

#exit()

# set yaxis offsets to zero
Imax,Imin = (Imax,Imin)-np.mean(fcur)
Emax,Emin = (Emax,Emin)-np.mean(fefs)
Hmax,Hmin = (Hmax,Hmin)-np.mean(fhes)

for y in (fcur, fefs, fhes): y -= np.mean(y) #

dI = Imax-Imin
dE = Emax-Emin
dH = Hmax-Hmin

# setup PLOTS
fig, (ax0, ax2, ax1) = plt.subplots(3, 1) #

#ax0.set_title('Current (%s)' % cs[chp-1])
#ax2.set_title('Radome E-field')
#ax1.set_title('Herisau E-field')

# adjust axes
for ax in (ax0, ax2, ax1): ax.set_xlim(t1, t2)

ax0.set_ylim(-13.15, 0.45)#MP (Imin-.05*dI, Imax+.05*dI)
#(-1.66, 0.28)#SL (-0.695, -0.232)#RL # UP2
#print(Imin-.05*dI, Imax+.05*dI)
ax2.set_ylim(-216, 502)#MP (Emin-.05*dE, Emax+.05*dE)
#(-1080, 560)#SL (-107, 229)#RL # UP2
#print(Emin-.05*dE, Emax+.05*dE)
ax1.set_ylim(-2.84, 17.65)#MP (Hmin-.05*dH, Hmax+.05*dH)
#(-2.39, 3.35)#SL (-0.81, 1.75)#RL # UP2
#print(Hmin-.05*dH, Hmax+.05*dH)

# remove x-axis tick marks for top two plots (keep bottom)
#for ax in (ax0, ax2): ax.set_xticks([])

fontsize='large'

plt.xlabel('Time (ms)', size=fontsize) #$\mu$

ax0.set_ylabel('$I$ (kA)', size=fontsize)
ax2.set_ylabel('$E_z$ (V/m)', size=fontsize)
ax1.set_ylabel('$E_z$ (V/m)', size=fontsize)

ax2.text(.01, .93, '20-m', transform=ax2.transAxes, size=fontsize,
         verticalalignment='top', horizontalalignment='left')
ax1.text(.01, .93, '15-km', transform=ax1.transAxes, size=fontsize,
         verticalalignment='top', horizontalalignment='left')

ax0.plot(tc[it1:it2], fcur[it1:it2], linewidth=0.8, color=colors[0])
ax2.plot(txes[ir1:ir2], fefs[ir1:ir2], linewidth=0.8, color=colors[2])
ax1.plot(thes[ih1:ih2], fhes[ih1:ih2], linewidth=0.8, color=colors[1])

# add space between plots
fig.subplots_adjust(hspace=1/3)#, wspace=1/3)

# add lines
for ax in (ax0, ax2, ax1): #
    ax.axhline(y=0, linestyle=':', lw=0.6, color='black')
    #ax.axvline(x=959.01, linestyle=':', lw=0.6, color='red') # UP2 UNL
    #ax.axvline(x=967.97, linestyle=':', lw=0.6, color='red') # UP2 branch
    #ax.axvline(x=972.2737, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.3154, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.3571, linestyle=':', lw=0.5, color='red')
    #ax.axvline(x=972.39, linestyle=':', lw=0.6, color='red') # UP2 RL/MP
    #ax.axvline(x=972.4404, linestyle=':', lw=0.5, color='red')
    ##ax.axvline(x=959.6411, linestyle=':', lw=0.5, color=colors[4])


# shade HSC frame region
# UP2 correction: -0.00625
# UN4 correction: +0.01349
#"""
frp = -1*np.array([323,322,321,320,319,318,  # start UNL
                   110,108,107,106,105,104,103,102,97,  # RL branch creat.
                     6,  5,  4,  3,  2,  1]) # RL - MP

fr = -1 #for fr in frp: #
et = 972.4675 + fr/24 # event time (ms) # peak - frames before
cpt = tc[np.argmax(np.abs(fcur))] - 0.00625 # I peak time - correction
ef = round((et-cpt)*24) # event frame (relative to peak)
print('Event Frame:', ef)
cof = cpt + ef/24 # center of event frame
print('Temporal Center of Event Frame (ms):', cof)
htw = .5/24 # half temporal width
for ax in (ax0, ax2, ax1):
    ax.axvspan(cof-htw, cof+htw, color='red', alpha=1/3, zorder=0)
#ax0.text(972.234, 1., 'F972', fontsize='small')
#ax0.text(972.275, 1., 'F973', fontsize='x-small')
#"""

#fig.savefig('IEH/'+g.names[f]+'_ieh_whole_100khzI.pdf', bbox_inches='tight')
#fig.savefig('IEH/'+g.names[f]+'_ieh_zoom_RLMP_raw.pdf',
#            bbox_inches='tight') # _lines
#fig.savefig('IEH/'+g.names[f]+'_ieh_Izoom_100khzI_lines.pdf',
#            bbox_inches='tight')
#fig.savefig(g.names[f]+'_ieh_zoomMP_F971-976_raw.pdf', bbox_inches='tight')
fig.savefig('IEH/'+g.names[f]+'_ieh_zoom_F976_raw_new.pdf', bbox_inches='tight')

plt.show()

# TO DO:
# 4. Update summary sheet and/or paper appendix.
# 6. Apply low-pass filter for frequencies > 5e6 Hz. DONE.
#    (1 MHz for temporal correlation OK, raw for max)
# 7. Align current and Ef based on 10% rise time.


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
