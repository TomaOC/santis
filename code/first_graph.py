'''
 File name: first_graph.ipynb
 Author: Florent Aviolat
 Date created: 28/02/2023
 Date last modified: 28/02/2023
 Version : V.1
 Description : graphic representation of lightning data : current, bdt, ef, xr
'''

# ----------------------------------------------------------------------------
# IMPORTS
# install mathjax in the used environment (used to display latex formula)

import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly_resampler import FigureResampler

# ----------------------------------------------------------------------------
# USER INPUTS
# choose flash
flash = 'UP2'

# title of the figure
title = flash # "Flash négatif ascendant du 16 aout 2021, UN5"

# path of the saved figure
path_save = "first_graph.html"

# documents paths
path_ef_xr = '../%s/%s_EF_XR_data_raw.bin' % (flash, flash) # raw or filt
path_pemt_bdtb = '../%s/%s_PEMb_Bdtt_data_raw.bin' % (flash, flash) # raw or filt

# selected window
t1 = 600 #ms
t2 = 1400 #ms

# parameters for the plot
# Using resampler
use_resampler = True
# Graph to html
html_graph = False
# Show graph
show_graph = True

# dictionary with the processing, key: name /
# value: value of the needed processing factor
# cf subsection DATA PROCESSING
dict_proc = {'No filter': None, 'With filter': 2}

# tickformat, used to align y-label
# cf.code (ctrl-F, tickformat)
# give the size of the ticks (nb. of characters)
ticklen = "6"

# Print the parameters
print("\nGRAPH: ONLY GRAPH")
print("\n%s\n\nSaved to : %s" %(title, path_save))
print("Selected time window (ms): %f - %f" % (t1,t2))
print("Using resampler: %d" % (use_resampler))
print("Graph to html: %d" % (html_graph))
print("Show graph: %d\n" % (show_graph))
# ----------------------------------------------------------------------------
# REMARKS

# go.scatter is used according that go.scattergl may induce lake of data ?
# (no real change of performance observed so...)
# cf. https://community.plotly.com/t/go-scatter-vs-go-scattergl/47617
# cf. https://plotly.com/python/webgl-vs-svg/

# documentation for resampler 
# cf. https://stackoverflow.com/questions/64384107/make-plotly-scatter-plots-faster-for-large-datasets-python
# cf. https://predict-idlab.github.io/plotly-resampler/getting_started.html#working-examples

# ----------------------------------------------------------------------------
# DATA
# numerical data
# electric field (ef) and x-ray (xr)
with open(path_ef_xr, 'rb') as f:
    loaded_data_ef_xr = np.load(f)

# current (pemt) and bdot (bdtb)
with open(path_pemt_bdtb, 'rb') as f:
    loaded_data_pemt_bdtb = np.load(f)

# time
time_ef_xr = loaded_data_ef_xr[0,:]
time_pemt_bdtb = loaded_data_pemt_bdtb[0,:] 

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

print("Data ready")

# ----------------------------------------------------------------------------
# DATA PROCESSING

# function for to call the different processings
def data_process(array, factor) :
    if factor == None:
        return array # None used to call no processing on data, i.e. keep it raw 
    else:
        return array*factor # HERE PUT THE REAL FILTERING FUNCTION
    
# ----------------------------------------------------------------------------
# GRAPH

# number of rows and columns
nb_rows = 4
nb_cols = 1

# subplots with shared axis
fig = None
if use_resampler:
    fig = FigureResampler(make_subplots(rows=nb_rows, cols=nb_cols, shared_xaxes=True, x_title='time [ms]', vertical_spacing=0.05))
else:
    fig = make_subplots(rows=nb_rows, cols=nb_cols, shared_xaxes=True, x_title=r'$time \textrm{ }  [ms]$', vertical_spacing=0.05)

# dropdown option list
dropdown_options = []

