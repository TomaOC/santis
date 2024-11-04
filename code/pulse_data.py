# Author: Toma OC
import numpy as np
#from scipy.optimize import curve_fit

# + Positive X-ray Pulses + #

# times from ICC start (microseconds)
pxst = [#778.2, # UPa
        150.9, # UP0
        0., 89.5, 334.6, 345.7, 465.6, 554.1, 774., # UP1
        46.3, 267.5, # UP2
        118., 355., 483., 785., 11452. # UP3
        ] # UP4

# energies (keV)
pxre = [#177.002, # UPa
         63.431, # UP0
        256.096,  85.075,  86.968, 55.046,  31.609,  79.765,  31.12 , # UP1
         54.619,  44.06 , # UP2
         26.503,  50.428,  52.992,  42.799, 227.308 # UP3
        ] # UP4
# to remove 2nd and last: list[:1]+list[2:-1]

# associated current peak (kA)
pxpi = [#1.218, # UPa
        0.8149, # UP0
        1.655, 2.008, 1.913, 2.889, 2.198, 2.795, 2.659, # UP1
        1.1405, 0.4085, # UP2
        2.442, 2.713, 1.818, 5.196, 3.622 # UP3
        ] # UP4
fpxpi=[i for i in pxpi if i is not None]
#print('+ XR Ip = %.8g +/- %.8g kA' % (np.mean(fpxpi), np.std(fpxpi)))
# mean: 2.0044286 +/- 0.87954401 kA (43.88%)

# max dI/dt (kA/us)
pxdi = [#1.640, # UPa
         6.151, # UP0
        14.211,  8.228,  2.182,  3.678,  1.434,  2.058,  1.497, # UP1
        8.747, 1.33 , # UP2
        5.174, 2.12 , 1.684, 2.058, 1.995 # UP3
        ] # UP4
fpxdi=[it for it in pxdi if it is not None]
#print('+ XR dI/dt = %.8g +/- %.8g kA/us' % (np.mean(fpxdi), np.std(fpxdi)))
# mean: 5.9047143 +/- 4.6044672 kA/us (77.98%)

# min current rise time
pxtmr = [va/pxdi[id] for id,va in enumerate(pxpi) if (va and pxdi[id])!=None]
#print('+ XR I t_mr = %.8g +/- %.8g us' % (np.mean(pxtmr), np.std(pxtmr)))
# mean: 0.44898344 +/- 0.39068889 us (87.02%)

# minimum charge transfer
pxit = [va**2/pxdi[id] for id,va in enumerate(pxpi)
        if (va and pxdi[id])!=None]
#print('+ XR dIdt = %.8g +/- %.8g mC' % (np.mean(pxit), np.std(pxit)))
# mean: 1.0880371 +/- 1.2502516 mC (114.91%)

# electric field change (V/m)
pxde = [#271, # UPa
         547, # UP0
        1027,  886,  634,  634,  329,  592,  352, # UP1
        1450,  282, # UP2
         718,  474,  176,  566, None # UP3
        ] # UP4
fpxde=[e for e in pxde if e is not None]
#print('+ XR dE = %.8g +/- %.8g V/m' % (np.mean(fpxde), np.std(fpxde)))
# mean: 1162.3333 +/- 240.11155 (20.66%)

# electric field rise time (microseconds) 0-100%
pxer = [#3.70, # UPa
        0.20, # UP0
        0.25, 0.40, 11.85, 11.85, 13.20, 21.40, 24.35, # UP1
        0.25, 13.80, # UP2
        0.30, 2.95, 8.35, 26.40, None # UP3
        ] # UP4
pxet = np.array([r*0.8 for r in pxer if r!=None]) #else r
#print('+ XR Ef rise times =', pxet)
# mean: 0.24 +/- 0.06 us (23.57%)

# electric field rate of change
pxedt = [va/(0.8*pxer[id]) for id,va in enumerate(pxde)
         if (va and pxer[id])!=None]
#print('+ XR dE/dt = %.8g +/- %.8g V/m/us' % (np.mean(pxedt), np.std(pxedt)))
# mean: 5232.2917 +/- 1864.4442 V/m/us (35.63%)

# magnetic flux gradient / vector potential
pxemt = [va*(0.8*pxer[id]) for id,va in enumerate(pxde)
         if (va and pxer[id])!=None]
#print('+ XR dEdt = %.8g +/- %.8g uT m' % (np.mean(pxemt), np.std(pxemt)))
# mean: 269.54667 +/- 39.566792 mT m (14.68%)

