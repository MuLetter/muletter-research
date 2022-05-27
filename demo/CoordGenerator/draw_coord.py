import matplotlib
import matplotlib.pyplot as plt

from math import pi
import numpy as np


def draw_coord(self):
    num_labels = self.K
    angles = [x/float(num_labels)*(2*pi)
              for x in range(num_labels)]
    angles += angles[:1]
    data = np.append(self.label_percentages_, self.label_percentages_[0])

    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize=(16, 6))

    # Radar : Before Coords
    ax = plt.subplot(1, 2, 1, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.tick_params(axis='x', which='major', pad=30)
    ax.set_rlabel_position(0)

    ax.plot(angles, data, color="#EE68A4")
    ax.fill(angles, data, color='#AC73CF')

    plt.xticks(angles[:-1], ["클러스터 {}".format(_) for _ in range(0, self.K)])
    plt.yticks(range(0, 101, 25), range(0, 101, 25), fontsize=10)
    plt.ylim(0, 100)
    plt.title("Radar : Before Coords")

    # Quadrant : After Coords
    ax = plt.subplot(1, 2, 2)
    data = self.point

    ax.axvline(0, color="#333", linewidth=1)
    ax.axhline(0, color="#333", linewidth=1)

    plt.scatter(data['x'], data['y'], color='#AC73CF', s=300, marker='v')

    plt.ylim(-100, 100)
    plt.xlim(-100, 100)
    ax.set_title("Quadrant : After Coords", pad=50)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.show()
