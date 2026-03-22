#!/usr/bin/env python

import os
import pickle
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.mlab as ml
import scipy.io.wavfile as wav
from IPython import embed
import plotting_functions as pf
from plotstyle import PlotStyle
from plotting_functions import cap_letter, pickle_stuff


def compute_spectrogram(data):
    # data is a wav file
    # Compute Spectrogram
    fr = data[0]
    song = data[1]
    t_min = 1.007
    t_max = 1.02
    spec_duration = t_max - t_min
    sample_min = int(t_min * fr)
    sample_max = int(t_max * fr)
    nfft = 64

    # Stolen from "audian" code:
    specpower, freqs, bins = ml.specgram(song[sample_min:sample_max], NFFT=nfft, Fs=fr, noverlap=nfft // 2,
                                         detrend=ml.detrend_mean)
    specpower[specpower <= 0.0] = np.min(specpower[specpower > 0.0])  # remove zeros
    z = 10 * np.log10(specpower)

    return spec_duration, specpower, freqs, bins, z


def load_data(data_path):
    # Call for Spectrogram
    call_audio = wav.read('data/calls/melese_PK1300_01.wav')
    spec_duration, spec_power, spec_freqs, spec_bins, spec_z = compute_spectrogram(call_audio)

    # Tuning Curves
    x_conv_f1 = pd.read_csv(f'{data_path}x_conv_f1.csv', index_col=0)['0']
    conv_approx_f1 = pd.read_csv(f'{data_path}conv_approx_f1.csv', index_col=0)['0']
    x_conv_f2 = pd.read_csv(f'{data_path}x_conv_f2.csv', index_col=0)['0']
    conv_approx_f2 = pd.read_csv(f'{data_path}conv_approx_f2.csv', index_col=0)['0']
    y_conv_f1 = pd.read_csv(f'{data_path}y_conv_f1.csv', index_col=0)['0']
    y_conv_f2 = pd.read_csv(f'{data_path}y_conv_f2.csv', index_col=0)['0']

    # Power Spectrum
    freqs_bats = pd.read_csv(f'{data_path}freqs_bats.csv', index_col=0).to_numpy()
    power_bats_mean = pd.read_csv(f'{data_path}power_bats_mean.csv', index_col=0)['0'].to_numpy()
    # power_bats_std = pd.read_csv(f'{data_path}power_bats_std.csv', index_col=0)['0'].to_numpy()
    freqs_estigmene = pd.read_csv(f'{data_path}freqs_estigmene.csv', index_col=0).to_numpy()
    power_estigmene = pd.read_csv(f'{data_path}power_estigmene.csv', index_col=0).to_numpy()
    freqs = pd.read_csv(f'{data_path}freqs.csv', index_col=0).to_numpy()
    mean_power = pd.read_csv(f'{data_path}mean_power.csv', index_col=0)['0'].to_numpy()
    # std_power = pd.read_csv(f'{data_path}std_power.csv', index_col=0)['0'].to_numpy()

    # Load FI Curve data
    P_PATH = f'{data_path}2017-11-03-aa_fi_analysis.txt'
    with open(P_PATH, 'rb') as fp:
        all_data = pickle.load(fp)
        _, _, _, _, _, _, conv_rate, dur = all_data
        # spike_count, rate, fsl, fisi, d_isi, instant_rate, conv_rate, dur = all_data

    # Load FI-Field / Audiogram / Freqency Tuning Data from HDD
    fi_20_estigmene = pickle_stuff(f'{data_path}fi_20_estigmene.pickle')
    fi_20_carales = pickle_stuff(f'{data_path}fi_20_carales.pickle')

    # Freq Histogram
    hist_dir = 'data/histogram/'
    freq_dist = pd.read_csv(f'{hist_dir}freqs.csv', index_col=0)

    data_for_plot = {
        'x_conv_f1': x_conv_f1,
        'x_conv_f2': x_conv_f2,
        'y_conv_f1': y_conv_f1,
        'y_conv_f2': y_conv_f2,
        'conv_approx_f1': conv_approx_f1,
        'conv_approx_f2': conv_approx_f2,
        'conv_rate': conv_rate,
        'freqs_bats': freqs_bats,
        'power_bats_mean': power_bats_mean,
        'freqs_estigmene': freqs_estigmene,
        'power_estigmene': power_estigmene,
        'freqs': freqs,
        'mean_power': mean_power,
        'fi_20_estigmene': fi_20_estigmene,
        'fi_20_carales': fi_20_carales,
        'freq_dist': freq_dist
    }

    spectrogram_data = {
        'spec_duration': spec_duration,
        'spec_power': spec_power,
        'spec_freqs': spec_freqs,
        'spec_bins': spec_bins,
        'spec_z': spec_z,
    }

    return data_for_plot, spectrogram_data