# characteristic distance d = XRE / (I*t*E)
cf = 0.1602 # unit conversion factor (to fm)
pdti = np.array([va*pxdi[id]/(pxde[id]*pxpi[id]**2)
                for id,va in enumerate(pxre)
                if (pxpi[id] and pxdi[id] and pxde[id])!=None])/cf
pdte = np.array([va/(pxpi[id]*pxde[id]*pxet[id]) for id,va in enumerate(pxre)
                if (pxpi[id] and pxde[id] and pxet[id])!=None])/cf
#print('PX char. dist. (ti) = %.8g +/- %.8g m' % (np.mean(pdti), np.std(pdti)))
# mean: 8.761891e-14 +/- 7.5933265e-14 m (86.66%)
#print('PX char. dist. (te) = %.8g +/- %.8g m' % (np.mean(pdte), np.std(pdte)))
# mean: 5.3938929e-14 +/- 4.2717407e-14 m (79.20%)


# - Negative X-ray Pulses - #

# energies (keV)
nxre = [33.752, 117.676, # UN4
        856.140, 1588.867, # UN5
        73.120, 25.391, 7.874, 58.777, 583.679, 312.134, 827.820, 1452.940,
        1004.700, 631.042] # UN6
#print('- XRE = %.8g +/- %.8g keV' % (np.mean(nxre), np.std(nxre)))
# mean: 643.23425 +/- 635.69364 keV (98.83%)

# associated current peak (kA)
nxpi = [0.953, 5.159, # UN4
        11.453, 15.075, # UN5
        0.695, 2.038, 11.982, 7.953, 9.242, 7.614, 8.903, 14.519, 9.839,
        7.343] # UN6
fnxpi=[i for i in nxpi if i is not None]
#print('- XR Ip = %.8g +/- %.8g kA' % (np.mean(fnxpi), np.std(fnxpi)))
# mean: 9.95425 +/- 3.7010351 kA (37.18%)

# measured current rise time (microseconds) 0-100%
#nxir = [9.0, None, 3.56, # UN4
#        None, None] # UN5

# max dI/dt (kA/us)
nxdi = [1.227, 10.701, # UN4
        26.764, 53.6765, # UN5
        1.193, 1.031, 42.591, 26.926, 51.740, 19.937, 36.410, 67.517, 33.865,
        40.903] # UN6
fnxdi=[it for it in nxdi if it is not None]
#print('- XR dI/dt = %.8g +/- %.8g kA/us' % (np.mean(fnxdi), np.std(fnxdi)))
# mean: 29.574125 +/- 15.418076 kA/us (52.13%)

# min current rise time
nxtmr = [va/nxdi[id] for id,va in enumerate(nxpi) if (va and nxdi[id])!=None]
#print('- XR I t_mr = %.8g +/- %.8g us' % (np.mean(nxtmr), np.std(nxtmr)))
# mean: 0.3725679 +/- 0.084896581 us (22.79%)

# minimum charge transfer (during first half)
nxit = [va**2/nxdi[id] for id,va in enumerate(nxpi)
        if (va and nxdi[id])!=None]
#print('- XR dIdt = %.8g +/- %.8g mC' % (np.mean(nxit), np.std(nxit)))
# mean: 3.5140174 +/- 1.0796534 mC (30.72%)

# electric field change (V/m)
nxde = [347, 1575, # UN4
        2619, 3517, # UN5
        136, 782, 2522, 2425, 2876, 2929, 2941, 4071, 2768, 3535] # UN6
fnxde=[e for e in nxde if e is not None]
#print('- XR dE = %.8g +/- %.8g V/m' % (np.mean(fnxde), np.std(fnxde)))
# mean: 2945.25 +/- 945.51372 V/m (32.10%) (excl. lower bounds)

# electric field rise time (microseconds) 0-100%
nxer = [480.45, 3.90, # UN4
        1.15, 0.20, # UN5
        93.80, 159.55, 0.30, 0.35, 0.60, 0.30, 0.55, 0.25, 1.25, 0.25] # UN6
nxet = [r*0.8 if r!=None else r for r in nxer]
#print('- XR Ef rise times =', nxet)
# mean: 1.07 +/- 1.23 us (114.78%)

# electric field rate of change
nxedt = [va/(0.8*nxer[id]) for id,va in enumerate(nxde)
         if (va and nxer[id])!=None]
#print('- XR dE/dt = %.8g +/- %.8g V/m/us' % (np.mean(nxedt), np.std(nxedt)))
# mean: 19051.949 +/- 20173.576 V/m/us (105.89%)

