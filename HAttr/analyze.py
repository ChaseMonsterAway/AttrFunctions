import os
from collections import defaultdict

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
mpl.rcParams['font.size'] = 12  # 字体大小
mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号


def label_distribution(txt, plot=False):
    label_dict = defaultdict(int)
    with open(txt, 'r') as f:
        for line in f.readlines():
            labels = line.split(' ')[1:]
            for label in labels:
                label_dict[label.strip()] += 1
    if plot:
        plt.bar(
            range(len(label_dict)), label_dict.values()
        )
        tick_label = list(label_dict.keys())
        for x in range(len(label_dict)):
            plt.text(x, -1, tick_label[x], fontsize=8, verticalalignment='center', horizontalalignment='center',
                     rotation=45)
        plt.show()

    return label_dict


def plot_diffs_label_distribution(txt1, txt2):
    label_dist1 = label_distribution(txt1)
    label_dist2 = label_distribution(txt2)
    total_keys = list(set(list(label_dist1.keys()) + list(label_dist2.keys())))
    value_dis1 = [label_dist1[tk] for tk in total_keys]
    value_dis2 = [label_dist2[tk] for tk in total_keys]
    x = range(len(total_keys))
    x2 = [_ + 0.35 for _ in x]
    plt.bar(x, value_dis1, width=0.35, label=os.path.basename(txt1))
    plt.bar(x2, value_dis2, width=0.35, label=os.path.basename(txt2))

    for idx in range(len(total_keys)):
        plt.text(x[idx] + 0.15, -1, total_keys[idx], fontsize=8,
                 verticalalignment='center',
                 horizontalalignment='center',
                 rotation=45)
    plt.show()
