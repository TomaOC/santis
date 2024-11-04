import numpy as np

## ds: data_size
## os: offset
## sr: samplerate

def read_field(directory = None, channel_number = None,
               factor_undersampling = None,ds_nS = None,
               os_nS = None,sr = None):
    # ITS REALLY IMPORTANTE TO MAKE THE DISPLACEMENT FROM EVEN NUMBERS, GIVER
    
    dt = 1 / sr
    dir = directory
    even_factor = factor_undersampling
    undersample_factor = even_factor
    # its important to think that if we undersample, the time vector change
    # accordingly, so take care in generating the time vector, so the
    # grid must be 10nS*undersample_factor
    data_dizaines_nS = ds_nS
    # number of datapoints to read 10nS units, max 120e6=1.2seconds
    #data_dizaines_nS=0.1e6;
    #os_start=35.35e6; # start offset 23e6;
    os_start = os_nS
    # assuring an even offset
    os_start = np.round(os_start / 2) * 2
    ajuste_datos = even_factor / 2 + 1
    ds = round(data_dizaines_nS / ajuste_datos)
    ds = round(ds / 2) * 2
    
    os_ch2 = 0
    os_ch3 = 0
    error_channel = 0
    
    if 1 == channel_number:
        fid_ch2 = open(dir+'dgtz2_ch0.dat', 'rb')
        #if (fid_ch2 < 0):
        #data_out = 0
        #error_channel = 1
            #error('could not open file "myfile.txt"');
        #else:
        header_data_ch2 = np.fromfile(fid_ch2, dtype='>d', count=3)
            #fseek(fid_ch2, (os_start + os_ch2)*2, 'bof')
        data_strike_ch2 = np.fromfile(fid_ch2, dtype='>h', count=ds)
                #, '*int16',undersample_factor, 'ieee-be')
        data_strike_ch2 = np.double(data_strike_ch2)
        # CH2 extract parameters gain, offset and increment
        gain_ch2, os_ch2, increment_ch2 = header_data_ch2
            #gain_ch2 = header_data_ch2(1)
            #os_ch2 = header_data_ch2(2)
            #increment_ch2 = header_data_ch2(3)
        data_strike_ch2 = data_strike_ch2*gain_ch2+os_ch2 #np.multiply(
        data_out = data_strike_ch2
    else:
        if 2 == channel_number:
            fid_ch3 = open(dir+'dgtz2_ch1.dat', 'rb')
            #if (fid_ch3 < 0):
            #data_out = 0
            #error_channel = 1
                #error('could not open file "myfile.txt"');
            #else:
            header_data_ch3 = np.fromfile(fid_ch3, dtype='>d', count=3)
                #fseek(fid_ch3, (os_start + os_ch3)*2, 'bof')
            data_strike_ch3 = np.fromfile(fid_ch3, dtype='>h', count=ds)
                    #ds,'*int16',undersample_factor,'ieee-be')
            data_strike_ch3 = np.double(data_strike_ch3)
                # CH3 extract parameters gain, offset and increment
            gain_ch3, os_ch3, increment_ch3 = header_data_ch3
                #gain_ch3 = header_data_ch3(1)
                #os_ch3 = header_data_ch3(2)
                #increment_ch3 = header_data_ch3(3)
            data_strike_ch3 = data_strike_ch3*gain_ch3 + os_ch3
            data_out = data_strike_ch3
        #else:
        #    print('Unknown Channel')
    
    #'all'.close()
    # CREATE the time vector and time in uS and mS to plot
    if (error_channel == 0):
        step = data_dizaines_nS * dt / ds
        time_dizaines_nS = np.transpose(np.arange(os_start/sr,
                                                  (os_start/sr + ds*step),
                                                  step))
        #time_dizaines_nS=(0:step:data_dizaines_nS*dt-step)';
    else:
        time_dizaines_nS = 0
    
    #varargout[1] = np.array([time_dizaines_nS])
    #varargout[2] = np.array([error_channel])
    #varargout=time_dizaines_nS;
# timeus=time_dizaines_nS/1e-6;
# timems=time_dizaines_nS/1e-3;
    return data_out, time_dizaines_nS, error_channel
