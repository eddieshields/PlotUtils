import ROOT as r
from ROOT import TH1, TH2, TH3

import matplotlib.pyplot as plt

from matplotlib import rc 
#rc('font',**{'family':'serif','serif':['Roman']}) 
#rc('text', usetex=True)



'''
Class that takes in a ROOT histogram and plots it nicely using matplotlib
'''
class PlotHistogram:
    def __init__(hist,simulation=False,preliminary=True,pulls=True,**kwargs):
        '''
        Initiate class
        '''
        # Set font.
        rc('font',**{'family':'serif','serif':['Roman']}) 
        rc('text', usetex=True)

        # Set axis.
        self.xtitle = kwargs['xtitle'] if ( 'xtitle' in kwargs) else hist.GetXaxis().GetTitle()
        self.ytitle = kwargs['ytitle'] if ( 'ytitle' in kwargs) else hist.GetYaxis().GetTitle()
        self.units  = kwargs['units']  if ( 'units' in kwargs ) else ''

        # Miscellanious.
        self.simulation = simulation
        self.preliminary = preliminary
        self.pulls = pulls


    def listfromhist(hist):
        '''
        Take the values from the histogram and add them to a series 
        of arrays.
        '''
        x, y, x_err, y_err = [ ], [ ], [ ], [ ]
        for n in range(1,hist.GetNbinsX()+1):
            x.append(hist.GetXaxis().GetBinCenter(n))
            y.append(hist.GetBinContent(n))
            x_err.append(hist.GetXaxis().GetBinWidth(n)*0.5)
            y_err.append(hist.GetBinError(n))

        return x, y, x_err, y_err

    def plot():
        '''
        Plot everything.
        '''
        plt.errorbar(x_comb,y_comb,yerr=yerr_comb,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8)

        # Axis.
        plt.ylabel("Candidates / (%.1f MeV/$c^2$)" % bin_width,fontsize=35,horizontalalignment='right', y=1.0)
		plt.xlabel("$%s$ [%s]" % (self.xtitle,self.units),fontsize=35,horizontalalignment='right', x=1.0)
		ax.tick_params(axis='both', which='major', labelsize=30)
		plt.xlim(4901,5599)
		plt.ylim(0.1,c_max*1.05)

        #Add LHCb logo
        plt.text(5450,0.9*c_max,"\\textbf{LHCb}",fontsize=35)
        if ( self.simulation ): plt.text(5450,0.85*c_max,"\\textit{simulation}",fontsize=25)
        else:
            if ( self.preliminary ) plt.text(5450,0.85*c_max,"\\textit{preliminary}",fontsize=25)

    def pull():
        '''
        Plot pull
        '''
        plt.bar(x_comb,y_comb,color='lightskyblue',width=4.0)
		plt.axhline(y=0,color='lightskyblue',linestyle='--')
		plt.axhline(y=3,color='red',linestyle='--')
		plt.axhline(y=-3,color='red',linestyle='--')
		
		plt.ylabel("Residual ($\sigma$)",fontsize=25)

		ax.tick_params(axis='both', which='major', labelsize=20)
		plt.xlim(4901,5599)
		plt.ylim(-5,5)



