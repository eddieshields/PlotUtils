import ROOT as r
from ROOT import TH1, TH2, TH3, TF1, RooDataHist, RooRealVar, RooArgList, RooArgSet

import matplotlib.pyplot as plt

from matplotlib import rc 

from PlotUtils.PlotHistogram import PlotHistogram
from PlotUtils.ROOTutils import *

class PlotRooHistogram(PlotHistogram):
    '''
    Wrapper class that allows RooFit Objects to be plotted with MatPltiLib.
    '''
    
    def __init__(self,x,data,model,pull=True,legend=False,label='Preliminary',log_scale=False,name='canv',xname='',yname=''):
        self.x = x
        self.data = data
        self.model = model

        hist = self.th1fromroodatahist( self.x , self.data )

        if ( self.model ): tfunc = self.tf1fromroopdf( self.data , self.model ) 

        super(PlotRooHistogram, self).__init__(hist,func=tfunc,pull=pull,legend=legend,label=label,log_scale=log_scale,name=name,xname=xname,yname=yname)

        self.setTitle()

    def add_component(self,name,title='',style='l',**kwargs):
        '''
        Takes a component of a RooAbsPdf and adds to plot.
        '''
        func = self.tf1fromroopdfcomponents(self.data,self.model,name)
        x, y = listfromtf1( func )
        if ( style == 'l' ): self.add_plot(x,y,label=title,**kwargs)
        elif ( style == 'f' ): self.add_fill(x,y,label=title,**kwargs)

        return

    def th1fromroodatahist(self,x,roohist):
        '''
        Convert a RooDataHist into a TH1.
        '''
        # Convert RooDataSet to RooDataHist
        if ( isinstance(roohist,r.RooDataSet) ): roohist = roohist.binnedClone()
        hist = roohist.createHistogram( x.GetName() )

        return hist

    def tf1fromroopdf(self,roohist,roofunc):
        '''
        Convert a RooAbsPdf into a TF1.
        '''
        # Dirty trick to get correct normalization.
        # Plot data and model on frame then get the model back from the frame.
        frame = self.x.frame()
        roohist.plotOn( frame )
        roofunc.plotOn( frame, r.RooFit.Name("pdf_object") )
        func = frame.findObject( "pdf_object" )
        return func

    def tf1fromroopdfcomponents(self,roohist,roofunc,comp):
        '''
        Convert a RooAbsPdf into a TF1.
        '''
        # Dirty trick to get correct normalization.
        # Plot data and model on frame then get the model back from the frame.
        frame = self.x.frame()
        roohist.plotOn( frame )
        roofunc.plotOn( frame, r.RooFit.Name("pdf_object") )
        roofunc.plotOn( frame, r.RooFit.Components(comp),r.RooFit.Name("pdf_component") )
        func = frame.findObject( "pdf_component" )
        return func

    def setTitle(self):
        # x-title
        self.xtitle  = self.x.GetTitle()
        if ( self.x.getUnit() ): self.xtitle  += "\\ [%s]"%self.x.getUnit()

        # y-title
        if ( isinstance(self.data,r.RooDataHist) ): self.ytitle = "\\mathrm{Candidates}\\ /\\ "+str((self.x.getMax() - self.x.getMin())/self.data.numEntries())
        else: self.ytitle = "\\mathrm{Candidates}\\ /\\ "+str(self.x.getBinning().averageBinWidth())

        if ( self.x.getUnit() ): self.ytitle += "\\ %s"%self.x.getUnit()

        return

