import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import euclidean_distances as euc


def radar_test(self):
    matplotlib.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    map_size = -100, 100

    mailbox_docs = self.db.mailbox.find({"_id": {"$ne": self.mailbox_id}})

    mailboxes = [_ for _ in mailbox_docs]
    target_mailbox = self.mailbox

    points = np.array([[_['point']['x'], _['point']['y']] for _ in mailboxes])
    target_points = np.array(
        [[target_mailbox['point']['x'], target_mailbox['point']['y']]])
    ids = np.array([_['_id'] for _ in mailboxes])

    _euc = euc(target_points, points)[0]

    _in_idx = _euc.argsort()[:5]
    _out_idx = _euc.argsort()[-5:]
    print(_out_idx)

    in_points = points[_in_idx]
    out_points = points[_out_idx]
    print(in_points)
    print(out_points)

    print(self.mailbox_id)

    print(ids[_in_idx])
    print(ids[_out_idx])

    fig = plt.figure(figsize=(16, 14))

    quadrant_targets = [points, in_points, out_points]
    gs = fig.add_gridspec(3, 3)
    _axs = [fig.add_subplot(gs[0, :3]),
            plt.subplot(3, 3, 4),
            plt.subplot(3, 3, 7)]
    title = ["우체통 지도 현황", "반경 내 우체통", "반경 외 우체통"]
    for idx, target in enumerate(quadrant_targets):
        ax = _axs[idx]

        ax.axvline(0, color="#999", lw=0.5)
        ax.axhline(0, color="#999", lw=0.5)
        ax.scatter(target[:, 0], target[:, 1], color="#AC73CF", s=50)
        ax.scatter(target_points[:, 0], target_points[:,
                   1], color="#EE68A4", s=200, marker="v")
        ax.set_title(title[idx])
        ax.set_xlim(map_size[0], map_size[1])
        ax.set_ylim(map_size[0], map_size[1])

        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.label.set_color('#666')
        ax.yaxis.label.set_color('#666')

    target_label_percentages = np.array(target_mailbox['_labelPercentages'])

    label_percentages = np.array([_['_labelPercentages'] for _ in mailboxes])
    in_label_percentages = label_percentages[_in_idx].mean(axis=0)
    out_label_percentages = label_percentages[_out_idx].mean(axis=0)

    bar_items = [in_label_percentages, out_label_percentages]
    _axs = [plt.subplot(3, 3, 5), plt.subplot(3, 3, 8)]
    for idx, per in enumerate(bar_items):
        ax = _axs[idx]
        ax.bar(range(0, self.K),
               per, color="#EE68A4", alpha=0.3)
        ax.bar(range(0, self.K),
               target_label_percentages, color="#AC73CF", alpha=0.3)

    _axs = [plt.subplot(3, 3, 6), plt.subplot(3, 3, 9)]
    for idx, per in enumerate(bar_items):
        ax = _axs[idx]
        chk = np.array([])

        for idx, _per in enumerate(per):
            _target = target_label_percentages[idx]

            if _target == 0 or _per == 0:
                chk = np.append(chk, 0)
            else:
                if _target > _per:
                    chk = np.append(chk, _per)
                else:
                    chk = np.append(chk, _target)

        ax.bar(range(0, self.K),
               chk, color="#EE68A4", alpha=0.3)
        ax.bar(range(0, self.K),
               chk, color="#AC73CF", alpha=0.3)
        _max = target_label_percentages.max() \
            if target_label_percentages.max() > per.max() \
            else per.max()
        ax.set_ylim(0, _max)

    plt.show()
