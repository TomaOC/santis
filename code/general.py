# Author: Toma OC

# here
ppd = '/Users/TCB/Desktop/Research/Lightning/Data/postproc/'
# data directories
cfadir = '/Users/TCB/Desktop/Research/Lightning/Data/close_field_adlink/data/'
crdir = '/Users/TCB/Desktop/Research/Lightning/Data/control_room/data/'
hdir = '/Users/TCB/Desktop/Research/Lightning/Data/herisau/data/'

# radome
rds = ['2021-06-29_01.08.53,814570426/', # UPa
       '2021-06-29_01.27.06,860815048/', # UP0
       '2021-07-24_18.06.15,656520843/', # UP1
       '2021-07-24_18.24.11,515220642/', # UP2
       '2021-07-30_17.17.21,642941474/', # UN1
       '2021-07-30_17.31.03,523020744/', # UN2
       '2021-07-30_17.35.53,588362216/', # UN3
       '2021-07-30_17.38.21,666766166/', # UN4
       '2021-07-30_20.00.22,734939098/', # UP3
       '2021-07-30_20.05.05,753443241/', # UP4
       '2021-08-16_04.34.16,522378444/', # UN5
       '2021-08-16_07.53.29,494264602/', # UN6
       '2021-08-16_17.06.52,027379989/', # UN7
       '2021-08-16_17.08.40,478846549/'] # UN8

# control room
cds = ['2021-06-29_01.09.17.184027276/', # UPa
       '2021-06-29_01.27.30.430286026/', # UP0
       '2021-07-24_18.06.44.769081436/', # UP1
       '2021-07-24_18.24.40.678498596/', # UP2
       '2021-07-30_17.17.46.752138746/', # UN1
       '2021-07-30_17.31.28.218478656/', # UN2
       '2021-07-30_17.36.18.211094126/', # UN3
       '2021-07-30_17.38.47.073173566/', # UN4
       '2021-07-30_20.00.47.477396746/', # UP3
       '2021-07-30_20.05.30.176073566/', # UP4
       '2021-08-16_04.34.47.896447656/', # UN5
       '2021-08-16_07.54.01.244129456/', # UN6
       '2021-08-16_17.07.22.502677356/', # UN7
       '2021-08-16_17.09.11.962282746/'] # UN8

# Herisau
hds = ['2021-06-29_01.08.40.582095146/', # UPa
       '2021-06-29_01.26.53.611041545/', # UP0
       '2021-07-24_18.06.08.092065811/', # UP1
       '2021-07-24_18.24.03.949035167/', # UP2
       '2021-07-30_17.17.10.410085678/', # UN1
       '2021-07-30_17.30.52.227144718/', # UN2
       '2021-07-30_17.35.42.228182315/', # UN3
       '2021-07-30_17.38.10.279182434/', # UN4
       '2021-07-30_20.00.11.270195007/', # UP3
       '2021-07-30_20.04.54.327002525/', # UP4
       '2021-08-16_04.34.11.686114311/', # UN5
       '2021-08-16_07.53.24.416002273/', # UN6
       '2021-08-16_17.06.46.760082244/', # UN7
       '2021-08-16_17.08.35.226150989/'] # UN8

names = ['UPa',
         'UP0',
         'UP1',
         'UP2',
         'UN1',
         'UN2',
         'UN3',
         'UN4',
         'UP3',
         'UP4',
         'UN5',
         'UN6',
         'UN7',
         'UN8']

# Signal means and sigmas before flash
# X-ray energies average (keV)
xrm = [-1., # UPa -1.1765, -1.3228, -1.1415, -1.1108, -1.1240, -1.126
       -1.1, # UP0 -1.0602, -1.0501, -1.0937, -1.1189, -1.0762, -1.118
       -1.0, # UP1 -1.039, -0.99472, -0.94961, -1.0134, -1.0309, -1.0201
       -0.96, # UP2 -0.95279, -0.92524, -0.96835, -0.97919, -0.98075, -0.94004
       #,
       #,
       #,
       -1.43228, # UN4
       -0.93, # UP3 -0.92578, -0.92882, -0.91508, -0.9287, -0.98857, -0.91661
       -1.38175, # UP4
       1.286984, # UN5
       #, # UN6
       #,
       ]

# X-ray energy sigmas (raw)
xrs = [1.0 , # UPa 1.02656, 0.99473, 0.99965, 1.03329, 1.00421, 1.0129
       0.9 , # UP0 0.91734, 0.90077, 0.93195, 0.89267, 0.91115, 0.89517
       0.74, # UP1 0.7358, 0.74144, 0.72266, 0.74251, 0.70481, 0.76453
       0.74, # UP2 0.73204, 0.74019, 0.74538, 0.71702, 0.73539, 0.74594
       #,
       #,
       #,
       22.2081, # UN4
       0.78, # UP3 0.77815, 0.77666, 0.77756, 0.79103, 0.76862, 0.7792
       22.7639, # UP4
       25.6299, # UN5
       #, # UN6
       #,
       ]
       # avg. 22.76585167 +/- 2.16084328 keV

