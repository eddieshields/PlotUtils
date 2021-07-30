from ROOT import RooFit, RooRealVar, RooAbsData, RooAbsPdf
from ROOT import TH1, TF1


def _convert_roofit_object(x: RooRealVar, roofit_obj, *args, **kwargs):
    if isinstance(roofit_obj, RooAbsData):
        return _convert_rooabsdata_to_th1(x, roofit_obj)
    elif isinstance(roofit_obj, RooAbsPdf):
        if isinstance(args[0], RooAbsData):
            return _convert_rooabspdf_to_tf1(x, roofit_obj, *args, **kwargs)
        else:
            _convert_rooabspdf_to_tf1(x, roofit_obj)

    return


def _convert_rooabsdata_to_th1(x: RooRealVar, roofit_obj: RooAbsData) -> TH1:
    '''
    Convert a RooDataHist into a TH1.
    Parameters
    ----------
    x : RooRealVar
        ROOT RooRealVar observable
    roofit_obj : RooAbsData
        RooFit dataset

    Returns
    -------
    TH1
        ROOT histogram
    '''
    assert(isinstance(x, RooRealVar) and isinstance(roofit_obj, RooAbsData))

    return roofit_obj.createHistogram(x.GetName())


def _convert_rooabspdf_to_tf1(x: RooRealVar,
                              roofit_func: RooAbsPdf,
                              roofit_data: RooAbsData = None,
                              *args,
                              **kwargs) -> TF1:
    '''
    Convert a RooAbsPdf into a TF1.

    Parameters
    ----------
    x : RooRealVar
        RooFit RooRealVar observable
    roofit_func : RooAbsPdf
        RooFit pdf
    roofit_data : RooAbsData
        RooFit dataset

    Returns
    -------
    TF1
        ROOT TF1
    '''
    assert(isinstance(x, RooRealVar) and
           isinstance(roofit_func, RooAbsPdf) and
           isinstance(roofit_data, RooAbsData))
    # Dirty trick to get correct normalization.
    # Plot data and model on frame then get the model back from the frame.
    frame = x.frame()
    if roofit_data:
        roofit_data.plotOn(frame)
    roofit_func.plotOn(frame, RooFit.Name('tmp_pdf'))
    if 'component' in kwargs.keys():
        roofit_func.plotOn(frame, RooFit.Components(kwargs['component']),
                           RooFit.Name('tmp_pdf_component'))
        return frame.findObject('tmp_pdf_component')

    return frame.findObject('tmp_pdf')
