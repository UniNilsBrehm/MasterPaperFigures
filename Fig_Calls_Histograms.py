import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde
from IPython import embed
import plotting_functions as pf


# Import Data
save_path = 'data/histogram/'
inter_train_intervals = pd.read_csv(f'{save_path}inter_train_intervals.csv', index_col=0)
inter_pulse_intervals = pd.read_csv(f'{save_path}inter_pulse_intervals.csv', index_col=0)
single_pulse_duration = pd.read_csv(f'{save_path}single_pulse_duration.csv', index_col=0)
frequencies = pd.read_csv(f'{save_path}freqs.csv', index_col=0)
pulse_count_call_series = pd.read_csv(f'{save_path}pulse_count_callseries.csv', index_col=0)
duration_call_series = pd.read_csv(f'{save_path}duration_callseries.csv', index_col=0)


# ----------------------------------------------------------------------------------------------------------------------
# Plots
_, subfig_caps_text_sz, sub_fig_cap_upper_case = pf.plot_settings()

label_x_pos = -0.4
label_y_pos = 1.1
subfig_color = 'black'

fig, axs = plt.subplots(2, 3)
# Hist 1 ----
bin_count = 10
plt.sca(axs[0, 0])
sns.histplot(single_pulse_duration, kde=True, ax=axs[0, 0], bins=bin_count, legend=False, color='red',
             line_kws={'lw': 2, 'ls': '-'})
axs[0, 0].lines[0].set_color('black')
plt.xlabel('Pulse Duration [ms]')
plt.xlim([0, 0.6])
plt.xticks([0, 0.2, 0.4, 0.6])
plt.ylabel('Count')
plt.ylim([0, 160])
plt.yticks([0, 40, 80, 120, 160])
axs[0, 0].text(label_x_pos, label_y_pos, pf.cap_letter('a', sub_fig_cap_upper_case), transform=axs[0, 0].transAxes, size=subfig_caps_text_sz,
               color=subfig_color)

# Hist 2 ----
h_ax = axs[0, 1]
bin_count = 10
plt.sca(h_ax)
sns.histplot(inter_pulse_intervals, kde=True, ax=h_ax, bins=bin_count, legend=False,
             line_kws={'lw': 2, 'ls': '-'})
h_ax.lines[0].set_color('black')
plt.xlabel('Inter Pulse Interval [ms]')
plt.xlim([0, 30])
plt.xticks([0, 10, 20, 30])
plt.ylabel('')
plt.ylim([0, 320])
plt.yticks([0, 80, 160, 240, 320])
h_ax.text(label_x_pos, label_y_pos, pf.cap_letter('b', sub_fig_cap_upper_case), transform=h_ax.transAxes, size=subfig_caps_text_sz,
               color=subfig_color)

# Hist 3 ----
h_ax = axs[0, 2]
bin_count = 10
plt.sca(h_ax)
sns.histplot(frequencies, kde=True, ax=h_ax, bins=bin_count, legend=False,
             line_kws={'lw': 2, 'ls': '-'})
h_ax.lines[0].set_color('black')
plt.xlabel('Frequency [kHz]')
plt.xlim([0, 120])
plt.xticks(np.linspace(0, 120, 4))
plt.ylabel('')
plt.ylim([0, 150])
plt.yticks([0, 50, 100, 150])
h_ax.text(label_x_pos, label_y_pos, pf.cap_letter('c', sub_fig_cap_upper_case), transform=h_ax.transAxes, size=subfig_caps_text_sz,
               color=subfig_color)

# Hist 4 ----
h_ax = axs[1, 0]
bin_count = 10
plt.sca(h_ax)
sns.histplot(pulse_count_call_series, kde=True, ax=h_ax, bins=bin_count, legend=False,
             line_kws={'lw': 2, 'ls': '-'})
h_ax.lines[0].set_color('black')
plt.xlabel('Pulse Count')
plt.xlim([0, 1200])
plt.xticks(np.linspace(0, 1200, 4))
plt.ylabel('Count')
plt.ylim([0, 10])
plt.yticks([0, 4, 8, 12])
h_ax.text(label_x_pos, label_y_pos, pf.cap_letter('d', sub_fig_cap_upper_case), transform=h_ax.transAxes, size=subfig_caps_text_sz,
               color=subfig_color)

# Hist 5 ----
h_ax = axs[1, 1]
bin_count = 10
plt.sca(h_ax)
sns.histplot(inter_train_intervals, kde=True, ax=h_ax, bins=bin_count, legend=False,
             line_kws={'lw': 2, 'ls': '-'})
h_ax.lines[0].set_color('black')
plt.xlabel('Inter Train Interval [s]')
plt.xlim([0, 120])
plt.xticks(np.linspace(0, 120, 4))
plt.ylabel('')
plt.ylim([0, 24])
plt.yticks([0, 8, 16, 24])
h_ax.text(label_x_pos, label_y_pos, pf.cap_letter('e', sub_fig_cap_upper_case), transform=h_ax.transAxes, size=subfig_caps_text_sz,
               color=subfig_color)

# Hist 6
h_ax = axs[1, 2]
bin_count = 10
plt.sca(h_ax)
sns.histplot(duration_call_series, kde=True, ax=h_ax, bins=bin_count, legend=False,
             line_kws={'lw': 2, 'ls': '-'})
h_ax.lines[0].set_color('black')
plt.xlabel('Total Call Duration [s]')
plt.xlim([0, 6])
plt.xticks(np.linspace(0, 6, 4))
plt.ylabel('')
plt.ylim([0, 12])
plt.yticks([0, 4, 8, 12])
h_ax.text(label_x_pos, label_y_pos, pf.cap_letter('f', sub_fig_cap_upper_case), transform=h_ax.transAxes, size=subfig_caps_text_sz,
               color=subfig_color)

sns.despine()

# Save Plot to HDD
fig_path = '../figs/'
cm = 1 / 2.54  # centimeters in inches
fig.set_size_inches(14 * cm, 10 * cm)
fig.subplots_adjust(left=0.1, top=0.9, bottom=0.1, right=0.9, wspace=0.6, hspace=0.6)
fig.savefig(f'{fig_path}Fig_Histograms.pdf')
fig.savefig(f'{fig_path}Fig_Histograms.jpg', dpi=300)
# plt.show()
print('Saved Figs')
