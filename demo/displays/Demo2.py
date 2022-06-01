from IPython.display import display, Markdown, clear_output
from ..SeedZoneObserver import SeedZoneObserver
from ..CoordGenerator import CoordGenerator
from ..lib import DB


class Demo2:
    @staticmethod
    def _clear():
        clear_output(wait=True)

    @staticmethod
    def pt1():
        CoordGenerator.draw_map()

    @staticmethod
    def pt2():
        observer = SeedZoneObserver()

        observer.run()
        observer.sorting()
        observer.save()
        Demo2._clear()

        CoordGenerator.all_make_coords()

        display(
            Markdown("### 우체통 지도가 완성되었습니다.")
        )
        CoordGenerator.draw_map()

        display(
            Markdown("### 아래의 SeedZone Clustering 결과를 토대로 만들어졌어요.")
        )
        observer.kmeans.draw_cluster()
        CoordGenerator.draw_radar_map()

    @staticmethod
    def pt3():
        ran_mailbox = DB().random_mailbox()
        gen = CoordGenerator(str(ran_mailbox['_id']))

        gen.make_coords()
        gen.radar_test()
