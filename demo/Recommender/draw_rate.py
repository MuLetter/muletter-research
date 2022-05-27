import matplotlib
import matplotlib.pyplot as plt


def draw_rate(self):
    _count = self.reco_['tracks']['seedId'].value_counts()
    print("음악 간 표준편차 - {}".format(round(_count.std())))

    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(16, 8))

    plt.bar(_count.index, _count.values, color='#EE68A4')
    plt.title("추천음악 수량현황")
    plt.xlabel("Track ID")
    plt.ylabel("Rate")

    plt.show()
