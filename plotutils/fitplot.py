from ROOT import RooRealVar, RooAbsData, RooAbsPdf, RooDataHist

from plotutils.plot import Plot
from plotutils._roofit_utils import (_convert_rooabsdata_to_th1,
                                     _convert_rooabspdf_to_tf1)
from plotutils._root_utils import calculate_pull


class FitPlot(Plot):
    def __init__(self, x, data, pdf, xsize=12, ysize=8, pull=True):
        super(FitPlot, self).__init__(xsize=xsize, ysize=ysize, pull=pull)

        assert(isinstance(x, RooRealVar))
        assert(isinstance(data, RooAbsData))
        assert(isinstance(pdf, RooAbsPdf))

        self.x = x
        self.data = data
        self.pdf = pdf

        # Set plot
        self.set_plot(x)

        # Add data to plot.
        self.errorbar(x, data, fmt='o', markersize=3.5, color='black')

        # Set y to 0 here. Trick to get normalisation of RooPdf to work.
        self.set_ymin(0.1)

        # Add pdf to plot
        self.plot(x, pdf, data, color='blue', linewidth=2.5)

        # Add pull plot.
        if pull:
            self._calculate_pull()

        # Set title.
        self._set_titles(x, data)

    def _set_titles(self, x, data):
        """
        Use the information already contained in the RooFit objects
        to set the titles of the plots.
        """
        # x-title
        xtitle = x.GetTitle()
        if x.getUnit():
            xtitle += '\\ [%s]' % x.getUnit()
        self.set_xtitle(xtitle)

        # y-title
        if isinstance(data, RooDataHist):
            ytitle = ('\\mathrm{Candidates}\\ /\\ ' + str(
                      (x.getMax() - x.getMin()) / data.numEntries()))
        else:
            ytitle = ('\\mathrm{Candidates}\\ /\\ ' + str(
                      x.getBinning().averageBinWidth()))

        if x.getUnit():
            ytitle += '\\ %s' % x.getUnit()
        self.set_ytitle(ytitle)

        return

    def set_plot(self, x):
        """
        Set properties of the plot
        specific to fit plot.
        """
        self.set_xlim(x.getMin(), x.getMax())

        return 0

    def _calculate_pull(self):
        hist = _convert_rooabsdata_to_th1(self.x, self.data)
        ff = _convert_rooabspdf_to_tf1(self.x, self.pdf, self.data)
        x, y = calculate_pull(hist, ff)
        self.pullplot(x, y)

        return

    def save(self, name):
        # re-plot signal on top of everything.
        self.errorbar(self.x, self.data,
                      fmt='o', markersize=3.5, color='black',
                      label='Data')
        self.plot(self.x, self.pdf, self.data,
                  color='blue', linewidth=2.5,
                  label='Fit')

        # Call base save method.
        super(FitPlot, self).save(name)
