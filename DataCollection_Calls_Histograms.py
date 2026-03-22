import scipy.io as sio
import pandas as pd


def store_data(x, p, name):
    #y = pd.DataFrame(x)
    y = pd.Series(x)
    y.to_csv(f'{p}/{name}.csv')


# ----------------------------------------------------------------------------------------------------------------------
save_path = 'data/histogram/'
# Single Calls
pd_a = sio.loadmat('E:/Moth/CallStats/pd_a.mat')['pd_a_py'][0]
pd_p = sio.loadmat('E:/Moth/CallStats/pd_p.mat')['pd_p_py'][0]

ipi_a = sio.loadmat('E:/Moth/CallStats/ipi_a.mat')['ipi_a_py'][0]
ipi_p = sio.loadmat('E:/Moth/CallStats/ipi_p.mat')['ipi_p_py'][0]

freq_a = sio.loadmat('E:/Moth/CallStats/freq_a.mat')['freq_a_py'][0]
freq_p = sio.loadmat('E:/Moth/CallStats/freq_p.mat')['freq_p_py'][0]

pnr_a = sio.loadmat('E:/Moth/CallStats/pnr_a.mat')['pnr_a_py'][0]
pnr_p = sio.loadmat('E:/Moth/CallStats/pnr_p.mat')['pnr_p_py'][0]

ITI = sio.loadmat('E:/Moth/CallStats/ITI.mat')['ITI_py'][0]
call_dur = sio.loadmat('E:/Moth/CallStats/calldur.mat')['call_dur_py'][0]

# Get data into lists
# Single Pulse Duration:
single_pulse_duration = []
# First all active pulses
for k in range(len(pd_a)):
    for i in range(len(pd_a[k])):
        single_pulse_duration.append(pd_a[k][i][0])
# Now all passive pulses
for k in range(len(pd_p)):
    for i in range(len(pd_p[k])):
        single_pulse_duration.append(pd_p[k][i][0])
store_data(single_pulse_duration, save_path, 'single_pulse_duration')

# Pulse Count
pulse_count = []
# First all active pulses
for k in range(len(pnr_a)):
    for i in range(len(pnr_a[k])):
        pulse_count.append(pnr_a[k][i][0])
# Now all passive pulses
for k in range(len(pd_p)):
    for i in range(len(pnr_p[k])):
        pulse_count.append(pd_p[k][i][0])
store_data(pulse_count, save_path, 'pulse_count')

# Inter Pulse Interval
inter_pulse_intervals = []
# First all active pulses
for k in range(len(ipi_a)):
    for i in range(len(ipi_a[k])):
        inter_pulse_intervals.append(ipi_a[k][i][0])
# Now all passive pulses
for k in range(len(ipi_p)):
    for i in range(len(ipi_p[k])):
        inter_pulse_intervals.append(ipi_p[k][i][0])
store_data(inter_pulse_intervals, save_path, 'inter_pulse_intervals')

# Frequency
frequencies = []
# First all active pulses
for k in range(len(freq_a)):
    for i in range(len(freq_a[k])):
        frequencies.append(freq_a[k][i][0])
# Now all passive pulses
for k in range(len(freq_p)):
    for i in range(len(freq_p[k])):
        frequencies.append(freq_p[k][i][0])
store_data(frequencies, save_path, 'freqs')

# Inter Train Interval
inter_train_intervals = []
for k in range(len(ITI)):
    inter_train_intervals.append(ITI[k][0][0])
store_data(inter_train_intervals, save_path, 'inter_train_intervals')

# ----------------------------------------------------------------------------------------------------------------------
# Call Series
call_series_dur = sio.loadmat('E:/Moth/CallStats/CallSeries_Stats/call_dur.mat')['call_dur'][0]
call_series_samples = sio.loadmat('E:/Moth/CallStats/CallSeries_Stats/samples.mat')['samples'][0]

# Get Call Series Durations in list
duration_call_series = []
pulse_count_call_series = []
for k in range(len(call_series_dur)):
    duration_call_series.append(call_series_dur[k][0][0])
    pulse_count_call_series.append(len(call_series_samples[k][0]))
store_data(pulse_count_call_series, save_path, 'pulse_count_callseries')
store_data(duration_call_series, save_path, 'duration_callseries')

print('DONE!')