# magnetic flux gradient / vector potential
nxemt = [va*(0.8*nxer[id]) for id,va in enumerate(nxde)
         if (va and nxer[id])!=None]
#print('- XR dEdt = %.8g +/- %.8g uT m' % (np.mean(nxemt), np.std(nxemt)))
# mean: 2052.95 +/- 1838.2903 uT m (89.54%)

# characteristic distance d = XRE / (I*t*E)
ndti = np.array([va*nxdi[id]/(nxde[id]*nxpi[id]**2)
                for id,va in enumerate(nxre)
                if (nxpi[id] and nxdi[id] and nxde[id])!=None])*cf
ndte = np.array([va/(nxpi[id]*nxde[id]*nxet[id]) for id,va in enumerate(nxre)
                if (nxpi[id] and nxde[id] and nxet[id])!=None])*cf
#print('NX char. dist. (ti) = %.8g +/- %.8g m' % (np.mean(ndti), np.std(ndti)))
# mean: 8.1894033e-15 +/- 6.3503051e-15 m (77.54%)
#print('NX char. dist. (te) = %.8g +/- %.8g m' % (np.mean(ndte), np.std(ndte)))
# mean: 9.0849339e-15 +/- 1.2204752e-14 m (134.34%)


# + Positive pulses (no X-rays) + #

# times from ICC start (microseconds)
ppst = [#0.0, # UPa
          0.0,  43.5, 225.5, 253.5, 286.5,
        #365.5, 371.5, 460.5, 468.5, 499.0, 521.5, 569.5, 583.5, 629.0, 640.5,
        656.1, 682.3, 725.4, 874.5, 954.0, # UP0
        127.6, 191.9, 231.6, 256.7, 381.6, 416.6, 482.6, 571.6, 638.6, 755.6,
        804.6, 856.6, 884.6, 910.6, # UP1
          0.0,  10.8, 145.7, 193.5, 202.2, 385.9, 454.9, 533.9, 705.9, 815.9,
        987.9, 1122.9, 1327.9, 1497.9, 1705.9, 1928.9, 2059.9, 2149.9,
        13451.9, # UP2
          0.0,  73.0, 132.0, 158.0, 203.0, 256.0, 315.0, 325.0, 381.0, 452.0,
        463.0, 495.0, 527.0, 571.0, 610.0, 695.0, 839.0, 908.0,
        1036.0, 1114.0, 1266.0, 1381.0, 1582.0 # UP3
        ] # UP4

# associated current peak (kA)
pppi = [# UPa
        -.040, 0.489, 0.353, 0.706, 0.529, #, , , , , , , ,
        0.719, 0.760, 0.774, 0.896, 1.208, # UP0
        0.743, 2.032, 1.109, 2.588, 1.530, 1.950, 3.429,
        3.524, 3.673, 4.446, 2.452, 2.344, 4.297, 2.262, # UP1
        0.512, 0.153, 0.282, 0.390, 0.336, 0.268, 0.553, 0.241, 0.431, 0.471,
        0.675, 0.512, 0.485, 0.729, 0.580, 0.607, 0.471, 0.539, 12.102, # UP2
        0.729, 1.367, 0.648, 1.028, 0.716, 2.791, 2.805, 1.706, 1.489, 2.615,
        1.679, 1.692, 1.896, 3.212, 2.669, 3.931, 3.904, 4.745, 6.115, 4.718,
        5.287, 9.357, 7.675 # UP3
        ] # UP4
fpppi=[i for i in pppi if i is not None]
#print('+ pulse Ip = %.8g +/- %.8g kA' % (np.mean(fpppi), np.std(fpppi)))
# mean: 1.69075 +/- 1.3717835 kA (78.08%)

# max dI/dt (kA/us)
ppdi = [# UPa
        2.038, 5.777, 1.913, 1.851, 2.225, #, , , , , , , ,
        0.916, 1.352, 1.290, 1.041, 1.664, # UP0
        5.068, 4.881, 2.762, 3.510, 1.702, 2.076, 2.263,
        2.018, 1.827, 2.138, 1.640, 1.827, 2.325, 1.578, # UP1
        10.054, 3.136, 3.198, 1.827, 2.014, 1.578, 1.764, 1.453, 1.889, 1.515,
         1.578, 1.702, 1.702, 1.702, 1.640, 1.951, 1.640, 1.578, 2.389, # UP2
        9.618, 7.810, 4.258, 2.762, 1.951, 5.192, 3.198, 2.014, 2.014, 2.014,
        1.515, 1.515, 1.764, 1.640, 2.637, 2.512, 1.827, 2.014, 2.388, 1.827,
        1.702, 2.388, 1.764 # UP3
        ] # UP4
