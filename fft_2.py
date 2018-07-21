import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import csv

datapoint = 10000

class fft_obj():
    def __init__(self, x, y):# Number of samplepoints
        self.T = x[1] - x[0]
        self.npoints = len(x)

        ty = scipy.fftpack.fft(y)
        
        self.yf = 2.0/(self.npoints*self.npoints) * np.abs(ty[:self.npoints//2])
        self.xf = np.linspace(0.0, 1.0/(2.0*self.T), self.npoints/2)
        
    def getxf(self):
        return self.xf

    def getyf(self):
        return self.yf

class graph_obj():
    def __init__(self, x, y):
        self.x = []
        self.y = []
        self.x.append(x)
        self.y.append(y)
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.x[0], self.y[0])

    def add(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.ax.plot(self.x[-1], self.y[-1])

    def addplot(self, newplot)
        
    def display(self):
        plt.draw()
        plt.waitforbuttonpress(0) # this will wait for indefinite time
        plt.close(self.fig)

class sin_obj():
      def __init__(self, start, finish, npoints, amp):
            self.x = np.linspace(start, finish, npoints)
            self.y = np.sin(self.x)

      def getx(self):
            return self.x
      def getsin(self):
            return self.y

class note_obj():
      def __init__(self, freq, amp):
            self.freq = freq
            self.amp = amp
            self.t = np.linspace(0.0, 1.0, datapoint)
            self.x = 2.0 * np.pi * self.freq * self.t
            self.y = self.amp * np.sin(self.x)

      def gett(self):
            return self.t

      def geta(self):
            return self.y

      def getperiodpts(self):
            return int(datapoint / self.freq)
            

class chord_obj():
      def __init__(self):
            self.notes = []
            self.notes.append(note_obj(440.0, 0.0))
            
      def addNote(self, freq, amp):
            note = note_obj(freq, amp)

            self.notes.append(note)

      def gett(self):
            return self.notes[0].gett()

      def geta(self):
            a = self.notes[0].geta()

            for i in self.notes:
                  a = np.add(a, i.geta())
                  
            return a


def main():
# load data
      sin_datafilename = "./fftdata.csv"

      Cfreq = 261.6 # 2 / 261.6, which is the frequency of a C note.
      Efreq = 329.6
      Gfreq = 392.0

      co = chord_obj()
      co.addNote(Cfreq, 10.0)
      co.addNote(Efreq, 6.0)
      co.addNote(Gfreq, 4.0)

      cno = note_obj(Cfreq, 10)
      eno = note_obj(Efreq, 6)
      gno = note_obj(Gfreq, 4)
      pts = 2 * cno.getperiodpts()

      cgo = graph_obj(cno.gett()[:pts], cno.geta()[:pts])
      cgo.display()
      ego = graph_obj(eno.gett()[:pts], eno.geta()[:pts])
      ego.display()
      ggo = graph_obj(gno.gett()[:pts], gno.geta()[:pts])
      ggo.display()
      chgo = graph_obj(co.gett()[:pts], co.geta()[:pts])
      
      x2 = co.gett()
      y2 = co.geta()

      # ego.add(co.gett()[:pts], co.geta()[:pts])

      chgo.display()
      
      fobj = fft_obj(x2, y2)

      xf = fobj.getxf()
      yf = fobj.getyf()

      fchobj = graph_obj(xf[:1000], yf[:1000])
      
      fchobj.display()

if __name__ == '__main__':
      main()
