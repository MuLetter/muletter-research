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
        if hasattr(self, "parsed_labels_"):
            if np.isin(label, self.parsed_labels_):
                feature_color = "#EE68A4"
                features_lw = 1.25
                cluster_color = "#EE68A4"
                cluster_lw = 1.25
            else:
                feature_color = "white"
                features_lw = 0
                cluster_color = "white"
                cluster_lw = 0
        else:
            feature_color = "#2880D8"
            features_lw = 0.25
            cluster_color = "#EE68A4"
            cluster_lw = 3
        _features = features[kmeans.labels_ == label]
        _cluster = kmeans.clusters_[label]

        ax = plt.subplot(r, 4, label + 1)
        ax.plot(cols, _features.T, color=feature_color,
                linewidth=features_lw)
        ax.plot(cols, _cluster, color=cluster_color,
                linewidth=cluster_lw)
        ax.set_title("클러스터 {}".format(label))
        plt.ylabel("Value")
        plt.xlabel("Feature")

    plt.show()