fppdi=[it for it in ppdi if it is not None]
#print('+ pulse dI/dt = %.8g +/- %.8g kA/us' % (np.mean(fppdi), np.std(fppdi)))
# mean: 3.4573846 +/- 2.1782415 kA/us (37.86%)

# max current rise time
pptmr = [va/ppdi[id] for id,va in enumerate(pppi) if (va and ppdi[id])!=None]
#print('+ pulse I t_mr = %.8g +/- %.8g us' % (np.mean(pptmr), np.std(pptmr)))
# mean: 0.39716691 +/- 0.31353809 us (66.45%)

# minimum charge transfer
ppit = [va**2/ppdi[id] for id,va in enumerate(pppi)
        if (va and ppdi[id])!=None]
#print('+ pulse dIdt = %.8g +/- %.8g mC' % (np.mean(ppit), np.std(ppit)))
# mean: 0.74156141 +/- 0.76286862 mC (88.43%)

# electric field change (V/m)
ppde = [# UPa
        257, 509, 271, 280, 337, #, , , , , , , , ,
        253, 245, 249, 280, 310, # UP0
        374, 523, 385, 435, 309, 278, 370,
        633, 397, 320, 214, 294, 286, 248, # UP1
        858, 332, 401, 324, 324, 340, 309, 343,
        301, 332, 290, 317, 271, 397, 320, 320, 275,
        294, 490, # UP2
        1289, 1099, 370, 378, 259, 698, 511, 404, 221, 313, 206, 233, 233,
        328, 263, 305, 233, 237, 347, 347, 301, 298, 290 # UP3
        ] # UP4
fppde=[e for e in ppde if e is not None]
#print('+ pulse dE = %.8g +/- %.8g V/m' % (np.mean(fppde), np.std(fppde)))
# mean: 399.4 +/- 157.42439 V/m (11.38%)

# electric field rise time (microseconds) 0-100%
pper = [# UPa
        0.50, 0.10, 0.25, 1.00, 1.85, #, , , , , , , ,
        5.10, 7.10, 16.60, 17.30, 11.00, # UP0
        5.90, 4.25, 7.75, 1.70, 5.10, 13.10, 7.35,
        21.40, 16.45, 3.65, 5.60, 14.30, 13.65, 17.15, # UP1
        0.50, 0.10, 2.75, 16.70, 16.70, 29.20, 9.05, 20.10,
        21.15, 45.79, 12.95, 44.35, 74.35, 29.50, 82.65, 48.20, 29.45,
        75.60, 80, # UP2
        0.25, 0.25, 0.55, 12.25, 4.25, 4.70, 8.15, 9.00, 7.20, 10.70, 6.30,
        4.90, 4.20, 5.60, 6.25, 16.20, 5.85, 10.25, 21.70, 27.40, 34.05,
        30.40, 21.60 # UP3
        ] # UP4
ppet = [r*0.8 for r in pper if r!=None] # else r
#print('+ pulse Ef rise times =', ppet)
# mean: 7.05 +/- 6.80 us (96.47%)

# electric field rate of change
ppedt = [va/(0.8*pper[id]) for id,va in enumerate(ppde)
         if (va and pper[id])!=None]
#print('+ pulse dE/dt = %.8g +/- %.8g V/m/us'%(np.mean(ppedt),np.std(ppedt)))
# mean: 428.96639 +/- 700.04681 V/m/us (178.52%)

# magnetic flux gradient / vector potential
ppemt = [va*(0.8*pper[id]) for id,va in enumerate(ppde)
         if (va and pper[id])!=None]
#print('+ pulse dEdt = %.8g +/- %.8g uT m' % (np.mean(ppemt), np.std(ppemt)))
# mean: 2187.2 +/- 2252.4703 uT m (95.49%)


# - Negative pulses (no X-rays) - #

# associated current peak (kA)
nppi = [0.994, 0.912, 0.817, 1.224, 2.527, 1.591, 1.414, 1.604, 3.775, 1.699,
        1.428, 0.953, 2.174, 1.129, 1.658, 2.310, 3.666, 1.726, 2.798, 4.236,
        1.265, 2.215, 3.531, 2.228, 1.984, 1.265, 4.860, 1.808, 2.418, 1.306,
        2.350, 6.773, 1.658, 3.571, 4.738, 2.757, 5.389, 8.130, 1.374, # UN4
        0.532, 0.546, 0.451, 0.587, 0.709, 0.872, 0.505, 0.519, # UN5
        0.600, 5.484, 2.812, 2.988, 2.920] # UN6
