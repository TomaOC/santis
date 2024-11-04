'''
 File name: fourth_graph.py
 Author: Florent Aviolat, Toma OC
 Date created: 26/04/2023
 Date last modified: 13/06/2024
 Version : V.1.1
 Description : video representation of lightning data :
 video, ef, xr, pemb, bdtt (long + zoom graphs)
''';

# ----------------------------------------------------------------------------
# IMPORTS

import numpy as np
import cv2
from PIL import Image
import sys
import os

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyArrow

# monospace font in order to align the labels of the "long graph"
plt.rcParams["font.family"] = "monospace"

# if problem with latex formula displaying, try installing mathjax

os.chdir('../')

# ----------------------------------------------------------------------------
# USER INPUTS
# choose flash
flash = 'UP2' # 'UN4' #

# title of the figure
title = flash #"Flash négatif ascendant du 16 aout 2021, UN5"

# path of the saved figure
path_save = "%s/fourth_video_%s_filt_test.mp4" % (flash, flash)

# documents paths
path_ef_xr = '%s/%s_EF_XR_data_raw.bin' % (flash, flash)
path_pemb_bdtt = '%s/%s_pemb_bdtt_data_filt.bin' % (flash, flash) # raw or filt
path_video = '../hsc/kronberg/%s/2021-07-24_18.24.25.963149.avi'%flash # UP2
#path_video = '../hsc/kronberg/%s/2021-07-30_15.38.16.116663932.avi'%flash # UN4
# path of the document where store the images for the long graphs
path_long_figure = './long_figure/'

#if not os.path.exists(os.path.dirname(path_long_figure)):
#    os.makedirs(os.path.dirname(path_long_figure))

# mode # True: do only the long graphs (Cf. remarks), else do the video
do_long_graph = False # True #

# selected window for the graphs (to match length of video)
t1 = 930 # 575 # ms
t2 = 1080 # 1250 # ms
dt = t2-t1 #ms

# Some parameters for the graphs
# nb ticks on x axis
nb_x_ticks = 6
# nb ticks on y axis
nb_y_ticks = 6
# window zoom
wl_zoom = 2 #ms
# width of the timeline for the zoom graph (in fraction of the total width of the figure)
time_line_width_zoom = 0.003

# 1. offset pixel correction to make that the red line of the long graph is
#   better synchronized with the time axis.
#   if the timeline looks delayed regarding the time axis use a positive value.
#   try this correction first, this first correction should be enough
pixel_correction_1 = -1.7 #old one with ipynb: 1.25
# 2. offset pixel correction to make that the red line of the long graph is
#   better synchronized with the graph image.
#   if the timeline looks delayed regarding the long graph image use a
#   positive value
pixel_correction_2 = 0 #old one with ipynb: -4

# Some parameters for the saved video
# fps for the saved video
fps_video = 24 # 1/s

# show progress
show_progress = True

# Print the parameters
print("\nGRAPH: LONG VIDEO+GRAPH")
print("\n%s\n\nSaved to: %s" %(title, path_save))
print("Selected time window (ms): %f - %f" % (t1,t2))
if do_long_graph :
    print("Mode: compute the long graphs")
else :
    print("Mode: compute the video")
print("Show progress: %.0f" %(show_progress))

# ----------------------------------------------------------------------------
# DATA FOR DEVELOPMENT (TO REMOVE)
# UP2 (current_peak_time - current_peak_frame / fps)
t0_video = 931.7592 # ms, start time of the first frame of the video
# UN4 (current_peak_time - current_peak_frame / fps)
#t0_video = 579.5253 # ms, start time of the first frame of the video


nb_frames_converted = 16093 # to match length of time window

# ----------------------------------------------------------------------------
# REMARKS

# designation of the columns in these comments:
# 1st: video, 2nd: long graph, 3rd: zoom graph

# Recipe to make the long graphs :
# set do_long_graph to true, then go to "DO LONG GRAPH"
# run the graphs you want to update, set the size of the figure such that
# the proportion suits for the final figure, then select manually the graph
# only (remove the black axis, the light grey pixel can be kept) on the .png
# document
# ymin and ymax have to be the same when creating the long graphs and creating
# the video

