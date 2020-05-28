from future.moves import tkinter as tk
import random
import warnings
import itertools
import numpy as np
#import matplotlib.pyplot as plt

#plt.style.use('fivethirtyeight')
import pandas as pd
import numpy as numpy

total_df = pd.read_excel("Sudan20132019.xlsx")

dates = total_df['Dates']
totalHits=total_df['Total']

for k in range(4):
    dates = dates.append(dates)
    totalHits = totalHits.append(totalHits)



class getKeywordHit(object):
    def getDate(self): return total_df['Dates']
    def getHit(self): return -total_df['Total']*100

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.i = 0;
        tk.Frame.__init__(self, *args, **kwargs)
        self.count = getKeywordHit()
        self.canvas = tk.Canvas(self, background="black")
        self.canvas.pack(side="top", fill="both", expand=True)

        # create lines for velocity and torque
        self.hit_line = self.canvas.create_line(0,0,0,0, fill="red")
        #self.time_line = self.canvas.create_line(0,0,0,0, fill="blue")

        # start the update process
        self.update_plot()
  #      self.static_plot()

     # def static_plot(self):
     #    v = self.count.getHit()
     #    v.plot(figsize=(15, 6))
     #    plt.show()

    def update_plot(self):
        v = self.count.getHit()
        #t = self.count.getDate()
        self.add_point(self.hit_line, v[self.i])
        #self.add_point(self.time_line, t)
        self.canvas.xview_moveto(1.0)
        self.canvas.yview_moveto(0)
        self.i = self.i+1
        print(self.i)
        print( v[self.i])
        self.after(200, self.update_plot)

    def add_point(self, line, y):
        coords = self.canvas.coords(line)
        x = coords[-2] + 1
        coords.append(x)
        coords.append(y)
        coords = coords[-200:]  # keep # of points to a manageable size #was -200
        self.canvas.coords(line, *coords)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()