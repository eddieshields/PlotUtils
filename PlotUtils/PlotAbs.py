import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import gridspec

'''
Abstract class that provides some helpful functions for plotting with 
MatPlotLib.

It is the responsibility of the derived class to define the following:
  self.xmin,
  self.xmax,
  self.ymin,
  self.ymax,
  self.xtitle,
  self.ytitle
'''
class PlotAbs:
    def __init__(self,pull=False,**kwargs):
        '''
        Initiate class
        '''
        # Set font.
        rc('font',**{'family':'serif','serif':['Roman']}) 
        rc('text', usetex=True)

        # Create figure.
        self.fig = plt.figure(figsize=(12,8))

        self.pull = pull
        if ( pull ):
            self.spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[1, 3], hspace=None)
            self.ax_pull = self.fig.add_subplot(self.spec[0])
            self.ax = self.fig.add_subplot(self.spec[1])
        else:
            self.ax = self.fig.add_subplot(111)

        # Axis limits.
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0

        # Default titles.
        self.xtitle = kwargs['xtitle'] if ( kwargs.__contains__('xtitle') ) else ''
        self.ytitle = kwargs['ytitle'] if ( kwargs.__contains__('ytitle') ) else ''

        # Scale.
        self.logy = kwargs['log_scale'] if ( kwargs.__contains__('log_scale') ) else False

    def set_plot(self,output=0):
        '''
        Plot everything.
        '''
        # Axis.
        plt.xlabel('$%s$'%self.xtitle,fontsize=35,horizontalalignment='right', x=1.0)
        plt.ylabel('$%s$'%self.ytitle,fontsize=35,horizontalalignment='right', y=1.0)
        self.ax.tick_params(axis='both', which='major', labelsize=30)

        if ( self.xmax ): self.ax.set_xlim(self.xmin,self.xmax)
        if ( self.ymax ): self.ax.set_ylim(self.ymin,self.ymax)


        # Hide x labels and tick labels for all but bottom plot.
        if ( self.pull ): self.ax_pull.label_outer()
        
        margins = {  #     vvv margin in inches
        		"left"   : 0.17,
        		"bottom" : 0.15,
        		"right"  : 0.99,
        		"top"    : 0.98
        		}

        if ( self.logy ): self.ax.set_yscale('log')
        self.fig.subplots_adjust(hspace=0)
        self.fig.subplots_adjust(**margins)

        if ( output ):
            self.fig.savefig( output )
            print('Saved figure to '+output)
        return self.fig

    def add_LHCbLabel(self,simulation=False,preliminary=True,xpos=0.8,ypos=0.9,lhcbfontsize=35,labelfontsize=25):
        #Add LHCb logo
        self.ax.text(self.xmin+(xpos*(self.xmax-self.xmin)),self.ymin+(ypos*(self.ymax-self.ymin)),"\\textbf{LHCb}",fontsize=lhcbfontsize)
        if ( simulation ): self.ax.text(self.xmin+(xpos*(self.xmax-self.xmin)),self.ymin+((ypos-0.055)*(self.ymax-self.ymin)),"\\textit{simulation}",fontsize=labelfontsize)
        else:
            if ( preliminary ): self.ax.text(self.xmin+(xpos*(self.xmax-self.xmin)),self.ymin+((ypos-0.055)*(self.ymax-self.ymin)),"\\textit{preliminary}",fontsize=labelfontsize)

        return

    def add_text(self,text,xpos,ypos):
        '''
        Add text to main figure.
        '''
        self.ax.text(xpos,ypos,text,**kwargs)
        
        return

    def add_errorbar(self,x,y,x_err,y_err,**kwargs):
        '''
        Add errorbar to figure.
        '''
        self.ax.errorbar(x,y,xerr=x_err,yerr=y_err,**kwargs)

        return

    def add_plot(self,x,y,**kwargs):
        '''
        Add plot to figure.
        '''
        self.ax.plot(x,y,**kwargs)

        return

    def add_fill(self,x,y,**kwargs):
        '''
        Add fill plot to figure.
        '''
        self.ax.fill_between(x,y,**kwargs)

        return

    def add_legend(self,**kwargs):
        '''
        Add legend.
        Remeber to label all objects to be included in legend.
        '''
        self.ax.legend(**kwargs)

        return


    def add_pull(self,x,y):
        '''
        Plot pull
        '''
        binwidth = x[1] - x[0]
        self.ax_pull.bar(x,y,color='lightskyblue',width=binwidth)
        self.ax_pull.axhline(y=0,color='lightskyblue',linestyle='--')
        self.ax_pull.axhline(y=3,color='red',linestyle='--')
        self.ax_pull.axhline(y=-3,color='red',linestyle='--')

        self.ax_pull.set_ylabel("Residual ($\sigma$)",fontsize=20)
        self.ax_pull.tick_params(axis='both', which='major', labelsize=20)
        self.ax_pull.set_yticks((-3,0,3))
        if ( self.xmin and self.xmax ): self.ax_pull.set_xlim(self.xmin,self.xmax)
        self.ax_pull.set_ylim(-5,5)
        # Align y labels.
        self.fig.align_ylabels((self.ax,self.ax_pull))

        return
