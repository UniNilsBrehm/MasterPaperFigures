#!/usr/bin/env python
"""
SCRIPT FOR FIGURE 5 in PAPER
Creates a figure with spike train matching matrices
and classification performance matrices,
all based on the Van Rossum Distance Metric.

Nils Brehm - 2021
"""

from IPython import embed
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, colors, colorbar, ticker
from IPython import embed
import plotting_functions as pf
from plotstyle import PlotStyle
from plotting_functions import cap_letter, pickle_stuff

if __name__ == '__main__':
    # Figure Size (cm)
    fig_width_cm = 14
    fig_height_cm = 20

    # ==================================================================================================================
    # Load data
    save_path = 'figs/'

    # Spike Train Matching
    data_dir = 'data/Classification/spike_train_matching'
    stm_moth_series = np.load(f'{data_dir}/2018-02-16-aa_VanRossum_matches_moth_series_selected.npy', allow_pickle=True).item()
    stm_moth_series_extended = np.load(f'{data_dir}/2018-02-16-aa_VanRossum_matches_moth_series_selected_extended.npy', allow_pickle=True).item()

    # Classification Performance
    data_dir = 'data/Classification/performance'
    performance_moth_series = np.load(f'{data_dir}/2018-02-16-aa_VanRossum_correct_moth_series_selected.npy', allow_pickle=True)
    performance_moth_series_extended = np.load(f'{data_dir}/2018-02-16-aa_VanRossum_correct_moth_series_selected_extended.npy', allow_pickle=True)
    performance_poission_data = np.load(f'{data_dir}/2018-02-16-aa_VanRossum_correct_poisson_real.npy', allow_pickle=True)

    # Moths VS Bats
    data_dir = 'data/Classification/MothsVSBats'
    mb_vr_series = np.load(f'{data_dir}/2018-02-16-aa_MvsB_VanRossum_series.npy', allow_pickle=True).item()
    mb_vr_series_extended = np.load(f'{data_dir}/2018-02-16-aa_MvsB_VanRossum_series_extended.npy', allow_pickle=True).item()

    # Tau Values
    taus = list(np.concatenate([np.arange(1, 21, 1), np.arange(30, 105, 5), np.arange(200, 1000, 55)]))
    taus.append(1000)
    # ==================================================================================================================
    # FIGURE
    # Import Plot Styles
    styles = PlotStyle()

    # Create Grid
    fig_width = float(fig_width_cm / 2.54)
    fig_height = float(fig_height_cm / 2.54)

    fig = plt.figure(figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.1, top=0.95, bottom=0.05, right=0.95, wspace=0, hspace=0)

    # Create a grid that has mm resolution (200 x 140 mm)
    grid = gridspec.GridSpec(nrows=int(fig_height_cm * 10), ncols=int(fig_width_cm * 10))
    ax = dict()

    # grid[Height, Width]
    ax['stm_1'] = plt.subplot(grid[0:25, 0:25])  # Spike Train Matching with tau: 1 ms
    ax['stm_1_e'] = plt.subplot(grid[0:25, 30:55])  # Spike Train Extended Matching with tau: 1 ms
    ax['stm_10'] = plt.subplot(grid[30:55, 0:25])
    ax['stm_10_e'] = plt.subplot(grid[30:55, 30:55])
    ax['stm_1000'] = plt.subplot(grid[60:85, 0:25])
    ax['stm_1000_e'] = plt.subplot(grid[60:85, 30:55])

    ax['performance_call_series'] = plt.subplot(grid[0:20, 90:130])  # Performance
    ax['performance_call_series_extended'] = plt.subplot(grid[33:53, 90:130])
    ax['performance_poisson'] = plt.subplot(grid[65:85, 90:130])

    ax['spike_train_cb'] = plt.subplot(grid[1:84, 58:60])
    ax['performance_cb'] = plt.subplot(grid[1:84, 132:134])

    # Moths vs. Bats
    ax['mb_performance_1'] = plt.subplot(grid[110:135, 0:25])
    ax['mb_performance_1_e'] = plt.subplot(grid[110:135, 30:55])
    ax['mb_performance_10'] = plt.subplot(grid[140:165, 0:25])
    ax['mb_performance_10_e'] = plt.subplot(grid[140:165, 30:55])
    ax['mb_performance_1000'] = plt.subplot(grid[170:195, 0:25])
    ax['mb_performance_1000_e'] = plt.subplot(grid[170:195, 30:55])

    ax['mb_d_prime'] = plt.subplot(grid[110:145, 90:130])
    ax['mb_d_prime_e'] = plt.subplot(grid[160:195, 90:130])

    ax['mb_performance_cb'] = plt.subplot(grid[109:194, 58:60])
    ax['mb_d_prime_cb'] = plt.subplot(grid[109:194, 132:134])

    # ==================================================================================================================
    # A) SPIKE TRAIN MATCHING MATRIX PLOTS
    y_ticks = np.arange(0, 16, 5)
    x_ticks = np.arange(0, 16, 5)
    ax['stm_1'].pcolormesh(stm_moth_series[1][20], cmap=styles.cmap, vmin=0, vmax=20, shading='flat', rasterized=True)
    ax['stm_1_e'].pcolormesh(stm_moth_series_extended[1][20], cmap=styles.cmap, vmin=0, vmax=20, shading='flat', rasterized=True)
    ax['stm_10'].pcolormesh(stm_moth_series[10][20], cmap=styles.cmap, vmin=0, vmax=20, shading='flat', rasterized=True)
    ax['stm_10_e'].pcolormesh(stm_moth_series_extended[10][20], cmap=styles.cmap, vmin=0, vmax=20, shading='flat', rasterized=True)
    ax['stm_1000'].pcolormesh(stm_moth_series[1000][20], cmap=styles.cmap, vmin=0, vmax=20, shading='flat', rasterized=True)
    ax['stm_1000_e'].pcolormesh(stm_moth_series_extended[1000][20], cmap=styles.cmap, vmin=0, vmax=20, shading='flat', rasterized=True)

    # Set X and Y Ticks
    tau_label_x = 0.35
    tau_label_y = 0.9
    tau_label_vals = [1, 1, 10, 10, 1000, 1000]
    i = 0
    for ax_name in ['stm_1', 'stm_1_e', 'stm_10', 'stm_10_e', 'stm_1000', 'stm_1000_e']:
        ax[ax_name].set_xticks(x_ticks)
        ax[ax_name].set_yticks(y_ticks)
        ax[ax_name].text(tau_label_x, tau_label_y, fr'$\tau$ {tau_label_vals[i]} ms', ha='center', va='center', rotation=0, transform=ax[ax_name].transAxes, **styles.txtWhite)
        i += 1

    # Add Headers
    ax['stm_1'].set_title('Call series', pad=5, **styles.txtHeader)
    ax['stm_1_e'].set_title('Extended', pad=5, **styles.txtHeader)

    # ==================================================================================================================
    # B) PLOT PEFORMANCE MATRIX PLOT (VanRossum: Tau vs. Duration)
    GRID_COLOR = '0.75'
    GRID_LINEWIDTH = 0.5
    x_series = list(np.arange(0, 2.55, 0.05))
    # Log Axis
    locmaj = ticker.LogLocator(base=10, numticks=12)
    locmin = ticker.LogLocator(base=10.0, subs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), numticks=12)

    # Color Mesh Plot
    ax['performance_call_series'].pcolormesh(x_series, taus, performance_moth_series.T, cmap=styles.cmap, vmin=0, vmax=1, shading='auto', rasterized=True)
    ax['performance_call_series_extended'].pcolormesh(x_series, taus, performance_moth_series_extended.T, cmap=styles.cmap, vmin=0, vmax=1, shading='auto', rasterized=True)
    ax['performance_poisson'].pcolormesh(x_series, taus, performance_poission_data.T, cmap=styles.cmap, vmin=0, vmax=1, shading='auto', rasterized=True)
    plot_labels = ['Call series', 'Extended', 'Poisson']
    i = 0
    for ax_name in ['performance_call_series', 'performance_call_series_extended', 'performance_poisson']:
        ax[ax_name].set_xticks([0, 1, 2])
        ax[ax_name].set_yscale('log')
        ax[ax_name].yaxis.set_major_locator(locmaj)
        ax[ax_name].yaxis.set_minor_locator(locmin)
        ax[ax_name].yaxis.set_minor_formatter(ticker.NullFormatter())
        ax[ax_name].set_title(plot_labels[i], pad=5, **styles.txtHeader)
        i += 1

    # Plot a vertical line at thresholds
    ls = '--'

    # 50%: 50 ms, 80%: 300 ms
    ax['performance_call_series'].plot([300/1000]*2, [0, 10**1], color='black', ls=ls)
    ax['performance_call_series'].plot([50/1000]*2, [0, 10**1], color='black', ls=ls)

    # 50%: 50 ms, 80%: 300 ms, small drop after 1500 ms
    ax['performance_call_series_extended'].plot([300 / 1000] * 2, [0, 10 ** 1], color='black', ls=ls)
    ax['performance_call_series_extended'].plot([50 / 1000] * 2, [0, 10 ** 1], color='black', ls=ls)
    ax['performance_call_series_extended'].plot([1500 / 1000] * 2, [0, 10 ** 1], color='black', ls=ls)

    # 50%: 1100 ms, 80%: 2200 ms
    ax['performance_poisson'].plot([1100 / 1000] * 2, [0, 10 ** 1], color='black', ls=ls)
    ax['performance_poisson'].plot([2200 / 1000] * 2, [0, 10 ** 1], color='black', ls=ls)

    # Remove X Ticks
    for ax_name in ['performance_call_series', 'performance_call_series_extended', 'stm_1', 'stm_1_e', 'stm_10', 'stm_10_e']:
        ax[ax_name].set_xticklabels([])

    # Remove Y Ticks
    for ax_name in ['stm_1_e', 'stm_10_e', 'stm_1000_e']:
        ax[ax_name].set_yticklabels([])

    # Add Y Labels
    ax['stm_10'].set_ylabel('Call ID')
    ax['performance_call_series_extended'].set_ylabel(r'$\tau$ [ms]')

    # Add X Labels
    fig.text(0.25, 0.52, 'Call ID', ha='center')  # X Label for Spike Train Matching
    fig.text(0.78, 0.52, 'Spike train duration [s]', ha='center')  # X Label for Performance

    # ==================================================================================================================
    # Moth VS Bats
    # ==================================================================================================================
    # C) Classification
    y_series = np.arange(0, 27, 1)
    x_series = np.arange(0, 2550, 50)
    X_series, Y_series = np.meshgrid(x_series, y_series)
    data_1 = np.array(mb_vr_series['pmoth'][0]).T  # 0 == tau 1 ms
    data_10 = np.array(mb_vr_series['pmoth'][9]).T  # 9 == tau 10 ms
    data_1000 = np.array(mb_vr_series['pmoth'][50]).T  # 50 == tau 1000 ms
    data_1_e = np.array(mb_vr_series_extended['pmoth'][0]).T  # 0 == tau 1 ms
    data_10_e = np.array(mb_vr_series_extended['pmoth'][9]).T  # 9 == tau 10 ms
    data_1000_e = np.array(mb_vr_series_extended['pmoth'][50]).T  # 50 == tau 1000 ms

    ax['mb_performance_1'].pcolormesh(X_series, Y_series, data_1, cmap=styles.cmap_gray, shading='auto', vmin=0, vmax=1, rasterized=False)
    ax['mb_performance_1_e'].pcolormesh(X_series, Y_series, data_1_e, cmap=styles.cmap_gray, shading='auto', vmin=0, vmax=1, rasterized=False)
    ax['mb_performance_10'].pcolormesh(X_series, Y_series, data_10, cmap=styles.cmap_gray, shading='auto', vmin=0, vmax=1, rasterized=False)
    ax['mb_performance_10_e'].pcolormesh(X_series, Y_series, data_10_e, cmap=styles.cmap_gray, shading='auto', vmin=0, vmax=1, rasterized=False)
    ax['mb_performance_1000'].pcolormesh(X_series, Y_series, data_1000, cmap=styles.cmap_gray, shading='auto', vmin=0, vmax=1, rasterized=False)
    ax['mb_performance_1000_e'].pcolormesh(X_series, Y_series, data_1000_e, cmap=styles.cmap_gray, shading='auto', vmin=0, vmax=1, rasterized=False)

    # ==================================================================================================================
    # D) d-prime
    taus = list(np.concatenate([np.arange(1, 21, 1), np.arange(30, 105, 5), np.arange(200, 1000, 55)]))
    taus.append(1000)
    y_series = taus
    x_series = np.arange(0, 2550, 50)
    x_series[0] = 10
    X_series, Y_series = np.meshgrid(x_series, y_series)
    ax['mb_d_prime'].pcolormesh(X_series, Y_series, mb_vr_series['dprime'], cmap=styles.cmap, shading='gouraud', vmin=0, vmax=2, rasterized=False)
    ax['mb_d_prime_e'].pcolormesh(X_series, Y_series, mb_vr_series_extended['dprime'], cmap=styles.cmap, shading='gouraud', vmin=0, vmax=2, rasterized=False)

    # Log Axis
    locmaj = ticker.LogLocator(base=10, numticks=12)
    locmin = ticker.LogLocator(base=10.0, subs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), numticks=12)
    k = 0
    plot_labels = ['Call series', 'Extended']
    for i in ['mb_d_prime', 'mb_d_prime_e']:
        ax[i].set_yscale('log')
        ax[i].yaxis.set_major_locator(locmaj)
        ax[i].yaxis.set_minor_locator(locmin)
        ax[i].yaxis.set_minor_formatter(ticker.NullFormatter())
        ax[i].set_xticks([0, 1000, 2000])
        ax[i].set_xticklabels([0, 1, 2])
        ax[i].set_title(plot_labels[k], pad=5, **styles.txtHeader)
        k += 1

    # Set Ticks
    boarder_series = 17
    tau_label_vals = [1, 1, 10, 10, 1000, 1000]
    i = 0
    for ax_name in ['mb_performance_1', 'mb_performance_1_e', 'mb_performance_10', 'mb_performance_10_e', 'mb_performance_1000', 'mb_performance_1000_e']:
        ax[ax_name].set_yticks(np.arange(0.5, 27.5, 10))
        ax[ax_name].set_yticklabels([0, 10, 20])
        ax[ax_name].plot([10, 2500], [boarder_series - 0.5, boarder_series - 0.5], **styles.sep_line)
        ax[ax_name].set_xticks([0, 1000, 2000])
        ax[ax_name].set_xticklabels([0, 1, 2])
        ax[ax_name].text(tau_label_x, tau_label_y, fr'$\tau$ {tau_label_vals[i]} ms', ha='center', va='center', rotation=0, transform=ax[ax_name].transAxes, **styles.txtRed)
        i += 1

    # Remove X Ticks
    for ax_name in ['mb_performance_1', 'mb_performance_1_e', 'mb_performance_10', 'mb_performance_10_e']:
        ax[ax_name].set_xticklabels([])

    # Remove Y Ticks
    for ax_name in ['mb_performance_1_e', 'mb_performance_10_e', 'mb_performance_1000_e']:
        ax[ax_name].set_yticklabels([])

    ax['mb_d_prime'].set_xticklabels([])

    # Labels Moth and Bats
    b_label = ax['mb_performance_1'].text(0.75, 0.78, 'B', transform=ax['mb_performance_1'].transAxes,
                                          **styles.mb_label_text)
    b_label.set_bbox(styles.mb_label_box)
    m_label = ax['mb_performance_1'].text(0.75, 0.30, 'M', transform=ax['mb_performance_1'].transAxes,
                                          **styles.mb_label_text)
    m_label.set_bbox(styles.mb_label_box)  # needs the dict directly

    # Add Headers
    ax['mb_performance_1'].set_title('Call series', pad=5, **styles.txtHeader)
    ax['mb_performance_1_e'].set_title('Extended', pad=5, **styles.txtHeader)

    # Add Y Labels
    ax['mb_performance_10'].set_ylabel('Call ID')
    ax['mb_d_prime'].set_ylabel(r'$\tau$ [ms]')
    ax['mb_d_prime_e'].set_ylabel(r'$\tau$ [ms]')

    # Add X Labels
    fig.text(0.28, 0.025, 'Spike train duration [s]', ha='center')
    fig.text(0.78, 0.025, 'Spike train duration [s]', ha='center')

    # ==================================================================================================================
    # Colorbar for Spike Train Matching
    norm = colors.Normalize(vmin=0, vmax=20)

    cb1 = colorbar.ColorbarBase(ax['spike_train_cb'], cmap=styles.cmap, norm=norm)
    cb1.ax.tick_params(labelsize=styles.cb_text_size)
    cb1.set_label('Spike trains', rotation=270, labelpad=10)
    cb1.set_ticks([0, 5, 10, 15, 20])

    # Colorbar for Performance Matrix Plot
    norm = colors.Normalize(vmin=0, vmax=1)
    cb2 = colorbar.ColorbarBase(ax['performance_cb'], cmap=styles.cmap, norm=norm)
    cb2.ax.tick_params(labelsize=styles.cb_text_size)
    cb2.set_label('Correct', rotation=270, labelpad=10)

    # Colorbar for Moths vs. Bats Classification
    norm = colors.Normalize(vmin=0, vmax=1)
    cb3 = colorbar.ColorbarBase(ax['mb_performance_cb'], cmap=styles.cmap_gray, norm=norm)
    cb3.ax.tick_params(labelsize=styles.cb_text_size)
    cb3.set_label('% of moth classification', rotation=270, labelpad=10)

    # Colorbar for Moths vs. Bats d prime
    norm = colors.Normalize(vmin=0, vmax=2)
    cb4 = colorbar.ColorbarBase(ax['mb_d_prime_cb'], cmap=styles.cmap, norm=norm)
    cb4.ax.tick_params(labelsize=styles.cb_text_size)
    cb4.set_label('d-prime', rotation=270, labelpad=10)
    cb4.ax.yaxis.set_major_locator(ticker.MultipleLocator(0.4))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Subplot Letters
    LABEL_X_POS = -0.3
    LABEL_Y_POS = 1.2

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    i = 0
    for ax_name in ['stm_1', 'performance_call_series', 'mb_performance_1', 'mb_d_prime']:
        ax[ax_name].text(
            LABEL_X_POS, LABEL_Y_POS,
            cap_letter(letters[i], styles.sub_fig_cap_upper_case),
            transform=ax[ax_name].transAxes,
            size=styles.sub_fig_cap_text_size
        )
        i += 1

    # Save Fig ========================================================================================
    fig.savefig(f'{save_path}Fig_03_Classification.pdf')
    fig.savefig(f'{save_path}Fig_03_Classification.svg')
    # fig.savefig(f'{save_path}Fig_03_Classification.jpeg', dpi=300)
    plt.close(fig)
    print('Fig. 3: Classification, saved!')