# Time line on long graphs : it may have imprecision due to the imprecision of
# the method, change the parameters in USER INPUTS.
# the first correction should be enough. to check impact on the code, go to
# (ctrl-F: #100)

# The width of the timeline does not represent the window length of the frame
# of the video. Indeed, with 10ms zoom, this would be too thin.
# However if it is wanted change code at (ctrl-F: #100)

# The rounding is set to 2 decimals but can be changed in the code by looking
# at 'round()' functions and 'rounding' parameters of the functions
# make_yaxis, make_xaxis, make_xaxis_zoom

# Result a little more blurred if run with an '.ipynb' instead of a '.py'

# ----------------------------------------------------------------------------
# DATA

# numerical data

# electric filed  (ef) and x-ray (xr)
with open(path_ef_xr, 'rb') as f:
    loaded_data_ef_xr = np.load(f)

# current (pemb) and bdot (bdtt)
with open(path_pemb_bdtt, 'rb') as f:
    loaded_data_pemb_bdtt = np.load(f)

# time
time_ef_xr = loaded_data_ef_xr[0,:]
time_pemb_bdtt = loaded_data_pemb_bdtt[0,:] 

# find the indices of interest for t1 and t2
ind_t1_ef_xr = np.argmin(np.abs(time_ef_xr-t1))
ind_t2_ef_xr = np.argmin(np.abs(time_ef_xr-t2))
ind_t1_pemb_bdtt = np.argmin(np.abs(time_pemb_bdtt-t1))
ind_t2_pemb_bdtt = np.argmin(np.abs(time_pemb_bdtt-t2))

# get the data we want
# (! the time arrays are updated here according the time window)
time_ef_xr = time_ef_xr[ind_t1_ef_xr:ind_t2_ef_xr+1]
ef = loaded_data_ef_xr[1,ind_t1_ef_xr:ind_t2_ef_xr+1]
#xr = loaded_data_ef_xr[2,ind_t1_ef_xr:ind_t2_ef_xr+1]
time_pemb_bdtt = time_pemb_bdtt[ind_t1_pemb_bdtt:ind_t2_pemb_bdtt+1]
pemb = loaded_data_pemb_bdtt[1,ind_t1_pemb_bdtt:ind_t2_pemb_bdtt+1]
#bdtt = loaded_data_pemb_bdtt[2,ind_t1_pemb_bdtt:ind_t2_pemb_bdtt+1]

# get the limit values for the graph u:up, l:low
# used to establish the height of the time lines
efu = np.max(ef)
efl = np.min(ef)
print('EF signal range:', efl, '-', efu, 'V/m')
#xru = np.max(xr)
#xrl = np.min(xr)
pembu = np.max(pemb)
pembl = np.min(pemb)
print('I signal range:', pembl, '-', pembu, 'kA')
#bdttu = np.max(bdtt)
#bdttl = np.min(bdtt)

# deleted the unnecessary heavy data
del loaded_data_ef_xr
del loaded_data_pemb_bdtt

print("\nNumerical data ready")

# video data
# technical data for the video
# frame per ms
fpms_video = 24 #frame/ms
# window length, duration of one frame
wl = 1/fpms_video # ms/frame

# import the video using cv2
# TODO: WITH REAL DATA, use : 'while vidcap.isOpened():' instead of the 'for',
# in order to read all frames of the video
# TODO: WITH REAL DATA, time_video is an import. get the good video data
# according the time terminals
vidcap = cv2.VideoCapture(path_video)
# list to store each frames, each images of the video of the lightning
images = []
# store the capture time of each image in a corresponding array
# i.e. time_video[0] corresponds to the frame stored images[0],
# time_video[1] corresponds to the frame stored images[1]...
time_video = np.array([])
ctn = 0
for ctn in range(nb_frames_converted):
# TODO: while vidcap.isOpened():
    success, image = vidcap.read()
    current_time = t0_video+ctn*wl # TODO: WITH REAL DATA, remove this and remove ctn
    ctn = ctn+1
    if not success:
        break
    images.append(image)
    time_video = np.concatenate((time_video, np.array([current_time])))
