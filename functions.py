
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from pathlib import Path
import math

def load_xy(data_dir, filename="data1", cols=(0, 1), header_row=0):
    """
    Lädt eine Datei aus data_dir und gibt ausgewählte Spalten als numpy arrays zurück.

    Unterstützte Formate: csv, txt, dat, tsv (automatische Erkennung des Separators)

    Parameters
    ----------
    data_dir : str
        Ordnerpfad
    filename : str
        Dateiname ohne oder mit Endung
    cols : int, str oder Liste/Tuple davon
        Spalten die geladen werden sollen

    Returns
    -------
    arrays : np.ndarray oder list[np.ndarray]
    """

    # Falls keine Endung angegeben → suche passende Datei
    if not os.path.splitext(filename)[1]:
        for ext in [".csv", ".txt", ".dat", ".tsv"]:
            path = os.path.join(data_dir, filename + ext)
            if os.path.exists(path):
                filename = filename + ext
                break

    filepath = os.path.join(data_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")

    # Datei mit pandas laden
    try:
        df = pd.read_csv(
            filepath,
            sep=None,        # deine Datei ist tab-getrennt
            engine="python"
        )
    except Exception:
        data = np.loadtxt(filepath)

        if isinstance(cols, (list, tuple)):
            return [data[:, col] for col in cols]
        else:
            return data[:, cols]

    # Spalten auswählen
    if isinstance(cols, (list, tuple)):
        arrays = [
            (df.iloc[:, col] if isinstance(col, int) else df[col]).to_numpy()
            for col in cols
        ]
    else:
        arrays = (
            df.iloc[:, cols] if isinstance(cols, int) else df[cols]
        ).to_numpy()

    return arrays

def plot_datasets(data, xlabel="X-Axis", ylabel="Y-Axis", xscale="linear", yscale="linear", title="", figsize=(6,4), fontsizetitle=20, fontsize=12, set_x_lim=False, x_min=0, x_max=1, set_y_lim=False, y_min=0, y_max=1, plot=False, legendsloc = "best"):

    """
    Plottet mehrere Datensätze mit anpassbaren Achsen und Stilen.

    :param xlabel: Beschriftung der X-Achse
    :param ylabel: Beschriftung der Y-Achse
    :param xscale: Skala der X-Achse ('linear' oder 'log')
    :param yscale: Skala der Y-Achse ('linear' oder 'log')
    :param title: Titel des Plots
    :param figsize: Größe der Figur (Breite, Höhe) voreingestellt auf 8:6
    :param fontsizetitle: Schriftgröße für Titel
    :param fontsize: Schriftgröße für Achsenbeschriftung
    :param set_x_lim: Durch True werden x_min und x_max freigeschaltet
    :param x_min: Minimum der x-Achse
    :param x_max: Maximum der x-Achse
    : ... analog für y-Achse
    """


    
#   Erstellen des Plots:
    fig = plt.figure(figsize=figsize) # Erstellen der Abbildung mit ihren Maßen
#   Festlegung der Schrifteinstellungen für Legende und Rest:
    font_title = fm.FontProperties(family='Arial', size=fontsizetitle)
    font_all = fm.FontProperties(family='Arial', size=fontsize)

    
    for entry in data: # Für jeden Datensatz in data werden die relevanten Infos ausgelesen
        x, y, label, style, art, size, color = entry[:7]
        yerr = entry[7] if style == 'errorbar' and len(entry) > 7 else None
        xerr = entry[8] if style == 'errorbar' and len(entry) > 8 else None
        
        if style == 'line': # Plot einer Kurve
            plt.plot(x, y, label=label, linestyle=art, linewidth=size, color=color)
        elif style == 'datapoints': # Plot einer Datenwolke
            plt.scatter(x, y, label=label, marker=art, s=size, color=color)
        elif style == 'errorbar': # Plot einer Datenwolke mit Fehler
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, label=label, fmt=art, markersize=size, linestyle='None', capsize=3, color=color)
        elif style == "text":
            plt.text(x, y, label, fontsize=size, color=color)
        
    plt.xlabel(xlabel, fontproperties = font_all)
    plt.ylabel(ylabel, fontproperties = font_all)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.title(title, fontproperties = font_title)
    plt.legend(prop = font_all, borderaxespad = 0.9, loc=legendsloc)
    
#   Falls in der Eingabe "True" angegeben wurde, können die Achsen manuell begrenzt werden
    if set_x_lim == True:
        plt.xlim(x_min, x_max)
    if set_y_lim == True:
        plt.ylim(y_min, y_max)
    
    plt.tick_params(axis='x', which='major', direction='in', width=1, length=5, top=True,  bottom=True, labelsize=fontsize)
    plt.tick_params(axis='y', which='major', direction='in', width=1, length=5, left=True, right=True,  labelsize=fontsize)

    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.tick_params(
        axis='both',          # 'x', 'y' oder 'both'
        which='minor',         # 'major', 'minor' oder 'both'
        #width=1.5, length=10, labelsize=fontsize,
        bottom=True,          # Ticks am unteren Rand anzeigen
        top=True,             # Ticks am oberen Rand anzeigen
        left=True,            # Ticks am linken Rand anzeigen
        right=True,
        direction='in')           # Ticks am rechten Rand anzeigen

    if plot == True:
        plt.show()

    return fig

import os
import re

def write_values_to_tex(values_dict, values_dir,delete_existing=False):
    _write_values_to_tex(values_dict, values_dir,delete_existing=delete_existing)

def round2(val, err, mode="normal"):
    # 1. Bestimme die Größenordnung der Unsicherheit
    if err == 0 or math.isnan(err):
        return rf"${val:.2f} \pm 0.00$" # Oder ein anderes Standardformat     
    order_of_magnitude = math.floor(math.log10(abs(err)))
    
    # 2. Wir wollen zwei signifikante Stellen für den Fehler
    # Wir runden auf die Stelle: (Größenordnung - 1)
    precision = -(order_of_magnitude - 1)
    
    # 3. Runden beider Werte
    rounded_err = round(err, precision)
    rounded_val = round(val, precision)
    
    # 4. Formatierung für den String (Padding mit Nullen falls nötig)
    fmt = f".{max(0, precision)}f"
    if mode == 2:
        return rf"${format(rounded_val, fmt)} \pm {format(rounded_err, fmt)}$"
    if mode == "normal":
        return rf"{format(rounded_val, fmt)}",  rf"{format(rounded_err, fmt)}"


def slope(X, Y, sigma_Y=None):
    X = np.asarray(X)
    Y = np.asarray(Y)

    # Falls Fehler angegeben sind, berechne Gewichte
    if sigma_Y is not None:
        sigma_Y = np.asarray(sigma_Y)
        w = 1 / sigma_Y
    else:
        w = None

    # Fit + Kovarianzmatrix
    p, cov = np.polyfit(X, Y, 1, w=w, cov=True)

    m, b = p
    sigma_m = np.sqrt(cov[0,0])
    sigma_b = np.sqrt(cov[1,1])

    return m, b, sigma_m, sigma_b
