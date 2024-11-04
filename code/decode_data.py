'''
Author: Toma OC
Description : pulls binary data files of E-field, X-ray, Current, and B-data
              and converts them into numpy arrays
''';

# ----------------------------------------------------------------------------
# IMPORTS
import numpy as np

# ----------------------------------------------------------------------------
# USER INPUTS
# choose flash
flash = 'UN5'

# file paths
path_ef_xr = '%s_EF_XR_data_raw.bin' % flash
path_pemt_bdtb = '%s_PEMt_Bdtb_data_raw.bin' % flash

# ----------------------------------------------------------------------------
# DATA

# electric field (ef) and x-ray (xr)
with open(path_ef_xr, 'rb') as f:
    loaded_data_ef_xr = np.load(f)

# current (pemt) and bdot (bdtb)
with open(path_pemt_bdtb, 'rb') as f:
    loaded_data_pemt_bdtb = np.load(f)


time_ef_xr = loaded_data_ef_xr[0,:]
ef = loaded_data_ef_xr[1,:]
xr = loaded_data_ef_xr[2,:]
time_pemt_bdtb = loaded_data_pemt_bdtb[0,:]
pemt = loaded_data_pemt_bdtb[1,:]
bdtb = loaded_data_pemt_bdtb[2,:]


# ----------------------------------------------------------------------------
# To only look at a specific region

# select time window
t1 = 900 # ms
t2 = 1100 # ms

# find the indices of interest for t1 and t2
ind_t1_ef_xr = np.argmin(np.abs(time_ef_xr-t1))
ind_t2_ef_xr = np.argmin(np.abs(time_ef_xr-t2))
ind_t1_pemt_bdtb = np.argmin(np.abs(time_pemt_bdtb-t1))
ind_t2_pemt_bdtb = np.argmin(np.abs(time_pemt_bdtb-t2))

# get the data we want (! the time arrays are updated here according the time window)
time_ef_xr = time_ef_xr[ind_t1_ef_xr:ind_t2_ef_xr+1]
ef = loaded_data_ef_xr[1,ind_t1_ef_xr:ind_t2_ef_xr+1]
xr = loaded_data_ef_xr[2,ind_t1_ef_xr:ind_t2_ef_xr+1]
time_pemt_bdtb = time_pemt_bdtb[ind_t1_pemt_bdtb:ind_t2_pemt_bdtb+1]
pemt = loaded_data_pemt_bdtb[1,ind_t1_pemt_bdtb:ind_t2_pemt_bdtb+1]
bdtb = loaded_data_pemt_bdtb[2,ind_t1_pemt_bdtb:ind_t2_pemt_bdtb+1]

    
