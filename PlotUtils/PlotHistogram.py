import ROOT as r
from ROOT import TH1, TH2, TH3

import matplotlib.pyplot as plt

from PlotUtils.ROOTutils import *
from PlotUtils.PlotAbs import PlotAbs

'''
Class for plotting ROOT TH1 objects.

Generally MatPlotLib produces nicer plots than root so this class
converts ROOT objects like TH1 and TF1 and plots them in MatPlotLib.
'''
class PlotHistogram(PlotAbs):
    def __init__(self,hist,func=False,pull=False,simulation=False,preliminary=True,legend=True,**kwargs):
        # Initiate base class.
        super(PlotHistogram, self).__init__(pull=pull)

        self.hist = hist
        self.ff = func
        self.xmin = hist.GetXaxis().GetXmin()
        self.xmax = hist.GetXaxis().GetXmax()
        self.ymin = 0.1
        self.ymax = 1.1 * hist.GetMaximum()
        self.bin_width = hist.GetBinWidth(1)

        # Set axis.
        self.xtitle = kwargs['xtitle'] if ( kwargs.__contains__('xtitle') ) else hist.GetXaxis().GetTitle()
        self.ytitle = kwargs['ytitle'] if ( kwargs.__contains__('ytitle') ) else hist.GetYaxis().GetTitle()
        self.units  = kwargs['units']  if ( kwargs.__contains__('units')  ) else ''

        #if ( self.units ):
        #    if ( self.units not in self.xtitle ):
        #        self.xtitle += ' [$%s$]'%self.units

        self.components = kwargs['components'] if ( kwargs.__contains__('components') ) else {}

        # Miscellanious.
        self.legend = legend
        self.simulation = simulation
        self.preliminary = preliminary

    def plot(self,output=0):
        # Plot components.
        if ( self.components ): self.addcomponents( self.components )

        # Plot function.
        if ( self.ff ):
            x_vals, pdf_vals = listfromtf1( self.ff )
            self.add_plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')

        # Plot points.
        x, y, x_err, yerr = listfromhist( self.hist )
        self.add_errorbar(x,y,x_err,yerr,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')

        # Add legend.
        if ( self.legend ): self.add_legend(loc='upper right',fontsize=20,ncol=1,frameon=False)

        # Add label.
        self.add_LHCbLabel(simulation=self.simulation,preliminary=self.preliminary)

        # Add pull.
        if ( self.pull ):
            x, pull_vals = listforpull( self.hist, self.ff )
            self.add_pull(x,pull_vals)

        return self.set_plot(output)

        
    def addcomponents(self,components):
        '''
        Plots components
        '''
        for comp, settings in components.items():
            x, y = listfromtf1( comp )
            if ( settings.__contains__('fill') ):
                fill = settings.pop('fill')
                if ( fill == True ):
                    self.add_fill(x,y,**settings)
                else:
                    self.add_plot(x,y,**settings)
            else:
                self.add_fill(x,y,**settings)

        return



#'''
#Class that takes in a ROOT histogram and plots it nicely using matplotlib
#'''
#class PlotHistogram:
#    def __init__(self,hist,func=False,simulation=False,preliminary=True,pulls=True,**kwargs):
#        '''
#        Initiate class
#        '''
#        # Set font.
#        rc('font',**{'family':'serif','serif':['Roman']}) 
#        rc('text', usetex=True)
#
#        self.hist = hist
#        self.ff = func
#        self.xmin = hist.GetXaxis().GetXmin()
#        self.xmax = hist.GetXaxis().GetXmax()
#        self.ymin = hist.GetMinimum()
#        self.ymax = hist.GetMaximum()
#        self.bin_width = hist.GetBinWidth(1)
#        # Set axis.
#        self.xtitle = kwargs['xtitle'] if ( 'xtitle' in kwargs) else hist.GetXaxis().GetTitle()
#        self.ytitle = kwargs['ytitle'] if ( 'ytitle' in kwargs) else hist.GetYaxis().GetTitle()
#        self.units  = kwargs['units']  if ( 'units' in kwargs ) else ''
#
#        self.components = kwargs['components'] if ( 'components' in kwargs ) else {}
#
#        # Miscellanious.
#        self.simulation = simulation
#        self.preliminary = preliminary
#        self.pulls = pulls
#
#    def plot(self,output=0):
#        '''
#        Plot everything.
#        '''
#        fig = plt.figure(figsize=(12,8))
#        if ( self.pulls ):
#            spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[1, 3], hspace=None)
#            ax_pull = fig.add_subplot(spec[0])
#            ax = fig.add_subplot(spec[1])
#        else:
#            ax = fig.add_subplot(111)
#          
#        # Plot components.
#        if ( self.components ):
#            ax = self.addcomponents( ax, self.components )
#
#        # Plot function.
#        if ( self.ff ):
#            x_vals, pdf_vals = listfromtf1( self.ff )
#            ax.plot(x_vals,pdf_vals,color='blue',linewidth=2.5,label='Fit')
#
#        # Plot data.
#        x, y, x_err, yerr = listfromhist( self.hist )
#        ax.errorbar(x,y,xerr=x_err,yerr=yerr,ls=None,color='k',fmt='o',markersize=3.5,mfc='black',alpha=0.8,label='Data')
#
#        # Legend.
#        ax.legend(loc='upper right',fontsize=20,ncol=1,frameon=False)
#
#        # Axis.
#        plt.ylabel("Candidates / (%.1f MeV/$c^2$)" % self.bin_width,fontsize=35,horizontalalignment='right', y=1.0)
#        plt.xlabel("$%s$ [%s]" % (self.xtitle,self.units),fontsize=35,horizontalalignment='right', x=1.0)
#        ax.tick_params(axis='both', which='major', labelsize=30)
#        ax.set_xlim(self.xmin,self.xmax)
#        ax.set_ylim(0.1,self.ymax*1.05)
#
#        #Add LHCb logo
#        plt.text(0.7*self.xmax,0.9*self.ymax,"\\textbf{LHCb}",fontsize=35)
#        if ( self.simulation ): plt.text(0.7*self.xmax,0.85*self.ymax,"\\textit{simulation}",fontsize=25)
#        else:
#            if ( self.preliminary ): plt.text(0.7*self.xmax,0.85*self.ymax,"\\textit{preliminary}",fontsize=25)
#
#        # Hide x labels and tick labels for all but bottom plot.
#        if ( self.pull ):
#            ax_pull = self.pull(ax_pull)
#            ax_pull.label_outer()
#        
#        margins = {  #     vvv margin in inches
#        		"left"   : 0.17,
#        		"bottom" : 0.15,
#        		"right"  : 0.99,
#        		"top"    : 0.98
#        		}
#
#        fig.subplots_adjust(wspace=None, hspace=None)
#        fig.subplots_adjust(**margins)
#
#        if ( output ):
#            fig.savefig( output )
#            print('Saved figure to '+output)
#        return fig
#
#
#    def pull(self,ax):
#        '''
#        Plot pull
#        '''
#        # Cant calculate pull without function.
#        if not ( self.ff ): return False
#        # Calculate pulls.
#        x, pull_vals = listforpull( self.hist, self.ff )
#        ax.bar(x,pull_vals,color='lightskyblue',width=self.bin_width)
#        ax.axhline(y=0,color='lightskyblue',linestyle='--')
#        ax.axhline(y=3,color='red',linestyle='--')
#        ax.axhline(y=-3,color='red',linestyle='--')
#
#        ax.set_ylabel("Residual ($\sigma$)",fontsize=25)
#        ax.tick_params(axis='both', which='major', labelsize=20)
#        ax.set_xlim(self.xmin,self.xmax)
#        ax.set_ylim(-5,5)
#
#        return ax
#
#    def addcomponents(self,ax,components):
#        '''
#        Plots components
#        '''
#        for comp, settings in components.items():
#            x_vals, pdf_vals = listfromtf1( comp )
#            if ( 'fill' in settings ):
#                if ( settings['fill'] == True ):
#                    ax.fill_between(x_vals,pdf_vals,color=settings['colour'],label=settings['name'])
#                else:
#                    ax.plot(x_vals,pdf_vals,color=settings['colour'],linewidth=2.5,linestyle=settings['fill'],label=settings['name'])
#            else:
#                ax.fill_between(x_vals,pdf_vals,color=settings['colour'],label=settings['name'])
#
#        return ax
