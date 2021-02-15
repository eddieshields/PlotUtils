import ROOT as r
from ROOT import TH1D

from PlotUtils.PlotHistogram import PlotHistogram


def main():
    hist = TH1D("hist","hist",100,0,100)
    for i in range(1,hist.GetNbinsX()+1):
        hist.SetBinContent(i,i**2)

    fig = PlotHistogram(hist,xtitle='x',ytitle='y').plot()
    fig.savefig('figs/example_histogram.pdf')
    import pdb; pdb.set_trace()

    

#-------------------------
if __name__ == '__main__':
    main()