fnppi=[i for i in nppi if i is not None]
#print('- pulse Ip = %.8g +/- %.8g kA' % (np.mean(fnppi), np.std(fnppi)))
# mean: 3.00225 +/- 1.668656 kA (57.42%)

# max dI/dt (kA/us)
npdi = [0.666, 0.853, 0.417, 0.417, 3.658, 4.842, 3.720, 5.029, 5.029, 4.219,
        3.471, 0.604, 3.533, 1.414, 1.663, 3.970, 1.663, 5.341, 3.035, 3.970,
        0.978, 4.157, 12.321, 1.850, 2.162, 0.417, 4.094, 0.666, 5.278, 1.290,
        1.477, 4.842, 0.666, 0.604, 3.783, 3.658, 7.335, 27.155, 0.479, # UN4
        1.727, 1.453, 0.783, 1.503, 0.858, 0.994, 2.236, 1.230, # UN5
        0.696, 0.920, 0.771, 1.056, 4.594] # UN6
fnpdi=[it for it in npdi if it is not None]
#print('- pulse dI/dt = %.8g +/- %.8g kA/us' % (np.mean(fnpdi), np.std(fnpdi)))
# mean: 3.6126364 +/- 1.7502747 kA/us (48.31%)

# max current rise time
nptmr = [va/npdi[id] for id,va in enumerate(nppi) if (va and npdi[id])!=None]
#print('- pulse I t_mr = %.8g +/- %.8g us (%.4g)' % (np.mean(nptmr), np.std(nptmr), ))
# mean: 1.0524843 +/- 0.30964547 us (31.54%)
  
# minimum charge transfer
npit = [va**2/npdi[id] for id,va in enumerate(nppi)
        if (va and npdi[id])!=None]
#print('- pulse dIdt = %.8g +/- %.8g mC' % (np.mean(npit), np.std(npit)))
# mean: 3.8552146 +/- 2.3867001 mC (58.56%)
  
# electric field change (V/m)
npde = [263, 294, 275, 340, 957, 759, 553, 843, 748, 744, 538, 313, 637, 366,
        492, 744, 626, 866, 614, 816, 385, 828, 1762, 534, 443, 366, 854, 378,
        965, 393, 572, 992, 679, 1156, 1457, 1022, 1350, 4070, 671, # UN4
        275, 204, 108, 120, 109, 275, 247, 335, # UN5
        63, 189, 96, 391, 982] # UN6
fnpde=[e for e in npde if e is not None]
#print('- pulse dE = %.8g +/- %.8g V/m' % (np.mean(fnpde), np.std(fnpde)))
# mean: 748.75 +/- 344.23366 V/m (46.14%) (excl. lower bounds)

# electric field rise time (microseconds) 0-100%
nper = [234.90, 359.25, 44.95, 99.80, 76.90, 84.75, 62.75, 77.20, 40.05,
        95.15, 42.05, 140.20, 37.70, 102.50, 79.20, 82.30, 87.70, 83.55,
        50.75, 81.05, 187.45, 64.30, 0.25, 147.30, 51.70, 82.80, 52.70,
        350.75, 137.35, 109.65, 73.65, 80.50, 94.90, 29.20, 16.80, 36.65,
        19.60, 0.10, 28.85, # UN4
        422.40, 352.90, 380.55, 263.75, 197.55, 379.20, 338.40, 444.40, # UN5
        47.55, 81.95, 60.05, 88.80, 2.00] # UN6
npet = [r*0.8 for r in nper if r!=None] # else r
#print('- pulse Ef rise times =', npet)
# mean: 45.68 +/- 23.12 us (50.62%)

# electric field rate of change
npedt = [va/(0.8*nper[id]) for id,va in enumerate(npde)
         if (va and nper[id])!=None]
#print('- pulse dE/dt = %.8g +/- %.8g V/m/us'%(np.mean(npedt),np.std(npedt)))
# mean: 28.068153 +/- 32.082356 V/m/us (106.38%)

# magnetic flux gradient / vector potential
npemt = [va*(0.8*nper[id]) for id,va in enumerate(npde)
         if (va and nper[id])!=None]
#print('- pulse dEdt = %.8g +/- %.8g uT m' % (np.mean(npemt), np.std(npemt)))
# mean: 32606.905 +/- 14449.44 uT m (46.79%)


# FITTING

# EM field bremsstrahlung length scale
