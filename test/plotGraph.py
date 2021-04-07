import ROOT as r
from ROOT import TGraphErrors, TF1

from array import *
from PlotUtils.PlotGraph import PlotGraph
from PlotUtils.ROOTutils import listfromtf1

def main():
    x, y, ex, ey = array('d'), array('d'), array('d'), array('d')
    for i in range(0,10):
        x.append( i + 0.5 )
        y.append( i**2 )
        ex.append( 0.5 )
        ey.append( i )

    gr = r.TGraphErrors(len(x),x,y,ex,ey)
    ff = TF1("ff","pol2",0,10)
    ff.SetParameter(2,1)
    gr.Fit('ff','S')
    
    gp = PlotGraph(gr,func=ff,xtitle='x',ytitle='y',confidencebands=True)
    gp.add_LHCbLabel(0.01,0.9,'Preliminary')
    gp.plot('figs/example_graph.pdf')



#-------------------------
if __name__ == '__main__':
    main()