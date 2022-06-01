from IPython.display import display, Markdown, clear_output
import matplotlib
import matplotlib.pyplot as plt


class Demo1:
    @staticmethod
    def _clear():
        clear_output(wait=True)

    @staticmethod
    def pt1(mailbox_id, spotify):
        display(
            Markdown("### 우체통 <u>'{}'</u>이 등록되었습니다.".format(mailbox_id))
        )
        display(
            Markdown(
                "**총 <u>{}개</u>의 Seed음악이 들어있습니다.**".format(len(spotify.sel_tracks)))
        )

    @staticmethod
    def pt2(recommender):
        display(Markdown(
            "### 우체통 <u>'{}'</u>의 음악들의 <u>Spoitfy 추천 음악은 총 {} 개</u> 입니다.".format(
                recommender.mailbox_id, recommender.reco['tracks'].index.size)
        ))

    @staticmethod
    def pt3(recommender):
        recommender.merge()
        recommender.data_preprocessing()
        recommender.run()

        Demo1._clear()
        Demo1.pt3_1(recommender)
        Demo1.pt3_2(recommender)
        Demo1.pt3_3(recommender)
        Demo1.pt3_4(recommender)
        Demo1.pt3_5(recommender)
        Demo1.pt3_6(recommender)

    @staticmethod
    def pt3_1(recommender):
        display(Markdown(
            "### 데이터 병합"))
        display(Markdown(
            "**Seed음악과 추천음악의 병합이 완료되었습니다. 총 <u>{}개의 음악</u>들로 구성되어 있습니다.**".format(
                recommender.merged['tracks'].index.size)
        ))
        print(recommender.merged['features'].head())

    @staticmethod
    def pt3_2(recommender):
        display(Markdown(
            "### 데이터 전처리"))
        display(Markdown(
            "**데이터셋의 Min-Max Normalization 작업이 완료되었습니다.**".format(
                recommender.merged['tracks'].index.size)
        ))
        recommender.draw_dataset()

    @staticmethod
    def pt3_3(recommender):
        display(Markdown(
            "### KMeans Clustering Fitting"))
        display(Markdown(
            "**클러스터링 작업이 완료되었습니다.**".format(
                recommender.merged['tracks'].index.size)
        ))
        recommender.draw_cluster()

    @staticmethod
    def pt3_4(recommender):
        recommender.parse_reco_cluster()
        display(Markdown(
            "### KMeans Clustering Parsing"))
        display(Markdown(
            "**우체통 <u>'{}'</u>의 음악들은 <u>클러스터{}번</u>에 속해 있습니다.**".format(recommender.mailbox_id,
                                                                        recommender.parsed_labels_)
        ))
        recommender.draw_cluster()
        display(
            Markdown("**우체통 <u>'{}'</u>를 위한 총 <u>{}개의 추천음악</u>이 선정 되었습니다.**".format(
                recommender.mailbox_id,
                recommender.reco_['tracks']['trackId'].size))
        )

    @staticmethod
    def pt3_5(recommender):
        matplotlib.rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(32, 8))

        ax = plt.subplot(1, 2, 1)

        prev_count = recommender.reco_['tracks']['seedId'].value_counts()

        ax.bar(prev_count.index, prev_count.values, color='#EE68A4')
        ax.set_title("추천음악 수량현황")
        ax.set_xlabel("Track ID")
        ax.set_ylabel("Rate")

        recommender.adjust_rate()
        ax = plt.subplot(1, 2, 2)

        next_count = recommender.reco_['tracks']['seedId'].value_counts()

        ax.bar(next_count.index, next_count.values, color='#EE68A4')
        ax.set_title("추천음악 수량현황")
        ax.set_xlabel("Track ID")
        ax.set_ylabel("Rate")

        display(Markdown(
            "### Rate Adjusting"))
        display(
            Markdown("**추천음악 수량이 <u>{}개</u>에서 <u>{}개</u>로 조정되었습니다.**".format(
                recommender.mailbox_id,
                recommender.reco_['tracks']['trackId'].size))
        )
        display(
            Markdown("<b>추천음악 수량 표준편차 변화 : <u>{} → {}</u></b>".format(
                round(prev_count.std()), round(next_count.std())))
        )

        plt.show()

    @staticmethod
    def pt3_6(recommender):
        display(Markdown(
            "### <u>우체통 {}를 위한</u> 음악 <u>{}개</u>가 준비 되었습니다.".format(
                recommender.mailbox_id,
                len(recommender.reco_['tracks']))
        ))
        recommender.draw_filtering()

    @staticmethod
    def pt4(recommender, mail_id):
        display(
            Markdown(
                "### 우체통 <u>{}</u>를 위한 음악편지 <u>{}</u>를 넣어놨어요.".format(
                    recommender.mailbox_id, mail_id)
            )
        )
