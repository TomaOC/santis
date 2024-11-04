'''
 File name: second_graph.ipynb
 Author: Florent Aviolat
 Date created: 28/02/2023
 Date last modified: 28/02/2023
 Version : V.1
 Description : graphic representation of lightning data : ef, xr, pemt, bdtb 
''';

# ---------------------------------------------------------------------------------------
# IMPORTS
# install mathjax in the used environment (used to display latex formula)

import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import cv2
from PIL import Image

# ---------------------------------------------------------------------------------------
# USER INPUTS

# title of the figure
title = "Flash négatif ascendant du 16 aout 2021, UN5"

# path of the saved figure
path_save = "second_graph.html"

# documents paths
path_ef_xr = 'data/UN5_EF_XR_data_raw.bin'
path_pemt_bdtb = 'data/UN5_PEMt_Bdtb_data_raw.bin'
path_video = 'data/blitz_video.avi'

# selected window
t1 = 900 #ms
t2 = 910 #ms

# parameters for the plot
# Graph to html
html_graph = True 
# Show graph
show_graph = True 

# tickformat, used to align y-label
# cf.code (ctrl-F, tickformat)
# give the size of the ticks (nb. of characters)
ticklen = "6"

# parameters for the slider animation
# duration
duration = 0.001
# size of the minor ticks (default is 4), i.e. ticks between the ticks displayed on the slider
minorticklen = 0

# Print the parameters
print("\nGRAPH: VIDEO+GRAPH")
print("\n%s\n\nSaved to : %s" %(title, path_save))
print("Selected time window (ms): %f - %f" % (t1,t2))
print("Graph to html: %d" % (html_graph))
print("Show graph: %d\n" % (show_graph))
# ---------------------------------------------------------------------------------------
# REMARKS
# Hypothesis : the rectangles that shows the frame duration is centered on the instant of the frame (Hyp 1)

# Nice for slider and buttons : https://plotly.com/python/v3/gapminder-example/ - https://plotly.com/python/reference/#layout-sliders 

# ---------------------------------------------------------------------------------------
# DATA

# numerical data

# electric filed  (ef) and x-ray (xr)
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

# get the limit values for the graph u:up, l:low
# used to establish the height of the rectangles
limit_margin = 1.05
efu = limit_margin*np.max(ef)
efl = limit_margin*np.min(ef)
xru = limit_margin*np.max(xr)
xrl = limit_margin*np.min(xr)
pemtu = limit_margin*np.max(pemt)
pemtl = limit_margin*np.min(pemt)
bdtbu = limit_margin*np.max(bdtb)
bdtbl = limit_margin*np.min(bdtb)

print("Numerical data ready")

# video data
# technical data for the video
# frame per ms
fpms_video = 24 #frame/ms
# window length, duration of one frame
wl = 1/fpms_video # ms/frame

# import the video using cv2

vidcap = cv2.VideoCapture(path_video) 
images = []
while vidcap.isOpened():
    success, image = vidcap.read()
    if not success:
        break
    images.append(image)
vidcap.release()
print('Video data imported')

# convert the frames in PIL
# keep only the number of frames needed according t1 and t2 
# Here : DUMMY selection USED FOR DEVELOPMENT
nb_video_frame = int(fpms_video*(t2-t1)) #frame, USED FOR DEVELOPMENT
# store all the PIL images in a list
images_pil = []
# store the time of each image in a corresponding array
time_video = np.array([])
for i in range(int(nb_video_frame)+1) :
    images_pil.append(Image.fromarray(images[955+i]))
    current_time = t1+i/fpms_video
    if int(str(current_time).split('.')[1]) == 0:
        current_time = current_time+0.00000001 # TECHNIQUE DE ROUBLARD
    time_video = np.concatenate((time_video, np.array([current_time])))

print('Video data converted')

# ---------------------------------------------------------------------------------------
# GRAPH
# make the subplots 
fig = make_subplots(rows=4, cols=2, specs=[[{"rowspan": 4}, {}], [None, {}], [None, {}], [None, {}]], shared_xaxes=True, vertical_spacing=0.05) 

