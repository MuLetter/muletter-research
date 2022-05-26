import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math as mt


def draw_cluster(self):
    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    kmeans = self.kmeans
    features = self.features['norm']
    cols = self.user['features'].columns.values[1:]

    r, c = mt.ceil(kmeans.K / 4), 4
    plt.figure(figsize=(38, 8 * mt.ceil(self.kmeans.K / 4)))

    for label in np.unique(kmeans.labels_):
        _features = features[kmeans.labels_ == label]
        _cluster = kmeans.clusters_[label]

        ax = plt.subplot(r, 4, label + 1)
        ax.plot(cols, _features.T, color="#2880D8",
                linewidth=0.5)
        ax.plot(cols, _cluster, color="#EE68A4",
                linewidth=3)
        ax.set_title("클러스터 {}".format(label))
        plt.ylabel("Value")
        plt.xlabel("Feature")

    plt.show()
