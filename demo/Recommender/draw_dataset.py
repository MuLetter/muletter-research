import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def draw_dataset(self):
    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    cols = self.user['features'].columns.values[1:]
    user_idxes = np.isin(
        self.merged['features']['trackId'], self.user['features']['trackId'])

    plt.figure(figsize=(24, 6))

    for idx, key in enumerate(self.features.keys()):
        ax = plt.subplot(1, 2, idx+1)

        if key == "default":
            title = "일반"
            features = self.features[key][:, 1:]
        elif key == "norm":
            title = "정규화"
            features = self.features[key]

        ax.plot(cols, features[user_idxes][:1].T,
                color="#EE68A4", linewidth=2, label='사용자 음악 데이터')
        ax.plot(cols, features[:1].T, color="#2880D8",
                linewidth=0.1, label='추천 음악 데이터')
        ax.plot(cols, features.T, color="#2880D8", linewidth=0.1)
        ax.plot(cols, features[user_idxes].T, color="#EE68A4", linewidth=2)
        ax.set_title("{} 데이터셋 현황".format(title))

        plt.ylabel("Value")
        plt.xlabel("Features")

        plt.legend(loc='upper right')

    plt.show()
