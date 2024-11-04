'''
 File name: third_graph.py
 Author: Florent Aviolat
 Date created: 08/03/2023
 Date last modified: 08/03/2023
 Version : V.1
 Description : graphic representation of lightning data : video, interferometer, pemt 
''';
# ---------------------------------------------------------------------------------------
# IMPORTS
# install mathjax in the used environment (used to display latex formula)

import numpy as np
import plotly.graph_objects as go
import cv2
from PIL import Image
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash.dependencies
import dash_player as player
import plotly.graph_objects as go

# ---------------------------------------------------------------------------------------
# USER INPUTS
# title of the figure
title = "Flash négatif ascendant du 16 aout 2021, UN5"

# documents paths
path_pemt_bdtb = 'assets/UN5_PEMt_Bdtb_data_raw.bin'
path_video = 'assets/blitz_video.avi'

# selected window for the graphs
t1 = 445 #ms
t2 = 2395 #ms
dt = t2-t1 #ms

# some parameters for the graph
# number of markers for the slider
n_markers = 7
# used for margin of the interferometer figure
marg  = 0.025 

# Print the parameters
print("\nGRAPH: INTERFEROMETER")
print("\n%s" % (title))
print("Selected time window (ms): %f - %f" % (t1,t2))
# ---------------------------------------------------------------------------------------
# DEVELOPMENT DUMMY DATA (TO REMOVE WHEN FINAL CODE WITH REAL DATA IMPLEMENTED)

time_duration = 700/1000 #ms
fpms_interferometer = 200*1000 #frame/ms
nb_data = int(time_duration*fpms_interferometer)

fpms_current = 50000 #frame/ms
fpms_video = 24 #frame/ms

# ---------------------------------------------------------------------------------------
# REMARKS

# close the figure in the terminal with ctrl-c when you are finished with it ! (else, if you re-run the code, it may not work)

# the window length displayed by the video is 1/(24 [frames/ms]), the frame is choosen as the closest to the interferometer data

# the ticks of the sliders represent times, however the slider 'tooltip' represents the frame of the interferometer

# when choosing higher time, please mind that the code is slower. To avoid crashing, wait until the figures are well implemented 
# before interacting with it

# on the graph, the rectangle represent the window of the video frame (centered on the capture time of the frame) and the black
# line is the time of the last printed interferometer data

# ---------------------------------------------------------------------------------------
# DATA

## interferometer
azimuth = np.arange(nb_data)
elevation = np.sin(azimuth*np.pi/np.max(azimuth))
time_interferometer = [100+i/fpms_interferometer for i in range(nb_data)]

# WITH REAL DATA: 
# import azimuth, elevation and time_interferometer from the interferometer
# use np.argmin(np.abs(time_interferometer-t1)) to find the tmin indice of the graph
# use np.argmin(np.abs(time_interferometer-t2)) to find the tmax indice of the graph
# then select the data of azimuth, elevation and time_interferometer between the indices min and max

# these times define the terminals of the graph
time_interferometer_min = np.min(time_interferometer)
time_interferometer_max = np.max(time_interferometer)

# get min/max of interferometer data for the graph limit
azl = np.min(azimuth)
azu = np.max(azimuth)
azdiff = azu-azl
ell = np.min(elevation)
elu = np.max(elevation)
eldiff = elu-ell

print('\nInterferometer data ready')

## current data (pemt)
with open(path_pemt_bdtb, 'rb') as f:
    loaded_data_pemt_bdtb = np.load(f)
time_pemt_bdtb = loaded_data_pemt_bdtb[0,:] 

# find the indices of interest for tmin and tmax
ind_tmin_pemt_bdtb = np.argmin(np.abs(time_pemt_bdtb-time_interferometer_min))
ind_tmax_pemt_bdtb = np.argmin(np.abs(time_pemt_bdtb-time_interferometer_max))

# select the needed data
time_current = time_pemt_bdtb[ind_tmin_pemt_bdtb:ind_tmax_pemt_bdtb+1]
current = loaded_data_pemt_bdtb[1,ind_tmin_pemt_bdtb:ind_tmax_pemt_bdtb+1]

# get min/max of the current data
curl = np.min(current)
curu = np.max(current)

# delete unnecessary heavy data
del loaded_data_pemt_bdtb
del time_pemt_bdtb

print('Current data ready')

