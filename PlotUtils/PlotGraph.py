import ROOT as r
from ROOT import TGraph, TGraphErrors

import matplotlib.pyplot as plt

from matplotlib import rc 

'''
Class that takes in a ROOT histogram and plots it nicely using matplotlib
'''
class PlotGraph
    def __init__(gr,simulation=False,preliminary=True,confidencebands=True,**kwargs):
        '''
        Initiate class
        '''
        # Set font.
        rc('font',**{'family':'serif','serif':['Roman']}) 
        rc('text', usetex=True)

        # Set axis.
        self.xtitle = kwargs['xtitle'] if ( 'xtitle' in kwargs) else gr.GetXaxis().GetTitle()
        self.ytitle = kwargs['ytitle'] if ( 'ytitle' in kwargs) else gr.GetYaxis().GetTitle()
        self.units  = kwargs['units']  if ( 'units' in kwargs ) else ''

        # Miscellanious.
        self.simulation = simulation
        self.preliminary = preliminary
        self.confidencebands = confidencebands