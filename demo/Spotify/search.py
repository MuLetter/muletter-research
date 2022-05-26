import requests as req
from functools import reduce
from urllib.parse import urlencode
from IPython.display import clear_output
import pandas as pd

# Setting self.Search


def search(self):
    sel_tracks = pd.DataFrame(
        columns=['trackId', 'trackName', 'artistIds', 'artistNames', "image"])

    while True:
        q = input("검색어를 입력해주세요.")
        offset = 0
        limit = 10

        while True:
            search_url = "https://api.spotify.com/v1/search"
            query = urlencode({
                "q": q,
                "type": "track",
                "market": "KR",
                "limit": limit,
                "offset": offset
            })
            headers = {
                "Authorization": "Bearer {}".format(self.token)
            }
            res = req.get("{}?{}".format(search_url, query), headers=headers)
            result = res.json()['tracks']
            _result = list()

            for item in result['items']:
                _id = item["id"]
                _name = item["name"]
                album = item['album']
                images = album["images"]

                if len(images) == 0:
                    _image = ""
                else:
                    _image = images[0]['url']

                artist_list = album['artists']
                artists = reduce(
                    lambda acc, cur: cur[1]['name'] if cur[0] == 0 else acc +
                    "," + cur[1]['name'],
                    enumerate(artist_list),
                    ""
                )
                artists_id = reduce(
                    lambda acc, cur: cur[1]['id'] if cur[0] == 0 else acc +
                    "," + cur[1]['id'],
                    enumerate(artist_list),
                    ""
                )
                _result.append({
                    "trackId": _id,
                    "trackName": _name,
                    "artistIds": artists_id.split(",")[0],
                    "artistNames": artists.split(",")[0],
                    "image": _image
                })

            for idx, _ in enumerate(_result):
                print("\t{}.{} - {} ({})".format(idx + 1, _['artistNames'],
                                                 _['trackName'], _['trackId']))
            _total = (offset + 1)
            _total = result['total'] if _total > result['total'] else _total
            print("{}/{}".format(_total, result['total']))
            _action = input("선택은 번호입력을 해주세요." +
                            "\n종료는 exit, 다음페이지는 next를 입력해주세요.")

            if _action == "exit":
                clear_output()
                break
            elif _action == "next":
                offset += limit
                clear_output()
            else:
                _action = int(_action) - 1
                sel_tracks = sel_tracks.append(
                    _result[_action], ignore_index=True)
                clear_output()
                break

        _action = input("계속하시려면 아무거나, 종료는 exit를 입력해주세요.")

        if _action == "exit":
            break
        else:
            clear_output(wait=True)

    self.sel_tracks = sel_tracks