## video
fpms_video = 24 #frame/ms
wl = 1/fpms_video #ms/frame
# import the video using cv2
vidcap = cv2.VideoCapture(path_video) 
images = []
while vidcap.isOpened():
    success, image = vidcap.read()
    if not success:
        break
    images.append(image)
vidcap.release()
# get the corresponding time
time_video = np.array([0+i/fpms_video for i in range(len(images))])
# find the indices of interest for tmin and tmax
ind_tmin_pemt_video = np.argmin(np.abs(time_video-time_interferometer_min))
ind_tmax_pemt_video = np.argmin(np.abs(time_video-time_interferometer_max))

# WITH REAL DATA
# the time of the video is a data imported with the video

# store all the needed PIL images in a list
images_pil = []
for img in images[ind_tmin_pemt_video:ind_tmax_pemt_video+1]:
    images_pil.append(Image.fromarray(img))
# update the time according the data in images_pil
time_video = time_video[ind_tmin_pemt_video:ind_tmax_pemt_video+1]

print('Video data ready')

# ---------------------------------------------------------------------------------------
# GRAPH
# first frame to display
# figure of the video
fig_video= go.Figure()
fig_video.add_trace(go.Scatter()) #trace used as support for the video
fig_video.add_layout_image(source=images_pil[0], xref="x domain", yref="y domain", x=1, y=1, xanchor="right", yanchor="top", sizex=1, sizey=1)
title_video  = 'Frame: ' + str(0) + ', captured at time ' + str(round(time_video[0],5)) + ' (ms)'
fig_video.update_layout(width=430, height=450, title=title_video, xaxis=dict(showticklabels=False), 
                        yaxis=dict(showticklabels=False), title_font_size=12, font_family="Monaco")
fig_video.layout.xaxis.fixedrange = True
fig_video.layout.yaxis.fixedrange = True
# figure interferometer
fig_interferometer = go.Figure()
fig_interferometer.add_trace(go.Scattergl(x=np.array(azimuth[0]), y=np.array(elevation[0]), customdata=np.array(time_interferometer[0]), mode="markers",
                         marker=dict(size=6, cmin=time_interferometer_min, cmax=time_interferometer_max, color=np.array(time_interferometer[0]), colorbar=dict(title="Time (ms)"), colorscale="Viridis"),
                         hovertemplate='azimuth:%{x} <br><b>elevation:%{y}</b><br>time: %{customdata}'))
fig_interferometer.update_layout(xaxis = {'title': "Azimuth (deg)", "range": [azl-marg*azdiff ,azu+marg*azdiff]}, template="plotly_white",
                                 yaxis = {'title': "Elevation (deg)", "range": [ell-marg*eldiff ,elu+marg*eldiff]},  height=450, width=450, showlegend=False,
                                 font_family="Monaco", font_size=12, title_font_size=12, hoverlabel_font_family="Monaco", hoverlabel_font_size=11)
# figure current
fig_current = go.Figure()
fig_current.add_trace(go.Scattergl(x=time_current, y=current, mode="lines",line=dict(color='#B51F1F')))
fig_current.update_layout(xaxis = {'title': "Time (ms)", "range": [time_interferometer_min ,time_interferometer_max]}, template="plotly_white",
                          yaxis = {'title': "Current (kA)"},  height=450, width=450, showlegend=False,
                          font_family="Monaco", font_size=12, title_font_size=12, hoverlabel_font_family="Monaco", hoverlabel_font_size=11)
