import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import gridspec
import mplhep as hep

from plotutils._root_utils import root_plotable, confidence_band


class Plot(object):
    matplotlib.rc_file(
        os.path.dirname(os.path.realpath(__file__)) + '/matplotlibrc_LHCb')
    rc('font', **{'family': 'serif', 'serif': ['Roman']})
    rc('text', usetex=True)

    def __init__(self, xsize=12, ysize=8, pull=False):

        # Create figure.
        setattr(self, 'fig', plt.figure(figsize=(xsize, ysize)))

        setattr(self, 'pull', pull)
        if pull:
            setattr(self, 'spec', gridspec.GridSpec(ncols=1,
                                                    nrows=2,
                                                    height_ratios=[1, 3],
                                                    hspace=None))
            self.ax = self.fig.add_subplot(self.spec[1])
            self.ax_pull = self.fig.add_subplot(self.spec[0])
            self.fig.subplots_adjust(wspace=0, hspace=0)
        else:
            setattr(self, 'ax', self.fig.add_subplot(111))

    def add(self, *args, **kwargs):
        try:
            style = kwargs['style']
        except:
            KeyError('Style not specified')

        # Remove style from arguments.
        kwargs.pop('style')
        if style == 'l':
            self.plot(*args, **kwargs)
        elif style == 'f':
            self.fill_between(*args, **kwargs)
        elif style == 'p':
            self.errorbar(*args, **kwargs)
        elif style == 'h':
            self.hist(*args, **kwargs)

        return

    def confidenceband(self, ff, ci, *args, **kwargs):
        points = confidence_band(ff, ci)
        self.ax.fill_between(**points, **kwargs)

        return

    def confidencebands(self, ff, *args, **kwargs):
        self.confidenceband(ff, 0.95, *args, color='yellow', **kwargs)
        self.confidenceband(ff, 0.68, *args, color='green', **kwargs)

        return

    def pullplot(self, x, y):
        """
        Plot pull

        Parameters
        ----------
        x, y : np.array, np.array
            Values of pull plot
        """
        self.ax_pull.fill_between(x, y, step='pre', color='lightskyblue')
        self.ax_pull.axhline(y=0, color='lightskyblue', linestyle='--')
        self.ax_pull.axhline(y=3, color='red', linestyle='--')
        self.ax_pull.axhline(y=-3, color='red', linestyle='--')

        self.ax_pull.set_ylabel('Residual ($\\sigma$)', fontsize=20)
        self.ax_pull.tick_params(axis='both', which='major', labelsize=20)
        self.ax_pull.set_xticks([])
        self.ax_pull.set_yticks((-3, 0, 3))
        self.ax_pull.set_ylim(-5, 5)
        self.ax_pull.label_outer()
        # Align y labels.
        self.fig.align_ylabels((self.ax, self.ax_pull))

        return

    def __getattribute__(self, value):
        try:
            attr = object.__getattribute__(self, value)
        except:
            attr = object.__getattribute__(self, 'ax').__getattribute__(value)
            if hasattr(attr, '__call__'):
                return root_plotable(attr)

        return attr

    def add_label(self, text='Preliminary', data=True, **kwargs):
        '''
        Add LHCb label.
        '''

        hep.lhcb.label(text, data=data, **kwargs)

        return

    def add_text(self, text, xpos, ypos, **kwargs):
        '''
        Add text to main figure.
        '''
        xmin = self.ax.get_xlim()[0]
        xmax = self.ax.get_xlim()[1]
        ymin = self.ax.get_ylim()[0]
        ymax = self.ax.get_ylim()[1]
        self.ax.text(xmin + (xpos * (xmax - xmin)),
                     ymin + (ypos * (ymax - ymin)), text, **kwargs)

        return

    def set_xtitle(self, title):
        '''
        Set the x-axis title.
        '''
        self.ax.set_xlabel('$%s$' % title,
                           fontsize=35, horizontalalignment='right', x=1.0)

        return

    def set_ytitle(self, title):
        '''
        Set the x-axis title.
        '''
        self.ax.set_ylabel('$%s$' % title, fontsize=35, x=1.0, loc='top')

        return

    def set_xmin(self, min):
        '''
        Set the minimum of the x-axis.
        '''
        self.ax.set_xlim(min, self.ax.get_xlim()[1])
        if self.pull:
            self.ax_pull.set_xlim(min, self.ax.get_xlim()[1])

        return

    def set_xmax(self, max):
        '''
        Set the minimum of the x-axis.
        '''
        self.ax.set_xlim(self.ax.get_xlim()[0], max)
        if self.pull:
            self.ax_pull.set_xlim(self.ax.get_xlim()[0], max)

        return

    def set_xlim(self, min, max):
        '''
        Set the minimum of the x-axis.
        '''
        self.ax.set_xlim(min, max)
        if self.pull:
            self.ax_pull.set_xlim(min, max)

        return

    def set_ymin(self, min):
        '''
        Set the minimum of the x-axis.
        '''
        self.ax.set_ylim(min, self.ax.get_ylim()[1])

        return

    def set_ymax(self, max):
        '''
        Set the minimum of the x-axis.
        '''
        self.ax.set_ylim(self.ax.get_ylim()[0], max)

        return

    def set_ylim(self, min, max):
        '''
        Set the minimum of the x-axis.
        '''
        self.ax.set_ylim(min, max)

        return

    def add_vline(self, x, **kwargs):
        '''
        Add a vertical line
        '''
        self.ax.axvline(x=x, **kwargs)

        return

    def add_hline(self, y, **kwargs):
        '''
        Add a horizontal line.
        '''
        self.ax.axhline(y=y, **kwargs)

        return

    def set_logy(self):
        self.ax.set_yscale('log')

    def save(self, name):
        '''
        Save the plot.
        '''
        self.fig.savefig(name)
        print('Saved figure to ' + name)

        return