vidcap.release()
print('Video data ready')

# ----------------------------------------------------------------------------
# DO LONG GRAPH
# cell to perform the long graphs, (cf. REMARKS)
# ymin and ymax denotes the terminals of the graphs (y-axis)
ymin_pemb = -13
ymax_pemb = 1
d_y_pemb = ymax_pemb-ymin_pemb
if do_long_graph :
    # pemb
    f = plt.figure()
    f.set_figwidth(9)
    f.set_figheight(4)

    plt.plot(time_pemb_bdtt, pemb, '-', color='#B51F1F')
    plt.xlim((t1,t2))
    plt.ylim((ymin_pemb,ymax_pemb))
    plt.savefig(path_long_figure+'pemb.png')
    print(f"Figure saved to {path_long_figure}")


#ymin_bdtt = -28 # -1.5
#ymax_bdtt = 28 # 1.5
#d_y_bdtt = ymax_bdtt-ymin_bdtt
#if do_long_graph :
    # bdtt
#    f = plt.figure()
#    f.set_figwidth(9)
#    f.set_figheight(4)
#
#    plt.plot(time_pemb_bdtt, bdtt, '-', color='#007480')
#    plt.xlim((t1,t2))
#    plt.ylim((ymin_bdtt,ymax_bdtt))
#    plt.savefig(path_long_figure+'bdtt.png')

ymin_ef = -1100
ymax_ef = 600
d_y_ef = ymax_ef-ymin_ef
if do_long_graph :
    # ef
    f = plt.figure()
    f.set_figwidth(9)
    f.set_figheight(4)

    plt.plot(time_ef_xr, ef, '-', color='#FFB100')
    plt.xlim((t1,t2))
    plt.ylim((ymin_ef, ymax_ef))
    plt.savefig(path_long_figure+'ef.png')
    print(f"Figure saved to {path_long_figure}")

#ymin_xr = -2550
#ymax_xr = 850
#d_y_xr = ymax_xr-ymin_xr
#if do_long_graph :
    # xr
#    f = plt.figure()
#    f.set_figwidth(9)
#    f.set_figheight(4)
#
#    plt.plot(time_ef_xr, xr, '-', color='#69B58A')
#    plt.xlim((t1,t2))
#    plt.ylim((ymin_xr, ymax_xr))
#    plt.savefig(path_long_figure+'xr.png')

# if compute the long graph(s) then exit
if do_long_graph :
    print("\nProgram end\n")
    exit()

# ----------------------------------------------------------------------------
# SOME FUNCTIONS USED TO THE GRAPHS 

# Function to return the next indice (appearing at or after k0)
# such that the corresponding value from array is the closest to target.
# This search starts from the indice k0
# max len limit of the array is taken into account in the code
# input : array : array into consideration
# input : k0 : indice from where we start the search
# input : target : value that we aim to approach the best (at or after k0)
# output : next indice closest to the target (at or after k0)
def return_nearest(array, k0, target):
    searching_procedure = True
    previous_diff = np.abs(array[int(k0)]-target)
    i = 1
    while searching_procedure and k0+i < len(array): 
        current_diff = np.abs(array[int(k0+i)]-target)
        if current_diff > previous_diff: #i.e. we stop the procedure when we see we are going to far from the target
            searching_procedure = False
        else :
            i = i+1
            previous_diff = current_diff
    return int(k0+i-1)

# create the x_axis of a long graph
# input : width : width of the figure (pixel)
# input : n_tick : number of ticks on the axis
# input : t1 : first time value 
# input : dt : time interval between t2 and t1
# input : rounding : to round the value
# output : list_tick : list of ticks
# output : list_label : list of labels of the ticks
def make_xaxis(width, n_tick, t1, dt, rounding=2):
    # the real values of the axis are in pixel and
    # we have to convert the ticks to time values
    n = n_tick-1
    list_tick = []
    list_label = []
    for i in range(n+1):
        list_tick.append(i*width/n+pixel_correction_2)
        list_label.append(round(t1+i*dt/n,rounding))
    return list_tick, list_label

