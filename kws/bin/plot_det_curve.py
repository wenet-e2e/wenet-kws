# Copyright (c) 2021 Binbin Zhang(binbzha@qq.com)
#                    Menglong Xu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


def load_stats_file(stats_file):
    values = []
    with open(stats_file, 'r', encoding='utf8') as fin:
        for line in fin:
            arr = line.strip().split()
            threshold, fa_per_hour, frr = arr
            values.append([float(fa_per_hour), float(frr)])
    values.reverse()
    return np.array(values)


def plot_det_curve(keywords, stats_dir, figure_file):
    plt.figure(dpi=200)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = 12

    for index, keyword in enumerate(keywords):
        stats_file = os.path.join(stats_dir, 'stats.' + str(index) + '.txt')
        values = load_stats_file(stats_file)
        plt.plot(values[:, 0], values[:, 1], label=keyword)

    plt.xlim([0, 5])
    plt.ylim([0, 0.35])
    plt.xticks([0, 1, 2, 3, 4, 5], ['0', '1', '2', '3', '4', '5'])
    plt.yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35],
               ['0', '5', '10', '15', '20', '25', '30', '35'])
    plt.xlabel('False Alarm Per Hour')
    plt.ylabel('False Rejection Rate (\\%)')
    plt.grid(linestyle='--')
    plt.legend(loc='best', fontsize=16)
    plt.savefig(figure_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='plot det curve')
    parser.add_argument(
        '--keywords',
        required=True,
        help='keywords, must in the same order as in "dict/words.txt" separated by ", "')
    parser.add_argument('--stats_dir', required=True, help='dir of stats files')
    parser.add_argument(
        '--figure_file',
        required=True,
        help='path to save det curve')

    args = parser.parse_args()

    keywords = args.keywords.strip().split(', ')
    plot_det_curve(keywords, args.stats_dir, args.figure_file)
