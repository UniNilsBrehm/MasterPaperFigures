import matplotlib.pyplot as plt
import matplotlib
# import seaborn as sns
import numpy as np
import pandas as pd
import scipy.io.wavfile as wav
import matplotlib.mlab as ml
from plotstyle import PlotStyle
from plotting_functions import cap_letter
import matplotlib.patches as patches
from IPython import embed


def compute_audio_time_axis(wav_file):
    return np.arange(0, len(wav_file[1]) / wav_file[0], 1 / wav_file[0])


def scale_bar(axis, y_pos, length, unit, time_max, dy_text):
    """
    Adds a black scale bar to your axis.
    - default unit is secs but can be set to ms
    - color and line width can be changed inside the function code if needed.

    -----------
    Parameters:
        axis: scale bar is plotted on this axis
        y_pos: y-position of scale bar in y-units
        length: scale bar length in specified unit
        unit: unit of the scale bar (unit of length)
                default is secs.
        time_max: total duration of signal in secs
        dy_text: label text distance to scale bar (from below) in y-units
        sz_text: label text size
                default is 8
    """
    styles = PlotStyle()
    if unit == 'ms':
        length_bar = length / 1000  # convert to secs
    else:
        length_bar = length
    axis.hlines(y=y_pos, xmin=time_max - length_bar, xmax=time_max, **styles.boxScalebar)
    axis.text(time_max - length_bar / 2, y_pos - dy_text, f'{length} {unit}', ha='center', va='center', **styles.txtScalebar)


def annotate_label(ax, start, end, label):
    """
    Draws a rectangle from start to end coordinates, with a label below it centered.

    Parameters:
    - ax: matplotlib axes
    - start: tuple (x0, y0) for one corner of the rectangle
    - end: tuple (x1, y1) for opposite corner of the rectangle
    - label: text label to annotate below the rectangle
    """
    style = PlotStyle()
    # Determine bottom-left corner, width, and height
    x0, y0 = start
    x1, y1 = end

    lower_left_x = min(x0, x1)
    lower_left_y = min(y0, y1)
    width = abs(x1 - x0)
    height = abs(y1 - y0)

    # Draw rectangle
    rect = patches.Rectangle(
        (lower_left_x, lower_left_y),
        width=width,
        height=height,
        **style.barAnnotation
    )
    ax.add_patch(rect)

    # Place the label below the rectangle, centered horizontally
    text_x = lower_left_x + width / 2
    text_y = lower_left_y - 1.5 * height  # slightly below
    ax.text(
        text_x,
        text_y,
        label,
        ha='center',
        va='top',
        **style.txtAnnotation
    )


