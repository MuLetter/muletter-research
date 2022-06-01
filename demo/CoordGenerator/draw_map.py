import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from ..lib import DB


@staticmethod
def draw_map():
    db = DB()
    map_size = -100, 100
    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    mailbox_docs = db.mailbox.find({"point": {"$exists": True}})
    points = np.array([[_['point']['x'], _['point']['y']]
                      for _ in mailbox_docs])

    plt.figure(figsize=(16, 8))
    ax = plt.subplot(1, 1, 1)

    ax.axvline(0, color='#999', lw=0.5)
    ax.axhline(0, color='#999', lw=0.5)
    ax.scatter(points[:, 0], points[:, 1], s=200, color='#AC73CF')

    plt.ylim(map_size[0], map_size[1])
    plt.xlim(map_size[0], map_size[1])

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.xaxis.label.set_color('#666')
    ax.yaxis.label.set_color('#666')

    plt.show()
