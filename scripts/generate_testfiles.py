import os
from ROOT import TH1D, TFile
from ROOT import RooRealVar, RooArgList, RooGaussian, RooAddPdf


def generate_testfiles():
    h = TH1D("gaussian_hist", "Gaussian histgram", 100, -3, 3)
    h.FillRandom("gaus", 1000)

    file = TFile(os.path.dirname(__file__) + (
                 '/../testfiles/root_testfiles.root'),
                 'RECREATE')
    file.cd()
    h.Write()

    x = RooRealVar("D0_M", "m(K_{S}^{0}K^{+}K^{-})", 1860, 1800, 1930,
                   "\\mathrm{MeV}/c^{2}")
    x.setBins(130)
    m1 = RooRealVar("m1", "mean 1", 1864, 1860, 1870)
    s1 = RooRealVar("s1", "sigma 1", 2, 0, 5)
    g1 = RooGaussian("g1", "Gaussian 1", x, m1, s1)

    m2 = RooRealVar("m2", "mean 2", 1864, 1860, 1870)
    s2 = RooRealVar("s2", "sigma 2", 4, 0, 5)
    g2 = RooGaussian("g2", "Gaussian 2", x, m2, s2)

    f1 = RooRealVar("f", "f", 0.5, 0, 1)
    m = RooAddPdf("model", "model", RooArgList(g1, g2), f1)

    data = m.generate(x, 1e6)

    x.Write("x")
    m.Write("model")
    data.Write("data")

    file.Close()

    return


if __name__ == '__main__':
    generate_testfiles()