# E-field averages (V/m)
efa = [20, # UPa 19.184, 20.757, 18.805, 15.940, 17.274, 18.69
       20, # UP0 18.833, 15.059, 21.639, 19.885, 17.538, 19.117
       20, # UP1 17.876, 16.048, 11.539, 15.848, 14.341, 16.308
       11.5, # UP2 11.337, 11.059, 11.389, 11.551, 12.624, 11.53
       #,
       #,
       #,
       10.6195, # UN4
        7., # UP3 6.2093, 6.7993, 8.4242, 8.0218, 7.0192, 6.7167
       9.54610, # UP4
       0.001437132453918457, # UN5
       #, # UN6
       #,
       ]

# E-field sigmas (raw)
efm = [56., # UPa 56.262, 55.893, 56.168, 55.998, 56.283, 56.107
       56., # UP0 55.968, 56.249, 56.05, 55.919, 56.075, 55.932
       41., # UP1 41.509, 41.091, 41.145, 41.2, 41.116, 41.06
       42.11, # UP2 42.075, 42.21, 42.033, 42.033, 42.141, 42.143
       #,
       #,
       #,
       41.6016, # UN4
       41., # UP3 41.967, 40.624, 40.699, 40.776, 40.677, 41.274
       41.3882, # UP4
       0.013472036049062670, # UN5
       #, # UN6
       #,
       ]
       # ari.avg. 43.83943953 +/- 18.19519390 V/m
       # geo.avg. 39.162901 +26.789714/-15.907829 V/m

# Current averages (kA) (PEMb)
iavg = [0.49, # UPa 0.49364, 0.48329, 0.50008, 0.48833, 0.50349, 0.49263
        0.32, # UP0 0.31934, 0.34639, 0.33317, 0.31089, 0.32465, 0.30533
        0.34, # UP1 0.32576, 0.32656, 0.34492, 0.34525, 0.3407 , 0.34032
        0.41, # UP2 0.43209, 0.43677, 0.40631, 0.38834, 0.40754, 0.40749
        #,
        #,
        #,
        0.309178, # UN4
        0.35, # UP3 0.36074, 0.32322, 0.34741, 0.35389, 0.3486, 0.33433
        0.3123375, # UP4
        #, # UN5
        #, # UN6
        #,
        ]

# Current sigmas (kA) (PEMb)
istd = [0.048 , # UPa 0.04832, 0.04803, 0.04846, 0.04805, 0.04842, 0.04852
        0.0505, # UP0 0.05048, 0.05011, 0.050195, 0.05165, 0.050245, 0.052245
        0.051 , # UP1 0.05162, 0.05189, 0.05039, 0.05032, 0.05042, 0.05078
        0.0495, # UP2 0.04933, 0.04899, 0.04952, 0.04981, 0.04978, 0.04955
        #,
        #,
        #,
        0.184146, # UN4
        0.051, # UP3 0.05048, 0.05262, 0.05104, 0.05033, 0.05115, 0.051575
        0.317475, # UP4
        #, # UN5
        #, # UN6
        #,
        ]

# dI/dt averages (kA/us) (Bdtt)
dim = [-0.60, # UPa -0.5933, -0.5972, -0.5916, -0.5938, -0.6019, -0.6014
       -0.60, # UP0 -0.6027, -0.5983, -0.6068, -0.6068, -0.5992, -0.5939
       -0.62, # UP1 -0.6285, -0.6181, -0.62135, -0.6171, -0.6241, -0.6324
       -0.61, # UP2 -0.6050, -0.5953, -0.6048, -0.6156, -0.6172, -0.6075
        #, -0.605587
        #,
        #,
       -0.640742, # UN4
       -0.625, # UP3 -0.6333, -0.6216, -0.6263, -0.6221, -0.6288, -0.6213
       -0.617641, # UP4
        #, # UN5
        #, # UN6
        #,
        ]

# dI/dt sigmas (kA/us) (Bdtt)
dis = [0.315, # UPa 0.31812, 0.31286, 0.31834, 0.31296, 0.31514, 0.31229
       0.35, # UP0 0.35021, 0.36104, 0.3567, 0.34506, 0.3578, 0.34948
       0.33, # UP1 0.32413, 0.32464, 0.33836, 0.33795, 0.33725, 0.33022
       0.31, # UP2 0.30651, 0.30871, 0.30712, 0.29523, 0.30697, 0.30851
        #,
        #,
        #,
       0.730688, # UN4
       0.33, # UP3 0.33842, 0.32486, 0.32904, 0.32905, 0.32743, 0.34397
       0.721796, # UP4
        #, # UN5
        #, # UN6
        #,
        ]

# Avg. E-field abs(max,min) = 1.085 +/- 0.686 kV/m (Re-calc)

# NOTES:
# ------
# UPa: PEMb best for I (raw & 100kHz lpf);
#      raw ROCb best for dI/dt (alignment)
# UP0: PEMb best for I (raw & 100kHz lpf);
#      raw ROCb best for dI/dt (alignment)
# UP1: PEMb best for I (raw & 100kHz lpf);
#      raw ROCb / 100kHz lpf Bdtt best for dI/dt
# UP2: PEMb better for I (raw & 100kHz lpf);
#      raw ROCb best for dI/dt (alignment)
# UP3: PEMb best for I (raw & 100kHz lpf);
#      raw ROCb / 100kHz lpf Bdtt best for dI/dt

###
# E-field power spectrum from waveform: 
# (or estimate from Jef. for characteristic lengths (tower, channel l&r, etc.)
# convert exponential fit to exp(omega*t_SL) form
