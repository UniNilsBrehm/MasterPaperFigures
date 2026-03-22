#!/usr/bin/env python
"""
SCRIPT FOR  DATA COLLECTION FOR TUNING
This is the FI-Field / Frequency Tuning Figure in Master Thesis (Fig. 8)
based on the data sets listed below (Carales and Estigmene and Bat calls)
It will compute power spectra for Carales, Estigmene and Bat Calls

Nils Brehm - 2021
"""
import os
import pickle
import pandas as pd
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io.wavfile as wav
from scipy import signal
from IPython import embed
import plotting_functions as pf


def decibel(xx):
    return 10 * np.log10(xx)


# =================================================================================================
# Load data =======================================================================================
save_path = 'data/Tuning/'

# Load FI Curve data
with open(f'{save_path}2017-11-03-aa_fi_analysis.txt', 'rb') as fp:  # Unpickling
    all_data = pickle.load(fp)
    # spike_count, rate, fsl, fisi, d_isi, instant_rate, conv_rate, dur = all_data
    _, _, _, _, _, _, conv_rate, dur = all_data


# Estigmene Datasets for FI, first two = 20 ms, last two = 50 ms
# datasets_20_estigmene = ['2017-11-25-aa', '2017-11-27-aa', '2017-10-26-aa', '2017-12-05-aa']
datasets_20_estigmene = os.listdir(f'{save_path}fi_fields/estigmene/')
# Carales Datasets for FI, all are 20 ms
# datasets_20_carales = ['2017-11-01-aa', '2017-11-02-aa', '2017-11-02-ad', '2017-11-03-aa']  # 20 ms
datasets_20_carales = os.listdir(f'{save_path}fi_fields/carales/')

# -------------------------------------------------------------------------------------------------
# COMPUTE FITS FOR TUNING CURVES ------------------------------------------------------------------
# Select Frequencies (kHz) for plotting:
F1 = 20
F2 = 85
# Compute Fitting Curves
estimated_th_conv_f1, conv_approx_f1, x_conv_f1, y_conv_f1 = pf.fitting_fi_curves(dur,
                                                                                  conv_rate[F1])
estimated_th_conv_f2, conv_approx_f2, x_conv_f2, y_conv_f2 = pf.fitting_fi_curves(dur,
                                                                                  conv_rate[F2])
pd.DataFrame(x_conv_f1).to_csv(f'{save_path}x_conv_f1.csv')
pd.DataFrame(x_conv_f2).to_csv(f'{save_path}x_conv_f2.csv')

pd.DataFrame(y_conv_f1).to_csv(f'{save_path}y_conv_f1.csv')
pd.DataFrame(y_conv_f2).to_csv(f'{save_path}y_conv_f2.csv')

pd.DataFrame(conv_approx_f1).to_csv(f'{save_path}conv_approx_f1.csv')
pd.DataFrame(conv_approx_f2).to_csv(f'{save_path}conv_approx_f2.csv')

estimated_th = [estimated_th_conv_f1, estimated_th_conv_f2]
pd.DataFrame(estimated_th).to_csv(f'{save_path}estimated_th.csv')

# -----------------------------------

# COMPUTE POWER SPECTRA OF MOTH AND BAT CALLS: ----------------------------------------------------
FS_estigmene = 480 * 1000  # The wav file shows a different sampling rate, but Philipp said he recorded with 480 k
# carales_calls = ['carales_12x12_01', 'carales_12x12_02']
carales_calls = os.listdir(f'{save_path}audio/carales/')
_, estigmene = wav.read(f'data/Tuning/audio/estigmene/Pk13060008_m_original.wav')

y = estigmene[835000:996000]
freqs_estigmene, power_estigmene = signal.welch(y, FS_estigmene, scaling='spectrum', window='hann')
freqs_estigmene = freqs_estigmene / 1000
power_estigmene = decibel(power_estigmene)

# Store
pd.DataFrame(freqs_estigmene).to_csv(f'{save_path}freqs_estigmene.csv')
pd.DataFrame(power_estigmene).to_csv(f'{save_path}power_estigmene.csv')

freq = list()
power = list()

# Compute Power for both carales recordings:
for j, _ in enumerate(carales_calls):
    rec_dir = f'{save_path}audio/carales/{carales_calls[j]}'
    FS, rec = wav.read(rec_dir)
    f, p = signal.welch(rec, FS, scaling='spectrum', window='hann')
    power.append(decibel(p))
    freq.append(f / 1000)
# Store
pd.DataFrame(freq).to_csv(f'{save_path}freqs.csv')

# Bat Calls used for the power spectrum fig.
# bat_calls = ['Barbastella_barbastellus_1_n', 'Eptesicus_nilssonii_1_s', 'Myotis_bechsteinii_1_n',
#              'Myotis_brandtii_1_n', 'Myotis_nattereri_1_n', 'Nyctalus_leisleri_1_n',
#              'Nyctalus_noctula_2_s', 'Pipistrellus_pipistrellus_1_n', 'Pipistrellus_pygmaeus_2_n',
#              'Rhinolophus_ferrumequinum_1_n', 'Vespertilio_murinus_1_s']
bat_calls = os.listdir(f'{save_path}audio/bats/')

