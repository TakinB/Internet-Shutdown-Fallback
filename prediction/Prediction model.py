import datetime as dt
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import random
from matplotlib import rc, font_manager
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.image as mpimg
from PIL import Image, ImageTk
import time

import matplotlib.pyplot as plt

###############################################################################
# Parameters and global variables

# Parameters
update_interval = 200 # Time (ms) between polling/animation updates
max_elements = 1440     # Maximum number of elements to store in plot lists

# Declare global variables
root = None
dfont = None
frame = None
canvas = None
ax1 = None
temp_plot_visible = None


# Global variable to remember various states
fullscreen = False
temp_plot_visible = True
light_plot_visible = False


total_df = pd.read_excel("Sudan201320192.xlsx")

dates = total_df['Dates']
totalHits = total_df['Total']

push_button_img = mpimg.imread('push_a_button.png')
send_website_img = mpimg.imread('sending_website.png')
triggering_img = mpimg.imread('triggering_info_stream.png')
high_risk_img = mpimg.imread('high_risk_warning.png')

# NOT USED YET
class getKeywrodHit(object):
    def getDate(self): return total_df['Dates']
    def getHit(self): return total_df['Total']

###############################################################################
# Functions

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

# Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 40)))
    dfont.configure(size=new_size)

# Toggle plot
def toggle_total():

    global canvas
    global ax1
    global temp_plot_visible

    # Toggle plot and axis ticks/label
    temp_plot_visible = not temp_plot_visible
    ax1.collections[0].set_visible(temp_plot_visible)
    ax1.get_yaxis().set_visible(temp_plot_visible)
    canvas.draw()

# Toggle Specific Key Word Hit plot
def toggle_Keyword():

    global canvas
    global ax2
    global ax3
    global light_plot_visible

    # Toggle plot and axis ticks/label
    light_plot_visible = not light_plot_visible
    ax2.get_lines()[0].set_visible(light_plot_visible)
    ax2.get_yaxis().set_visible(light_plot_visible)
    canvas.draw()



def popupmsg(warningImage, m=0):
    popup = tk.Toplevel()
    popup.wm_title("Action")
    image = Image.open(warningImage[m]) # was previously push_a_button
    print(warningImage[m])
    image = image.resize((250, 150))
    photo = ImageTk.PhotoImage(image)
    label = ttk.Label(popup, image=photo, font=("DIN Alternate", 12))
    label.image = photo  # keep a reference!
    label.pack()

    if m < 3:
        m = m+1
        B1 = ttk.Button(popup, text="Next", command = lambda: popupmsg(warningImage, m)) # was previously popup.destroy

    B1.pack()



# This function is called periodically from FuncAnimation
def animate(i, ax1, xs, temps, probPercentage):
    # Update our labels
    probPercentage.set(round(totalHits[i]*100))
    politicalClimate.set(round(totalHits[i]*10))
    InfrastructureScore.set(3)
    PsychometricScore.set(8)
    InfoControl.set(9)

    #lux.set(new_lux)

    # Append timestamp to x-axis list
    timestamp = dates[i]  # mdates.date2num(dates[i])
    xs.append(timestamp)

    # Append sensor data to lists for plotting
    temps.append(totalHits[i])
   # lights.append(new_lux)

    #i = i + 1
   # print(totalHits[i])

    # Limit lists to a set number of elements
    xs = xs[-max_elements:]
    temps = temps[-max_elements:]
    #lights = lights[-max_elements:]

    # Clear, format, and plot light values first (behind)
    Greencolor = '#84cd2e'
    blackColor = '#212121'
    ax1.clear()
    ax1.set_ylabel('Probability', color=Greencolor, fontname="DIN Alternate")
    ax1.tick_params(axis='y', labelcolor=Greencolor)
    ax1.tick_params(axis='x', labelcolor=Greencolor)

    font_path = '~/Library/Fonts/MODES___.TTF'
    font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    ticks_font = font_manager.FontProperties(family='DIN Alternate', style='normal', size=12, weight='normal', stretch='normal')

    for label in ax1.get_xticklabels():
        label.set_fontproperties(ticks_font)

    for label in ax1.get_yticklabels():
        label.set_fontproperties(ticks_font)

    ax1.fill_between(xs, temps, 0, linewidth=2, color=Greencolor, alpha=0.3)
    ax1.set_facecolor(blackColor)




    # # Clear, format, and plot temperature values (in front)
    ax2.clear()
    ax3.clear()

    ax2.get_yaxis().set_visible(light_plot_visible)
    ax3.get_yaxis().set_visible(light_plot_visible)

    if i > 2:
        ax2.axvline(pd.Timestamp(dates[i-2]), color='#ff6666')

    # push_button_img = mpimg.imread('push_a_button.png')
    # send_website_img = mpimg.imread('sending_website.png')
    # triggering_img = mpimg.imread('triggering_info_stream.png')
    # high_risk_img = mpimg.imread('high_risk_warning.png')

    imageName = ["high_risk_warning.png", "triggering_info_stream.png", "push_a_button.png", "sending_website.png", "sending_website.png" ]

    if ( round(totalHits[i] * 100 )) > 80.0 :
        ax2.axvspan(pd.Timestamp(dates[i-2]), pd.Timestamp(dates[i+3]), fill='True', color='#ff6666', facecolor='blue', alpha=0.2)
        #print(pd.Timestamp(dates[i]))
        if (totalHits[i] == 0.8095238095238095):
            popupmsg(imageName, 0)

    # Format timestamps to be more readable
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    fig.autofmt_xdate()

    # Make sure plots stay visible or invisible as desired
    ax1.collections[0].set_visible(temp_plot_visible)
    #ax2.get_lines()[0].set_visible(light_plot_visible)

