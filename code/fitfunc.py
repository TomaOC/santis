# Author : Toma Chaumont Behrs
# Define functions and perform best fit

import numpy as np
#from lmfit import Model
from scipy.stats import lognorm #, chisquare
from scipy.optimize import curve_fit
# popt,pcov = curve_fit(func, xdat, ydat)
# perr = np.sqrt(np.diag(pcov)) # give 1-sigma of fit params
#from sklearn.metrics import r2_score
from pulse_data import *

# for func in [list, of, models]:
#    popt,pcov = curve_fit(func, xdat, ydat)
#     print('Fit params:', popt)
#     print('1-sigma Er:', np.sqrt(np.diag(pcov)))
#     y_pred=func(xdata, (unzip popt))
#     r2_calc(ydat, y_pred)

# linear model
def linear(x,a):
    return a*x

# affine model
def affine(x, a, b):
    return a*x + b

# quadratic models
def quadratic(x,a,b,c): # general
    return a*(x**2) + b*x + c

def quad_a00(x,a): # 1st only
    return quadratic(x,a,0,0)

def quad_ab0(x,a,b): # 1st and 2nd
    return quadratic(x,a,b,0)

def quad_a0c(x,a,c): # 1st and 3rd
    return quadratic(x,a,0,c)

# power law model
def powlaw(x,a,b):
  return a*(x**b)

# exponential model
def expfn(x,const,gamma):
  return const*np.exp(gamma*x)

# logarithmic model
def logfn(x,a,b):
    return a + b*np.log(x)

# Heidler function
def heidler(t,I,tau1,tau2,n):
    return (I/eta(tau1,tau2,n))*((t/tau1)**n)*np.exp(-t/tau2)/(((t/tau1)**n)+1)

# eta function (for Heidler)
def eta(tau1,tau2,n):
    return np.exp(-(tau1/tau2)*(n*(tau2/tau1))**(1/n))

# sum of 2 Heidler functions ***
def heidler2(t,I1,tau11,tau12,n1, I2,tau21,tau22,n2):
    return heidler(t,I1,tau11,tau12,n1) + heidler(t,I2,tau21,tau22,n2)

# E-field model
#def efm(

# lmfit
#plmod = Model(powlaw)
#efmod = Model(expfn)

def arstats(data):
    print('median, mean, sigma: ')
    return (np.median(data),
            np.mean(data),
            np.std(data))

def lnstats(data):
    lnd = np.log(np.array(data))
    mu = np.mean(lnd)
    med = np.exp(mu)
    s = np.std(lnd)
    sg = np.exp(s)
    #print('sigma =', sg) # geometric std
    print('Mode =', np.exp(mu-s**2))
    #print('Range:', med/sg, 'to', med*sg)
    print('m = %.8g (+%.8g, -%.8g)' % (med, med*sg-med, med-med/sg))
    return (lognorm.median(s, scale=med),
            lognorm.mean(s, scale=med),
            lognorm.std(s, scale=med))
    #lognorm.stats(s, scale=np.exp(mu))


# Calculate RSS/SSR & R-squared:
def r2_calc(y_true, y_pred):
    residuals = y_true - y_pred
    rss = np.sum(residuals**2)
    print('Residual Norm =', np.sqrt(rss)) # lower value = better fit
    tss = np.sum((y_true - np.mean(y_true))**2)
    return 1 - (rss/tss) # closer to 1 = better fit


# ***
# Tests
# t1, t2 = start, end time (fit and window) ; maxfev = max func evals
# popt = [I1, tau11, tau12, n1,
#         I2, tau21, tau22, n2]
# perr = [1-sigma errors of above params] # less than value

# USED PEMs (Rog.Coils) - remove
# Test 1
# t1 = 959.009, t2 = 959.013, maxfev=5e3
# popt = [-1.33084276e+00  6.63895312e-04  7.69782994e-04  9.98514857e+00
#          7.33170121e-01  1.08412894e-03  4.48769636e-05  1.83618638e+01]
# perr = [ 1.37042097e-01  3.85487159e-05  5.28771384e-05  3.71709322e+00  4
#          7.93256337e-01  1.01566907e-04  3.10578606e-05  1.14456545e+01] 3

# Test 2
# t1 = 959.0095, t2 = 959.0135, maxfev=4e4
# popt = [-2.23674227e-01  2.11062532e-03  1.14812750e-03  6.31983913e+01
#         -6.33060721e-01  1.78088047e-03  1.83412285e-04  4.52416055e+00]
# perr = [ 2.44642040e-02  2.72548819e-05  2.52481081e-04  4.27666537e+01  4
#          9.15782598e-01  8.09795790e-04  5.69288198e-05  9.63133085e-01] 3

# Test 3
# t1 = 959009.5, t2 = 959013.5, maxfev=200*len(tcn)
# popt = [-0.85048198    11.64342857     2.48210631     0.76369126
#         -0.3886457      1.61779998     0.13306514     6.04747429]
# perr = [ 6.26982947e+01 1.03587232e+03 1.65237736e+01 2.40971575e+00  0
#          7.57553577e-01 6.13349725e-01 5.49481563e-02 2.16621795e+00] 3

# Test 4
# t1 = 959009.4, t2 = 959011.0, maxfev=200*len(tcn)
# popt = [-9.70526164e-01  1.35309665e+00  7.87225538e-02  2.16562470e+01
#         -1.08700656e-02  1.59786732e+00  4.57808836e-02  1.68492993e+01]
# perr = [ 1.07205626e+00  7.46655394e-02  1.26731258e-01  1.92674771e+01  2
#          4.16412624e+00  4.19280664e+01  5.74334733e-03  1.92079100e+00] 2

# Test 5
# t1 = 959009.5, t2 = 959011.1, maxfev=200*len(tcn)
# popt = [ 1.19486513e+00  2.58719300e-01  1.27871089e+03  2.88335557e+00
#         -9.17439844e-08  1.80406781e+02  4.24621941e-01  2.01043222e+00]
# perr = [ 7.07582034e-01  4.66447252e-02  7.69811827e-07  1.12937021e+00  4
#          2.79385280e-06  7.82253579e-07  1.47990694e-01  6.23058901e-01] 3


# Typical values: -0.3-5 kA, 2 us, 0.5 us, 10
#                    peak I, rise,  decay, steepness

xdat = np.array(pxst[:1]+pxst[2:-1]) # pxdi[:1]+pxdi[2:-1] # pxst[:-1]
ydat = np.array(pxre[:1]+pxre[2:-1]) # pxre[:-1]

for func in [linear, affine, powlaw, expfn, logfn]: #linear,
    popt,pcov = curve_fit(func, xdat, ydat)
    print('Fit params:', popt)
    print('1-sigma Er:', np.sqrt(np.diag(pcov)))
    y_pred=func(xdat, *popt)
    print(r2_calc(ydat, y_pred))