tv_now = time_video[0] # time video at the beginning (captured time)
ti_now = time_interferometer[0] # time interferometer at the beginning
# add the rectangle and line on the figure of the current 
fig_current.update_layout( shapes=[
   dict(type="rect", x0=tv_now-wl/2, y0=curl, x1=tv_now+wl/2, y1=curu, fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
   dict(type="line", x0=ti_now, x1=ti_now, y0=curl, y1=curu, opacity=1, layer="above"),
   ])

# create the dash app
app = dash.Dash(__name__)

# marker for the slider
marks = {}
n = n_markers # number of markers for the slider
for i in range(n):
    marks[int(i*len(time_interferometer)/n)] = str(time_interferometer[int(i*len(time_interferometer)/n)])
# html layout   
app.layout = html.Div([
                  html.H1(title, style={'textAlign': 'left', 'font-family' : 'Monaco', 'font-size': 16}),
                  html.Div([
                        html.Div([
                              dcc.Graph(id='graph-image', figure=fig_video)
                                 ]),
                        html.Div([
                              dcc.Graph(id='graph-interferometer', figure=fig_interferometer)
                                 ]),
                        html.Div([
                              dcc.Graph(id='graph-current', figure=fig_current)
                                 ])
                           ], style={"display": "flex", "flexDirection": "row"}),
                  html.Div([
                        html.Div(id='slider-output-container', children="time: " + str(time_interferometer[0]) + " [ms]"),
                        dcc.Slider(id="slider", min=0, max=len(time_interferometer)-1, step=1, value=0, updatemode='drag',
                                   marks=marks, tooltip={"placement": "bottom", "always_visible": True})
                           ], style={"width": "90%", "display": "inline-block", 'font-family' : 'Monaco', 'font-size': 12})
                     ], style={'margin-left': '3vw', 'margin-top': '3vw'})
# callback function (called function when change the slider value)
@app.callback(
    Output('graph-image', 'figure'), # first : which id, second: which concerned parameter of this id thing
    Output('graph-interferometer', 'figure'),
    Output('graph-current', 'figure'),
    Output('slider-output-container', 'children'),
    Input('slider', 'value'),
    Input('graph-current', 'figure')
)
def update_graph(ind_interferometer, fig_current_):

    # update video figure
    # find the corresponding frame
    ind_video = np.argmin(np.abs(time_video-time_interferometer[ind_interferometer]))
    # do the graph
    fig_video_ = go.Figure()
    fig_video_.add_trace(go.Scatter()) #trace used as support for the video
    fig_video_.add_layout_image(source=images_pil[ind_video], xref="x domain", yref="y domain", x=1, y=1, xanchor="right", yanchor="top", sizex=1, sizey=1)
    title_video  = 'Frame: ' + str(ind_video) + ', captured at time ' + str(round(time_video[ind_video],5)) + ' (ms)'
    fig_video_.update_layout(width=430, height=450, title=title_video, xaxis=dict(showticklabels=False), 
                             yaxis=dict(showticklabels=False), title_font_size=12, font_family="Monaco")
    fig_video_.layout.xaxis.fixedrange = True
    fig_video_.layout.yaxis.fixedrange = True

    # update interferometer figure
    # build the figure with the data up to the corresponding time
    fig_interferometer_ = go.Figure()
    fig_interferometer_.add_trace(go.Scattergl(x=azimuth[:ind_interferometer+1], y=elevation[:ind_interferometer+1], customdata=time_interferometer[:ind_interferometer+1], mode="markers",
                            marker=dict(size=6, cmin=time_interferometer_min, cmax=time_interferometer_max, color=time_interferometer[:ind_interferometer+1], colorbar=dict(title="Time (ms)"), colorscale="Viridis"),
                            hovertemplate='azimuth:%{x} <br><b>elevation:%{y}</b><br>time: %{customdata}'))
    fig_interferometer_.update_layout(xaxis = {'title': "Azimuth (deg)", "range": [azl-marg*azdiff ,azu+marg*azdiff]}, template="plotly_white",
                                      yaxis = {'title': "Elevation (deg)", "range": [ell-marg*eldiff ,elu+marg*eldiff]},  height=450, width=450, showlegend=False,
                                      font_family="Monaco", font_size=12, title_font_size=12, hoverlabel_font_family="Monaco", hoverlabel_font_size=12)
    
    # update the current figure, i.e. the rectangle and the line representing the time
    tv_now = time_video[ind_video] # time video now (captured time)
    ti_now = time_interferometer[ind_interferometer] # time interferometer now
    fig_current_['layout']['shapes'] = (go.layout.Shape(type="rect", x0=tv_now-wl/2, y0=curl, x1=tv_now+wl/2, y1=curu, fillcolor="LightSalmon", opacity=0.5, layer="above",line_width=0),
                                        go.layout.Shape(type="line", x0=ti_now, x1=ti_now, y0=curl, y1=curu, opacity=1, layer="above"))
    
    return fig_video_, fig_interferometer_, fig_current_, "Time: " + str(ti_now) + " (ms)"

print('Graph ready')

# ---------------------------------------------------------------------------------------
# RUN THE APPLICATION

if __name__ == "__main__":
    #app.run(debug=True, use_reloader=False)  
    app.run()