# create the y_axis of a long graph
# input : height : height of the figure (pixel)
# input : n_tick : number of ticks on the axis
# input : ymax : max value of this graph (i.e. max tick shown) 
# input : d_y : ymax-ymin, where ymin is the min value of this graph
#               (i.e. min tick shown)
# input : format : format of the tick
# input : rounding : to round the value
# output : list_tick : list of ticks
# output : list_label : list of labels of the ticks
def make_yaxis(height, n_tick, ymax, d_y, format="%8.2f", rounding=2):
    # the real values of the axis are in pixel and
    # we have to convert the ticks to measure values (kA,...)
    n = n_tick-1
    list_tick = []
    list_label = []
    for i in range(n+1):
        list_tick.append(i*height/n)
        list_label.append(format %(round(ymax-i*d_y/n, rounding)))
    return list_tick, list_label

# create the y_axis of the zoom figures
# input : n_tick : number of ticks on the axis
# input : ymax : max value of this graph (i.e. max tick shown) 
# input : d_y : ymax-ymin, where ymin is the min value of this graph
#               (i.e. min tick shown)
# input : format : format of the tick
# input : rounding : to round the value
# output : list_tick : list of ticks
# output : list_label : list of labels of the ticks
def make_yaxis_zoom(n_tick, ymax, d_y, format="%8.2f", rounding=2):
    n = n_tick-1
    list_tick = []
    list_label = []
    for i in range(n+1):
        list_tick.append(ymax-(n-i)*d_y/n)
        list_label.append(format %(round(ymax-(n-i)*d_y/n, rounding)))
    return list_tick, list_label

# ----------------------------------------------------------------------------
# INITIALIZE THE GRAPH AND UPDATING FUNCTION FOR THE GRAPH

# initializing a figure
fig = plt.figure()
# title
fig.suptitle(title, x=0.025, horizontalalignment='left', fontsize=14)
# size of the figure
fig.set_size_inches(11.9, 7.65)
# grid of the figure, possible to change the width ratio between the columns
gs  = GridSpec(4, 3, width_ratios=[1,1,1])

# create the axes
ax1 = fig.add_subplot(gs[1:3, 0]) # video graph
ax2 = fig.add_subplot(gs[0:1, 1])   # pemb long graph
ax3 = fig.add_subplot(gs[0:1, 2])   # pemb zoom graph
#ax4 = fig.add_subplot(gs[1, 1])   # bdtt long graph
#ax5 = fig.add_subplot(gs[1, 2])   # bdtt zoom graph
ax6 = fig.add_subplot(gs[2:3, 1])   # ef long graph
ax7 = fig.add_subplot(gs[2:3, 2])   # ef zoom graph
#ax8 = fig.add_subplot(gs[3, 1])   # xr long graph
#ax9 = fig.add_subplot(gs[3, 2])   # xr zoom graph

# pemb long
# import the picture of the long graph
img_pemb = np.asarray(Image.open(path_long_figure+'pemb.png'))
# get the height and width of the image in pixel
# (nb. the x-y axis values of the ax2 graph represent the pixels of the image)
(height_pemb, width_pemb, _) = np.shape(img_pemb)
# plot
ax2.imshow(img_pemb)
# set the ylabel, yticks, xticks
ax2.set_ylabel(r"$current$" + " " + r"$[kA]$")
xtick_pemb, xvalue_pemb = make_xaxis(width_pemb, nb_x_ticks, t1, dt)
ax2.set_xticks(xtick_pemb, xvalue_pemb)
ytick_pemb, yvalue_pemb = make_yaxis(height_pemb, nb_y_ticks, ymax_pemb,
                                     d_y_pemb, "%6.1f")
ax2.set_yticks(ytick_pemb, yvalue_pemb)

# same idea for the other graphs
# bdtt long
#img_bdtt = np.asarray(Image.open(path_long_figure+'bdtt.png'))
#(height_bdtt, width_bdtt, _) = np.shape(img_bdtt)
#ax4.imshow(img_bdtt)
#ax4.set_ylabel(r"$dI/dt$" + " " + r"$[kA/\mu s]$")
#xtick_bdtt, xvalue_bdtt = make_xaxis(width_bdtt, nb_x_ticks, t1, dt)
#ax4.set_xticks(xtick_bdtt, xvalue_bdtt)
#ytick_bdtt, yvalue_bdtt = make_yaxis(height_bdtt, nb_y_ticks, ymax_bdtt,
#                                     d_y_bdtt, "%6.1f")
#ax4.set_yticks(ytick_bdtt, yvalue_bdtt)