def main():
    # Load Data
    data_path = 'data/Tuning/'
    data, spec_data = load_data(data_path)
    save_path = 'figs/'

    # ==================================================================================================================
    # FIGURE
    # Import Plot Styles
    styles = PlotStyle()

    # Figure Size (cm)
    fig_width_cm = 16
    fig_height_cm = 14

    # Create Grid
    fig_width = float(fig_width_cm / 2.54)
    fig_height = float(fig_height_cm / 2.54)

    fig = plt.figure(figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.15, top=0.90, bottom=0.1, right=0.90, wspace=0, hspace=0)

    # Create a grid that has mm resolution (height x width mm)
    grid = gridspec.GridSpec(nrows=int(fig_height_cm * 10), ncols=int(fig_width_cm * 10))
    ax = dict()
    # grid[Height:Width]
    ax['spec'] = plt.subplot(grid[0:30, 0:90])
    ax['spec_cb'] = plt.subplot(grid[5:25, 92:94])
    ax['freq_dist'] = plt.subplot(grid[0:30, 120:160])
    ax['intensity'] = plt.subplot(grid[50:80, 0:70])
    ax['power'] = plt.subplot(grid[50:80, 90:160])
    ax['freq_estigmene'] = plt.subplot(grid[100:130, 0:70])
    ax['freq_carales'] = plt.subplot(grid[100:130, 90:160])

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SPECTROGRAM
    db_min = -20
    db_max = np.max(spec_data['spec_z'])
    t_min = 0
    t_max = spec_data['spec_duration']
    t_min_ms = t_min * 1000
    t_max_ms = t_max * 1000
    bins_ms = spec_data['spec_bins'] * 1000  # seconds → ms

    ax['spec'].pcolormesh(bins_ms, spec_data['spec_freqs']/1000, spec_data['spec_z'], cmap=styles.cmapSpectrogram, vmin=db_min, vmax=db_max, shading='auto')
    ax['spec'].set_ylim(0, 150)
    ax['spec'].set_yticks([0, 50, 100, 150])
    ax['spec'].set_xlim(t_min_ms, t_max_ms)
    ax['spec'].set_ylabel('Freq. [kHz]')
    ax['spec'].set_xlabel('Time [ms]')

    # Remove the top, bottom and right spines
    ax['spec'].spines['top'].set_visible(False)
    ax['spec'].spines['right'].set_visible(False)

    # Colorbar on ax[6]
    # cmap = matplotlib.cm.jet  # set color map
    norm = matplotlib.colors.Normalize(vmin=db_min, vmax=db_max)
    cb = matplotlib.colorbar.ColorbarBase(ax['spec_cb'], cmap=styles.cmapSpectrogram, norm=norm)
    cb.set_label('Power [dB]', rotation=270, labelpad=8)
    cb.set_ticks([0, 20, 40])

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Freq Histogram
    inset_x = 0.8
    inset_y = 0.9
    y_tick_count = 5
    hist_data = data['freq_dist']
    ax_name = 'freq_dist'
    bin_count = int(np.sqrt(len(hist_data)))  # Square Root Choice
    ax[ax_name].hist(hist_data, bins=bin_count, **styles.histogram_style)
    ax[ax_name].text(
        inset_x, inset_y,
        f'n={len(hist_data)}',
        transform=ax[ax_name].transAxes,
        ha='center',
        va='center'
    )
    # Remove the top and right spines
    ax[ax_name].set_xlabel('Frequency [kHz]')
    ax[ax_name].set_ylabel('Count')
    ax[ax_name].spines['top'].set_visible(False)
    ax[ax_name].spines['right'].set_visible(False)
    ax[ax_name].yaxis.set_major_locator(plt.MaxNLocator(y_tick_count))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Plot Frequency Intensity Tuning Curves
    Y_MAX = 600
    F1 = 20
    F2 = 85
    # Half-Max Linear Fit
    ax['intensity'].plot(data['x_conv_f1'], data['conv_approx_f1'], **styles.lsTuningHM_Fit)
    ax['intensity'].plot(data['x_conv_f2'], data['conv_approx_f2'], **styles.lsTuningHM_Fit)

    # Scatter Plot with error bars
    ax['intensity'].errorbar(
        data['conv_rate'][F1][:, 0], data['conv_rate'][F1][:, 1], yerr=data['conv_rate'][F1][:, 2], label=f'{F1} kHz', **styles.scTuningCurve_20
    )
    ax['intensity'].errorbar(
        data['conv_rate'][F2][:, 0], data['conv_rate'][F2][:, 1], yerr=data['conv_rate'][F2][:, 2], label=f'{F2} kHz', **styles.scTuningCurve_85
    )
    # Sigmoid Fit Curve
    ax['intensity'].plot(data['x_conv_f1'], data['y_conv_f1'], **styles.lsBlack)
    ax['intensity'].plot(data['x_conv_f2'], data['y_conv_f2'], **styles.lsGray)

    ax['intensity'].set_ylabel('Firing rate [Hz]')
    ax['intensity'].set_ylim(0, Y_MAX)
    ax['intensity'].set_yticks(np.arange(0, Y_MAX + 100, 100))
    ax['intensity'].legend(frameon=False)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Plot Power Spectrum of calls
    ax['power'].plot(data['freqs_bats'][0], data['power_bats_mean'], label='Bats', **styles.lsBlack)
    ax['power'].plot(data['freqs_estigmene'], data['power_estigmene'], label='Estigmene', **styles.lsBlack_dashed)
    ax['power'].plot(data['freqs'][0], data['mean_power'], label='Carales', **styles.lsBlack_dotted)
    ax['power'].set_ylabel('Power [dB]')
    ax['power'].legend(frameon=False)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Plot Audiograms (FI Field)
    # Estigmene
    ax['freq_estigmene'].plot(data['fi_20_estigmene'][0][0], data['fi_20_estigmene'][0][1], label='20 ms', **styles.lsBlack)
    ax['freq_estigmene'].plot(data['fi_20_estigmene'][1][0], data['fi_20_estigmene'][1][1], **styles.lsBlack)
    ax['freq_estigmene'].plot(data['fi_20_estigmene'][2][0], data['fi_20_estigmene'][2][1], label='50 ms', **styles.lsBlack_dashed)
    ax['freq_estigmene'].plot(data['fi_20_estigmene'][3][0], data['fi_20_estigmene'][3][1], **styles.lsBlack_dashed)
    ax['freq_estigmene'].text(0.25, 0.9, 'Estigmene', transform=ax['freq_estigmene'].transAxes, **styles.txt)

    # Carales
    ax['freq_carales'].plot(data['fi_20_carales'][0][0], data['fi_20_carales'][0][1], label='20 ms', **styles.lsBlack)
    ax['freq_carales'].plot(data['fi_20_carales'][1][0], data['fi_20_carales'][1][1], **styles.lsBlack)
    ax['freq_carales'].plot(data['fi_20_carales'][2][0], data['fi_20_carales'][2][1], **styles.lsBlack)
    ax['freq_carales'].plot(data['fi_20_carales'][3][0], data['fi_20_carales'][3][1], **styles.lsBlack)
    ax['freq_carales'].text(0.25, 0.9, 'Carales', transform=ax['freq_carales'].transAxes, **styles.txt)

    ax['freq_estigmene'].legend(frameon=False, loc=1)
    ax['freq_carales'].legend(frameon=False, loc=1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Axis Labels
    ax['intensity'].set_xlabel('Intensity [db SPL]')
    ax['power'].set_xlabel('Frequency [kHz]')
    ax['freq_estigmene'].set_xlabel('Frequency [kHz]')
    ax['freq_carales'].set_xlabel('Frequency [kHz]')
    ax['freq_estigmene'].set_ylabel('Threshold [dB SPL]')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Subplot Letters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    i = 0
    for ax_name in ['spec', 'freq_dist', 'intensity', 'power', 'freq_estigmene', 'freq_carales']:
        if ax_name == 'spec':
            label_x = -0.15
            label_y = 1.1
        else:
            label_x = -0.2
            label_y = 1.1

        ax[ax_name].text(
            label_x, label_y,
            cap_letter(letters[i], styles.sub_fig_cap_upper_case),
            transform=ax[ax_name].transAxes,
            size=styles.sub_fig_cap_text_size
        )
        i += 1

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Set Axis Limits and Ticks
    Y_MIN = 0
    Y_MAX = 100
    Y_STEP = 20
    X_MIN = 0
    X_MAX = 100
    X_STEP = 20

    ax['intensity'].set_xlim(X_MIN, X_MAX)
    ax['intensity'].set_xticks(np.arange(X_MIN, X_MAX + X_STEP, X_STEP))

    ax['freq_estigmene'].set_ylim(Y_MIN, Y_MAX)
    ax['freq_estigmene'].set_yticks(np.arange(Y_MIN, Y_MAX + Y_STEP, Y_STEP))
    ax['freq_carales'].set_ylim(Y_MIN, Y_MAX)
    ax['freq_carales'].set_yticks(np.arange(Y_MIN, Y_MAX + Y_STEP, Y_STEP))

    ax['power'].set_ylim(-20, 60)
    ax['power'].set_yticks([-20, 0, 20, 40, 60])

    ax['power'].set_xlim(X_MIN, X_MAX)
    ax['power'].set_xticks(np.arange(X_MIN, X_MAX + X_STEP, X_STEP))

    ax['freq_estigmene'].set_xlim(X_MIN, X_MAX)
    ax['freq_estigmene'].set_xticks(np.arange(X_MIN, X_MAX + X_STEP, X_STEP))
    ax['freq_carales'].set_xlim(X_MIN, X_MAX)
    ax['freq_carales'].set_xticks(np.arange(X_MIN, X_MAX + X_STEP, X_STEP))

    # Remove top and right axis
    for k in ax:
        ax[k].spines['top'].set_visible(False)
        ax[k].spines['right'].set_visible(False)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Save Figure to HDD
    fig.savefig(f'{save_path}Supp_Fig_01.pdf')
    # fig.savefig(f'{save_path}Supp_Fig_01.svg')
    # fig.savefig(f'{save_path}Supp_Fig_01.jpeg', dpi=300)
    plt.close(fig)
    print('Supp Fig 1 saved!')


if __name__ == '__main__':
   main()
