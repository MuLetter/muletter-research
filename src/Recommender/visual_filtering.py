import datetime as dt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances as euc


def visual_filtering(self):
    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    features = self.features_bak
    norm_features = self.norm_features_bak

    my_tracks = self.my_tracks
    reco_tracks = self.reco_musics

    chk_idxes = my_tracks['trackId'].values
    my_idxes = features[np.isin(features['trackId'], chk_idxes)].index
    reco_idxes = features[~np.isin(features['trackId'], chk_idxes)].index

    my_features = norm_features[my_idxes]
    reco_features = norm_features[reco_idxes]

    titles = ['필터링 전', '필터링 후']
    plt.figure(figsize=(16, 4))

    for idx in range(0, 2):
        ax = plt.subplot(1, 2, idx+1)

        euc_check = euc(my_features, reco_features).mean()
        ax.plot(my_features.T, c='g', linewidth=1)
        ax.plot(reco_features.T, c='g', linewidth=0.03)

        reco_features = norm_features[
            features[np.isin(features['trackId'],
                             reco_tracks['trackId'])].index
        ]

        ax.text(
            0.05,
            0.9,
            "평균거리 : {}".format(round(euc_check * 100) / 100),
            ha='left',
            transform=ax.transAxes
        )
        ax.set_title(titles[idx])

    now_time = dt.datetime.now().strftime("%Y%m%dT%H%M%Sms%f")
    self.visual_image = "./visual_images/visual_{}.png".format(now_time)
    plt.savefig(self.visual_image)