# ef long
img_ef = np.asarray(Image.open(path_long_figure+'ef.png'))
(height_ef, width_ef, _) = np.shape(img_ef)
ax6.imshow(img_ef)
ax6.set_ylabel(r"$E_z$" + " " + r"$[V/m]$")
xtick_ef, xvalue_ef = make_xaxis(width_ef, nb_x_ticks, t1, dt)
ax6.set_xticks(xtick_ef, xvalue_ef)
ytick_ef, yvalue_ef = make_yaxis(height_ef, nb_y_ticks, ymax_ef,
                                 d_y_ef, "%6.0f")
ax6.set_yticks(ytick_ef, yvalue_ef)


# xr long
#img_xr = np.asarray(Image.open(path_long_figure+'xr.png'))
#(height_xr, width_xr, _) = np.shape(img_xr)
#ax8.imshow(img_xr)
#ax8.set_ylabel(r"$x-ray$" + " " + r"$[keV]$")
#xtick_xr, xvalue_xr = make_xaxis(width_xr, nb_x_ticks, t1, dt)
#ax8.set_xticks(xtick_xr, xvalue_xr)
#ytick_xr, yvalue_xr = make_yaxis(height_xr, nb_y_ticks, ymax_xr,
#                                 d_y_xr, "%6.0f")
#ax8.set_yticks(ytick_xr, yvalue_xr)

# compute the zoom ticks on y axis
ytick_pemb_z, yvalue_pemb_z = make_yaxis_zoom(nb_y_ticks, ymax_pemb, d_y_pemb)
#ytick_bdtt_z, yvalue_bdtt_z = make_yaxis_zoom(nb_y_ticks, ymax_bdtt, d_y_bdtt)
ytick_ef_z, yvalue_ef_z = make_yaxis_zoom(nb_y_ticks, ymax_ef, d_y_ef)
#ytick_xr_z, yvalue_xr_z = make_yaxis_zoom(nb_y_ticks, ymax_xr, d_y_xr)

# width of the timeline on the zoom graph
width_zoom = wl_zoom*time_line_width_zoom

