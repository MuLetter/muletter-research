from IPython.display import display, Markdown, clear_output


class Demo1:
    @staticmethod
    def _clear():
        clear_output(wait=True)

    @staticmethod
    def pt1(mailbox_id):
        display(
            Markdown("### 우체통 <u>'{}'</u>이 등록되었습니다.".format(mailbox_id))
        )

    @staticmethod
    def pt2_1(recommender):
        display(Markdown(
            "### 우체통 <u>'{}'</u>에는 총 <u>{}개의 음악</u>이 등록 되어 있습니다.".format(
                recommender.mailbox_id, recommender.user['tracks'].index.size)
        ))

    @staticmethod
    def pt2_2(recommender):
        display(Markdown(
            "### 우체통 <u>'{}'</u>의 음악들의 <u>Spoitfy 추천 음악은 총 {} 개</u> 입니다.".format(
                recommender.mailbox_id, recommender.reco['tracks'].index.size)
        ))

    @staticmethod
    def pt3(recommender):
        display(Markdown(
            "### Seed음악과 추천음악의 병합이 완료되었습니다. 총 <u>{}개의 음악</u>들로 구성되어 있습니다.".format(
                recommender.merged['tracks'].index.size)
        ))

    @staticmethod
    def pt6_1(recommender):
        display(Markdown(
            "### 우체통 <u>'{}'</u>의 음악들은 <u>클러스터{}번</u>에 속해 있습니다.".format(recommender.mailbox_id,
                                                                        recommender.parsed_labels_)
        ))

    @staticmethod
    def pt6_2(recommender):
        display(
            Markdown("### 우체통 <u>'{}'</u>를 위한 총 <u>{}개의 추천음악</u>이 선정 되었습니다.".format(
                recommender.mailbox_id,
                recommender.reco_['tracks']['trackId'].size))
        )

    @staticmethod
    def pt7(recommender):
        _count = recommender.reco_['tracks']['seedId'].value_counts()
        display(
            Markdown(
                "### 현재 Seed음악들의 추천음악 수량 표준편차는 <u>{}</u> 입니다.".format(
                    round(_count.std()))
            )
        )

    @staticmethod
    def pt8(recommender, mail_id):
        display(
            Markdown(
                "### 우체통 <u>{}</u>를 위한 음악편지 <u>{}</u>를 넣어놨어요.".format(
                    recommender.mailbox_id, mail_id)
            )
        )
