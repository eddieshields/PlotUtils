import ROOT as r
from ROOT import TH1, TH2, TH3, TF1, RooDataHist, RooRealVar, RooArgList, RooArgSet

import matplotlib.pyplot as plt

from matplotlib import rc 

from PlotUtils.PlotHistogram import PlotHistogram
from PlotUtils.ROOTutils import *

class PlotRooHistogram(PlotHistogram):
    def __init__(self,hist,var,func=False,weightedhist=False,simulation=False,preliminary=True,pull=True,**kwargs):
        self.var = var
        if ( weightedhist ):
            th1hist = weightedhist
        else:
            th1hist = self.th1fromroodatahist( hist )

        if ( func ):
            tfunc = self.tf1fromroopdf( hist , func )

        # Components.
        if ( 'components' in kwargs ):
            tmp = {}
            for comp, settings in kwargs['components'].items():
                tmp.update( {self.tf1fromroopdfcomponents( hist, func , comp ) : settings} )
            kwargs['components'] = tmp

        super(PlotRooHistogram, self).__init__(th1hist,func=tfunc,simulation=simulation,preliminary=preliminary,pull=pull,**kwargs)

    def th1fromroodatahist(self,roohist):
        '''
        Convert a RooDataHist into a TH1.
        '''
        hist = roohist.createHistogram( 'hist_conv' , self.var )
        # Dirty hack to get weights.
        for i in range(1,hist.GetNbinsX()):
            roohist.get(i)
            hist.SetBinContent(i,roohist.weight())

        return hist

    def tf1fromroopdf(self,roohist,roofunc):
        '''
        Convert a RooAbsPdf into a TF1.
        '''
        # Dirty trick to get correct normalization.
        # Plot data and model on frame then get the model back from the frame.
        frame = self.var.frame()
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
        frame = self.var.frame()
        roohist.plotOn( frame )
        roofunc.plotOn( frame, r.RooFit.Name("pdf_object") )
        roofunc.plotOn( frame, r.RooFit.Components(comp),r.RooFit.Name("pdf_component") )
        func = frame.findObject( "pdf_component" )
        return func

