import numpy as np
#import os
#import general as g

## rcs: read_channel_saentis
## chn: channel_number
## dsns: data_size_nS
## fs: samplerate

def rcs(dir = None,chn = None,dsns = None,fs = None):
# IMPORTANT TO MAKE THE DISPLACEMENT FROM EVEN NUMBERS, GIVEN
# THAT THERE EXISTS A BIT DISPLACEMENT
    dist = 3
    r = 0.135
    Aeq = np.pi * r ** 2
    mu0 = 4 * np.pi * 1e-7
    PEM_Constant = 20000.0
    ROCOIL_Constant = 1000.0
    mla = 1.1 # attenuation_meteolabor
    atten = 10 ** (50 / 20)
    AStokAuS = 1e-9 # conversion from AS to kAuS
    # important: change if digitizer configuration sampling time changes
    dt = 1 / fs
    # important: if we undersample, the time vector changes accordingly,
    # so take care in generating the time vector,
    # so the grid must be 10nS*usf
    data_dizaines_nS = dsns # 0.1e6;
    # number of datapoints to read 10nS units, max 120e6=1.2seconds
    # assuring an even offset
    ## ds: data_size
    ds = np.round(data_dizaines_nS)
    ds = np.round(ds / 2) * 2
    fiber_difference = - np.round((2.73e-7) * fs)
    # sampling time = 1/100MHz = 10nS, so fiber difference = 0.273uS = 27.3 samples
    offset_ch1 = - fs / 10000000.0
    # se deberia mas bien incluir el retardo de fase, no lineal en frecuencia
    # del integrador, en lugar de un numero
    offset_ch2 = 0
    offset_ch3 = 0 + fiber_difference
    offset_ch4 = 0 + fiber_difference
    error_channel = 0
    ## dsc: data_strike_ch
    
    if 1 == chn:
        # open the channel file
        fid_ch1 = open(dir+'dgtz1_ch0.dat', 'rb') # B-dot
        
        # open the header data: gain, offset and increment
        header_data_ch1 = np.fromfile(fid_ch1, dtype='>d', count=3)#[:3]
        # go to the offset start point
        # read and define the format of the Labview File: '*int16', 'ieee-be'
        dsc1 = np.fromfile(fid_ch1, dtype='>h')#, offset=os1)#[3:]
        # convert to double from '*int16', 'ieee-be'
        dsc1 = np.double(dsc1)
        #print('dsc1 type', type(dsc1[0]), type(dsc1[4]))
        # CH1 extract parameters gain, offset and increment
        gain_ch1 = header_data_ch1[0]
        offset_ch1 = header_data_ch1[1]
        increment_ch1 = header_data_ch1[2]
        ## apply gain, offset and increment for all the channels (x4)
        dat1 = dsc1*gain_ch1 + offset_ch1
        do = dat1*atten*(2*np.pi*dist*mla)*AStokAuS/(mu0*Aeq)
    else:
        if 2 == chn:
            fid_ch2 = open(dir+'dgtz1_ch1.dat', 'rb') # PEM UP
            
            header_data_ch2 = np.fromfile(fid_ch2, dtype='>d', count=3)
            dsc2 = np.fromfile(fid_ch2, dtype='>h')#[3:]
            dsc2 = np.double(dsc2)
            # CH2 extract parameters gain, offset and increment
            gain_ch2 = header_data_ch2[0] #[1]
            offset_ch2 = header_data_ch2[1] #[2]
            increment_ch2 = header_data_ch2[2] #[3]
            #print('header_data_ch2 =', gain_ch2, offset_ch2, increment_ch2)
            dat2 = dsc2*gain_ch2 + offset_ch2
            do = dat2*PEM_Constant/1000.0
        else:
            if 3 == chn:
                fid_ch3 = open(dir+'dgtz2_ch0.dat', 'rb') # Rocoil 1K
                
                header_data_ch3 = np.fromfile(fid_ch3, dtype='>d', count=3)
                dsc3 = np.fromfile(fid_ch3, dtype='>h')
                dsc3 = np.double(dsc3)
                # CH3 extract parameters gain, offset and increment
                gain_ch3 = header_data_ch3[0] #[1]
                offset_ch3 = header_data_ch3[1] #[2]
                increment_ch3 = header_data_ch3[2] #[3]
                #print('header_data_ch3 =', gain_ch3, offset_ch3, increment_ch3)
                dat3 = dsc3*gain_ch3 + offset_ch3
                do = dat3*ROCOIL_Constant/1000.0
            else:
                if 4 == chn:
                    fid_ch4 = open(dir+'dgtz2_ch1.dat', 'rb') # PEM DOWN
                    
                    header_data_ch4 = np.fromfile(fid_ch4, dtype='>d', count=3)
                    dsc4 = np.fromfile(fid_ch4, dtype='>h')
                    dsc4 = np.double(dsc4)
                    # CH4 extract parameters gain, offset and increment
                    gain_ch4 = header_data_ch4[0] #[1]
                    offset_ch4 = header_data_ch4[1] #[2]
                    increment_ch4 = header_data_ch4[2] #[3]
                    #print('header_data_ch4 =', gain_ch4, offset_ch4, increment_ch4)
                    dat4 = dsc4*gain_ch4 + offset_ch4
                    do = dat4*PEM_Constant/1000.0
                else:
                    print('Unknown Channel')
    
    # CREATE the time vector and time in uS and mS to plot
    if (error_channel == 0):
        step = data_dizaines_nS * dt / ds
        ## tdns: time_dizaines_nS
        tdns = np.transpose((np.arange(0, ds*step, step)))*1e3 # convert to ms
    else:
        tdns = 0
    
# timeus=tdns/1e-6;
# timems=tdns/1e-3;
    
    return do, tdns
