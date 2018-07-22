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
    def __init__(self, x, y, ylim = (0.0,0.0)):
        self.plotx = []
        self.ploty = []
        self.plotylim = []
        self.addplot(x, y, ylim)

    def addplot(self, x, y, ylim):
        self.plotx.append(x)
        self.ploty.append(y)
        if ylim == (0.0, 0.0):
            mid = (np.max(y) + np.min(y))/2.0
            rg = (np.max(y) - np.min(y))
            rd = rg / (0.9 * 2.0)
            ylim = (mid-rd,mid+rd)
        self.plotylim.append(ylim)
        
    def display(self):
        nplots = len(self.plotx)
        self.fig, self.ax = plt.subplots(nplots, 1)
        for i in range(nplots):
            plt.subplot((nplots) * 100 + 10 + (i+1), ylim = self.plotylim[i] )
            plt.plot(self.plotx[i], self.ploty[i])

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

      cgo = graph_obj(cno.gett()[:pts], cno.geta()[:pts], ( -10.0, 10.0))
      cgo.display()
      ego = graph_obj(eno.gett()[:pts], eno.geta()[:pts], ( -10.0, 10.0))
      ego.display()
      ggo = graph_obj(gno.gett()[:pts], gno.geta()[:pts], ( -10.0, 10.0))
      ggo.display()
      chgo = graph_obj(co.gett()[:pts], co.geta()[:pts], ( -20.0, 20.0))

      go = graph_obj(cno.gett()[:pts], cno.geta()[:pts], ( -10.0, 10.0))
      go.addplot(eno.gett()[:pts], eno.geta()[:pts], ( -10.0, 10.0))
      go.addplot(gno.gett()[:pts], gno.geta()[:pts], ( -10.0, 10.0))
      go.display()
      x2 = co.gett()
      y2 = co.geta()

      chgo.display()
      
      fobj = fft_obj(x2, y2)

      xf = fobj.getxf()
      yf = fobj.getyf()

      fchobj = graph_obj(xf[:1000], yf[:1000] ) #, (np.min(yf[:1000]) / 0.9, np.max(yf[:1000])/ 0.9) )
      
      fchobj.display()

if __name__ == '__main__':
      main()
