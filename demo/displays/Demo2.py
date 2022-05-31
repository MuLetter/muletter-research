from IPython.display import display, Markdown, clear_output


class Demo2:
    @staticmethod
    def _clear():
        clear_output(wait=True)

    @staticmethod
    def so_pt1(observer):
        display(
            Markdown("### 현재 SeedZone에는 <u>{}개의 Seed음악</u>들이 있습니다.".format(
                len(observer.features_df)
            ))
        )

    @staticmethod
    def so_pt3(observer):
        display(
            Markdown(
                "### 새로운 SeedZone 클러스터링 정보 <u>{}</u>가 등록 되었습니다.".format(str(observer.cluster_zone)))
        )