# function that is called to update the graph according the given video frame
# input : frame : current frame of the video (0,1,...N-1)
# output : fig : figure updated
def do_graph(frame):
    # time calculation
    tc = time_video[frame] # time of the video (image capture)
    t1_zoom = tc-wl_zoom/2 # zoom terminal times
    t2_zoom = tc+wl_zoom/2
    # zoom
    # find the indices of interest of the time array for t1 and t2
    # for the zoom, by "return_nearest method"
    # initialization for the first frame
    # (creation of the global variable and initialize them)
    if frame == 0 :
        global ind_t1_ef_xr_z 
        global ind_t2_ef_xr_z 
        global ind_t1_pemb_bdtt_z 
        global ind_t2_pemb_bdtt_z 
        ind_t1_ef_xr_z = np.argmin(np.abs(time_ef_xr-t1_zoom)) # index of time_ef_xr for t1
        ind_t2_ef_xr_z = np.argmin(np.abs(time_ef_xr-t2_zoom)) # index of time_ef_xr for t2
        ind_t1_pemb_bdtt_z = np.argmin(np.abs(time_pemb_bdtt-t1_zoom)) # index of time_pemb_bdtt for t1
        ind_t2_pemb_bdtt_z = np.argmin(np.abs(time_pemb_bdtt-t2_zoom)) # index of time_pemb_bdtt for t2
    # after initialization use the "return_nearest method"
    if frame != 0:
        ind_t1_ef_xr_z = return_nearest(time_ef_xr, ind_t1_ef_xr_z, t1_zoom)
        ind_t2_ef_xr_z = return_nearest(time_ef_xr, ind_t2_ef_xr_z, t2_zoom)
        ind_t1_pemb_bdtt_z = return_nearest(time_pemb_bdtt,
                                            ind_t1_pemb_bdtt_z, t1_zoom)
        ind_t2_pemb_bdtt_z = return_nearest(time_pemb_bdtt,
                                            ind_t2_pemb_bdtt_z, t2_zoom)

    # compute the current time lines (CODE: #100) using patches
    # no subscript for the zoom graph and with "_2" for the long graph
    #tc_adj = 0.01
    #current_time_pemb = FancyArrowPatch((tc+tc_adj, ymin_pemb),
    #                                    (tc+tc_adj, ymax_pemb), zorder=2,
    #                                    alpha=0.5, color="LightSalmon")
    current_time_pemb = Rectangle((tc-width_zoom/2, ymin_pemb),
                                  width_zoom, ymax_pemb-ymin_pemb, zorder=2,
                                  alpha=0.5, color="LightSalmon")
    tc_adjusted_pemb = (width_pemb/(t2-t1)*(time_video[frame]-t1) +
                        pixel_correction_1+pixel_correction_2(
    # adjusted mean that : the x-axis of "pemb long" is in pixel
    # so we have to convert the tc time into its corresponding pixel value
    current_time_pemb_2 = FancyArrow(tc_adjusted_pemb, 0, 0, width_pemb,
                                     alpha=0.5, color="LightSalmon")

    # same idea for the other data
    #current_time_bdtt = FancyArrowPatch((tc+tc_adj, ymin_bdtt),
    #                                    (tc+tc_adj, ymax_bdtt), zorder=2,
    #                                    alpha=0.5, color="LightSalmon")
    #current_time_bdtt = Rectangle((tc-width_zoom/2, ymin_bdtt), width_zoom,
    #                              ymax_bdtt-ymin_bdtt, zorder=2,
    #                              alpha=0.5, color="LightSalmon")
    #tc_adjusted_bdtt = width_bdtt/(t2-t1)*(time_video[frame]-t1) +
    #                   pixel_correction_1+pixel_correction_2
    #current_time_bdtt_2 = FancyArrow(tc_adjusted_bdtt, 0, 0, width_bdtt,
    #                                 alpha=0.5, color="LightSalmon")

    current_time_ef = Rectangle((tc-width_zoom/2, ymin_ef),
                                width_zoom, (ymax_ef-ymin_ef), zorder=2,
                                alpha=0.5, color="LightSalmon")
    tc_adjusted_ef = width_ef/(t2-t1)*(time_video[frame]-t1) +
                     pixel_correction_1 + pixel_correction_2
    current_time_ef_2 = FancyArrow(tc_adjusted_ef, 0, 0, width_ef,
                                   alpha=0.5, color="LightSalmon")

    #current_time_xr = Rectangle((tc-width_zoom/2, ymin_xr),
    #                            width_zoom, ymax_xr-ymin_xr, zorder=2,
    #                            alpha=0.5, color="LightSalmon")
    #tc_adjusted_xr = width_xr/(t2-t1)*(time_video[frame]-t1)
    #                 + pixel_correction_1+pixel_correction_2
    #current_time_xr_2 = FancyArrow(tc_adjusted_xr, 0, 0, width_xr,
    #                               alpha=0.5, color="LightSalmon")

    # x ticks for the time of the xaxis of zoom graph
    xtick_zoom = [tc-wl_zoom/2, tc, tc+wl_zoom/2]
    # x labels for the time of the xaxis of zoom graph
    xlabel_zoom = ["%7.2f" % (round(tc-wl_zoom/2, 2)),
                   "%7.2f" % (round(tc, 2)),
                   "%7.2f" % (round(tc+wl_zoom/2, 2))]


    # update the figures i.e. update the image of video,
    # update the zoom figures and update the time line on the "long" figures
    # update the image of video graph
    ax1.clear() # clear the preceding image
    ax1.set_title("frame:" + str(frame)) # print the frame in the title
    ax1.imshow(images[frame]) # plot
    ax1.get_xaxis().set_visible(False) # to render the figure below invisible
    ax1.get_yaxis().set_visible(False)
    # update the time line of pemb long graph
    for p in ax2.patches:
        p.remove() # remove the existing patches (i.e. previous time-line)
    ax2.add_patch(current_time_pemb_2) # add the current time line patch
    # update the zoom of the pemb zoom graph
    ax3.clear() # clear the preceding figure
    ax3.plot(time_pemb_bdtt[ind_t1_pemb_bdtt_z:ind_t2_pemb_bdtt_z+1],
             pemb[ind_t1_pemb_bdtt_z:ind_t2_pemb_bdtt_z+1],
             '-', color='#B51F1F') #plot
    ax3.add_patch(current_time_pemb) #time line patch
    ax3.set_xticks(xtick_zoom, xlabel_zoom) # x tick setting
    ax3.set_yticks(ytick_pemb_z) # y tick setting
    ax3.set_xlim(t1_zoom, t2_zoom) # set xlim
    ax3.set_ylim(ymin_pemb,ymax_pemb) # set y lim

    # same idea for the other graphs
    #for p in ax4.patches:
    #    p.remove()
    #ax4.add_patch(current_time_bdtt_2)
    
    #ax5.clear()
    #ax5.plot(time_pemb_bdtt[ind_t1_pemb_bdtt_z:ind_t2_pemb_bdtt_z+1],
    #         bdtt[ind_t1_pemb_bdtt_z:ind_t2_pemb_bdtt_z+1],
    #         '-', color='#007480')
    #ax5.add_patch(current_time_bdtt)
    #ax5.set_xticks(xtick_zoom, xlabel_zoom)
    #ax5.set_yticks(ytick_bdtt_z)
    #ax5.set_xlim(t1_zoom, t2_zoom)
    #ax5.set_ylim(ymin_bdtt,ymax_bdtt)

    for p in ax6.patches:
        p.remove()
    ax6.add_patch(current_time_ef_2)

    ax7.clear()
    ax7.plot(time_ef_xr[ind_t1_ef_xr_z:ind_t2_ef_xr_z+1],
             ef[ind_t1_ef_xr_z:ind_t2_ef_xr_z+1], '-', color='#FFB100')
    ax7.add_patch(current_time_ef)
    ax7.set_xticks(xtick_zoom, xlabel_zoom) 
    ax7.set_yticks(ytick_ef_z)
    ax7.set_xlim(t1_zoom, t2_zoom)
    ax7.set_ylim(ymin_ef,ymax_ef)

    #for p in ax8.patches:
    #    p.remove()
    #ax8.add_patch(current_time_xr_2)

    #ax9.clear()
    #ax9.plot(time_ef_xr[ind_t1_ef_xr_z:ind_t2_ef_xr_z+1],
    #         xr[ind_t1_ef_xr_z:ind_t2_ef_xr_z+1], '-', color='#69B58A')
    #ax9.add_patch(current_time_xr)
    #ax9.set_xticks(xtick_zoom, xlabel_zoom)
    #ax9.set_yticks(ytick_xr_z)
    #ax9.set_xlim(t1_zoom, t2_zoom)
    #ax9.set_ylim(ymin_xr,ymax_xr)

    # set the time labels
    #ax8.set_xlabel(r"$time$" + " " + r"$[ms]$")
    #ax9.set_xlabel(r"$time$" + " " + r"$[ms]$")

    # adjust the figure at the first frame
    if frame==0:
        fig.tight_layout()

    # show the progress
    if show_progress:
        sys.stdout.write("\r%.0f" % (frame))
        sys.stdout.flush()

    return fig,

plt.close()

# ----------------------------------------------------------------------------
# COMPUTE THE VIDEO

# create the animation
# nb. there is as many frames in the saved video save as number of elements
# in the list images (or as in time_video)
anim = animation.FuncAnimation(fig, do_graph, frames=len(images),
                               interval=10, blit=True, cache_frame_data=False)

# saving to m4 using ffmpeg writer
writervideo = animation.FFMpegWriter(fps=fps_video)
if show_progress:
    print('\nFrame indice converted, max %.0f: ' % (len(images)-1))
anim.save(path_save, writer=writervideo)
plt.close()

print("\n\nProgram end\n")