# loop that goes through the processings
for i, proc in enumerate(dict_proc.keys()):
    # set visibility to True for the first element of the dropdown menu and False for the next ones
    vis = False
    if i==0 :
        vis = True

    # add the traces : pemt, bdtd, ef, xr
    if use_resampler:
        fig.add_trace(go.Scattergl(name="Current", mode='lines', line=dict(color='#B51F1F'), visible=vis), hf_x=time_pemt_bdtb,  
                                   hf_y=data_process(pemt,dict_proc[proc]), row=1, col=1)
        fig.add_trace(go.Scattergl(name="dI/dt", mode='lines', line=dict(color='#007480'), visible=vis), hf_x=time_pemt_bdtb,  
                                   hf_y=data_process(bdtb,dict_proc[proc]), row=2, col=1)
        fig.add_trace(go.Scattergl(name="Ez", mode='lines', line=dict(color='#FFB100'), visible=vis), hf_x=time_ef_xr, 
                                   hf_y=data_process(ef,dict_proc[proc]), row=3, col=1)
        fig.add_trace(go.Scattergl(name="X-ray", mode='lines', line=dict(color='#69B58A'), visible=vis), hf_x=time_ef_xr, 
                                   hf_y=data_process(xr,dict_proc[proc]), row=4, col=1)
    else :
        fig.add_trace(go.Scatter(x=time_pemt_bdtb,  y=data_process(pemt,dict_proc[proc]), mode='lines', name="Current",
                                line=dict(color='#B51F1F'), visible=vis), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_pemt_bdtb,  y=data_process(bdtb,dict_proc[proc]), mode='lines', name="dI/dt",
                                line=dict(color='#007480'), visible=vis), row=2, col=1)
        fig.add_trace(go.Scatter(x=time_ef_xr, y=data_process(ef,dict_proc[proc]), mode='lines', name="Ez",
                                line=dict(color='#FFB100'), visible=vis), row=3, col=1)
        fig.add_trace(go.Scatter(x=time_ef_xr, y=data_process(xr,dict_proc[proc]), mode='lines', name="X-ray",
                                line=dict(color='#69B58A'), visible=vis), row=4, col=1)

    # change the parameters of the graph
    # y-axis names
    if use_resampler :
        fig['layout']['yaxis']['title']="Current [kA]"
        fig['layout']['yaxis2']['title']='dI/dt [kA/us]'
        fig['layout']['yaxis3']['title']='Ez [V/m]'
        fig['layout']['yaxis4']['title']='X-ray [keV]'
    else :
        fig['layout']['yaxis']['title']=r"$Current \textrm{ } [kA]$"
        fig['layout']['yaxis2']['title']=r'$dI/dt \textrm{ } [kA/us]$'
        fig['layout']['yaxis3']['title']=r'$E_z \textrm{ } [V/m]$'
        fig['layout']['yaxis4']['title']=r'$X-ray \textrm{ } [keV]$'
    # y-axis height
    fig['layout']['height']=750

    # tickformat and font
    fig.update_layout(yaxis  = {"tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"},  
                      yaxis2 = {"tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"}, 
                      yaxis3 = {"tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"}, 
                      yaxis4 = {"tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"})

    # change the template
    fig.update_layout(template="plotly_white")

    # make the visible list 
    visible_list = []
    for j, _ in enumerate(dict_proc.keys()):
        if i==j:
            visible_list = visible_list+[True]*4
        else:
            visible_list = visible_list+[False]*4

    # make the dropdown menu options
    dropdown_options.append({'label': proc, 'method': 'update', 'args': [{'visible': visible_list}]})

# update the layout to include the dropdown menu
fig.update_layout({'updatemenus': [{'x':1, 'y': 1.1, 'buttons': dropdown_options}]})

# update the layout to remove or keep the legend
if use_resampler:
    fig.update_layout(showlegend=True)
else :
    fig.update_layout(showlegend=False)

# x-axis
time_margin = (t2-t1)*0.02
fig.update_xaxes(range=[time_ef_xr[0]-time_margin, time_ef_xr[-1]+time_margin])

# Title
use_resampler_title = ""
if use_resampler:
    use_resampler_title = ' (resampler used)'

fig.update_layout(title={ 'text': title + use_resampler_title, 'y':0.935, 'x':0.05, 'xanchor': 'left', 'yanchor': 'top'}, font_family="Monaco",
                  hoverlabel_font_family="Monaco", hoverlabel_font_size=12)

print("Graph computed")

# ----------------------------------------------------------------------------
# EXPORT, SHOW THE GRAPH
if html_graph:
    fig.write_html(path_save, include_mathjax = 'cdn')
    print('Graph saved')

if use_resampler and show_graph :
    fig.show_dash(mode='inline')
    print('Graph shown (resampler)')
elif show_graph:
    fig.show()
    print('Graph shown')
    
print("End\n")
