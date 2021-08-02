from ROOT import TH1, TF1

from plotutils.plot import Plot


class PullPlot(Plot):
    def __init__(self, hist, pdf=None, color='blue', title=None,
                 xsize=12, ysize=8, pull=False):
        super(PullPlot, self).__init__(xsize=xsize, ysize=ysize, pull=pull)

        assert(isinstance(hist, TH1))
        self.hist = hist
        self.hist.Scale(1 / self.hist.Integral())
        self.step(self.hist, color='black')

        self.color = color

        self.ff = TF1('ff', 'gaus(0)',
                      self.hist.GetXaxis().GetXmin(),
                      self.hist.GetXaxis().GetXmax())  # Fit function
        self.res = self.hist.Fit(self.ff, 'NSQ')
        self.nf = TF1('nf', 'gaus(0)', -3, 3)  # Normalisation function

        self.confidenceband(self.ff, 0.95, color=self.color, alpha=0.1)
        self.confidenceband(self.ff, 0.68, color=self.color, alpha=0.2)
        self.step(self.hist, color='black')
        self.plot(self.ff, color=self.color)

        self._add_info()
        self._set_title(title)
        self.set_ymin(0)
        self.set_xlim(self.hist.GetXaxis().GetXmin(),
                      self.hist.GetXaxis().GetXmax())

        return

    def _add_normalisation(self):
        self.nf.SetParameters(1, 0, 1)
        self.nf.SetNormalized(True)
        self.plot(self.nf, color=self.color, linestyle='--')

    def _add_info(self):
        mu = ('$\\mu = %.2f \\pm %.2f' % (self.res.Parameter(1),
                                          self.res.ParError(1)) + ' \\%$')
        indent = ' ' if self.res.Parameter(1) < 0. else ''
        sig = ('$\\sigma = ' + indent + (
               '%.2f \\pm %.2f' % (self.res.Parameter(2),
                                   self.res.ParError(2))) + ' \\%$')
        self.add_text(mu, 0.63, 0.92, fontsize=30)
        self.add_text(sig, 0.63, 0.85, fontsize=30)

        self.ax.set_yticks([])
        return

    def _set_title(self, title: str):
        t = ('\\left( v^{\\mathrm{meas.}} - v^{\\mathrm{true}} \\right)'
             '/\\sigma_{v}')
        if title:
            self.set_xtitle(t.replace('v', title))
        else:
            self.set_xtitle(t.replace('v', self.hist.GetTitle()))

        return
