import matplotlib.pyplot as plt
import matplotlib


class PlotStyle:
    def __init__(self):
        self.signal_color = 'black'

        # Line Styles
        self.lsBlack = dict(color='black', lw=1)
        self.lsBlack_dotted = dict(color='black', lw=1, linestyle=':')
        self.lsBlack_dashed = dict(color='black', lw=1, linestyle='--')
        self.lsGray = dict(color=(0.5, 0.5, 0.5), lw=1)
        self.lsCalls = dict(color='black', lw=0.5)  # Figure 1

        self.lsTuningHM_Fit = dict(color='r', linestyle='-', lw=1)

        # Scatter Styles
        self.scTuningCurve_20 = dict(marker='s', linestyle='', color='k', lw=1)
        self.scTuningCurve_85 = dict(marker='o', linestyle='', color=(0.5, 0.5, 0.5), lw=1)

        # Text Styles
        self.txt = dict(color='black', fontsize=8)
        self.txtHeader = dict(color='black', fontsize=10)
        self.txtWhite = dict(color='white', fontsize=8)
        self.txtRed = dict(color='red', fontsize=8)
        self.txtAnnotation = dict(color='black', fontsize=6)
        self.barAnnotation = dict(linewidth=1, edgecolor='black', facecolor='black')

        # Histogram
        self.histogram_style = dict(edgecolor='black', facecolor='gray', histtype='bar')
        self.text_inset = dict(fontsize=8, color='black')

        # Error Bar Plots
        self.markers = ['o', 's', 'v', '>', 'd']
        self.lsErrorBar_sig = dict(color='k', linestyle='-', markerfacecolor='black', markeredgecolor='black', markeredgewidth=0.5, markersize=4)
        self.lsErrorBar_ns = dict(color='k', linestyle='-', markerfacecolor='white', markeredgecolor='black', markeredgewidth=0.5, markersize=4)

        # Color maps and color bars
        self.cmapSpectrogram = 'jet'
        self.cmap = 'jet'
        self.cmap_gray = 'gray'
        self.cb_text_size = 8

        # Scale Bars
        self.txtScalebar = dict(size=6)
        self.boxScalebar = dict(color='black', lw=3)

        # Separation Lines
        self.sep_line = dict(color='r', linestyle='-',  lw=1.0)

        # Moth vs. Bats Labels
        self.mb_label_text = dict(fontsize=8, color='r')
        self.mb_label_box = dict(facecolor='k', alpha=0.5, edgecolor='red')

        # Sub Fig Cap Text Size
        self.sub_fig_cap_text_size = 12
        self.sub_fig_text_color = 'black'
        self.sub_fig_cap_upper_case = True
        self.subfig_caps_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

        # MATPLOTLIB global settings:
        # Font:
        # matplotlib.rc('font',**{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
        # matplotlib.rcParams['font.sans-serif'] = 'Helvetica'
        matplotlib.rcParams['font.sans-serif'] = 'Arial'
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.size'] = 6

        # Ticks:
        matplotlib.rcParams['xtick.major.pad'] = '2'
        matplotlib.rcParams['ytick.major.pad'] = '2'
        matplotlib.rcParams['ytick.major.size'] = 3
        matplotlib.rcParams['xtick.major.size'] = 3

        # Title Size:
        matplotlib.rcParams['axes.titlesize'] = 8

        # Axes Label Size:
        matplotlib.rcParams['axes.labelsize'] = 6

        # Axes Line Width:
        matplotlib.rcParams['axes.linewidth'] = 1

        # Tick Label Size:
        matplotlib.rcParams['xtick.labelsize'] = 6
        matplotlib.rcParams['ytick.labelsize'] = 6

        # Line Width:
        matplotlib.rcParams['lines.linewidth'] = 1
        matplotlib.rcParams['lines.color'] = 'k'

        # Marker Size:
        matplotlib.rcParams['lines.markersize'] = 2

        # Error Bars:
        matplotlib.rcParams['errorbar.capsize'] = 0

        # Legend Font Size:
        matplotlib.rcParams['legend.fontsize'] = 6

        # Set pcolor shading
        matplotlib.rcParams['pcolor.shading'] = 'auto'
