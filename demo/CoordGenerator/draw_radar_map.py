from ..lib import DB
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from math import pi


@staticmethod
def draw_radar_map():
    db = DB()

    mailboxes = [_ for _ in db.mailbox.find()]
    ran_mailboxes = np.random.choice(mailboxes, 8)
    points = np.array([[_['point']['x'], _['point']['y']] for _ in mailboxes])

    K = db.cluster_zone.find().sort("version", -1)[0]['K']

    num_labels = K
    angles = [x/float(num_labels)*(2*pi)
              for x in range(num_labels)]
    angles += angles[:1]

    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize=(32, 16))

    mailbox_cnt = 0
    for idx, left_idx in enumerate(range(1, 16, 6)):
        for _idx, radar_idx in enumerate(range(left_idx, left_idx + 3)):
            if radar_idx == 15:
                ax = plt.subplot(3, 6, radar_idx)
                ax.text(0.5, 0.5, "+{}".format(len(mailboxes) - len(ran_mailboxes)),
                        fontsize=64,
                        color="#333",
                        va='center',
                        ha='center',
                        transform=ax.transAxes
                        )
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.yaxis.set_visible(False)
                ax.xaxis.set_visible(False)
            else:
                ax = plt.subplot(3, 6, radar_idx, polar=True)
                ax.set_theta_offset(pi / 2)
                ax.set_theta_direction(-1)
                ax.set_xticklabels('')
                ax.set_yticklabels('')
                ax.set_rlabel_position(0)

                ax.plot(angles, np.append(ran_mailboxes[mailbox_cnt]['_labelPercentages'],
                                          ran_mailboxes[mailbox_cnt]['_labelPercentages'][0]), color="#EE68A4")
                ax.fill(angles, np.append(ran_mailboxes[mailbox_cnt]['_labelPercentages'],
                                          ran_mailboxes[mailbox_cnt]['_labelPercentages'][0]), color="#AC73CF")
                mailbox_cnt += 1

            ax.set_ylim(-100, 100)
            ax.set_xlim(-100, 100)

    gs = fig.add_gridspec(3, 6)
    ax = fig.add_subplot(gs[:, 3:6])

    ax.axvline(0, color="#333", linewidth=3)
    ax.axhline(0, color="#333", linewidth=3)

    ax.scatter(points[:, 0], points[:, 1], color='#AC73CF', s=500, marker='v')

    plt.ylim(-100, 100)
    plt.xlim(-100, 100)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_title("좌표 현황")

    plt.show()