# Add the first frame
# trace of index 0, used as support for the video
fig.add_trace(go.Scatter(), row=1, col=1) #trace of index 0 used as support for the video
# trace of index 1, pemt
fig.add_trace(go.Scatter(name='Current', x=time_pemt_bdtb, y=pemt, showlegend=False, line=dict(color='#B51F1F')), row=1, col=2) 
# trace of index 2, bdtd
fig.add_trace(go.Scatter(name='dI/dt', x=time_pemt_bdtb, y=bdtb, showlegend=False, line=dict(color='#007480')), row=2, col=2)
# trace of index 3, ef
fig.add_trace(go.Scatter(name='Ez', x=time_ef_xr, y=ef, showlegend=False, line=dict(color='#FFB100')), row=3, col=2)
# trace of index 4, xr
fig.add_trace(go.Scatter(name='X-ray',x=time_ef_xr, y=xr, showlegend=False, line=dict(color='#69B58A')), row=4, col=2)
# add the first image
fig.add_layout_image(row=1, col=1, source=images_pil[0], xref="x domain", yref="y domain", x=1, y=1, xanchor="right", yanchor="top", sizex=1, sizey=1)
# add the rectangles that shows the time window of the first frame (using Hyp 1)
t0 = time_video[0]-wl/2 # lower time
t1 = time_video[0]+wl/2 # upper time
fig.update_layout(
shapes=[
   dict(type="rect", xref="x2", yref="y2", x0=t0, y0=pemtl, x1=t1, y1=pemtu, fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
   dict(type="rect", xref="x2", yref="y3", x0=t0, y0=bdtbl, x1=t1, y1=bdtbu, fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
   dict(type="rect", xref="x2", yref="y4", x0=t0, y0=efl  , x1=t1, y1=efu  , fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
   dict(type="rect", xref="x2", yref="y5", x0=t0, y0=xrl  , x1=t1, y1=xru  , fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0)
])

# add all the frames
fig.frames = [go.Frame( # name according its time
                        name=time_video[k],
                        # no update needed on the scatter plots 
                        data=[  go.Scatter(visible=True),
                                go.Scatter(visible=True),
                                go.Scatter(visible=True),
                                go.Scatter(visible=True),
                                go.Scatter(visible=True)],
                        # update of the image and the rectangles
                        layout = go.Layout( images=[go.layout.Image(source=images_pil[k], xref="x domain", yref="y domain", x=1, y=1, xanchor="right",
                                                                    yanchor="top", sizex=1, sizey=1)],
                                            shapes=[dict(type="rect", xref="x2", yref="y2", x0=time_video[k]-wl/2, x1=time_video[k]+wl/2,
                                                        y0=pemtl, y1=pemtu, fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
                                                    dict(type="rect", xref="x2", yref="y3", x0=time_video[k]-wl/2, x1=time_video[k]+wl/2,
                                                        y0=bdtbl, y1=bdtbu, fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
                                                    dict(type="rect", xref="x2", yref="y4", x0=time_video[k]-wl/2, x1=time_video[k]+wl/2,
                                                        y0=efl, y1=efu  , fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
                                                    dict(type="rect", xref="x2", yref="y5", x0=time_video[k]-wl/2, x1=time_video[k]+wl/2,
                                                        y0=xrl, y1=xru  , fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0)]),  
                        # consider each trace           
                        traces=[0,1,2,3,4]) for k in range(len(images_pil))]  # define the nbr of frames according the video frames

# make the sliders and buttons
# make the buttons play/pause
fig['layout']['updatemenus'] = [{'buttons': [  {'args': [None, {'frame': {'duration': duration, 'redraw': False},
                                                'fromcurrent': True, 'transition': {'duration': duration, 'easing': 'quadratic-in-out'}}],
                                                'label': 'Play', 'method': 'animate'},
                                               {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                                'transition': {'duration': 0}}], 'label': 'Pause', 'method': 'animate'}],
                                'direction': 'left', 'pad': {'r': 10, 't': 87}, 'showactive': False, 'type': 'buttons', 'x': 0.1,
                                'xanchor': 'right', 'y': 0.1, 'yanchor': 'top'}]
# slider parameters
sliders_dict = {'active': 0, 'yanchor': 'top', 'xanchor': 'left', 'len': 0.9, 'x': 0.1, 'y': 0, 'steps': [], 'minorticklen': minorticklen,
                'currentvalue': {'suffix': ' [ms]:', 'visible': True, 'xanchor': 'right'},
                'transition': {'duration': duration, 'easing': 'cubic-in-out'}, 'pad': {'b': 10, 't': 50}}
# define the slider for each step
for time in list(time_video) : 
    # slider step
    slider_step = {'args': [[time], {'frame': {'duration': 300, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 300}}],
                   'label': "%.4f" % (time), 'method': 'animate'}
    # add to the list of steps
    sliders_dict['steps'].append(slider_step)
# add the slider steps
fig['layout']['sliders'] = [sliders_dict]

# template 
fig.update_layout(template="plotly_white") 
# make the support plot of the video invisible
fig.update_layout(xaxis=dict(showgrid=False, zeroline=False, visible=False),
                  yaxis=dict(showgrid=False, zeroline=False, visible=False))
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
# label the subplots
fig.update_layout(yaxis2 = {'title': r"$Current \textrm{ } [kA]$", "tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"}, 
                  yaxis3 = {'title': r'$dI/dt \textrm{ } [kA/ms]$', "tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"}, 
                  yaxis4 = {'title': r'$E_z \textrm{ } [V/m]$', "tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"},      
                  yaxis5 = {'title': r'$X-ray \textrm{ } [keV]$', "tickformat": '{0}.0f'.format(ticklen), "hoverformat": "f"},
                  xaxis5 = {'title': r'$time \textrm{ }  [ms]$', 'anchor': 'free', 'position':0.0})
# x-axis range
fig.update_layout(xaxis2 = {"range": [t1-(t2-t1)*0.04, t2+(t2-t1)*0.04]})
# Some parameters of the figure
fig.layout.update(title=title, height=650, width=1100, showlegend=False, 
                  font_family="Monaco", font_size=11, title_font_size=16, hoverlabel_font_family="Monaco", hoverlabel_font_size=11)


print("Graph computed")
# ---------------------------------------------------------------------------------------
# EXPORT, SHOW THE GRAPH
if html_graph:
    fig.write_html(path_save, include_mathjax = 'cdn')
    print('Graph saved')

if show_graph:
    fig.show()
    print('Graph shown')
    
print("End\n")

