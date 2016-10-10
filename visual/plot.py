#!/usr/bin/env pytnon
# -*- coding: utf-8 -*-

import datetime

import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties

matplotlib.rc('font', **{'sans-serif' : 'Arial',
                           'family' : 'sans-serif'})


matplotlib.use('Agg')

PERIOD = 0.004

def plot(data1, data2, team=None):
    plt.clf()

    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    now = datetime.datetime.now().strftime('%d-%m-%y %X')

    if team is None:
        plt.suptitle(now)
    else:
        plt.suptitle(' '.join([team, now]))

    x_list = map(lambda x: x * PERIOD + PERIOD, range(len(data1)))

    ax0 = plt.subplot(gs[0])
    ax0.set_xlabel(u'Время (с)')
    ax0.set_ylabel(u'Мощность (мкВт)')
    ax0.plot(x_list, data1, 'b-')
    ax0.grid(True)

    ax1 = plt.subplot(gs[1])
    ax1.set_xlabel(u'Время (с)')
    ax1.set_ylabel(u'\u03ffнергия (мкВт·ч)')
    # ax1.set_ylabel(u'Энергия (мкВт·ч)')
    ax1.plot(x_list, data2, 'b-')
    ax1.grid(True)

    plt.subplots_adjust(top=0.75)

    plt.tight_layout()

    if team is None:
        filepath = 'foo.pdf'
    else:
        filepath = os.path.join('out', ' '.join([team, now.replace(':', '-') + '.pdf']))

    with PdfPages(filepath) as pdf:
        pdf.savefig()


def main():
    a = [1, 2, 3, 4, 5, 4, 3, 4, 5, 4, 3, 2, 1]
    b = [1, 3, 6, 10, 15, 19, 22, 26, 31, 35, 38, 40, 41]
    plot(a, b)


if __name__ == '__main__':
    main()
