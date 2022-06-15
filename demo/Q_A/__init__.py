from ..lib import DB
from ..CoordGenerator import CoordGenerator, get_coord
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from IPython.display import Markdown, display


class QA:
    @staticmethod
    def view():
        ran_mailbox = DB().random_mailbox()
        gen = CoordGenerator(str(ran_mailbox['_id']))

        tracks = pd.DataFrame(gen.mailbox['tracks'])
        print(tracks.head())

        display(Markdown(
            "사용자에 우체통에는 이런 노래들이 등록되어 있어요. 그리고 이들은 모두 **추천 프로세스에 한 번씩 사용이 됐었기 때문에 SeedZone Database**에 들어있을테구요. 이 음악들이 **SeedZone Observer의 클러스터링 대상**이 됩니다.")
        )

        matplotlib.rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False

        lp = np.array(gen.mailbox['_labelPercentages'])
        print(lp)
        plt.figure(figsize=(8, 8))

        plt.pie(lp, autopct='%.1f%%', labels=[
                "클러스터 {}".format(_) for _ in range(len(lp))])

        plt.show()

        display(Markdown(
            "그러면 사용자가 가지고 있는 총 음악 개수에 각 라벨 숫자들을 그룹화하여 각 각의 클러스터 성향으 수를 나눠주면 사용자가 어느 성향의 음악들을 가지고 있는지 비율적으로 알 수 있겠죠?"))

        print("성향 0의 개수:", lp[lp == 0].size)
        print("좌표 생성에 쓰일 값 개수:", lp[lp != 0].size)

        detail, point = get_coord(lp, detail=True)

        plt.figure(figsize=(32, 4))

        for idx, _detail in enumerate(detail):
            ax = plt.subplot(1, len(detail), idx + 1)

            if idx == 0:
                point_movement = _detail
            else:
                point_movement += _detail

            ax.axvline(0, color="#333", linewidth=1)
            ax.axhline(0, color="#333", linewidth=1)

            plt.scatter(point_movement[0], point_movement[1],
                        color='#AC73CF', s=300, marker='v')

            plt.ylim(-100, 100)
            plt.xlim(-100, 100)

            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

        print(detail)
        plt.show()

        display(Markdown("여기서 클러스터 성향을 각도로, 그리고 비율을 거리로 사용하여 이를 사분면에 나타낸다면 각 클러스터 성향의 각도쪽으로 직선거리상으로는 어떻게 가야할까에 대한 변환을 해줍니다.<br/>그리고 이들을 모두 합해주면 됩니다. "))

        gen.make_coords()
        gen.draw_coord()