def main():
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Load Data
    # Import example moth song recording
    save_path = 'figs/'
    call_audio = wav.read('data/calls/melese_PK1300_01.wav')
    call_audio_02 = wav.read('data/calls/Eucereon_appunctata.wav')
    call_audio_03 = wav.read('data/calls/carales_PK1275.wav')
    call_audio_04 = wav.read('data/calls/Chrostosoma_thoracicum.wav')
    call_audio_05 = wav.read('data/calls/Creatonotos.wav')

    # Import Histogram data
    hist_dir = 'data/histogram/'
    inter_train_intervals = pd.read_csv(f'{hist_dir}inter_train_intervals.csv', index_col=0)
    inter_pulse_intervals = pd.read_csv(f'{hist_dir}inter_pulse_intervals.csv', index_col=0)
    single_pulse_duration = pd.read_csv(f'{hist_dir}single_pulse_duration.csv', index_col=0)
    frequencies = pd.read_csv(f'{hist_dir}freqs.csv', index_col=0)
    pulse_count_call_series = pd.read_csv(f'{hist_dir}pulse_count_callseries.csv', index_col=0)
    duration_call_series = pd.read_csv(f'{hist_dir}duration_callseries.csv', index_col=0)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Import Plot Styles
    styles = PlotStyle()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Rearrange Wav File
    t_audio = compute_audio_time_axis(call_audio)
    t_audio_02 = compute_audio_time_axis(call_audio_02)
    t_audio_03 = compute_audio_time_axis(call_audio_03)
    t_audio_04 = compute_audio_time_axis(call_audio_04)
    t_audio_05 = compute_audio_time_axis(call_audio_05)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # FIGURE
    # Figure Size (cm)
    fig_width_cm = 16
    fig_height_cm = 16

    # Create Grid
    fig_width = float(fig_width_cm / 2.54)
    fig_height = float(fig_height_cm / 2.54)

    fig = plt.figure(figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.1, top=0.95, bottom=0.05, right=0.95, wspace=0, hspace=0)

    # Create a grid that has mm resolution (height x width)
    grid = matplotlib.gridspec.GridSpec(nrows=int(fig_height_cm * 10), ncols=int(fig_width_cm * 10))
    ax = dict()

    # Panel A: Different timescale examples of one species (Melese sp.)
    ax['blocks'] = plt.subplot(grid[0:20, 0:75])  # Blocks of Call Series
    ax['call_series'] = plt.subplot(grid[25:45, 0:75])  # Call Series
    ax['call'] = plt.subplot(grid[50:70, 0:75])  # Call
    ax['active_train'] = plt.subplot(grid[75:95, 0:75])  # Active Train

    # Four more species
    ax['species_02'] = plt.subplot(grid[0:20, 85:160])
    ax['species_03'] = plt.subplot(grid[25:45, 85:160])
    ax['species_04'] = plt.subplot(grid[50:70, 85:160])
    ax['species_05'] = plt.subplot(grid[75:95, 85:160])

    # Quantitative description of calls in histograms (in one row)
    ax['hist1'] = plt.subplot(grid[110:140, 0:24])
    ax['hist2'] = plt.subplot(grid[110:140, 34:58])
    ax['hist3'] = plt.subplot(grid[110:140, 68:92])
    ax['hist4'] = plt.subplot(grid[110:140, 102:126])
    ax['hist5'] = plt.subplot(grid[110:140, 136:160])

    # ==================================================================================================================
    # Blocks of Call Series
    song_min = int(np.min(call_audio[1]))
    dy_text_val = int(np.max(call_audio[1]) * 0.3)
    ax['blocks'].plot(t_audio, call_audio[1], **styles.lsCalls)
    t_min = 0.25
    t_max = float(t_audio[-1])
    ax['blocks'].set_xlim(t_min, t_max)
    ax['blocks'].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax['blocks'], y_pos=song_min, length=500, unit='ms', time_max=t_max, dy_text=dy_text_val)

    # Call Series
    ax['call_series'].plot(t_audio, call_audio[1], **styles.lsCalls)
    t_min = 1.55
    t_max = 1.68
    ax['call_series'].set_xlim(t_min, t_max)
    ax['call_series'].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax['call_series'], y_pos=song_min, length=10, unit='ms', time_max=t_max, dy_text=dy_text_val)

    # Call
    ax['call'].plot(t_audio, call_audio[1], **styles.lsCalls)
    t_min = 1.006
    t_max = 1.04
    ax['call'].set_xlim(t_min, t_max)
    ax['call'].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax['call'], y_pos=song_min, length=2, unit='ms', time_max=t_max, dy_text=dy_text_val)

    # Active Train
    ax['active_train'].plot(t_audio, call_audio[1], **styles.lsCalls)
    t_min = 1.007
    t_max = 1.02
    ax['active_train'].set_xlim(t_min, t_max)
    ax['active_train'].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax['active_train'], y_pos=song_min, length=1, unit='ms', time_max=t_max, dy_text=dy_text_val)

    # Annotations
    inset_x = 0.5
    inset_y = 1.1
    ax['blocks'].text(inset_x, inset_y, 'Melese sp.', transform=ax['blocks'].transAxes, ha='center', va='center')

    bar_size = np.max(call_audio[1]) * 0.05
    min_y = np.min(call_audio[1])
    annotate_label(ax['active_train'], start=(1.0079, min_y), end=(1.0085, min_y + bar_size), label="pulse duration")

    min_y = min_y + np.max(call_audio[1]) * 0.1
    annotate_label(ax['call'], start=(1.0193, min_y), end=(1.0251, min_y + bar_size), label="ITI")
    annotate_label(ax['call'], start=(1.0335, min_y), end=(1.0345, min_y + bar_size), label="IPI")

    # ==================================================================================================================
    # Other Species
    # Nr 2: Eucereon appunctata
    inset_x = 0.5
    inset_y = 1.1
    dy_text_val = int(np.max(call_audio_02[1]) * 0.3)
    song_min = int(np.min(call_audio_02[1]))
    ax_name = 'species_02'
    ax[ax_name].plot(t_audio_02, call_audio_02[1], **styles.lsCalls)
    t_min = 0.28
    t_max = 0.54
    ax[ax_name].set_xlim(t_min, t_max)
    ax[ax_name].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax[ax_name], y_pos=song_min, length=10, unit='ms', time_max=t_max, dy_text=dy_text_val)
    ax[ax_name].text(inset_x, inset_y, 'Eucereon appunctata', transform=ax[ax_name].transAxes, ha='center', va='center')

    # Nr 3: Carales astur
    dy_text_val = int(np.max(call_audio_03[1]) * 0.3)
    song_min = int(np.min(call_audio_03[1]))
    ax_name = 'species_03'
    ax[ax_name].plot(t_audio_03, call_audio_03[1], **styles.lsCalls)
    t_min = 0.85
    t_max = 1.28
    ax[ax_name].set_xlim(t_min, t_max)
    ax[ax_name].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax[ax_name], y_pos=song_min, length=10, unit='ms', time_max=t_max, dy_text=dy_text_val)
    ax[ax_name].text(inset_x, inset_y, 'Carales astur', transform=ax[ax_name].transAxes, ha='center', va='center')

    # Nr 4: Chrostosoma thoracicum
    dy_text_val = int(np.max(call_audio_04[1]) * 0.3)
    song_min = int(np.min(call_audio_04[1]))
    ax_name = 'species_04'
    ax[ax_name].plot(t_audio_04, call_audio_04[1], **styles.lsCalls)
    t_min = 1.15
    t_max = 1.48
    ax[ax_name].set_xlim(t_min, t_max)
    ax[ax_name].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax[ax_name], y_pos=song_min, length=10, unit='ms', time_max=t_max, dy_text=dy_text_val)
    ax[ax_name].text(inset_x, inset_y, 'Chrostosoma thoracicum', transform=ax[ax_name].transAxes, ha='center',
                     va='center')

    # Nr 5: Creatonotos sp.
    dy_text_val = int(np.max(call_audio_05[1]) * 0.3)
    song_min = int(np.min(call_audio_05[1]))
    ax_name = 'species_05'
    ax[ax_name].plot(t_audio_05, call_audio_05[1], **styles.lsCalls)
    t_min = 0.35
    t_max = 0.88
    ax[ax_name].set_xlim(t_min, t_max)
    ax[ax_name].axis('off')  # Remove axis, ticks, and tick labels
    scale_bar(axis=ax[ax_name], y_pos=song_min, length=10, unit='ms', time_max=t_max, dy_text=dy_text_val)
    ax[ax_name].text(inset_x, inset_y, 'Creatonotos sp.', transform=ax[ax_name].transAxes, ha='center', va='center')

    # ==================================================================================================================
    # Histograms
    inset_x = 0.8
    inset_y = 0.9
    y_tick_count = 5
    x_tick_count = 3

    # 1. Single pulse duration
    data = single_pulse_duration
    ax_name = 'hist1'
    bin_count = int(np.sqrt(len(data)))  # Square Root Choice
    ax[ax_name].hist(data, bins=bin_count, **styles.histogram_style)
    ax[ax_name].text(
        inset_x, inset_y,
        f'n={len(data)}',
        transform=ax[ax_name].transAxes,
        ha='center',
        va='center'
    )
    # Remove the top and right spines
    ax[ax_name].set_ylabel('Count')
    ax[ax_name].set_xlabel('Pulse Duration [ms]')
    ax[ax_name].spines['top'].set_visible(False)
    ax[ax_name].spines['right'].set_visible(False)
    ax[ax_name].yaxis.set_major_locator(plt.MaxNLocator(y_tick_count))
    ax[ax_name].xaxis.set_major_locator(plt.MaxNLocator(x_tick_count))

    # 2. Inter Pulse Interval
    data = inter_pulse_intervals
    ax_name = 'hist2'
    bin_count = int(np.sqrt(len(data)))  # Square Root Choice
    ax[ax_name].hist(data, bins=bin_count, **styles.histogram_style)
    ax[ax_name].text(
        inset_x, inset_y,
        f'n={len(data)}',
        transform=ax[ax_name].transAxes,
        ha='center',
        va='center'
    )
    # Remove the top and right spines
    ax[ax_name].set_xlabel('Inter Pulse Interval [ms]')
    ax[ax_name].spines['top'].set_visible(False)
    ax[ax_name].spines['right'].set_visible(False)
    ax[ax_name].yaxis.set_major_locator(plt.MaxNLocator(y_tick_count))
    ax[ax_name].xaxis.set_major_locator(plt.MaxNLocator(x_tick_count))

    # 3. Pulse Count
    data = pulse_count_call_series
    ax_name = 'hist3'
    bin_count = int(2 * len(data) ** (1 / 3)) * 2  # Rice Rule
    ax[ax_name].hist(data, bins=bin_count, **styles.histogram_style)
    ax[ax_name].text(
        inset_x, inset_y,
        f'n={len(data)}',
        transform=ax[ax_name].transAxes,
        ha='center',
        va='center'
    )
    # Remove the top and right spines
    ax[ax_name].set_ylabel('Count')
    ax[ax_name].set_xlabel('Pulse Count')
    ax[ax_name].spines['top'].set_visible(False)
    ax[ax_name].spines['right'].set_visible(False)
    ax[ax_name].yaxis.set_major_locator(plt.MaxNLocator(y_tick_count))
    ax[ax_name].xaxis.set_major_locator(plt.MaxNLocator(x_tick_count))

    # 4. Inter Train Interval
    data = inter_train_intervals
    ax_name = 'hist4'
    bin_count = int(2 * len(data) ** (1 / 3)) * 2  # Rice Rule
    ax[ax_name].hist(data, bins=bin_count, **styles.histogram_style)
    ax[ax_name].text(
        inset_x, inset_y,
        f'n={len(data)}',
        transform=ax[ax_name].transAxes,
        ha='center',
        va='center'
    )
    # Remove the top and right spines
    ax[ax_name].set_xlabel('Inter Train Interval [ms]')
    ax[ax_name].spines['top'].set_visible(False)
    ax[ax_name].spines['right'].set_visible(False)
    ax[ax_name].yaxis.set_major_locator(plt.MaxNLocator(y_tick_count))
    ax[ax_name].xaxis.set_major_locator(plt.MaxNLocator(x_tick_count))

    # 5. Call Series Duration
    data = duration_call_series
    ax_name = 'hist5'
    bin_count = int(2 * len(data) ** (1 / 3)) * 2  # Rice Rule
    ax[ax_name].hist(data, bins=bin_count, **styles.histogram_style)
    ax[ax_name].text(
        inset_x, inset_y,
        f'n={len(data)}',
        transform=ax[ax_name].transAxes,
        ha='center',
        va='center'
    )
    # Remove the top and right spines
    ax[ax_name].set_xlabel('Total Call Series Duration [s]')
    ax[ax_name].spines['top'].set_visible(False)
    ax[ax_name].spines['right'].set_visible(False)
    ax[ax_name].yaxis.set_major_locator(plt.MaxNLocator(y_tick_count))
    ax[ax_name].xaxis.set_major_locator(plt.MaxNLocator(x_tick_count))

    # Add Sub-Figure Caps
    hist_x = -0.25
    hist_y = 1.1
    label_x_pos = [-0.1, -0.1, hist_x, hist_x, hist_x, hist_x, hist_x, hist_x]
    label_y_pos = [0.9, 0.9, hist_y, hist_y, hist_y, hist_y, hist_y, hist_y]
    subfig_caps_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    for i, v in enumerate(['blocks', 'species_02', 'hist1', 'hist2', 'hist3', 'hist4', 'hist5']):
        ax[v].text(
            label_x_pos[i],
            label_y_pos[i],
            cap_letter(subfig_caps_labels[i], styles.sub_fig_cap_upper_case),
            transform=ax[v].transAxes,
            size=styles.sub_fig_cap_text_size,
            color=styles.sub_fig_text_color,
            # fontfamily='Arial'
        )

    # Save Figure to HDD
    fig.savefig(f'{save_path}Fig_01_Call_structure.pdf')
    fig.savefig(f'{save_path}Fig_01_Call_structure.svg')
    # fig.savefig(f'{save_path}Fig_01_Call_structure.jpeg', dpi=300)
    plt.close(fig)
    print('Fig. 1: Call Structure, saved!')


if __name__ == '__main__':
    main()

