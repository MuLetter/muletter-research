import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def draw_filtering(self):
    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    after_filtering_features = self.features['default'][np.any(np.isin(self.features['default'],
                                                                       np.append(
        self.user['tracks']['trackId'], self.reco_['tracks']['trackId'])
    ),
        axis=1)]
    after_filtering_user_idx = np.any(
        np.isin(after_filtering_features, self.user['tracks']['trackId']), axis=1)

    after_filtering_norm_features = self.features['norm'][np.any(np.isin(self.features['default'],
                                                                         np.append(
        self.user['tracks']['trackId'], self.reco_['tracks']['trackId'])
    ),
        axis=1)]

    cols = self.user['features'].columns.values[1:]
    _list = [("필터링 전", self.features['norm'], self.user_idx),
             ("필터링 후", after_filtering_norm_features, after_filtering_user_idx)]

    plt.figure(figsize=(24, 6))
    for idx, (title, features, user_idx) in enumerate(_list):
        ax = plt.subplot(1, 2, idx+1)

        ax.plot(cols, features[user_idx][:1].T,
                color="#EE68A4", linewidth=2, label='사용자 음악 데이터')
        ax.plot(cols, features[:1].T, color="#2880D8",
                linewidth=0.1, label='추천 음악 데이터')
        ax.plot(cols, features[~user_idx].T,
                color="#2880D8", linewidth=0.1)
        ax.plot(cols, features[user_idx].T, color="#EE68A4", linewidth=2)

        ax.set_title(title)
        plt.ylabel("Value")
        plt.xlabel("Feature")
        plt.legend(loc='upper right')

    plt.show()

    return features[~user_idx], features[user_idx]