# Dummy function prevents segfault
def _destroy(event):
    pass

###############################################################################
# Main script
blackColor = '#212121'
Greencolor = '#84cd2e'
# Create the main window
root = tk.Tk()
root.title("Internet Shutdown Probability in Sudan")

# Create the main container
frame = tk.Frame(root)
frame.configure(bg=blackColor)

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Create figure for plotting
fig = figure.Figure(figsize=(9, 5))
fig.set_facecolor(blackColor)
fig.subplots_adjust(left=0.1, right=0.8)
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()

fig3 = figure.Figure(figsize=(9, 5))
ax3= fig3.add_subplot(1, 1, 1)
ax3 = ax1.twinx()

# Instantiate a new set of axes that shares the same x-axis
#ax2 = ax1.twinx()

# Empty x and y lists for storing data to plot later
xs = []
temps = []
lights = []

# Variables for holding temperature and light data
probPercentage = tk.DoubleVar()
politicalClimate = tk.DoubleVar()
InfrastructureScore = tk.DoubleVar()
PsychometricScore = tk.DoubleVar()
InfoControl = tk.DoubleVar()


lux = tk.DoubleVar()

# Create dynamic font for text
dfont = tkFont.Font(family='DIN Alternate', size=12)

# Create a Tk Canvas widget out of our figure
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_plot = canvas.get_tk_widget()

# Create other supporting widgets
label_prob = tk.Label(frame, text='Probability:', font=dfont, bg=blackColor, fg = Greencolor )
label_prob_value = tk.Label(frame, textvariable=probPercentage, font=dfont, bg=blackColor, fg = Greencolor )
label_percent = tk.Label(frame, text="%", font=dfont, bg=blackColor , fg = Greencolor )

label_psycho = tk.Label(frame, text='Political climate score:', font=dfont, bg=blackColor, fg = Greencolor )
label_psycho_value = tk.Label(frame, textvariable=politicalClimate, font=dfont, bg=blackColor, fg = Greencolor )

label_tech_complexity = tk.Label(frame, text='InfrastructureScore:', font=dfont, bg=blackColor, fg = Greencolor )
label_tech_complexity_value = tk.Label(frame, textvariable=InfrastructureScore, font=dfont, bg=blackColor, fg = Greencolor )

label_psyco_complexity = tk.Label(frame, text='Psychometric score:', font=dfont, bg=blackColor, fg = Greencolor )
label_psyco_complexity_value = tk.Label(frame, textvariable=PsychometricScore, font=dfont, bg=blackColor, fg = Greencolor )

label_information_control = tk.Label(frame, text='Info control score:', font=dfont, bg=blackColor, fg = Greencolor )
label_information_control_value = tk.Label(frame, textvariable=InfoControl, font=dfont, bg=blackColor, fg = Greencolor )

# button_temp = tk.Button(    frame,
#                             text="Toggle Total Hit",
#                             font=dfont,
#                             command=toggle_total)
# button_light = tk.Button(   frame,
#                         text="Toggle keyword",
#                         font=dfont,
#                         command=toggle_Keyword)
# button_quit = tk.Button(    frame,
#                         text="Quit",
#                         font=dfont,
#                         command=root.destroy)

# Lay out widgets in a grid in the frame
canvas_plot.grid(   row=0,
                    column=0,
                    rowspan=5,
                    columnspan=4,
                    sticky=tk.W+tk.E+tk.N+tk.S)

label_prob.grid(row=0, rowspan=2, column=3, columnspan=2)
label_prob_value.grid(row=0,rowspan=2, column=4, sticky=tk.E)
label_percent.grid(row=0, rowspan=2,column=5, sticky=tk.W)

label_psycho.grid(row=1, rowspan=1, column=3, columnspan=2)
label_psycho_value.grid(row=1, rowspan=1, column=4, sticky=tk.E)

label_tech_complexity.grid(row=1, rowspan=2, column=3, columnspan=2)
label_tech_complexity_value.grid(row=1, rowspan=2, column=4, sticky=tk.E)

label_psyco_complexity.grid(row=1, rowspan=3, column=3, columnspan=2)
label_psyco_complexity_value.grid(row=1, rowspan=3, column=4, sticky=tk.E)

label_information_control.grid(row=1, rowspan=4, column=3, columnspan=2)
label_information_control_value.grid(row=1, rowspan=4, column=4, sticky=tk.E)

#label_unitlux.grid(row=2, column=5, sticky=tk.W)
# button_temp.grid(row=5, column=0, columnspan=2)
# button_light.grid(row=5, column=2, columnspan=2)
# button_quit.grid(row=5, column=4, columnspan=2)

# Add a standard 5 pixel padding to all widgets
for w in frame.winfo_children():
    w.grid(padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 5):
    frame.rowconfigure(i, weight=1)
for i in range(0, 5):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Call empty _destroy function on exit to prevent segmentation fault
root.bind("<Destroy>", _destroy)

# Initialize our sensors
#tmp102.init()
#apds9301.init()

# Call animate() function periodically
fargs = ( ax1, xs, temps, probPercentage)
ani = animation.FuncAnimation(fig,
                                animate,
                                fargs=fargs,
                                interval=update_interval)

# Start in fullscreen mode and run
#toggle_fullscreen()
root.mainloop()
