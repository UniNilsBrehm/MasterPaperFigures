import csv
import numpy as np
from scipy.optimize import curve_fit
from IPython import embed
import string
from ctypes import windll
import pickle


def find_integer_panel_positions(
    total_width_mm=160,
    num_panels=5,
    min_gap_mm=1,
    max_gap_mm=10
):
    """
    Finds integer panel widths and gaps fitting the total figure width,
    and returns positions in millimeters for each panel.
    """
    num_gaps = num_panels - 1
    solutions = []

    for s in range(min_gap_mm, max_gap_mm + 1):
        remaining_width = total_width_mm - num_gaps * s
        if remaining_width <= 0:
            continue
        if remaining_width % num_panels == 0:
            w = remaining_width // num_panels
            # compute positions:
            positions = []
            current_left = 0
            for i in range(num_panels):
                start = current_left
                end = start + w
                positions.append((start, end))
                current_left = end + s  # move to next
            solutions.append({
                "panel_width": w,
                "gap": s,
                "positions": positions
            })

    if solutions:
        for sol in solutions:
            print(f"\npanel width = {sol['panel_width']} mm, gap = {sol['gap']} mm")
            print("positions:")
            for idx, (start, end) in enumerate(sol['positions']):
                print(f"  Panel {idx+1}: [{start} : {end}] mm")
    else:
        print("No integer solutions found in this range.")


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def select_data(rd_path, INTERVAL_MAS, INTERVAL_REC, GAP, FIFIELD, CALLS):
    # p = os.path.join('..', 'overview.csv')
    p = f'{rd_path}overview.csv'
    with open(p, newline='') as f:
        datasets = []
        reader = csv.reader(f)
        for row in reader:
            if INTERVAL_MAS:
                if row[3] == 'True':  # this is MAS
                    datasets.append(row[0])
            if INTERVAL_REC:
                if row[2] == 'True':  # this is RectIntervals
                    datasets.append(row[0])
            if GAP:
                if row[1] == 'True':  # this is GAP
                    datasets.append(row[0])
            if FIFIELD:
                if row[4] == 'True' and row[6] == 'Estigmene':  # this is FI
                    datasets.append(row[0])
            if CALLS:
                if row[5] == 'True':  # this is calls
                    datasets.append(row[0])
    datasets = sorted(datasets)
    return datasets


def cap_letter(letter, upper_case):
    if upper_case:
        letter = letter.upper()
    else:
        letter = letter.lower()
    return letter


# def plot_settings():
#     # Font:
#     # matplotlib.rc('font',**{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
#     # matplotlib.rcParams['font.sans-serif'] = 'Helvetica'
#     matplotlib.rcParams['font.sans-serif'] = 'Arial'
#     matplotlib.rcParams['font.family'] = 'sans-serif'
#     matplotlib.rcParams['font.size'] = 8
#
#     # Ticks:
#     matplotlib.rcParams['xtick.major.pad'] = '2'
#     matplotlib.rcParams['ytick.major.pad'] = '2'
#     matplotlib.rcParams['ytick.major.size'] = 4
#     matplotlib.rcParams['xtick.major.size'] = 4
#
#     # Title Size:
#     matplotlib.rcParams['axes.titlesize'] = 8
#
#     # Axes Label Size:
#     matplotlib.rcParams['axes.labelsize'] = 8
#
#     # Axes Line Width:
#     matplotlib.rcParams['axes.linewidth'] = 1
#
#     # Tick Label Size:
#     matplotlib.rcParams['xtick.labelsize'] = 8
#     matplotlib.rcParams['ytick.labelsize'] = 8
#
#     # Line Width:
#     matplotlib.rcParams['lines.linewidth'] = 1
#     matplotlib.rcParams['lines.color'] = 'k'
#
#     # Marker Size:
#     matplotlib.rcParams['lines.markersize'] = 2
#
#     # Error Bars:
#     matplotlib.rcParams['errorbar.capsize'] = 0
#
#     # Legend Font Size:
#     matplotlib.rcParams['legend.fontsize'] = 8
#
#     # Set pcolor shading
#     matplotlib.rcParams['pcolor.shading'] = 'auto'
#
#     # Sub Fig Cap Text Size
#     sub_fig_cap_text_size = 12
#     sub_fig_cap_upper_case = False
#
#     return matplotlib.rcParams, sub_fig_cap_text_size, sub_fig_cap_upper_case
#

def fit_function(x_fit, data):
    def func(xx, bottom, top, V50, Slope):
        # return a * np.exp(-d * x1) + c
        # return bottom + ((top-bottom)/(1+np.exp((V50-xx)/Slope)))
        return bottom + ((top-bottom)/(1+np.exp(-Slope*(xx-V50))))

    # Check for Nans
    if np.isnan(data).all():
        x, y = [np.nan] * 2
        popt = [np.nan] * 4
        perr = [np.inf] * 4
        return x, y, popt, perr
    # Remove NaNs
    idx = ~np.isnan(data)
    data = data[idx]
    x_fit = x_fit[idx]
    p0 = [0, np.max(data), np.max(x_fit)/2, 1]
    bounds = (0, [np.max(data)/2+10, np.max(data)*2+10, np.max(x_fit), np.inf])
    # print('p0:')
    # print(p0)
    # print('bounds:')
    # print(bounds)
    # print('-----------------')
    popt, pcov = curve_fit(func, x_fit, data, p0=p0, maxfev=10000,  bounds=bounds)
    x = np.linspace(np.min(x_fit), np.max(x_fit), 1000)
    y = func(x, *popt)
    y0 = func(popt[-2], *popt)
    perr = np.sqrt(np.diag(pcov))
    return x, y, popt, perr, y0


def fitting_fi_curves(dur, conv_rate):
    duration = []
    duration.append(dur)
    freqs = [[]] * len(conv_rate)
    for k in range(len(conv_rate)):
        freqs[k] = int(conv_rate[k][0])
    freqs = sorted(freqs)
    estimated_th_conv = np.zeros(len(freqs))

    # Fit Boltzman
    x_conv, y_conv, params_conv, perr_conv, y0_conv = fit_function(conv_rate[:, 0], conv_rate[:, 1])

    # Compute Fitting Error
    # print(str(ff) + ' kHz: Summed Error = ' + str(perr_conv[2]+perr_conv[1]))
    k_conv = params_conv[-1]
    I0_conv = params_conv[-2]
    slope_conv = (params_conv[1]-params_conv[0])*k_conv / 4
    c_conv = y0_conv / slope_conv - I0_conv
    summed_error_conv = perr_conv[1]

    # Estimate Thresholds from Boltzman Fit
    th_conv_fit = I0_conv - (2/k_conv)

    # Linear approximation
    conv_approx = slope_conv * (x_conv + c_conv)

    # # V50
    # th_conv_fit = params_conv[2]
    limit_conv = np.min(y_conv) * 1.5

    no_th = False
    control_for_no_response = True
    if control_for_no_response:
        if np.max(y_conv) < limit_conv or np.max(y_conv) <= 0 or slope_conv <= 0:
            estimated_th_conv = np.max(conv_rate[:, 0])
            no_th = True
        else:
            estimated_th_conv = th_conv_fit
    else:
        estimated_th_conv = th_conv_fit

    return estimated_th_conv, conv_approx, x_conv, y_conv


def pickle_stuff(file_name, data=None):
    if data is None:
        with open(file_name, 'rb') as handle:
            result = pickle.load(handle)
        return result
    else:
        with open(file_name, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True