bats = [[]] * len(bat_calls)
freqs_bats = [[]] * len(bat_calls)
power_bats = [[]] * len(bat_calls)

for j, file_name in enumerate(bat_calls):
    rec_dir = f'{save_path}audio/bats/{file_name}'
    FS, x = wav.read(rec_dir)
    f, p = signal.welch(x, FS, scaling='spectrum', window='hann')
    power_bats[j] = decibel(p)
    freqs_bats[j] = f / 1000
power_bats_mean = np.median(np.array(power_bats), axis=0)
power_bats_std = np.std(np.array(power_bats), axis=0)
power_bats_mean[freqs_bats[0] <= 5] = 0

# Store
pd.DataFrame(freqs_bats).to_csv(f'{save_path}freqs_bats.csv')
pd.DataFrame(power_bats_mean).to_csv(f'{save_path}power_bats_mean.csv')
pd.DataFrame(power_bats_std).to_csv(f'{save_path}power_bats_std.csv')

# Mean Power for Carales:
mean_power = np.mean(np.array(power), axis=0)
std_power = np.std(np.array(power), axis=0)
error_up = mean_power + std_power
error_down = mean_power - std_power
idx = error_down < 0
error_down[idx] = 1

# Load FI-Field / Audiogram / Freqency Tuning Data from HDD
fi_20_estigmene = list()
for i, f_name in enumerate(datasets_20_estigmene):
    with open(f'{save_path}/fi_fields/estigmene/{f_name}', 'rb') as fp:  # Unpickling
        fi_20_estigmene.append(pickle.load(fp))

fi_20_carales = list()
for f_name in datasets_20_carales:
    with open(f'{save_path}/fi_fields/carales/{f_name}', 'rb') as fp:  # Unpickling
        fi_20_carales.append(pickle.load(fp))

# Store
pd.DataFrame(mean_power).to_csv(f'{save_path}mean_power.csv')
pd.DataFrame(std_power).to_csv(f'{save_path}std_power.csv')

with open(f'{save_path}/fi_20_estigmene.pickle', 'wb') as handle:
    pickle.dump(fi_20_estigmene, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(f'{save_path}/fi_20_carales.pickle', 'wb') as handle:
    pickle.dump(fi_20_carales, handle, protocol=pickle.HIGHEST_PROTOCOL)

# ======================================================================================================================
# Gap Detection
gaps_dir = 'data/Gaps'
rects = os.listdir(f'{gaps_dir}/raw/rect/')
models = os.listdir(f'{gaps_dir}/raw/model/')
rects_data = list()
models_data = list()

# Rectangular Pulses
# From 0 to 17: data for 10 ms duration
# From 17 to 34: data for 5 ms duration
cut1_rec = 17
cut2_rec = 34
for f_name in rects:
    vs = np.load(f'{gaps_dir}/raw/rect/{f_name}')
    result = pd.DataFrame()
    result['mean_vs'] = vs[0:cut1_rec, 3]
    result['gaps'] = vs[0:cut1_rec, 2]
    result['percentile'] = vs[0:cut1_rec, 7]
    result['ci_low'] = vs[0:cut1_rec, 4]
    result['ci_up'] = vs[0:cut1_rec, 5]
    result.to_csv(f'{gaps_dir}/rectangular_pulses/10ms/rect_10ms_{f_name}.csv')

    result = pd.DataFrame()
    result['mean_vs'] = vs[cut1_rec:cut2_rec, 3]
    result['gaps'] = vs[cut1_rec:cut2_rec, 2]
    result['percentile'] = vs[cut1_rec:cut2_rec, 7]
    result['ci_low'] = vs[cut1_rec:cut2_rec, 4]
    result['ci_up'] = vs[cut1_rec:cut2_rec, 5]
    result.to_csv(f'{gaps_dir}/rectangular_pulses/05ms/rect_05ms_{f_name}.csv')

# Model Pulses
cut1_model = 16
cut2_model = 32
for f_name in models:
    vs = np.load(f'{gaps_dir}/raw/model/{f_name}')
    result = pd.DataFrame()
    result['mean_vs'] = vs[0:cut1_model, 3]
    result['gaps'] = vs[0:cut1_model, 2]
    result['percentile'] = vs[0:cut1_model, 7]
    result['ci_low'] = vs[0:cut1_model, 4]
    result['ci_up'] = vs[0:cut1_model, 5]
    result.to_csv(f'{gaps_dir}/model_pulses/05ms/model_05ms_{f_name}.csv')

    result = pd.DataFrame()
    result['mean_vs'] = vs[cut1_model:cut2_model, 3]
    result['gaps'] = vs[cut1_model:cut2_model, 2]
    result['percentile'] = vs[cut1_model:cut2_model, 7]
    result['ci_low'] = vs[cut1_model:cut2_model, 4]
    result['ci_up'] = vs[cut1_model:cut2_model, 5]
    result.to_csv(f'{gaps_dir}/model_pulses/10ms/model_10ms_{f_name}.csv')

print('Stored Data to HDD')
