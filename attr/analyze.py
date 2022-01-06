from collections import defaultdict

import matplotlib.pyplot as plt


def label_distribution(txt, plot=False):
    label_dict = defaultdict(int)
    with open(txt, 'r') as f:
        for line in f.readlines():
            labels = line.split(' ')[1:]
            for label in labels:
                label_dict[label.strip()] += 1
    if plot:
        plt.bar(
            range(len(label_dict)), label_dict.values(), tick_label=list(label_dict.keys())
        )
        plt.show()

    return label_dict
