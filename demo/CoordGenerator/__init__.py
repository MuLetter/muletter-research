import math as mt
import numpy as np
from ..lib import DB
from bson import ObjectId
from .draw_coord import draw_coord, save_draw_radar, save_draw_quadrant
from .draw_map import draw_map
from .get_map_table import get_map_table
from .draw_radar_map import draw_radar_map
from .radar_test import radar_test

quadrant_check = [[1, 1], [1, -1], [-1, -1], [-1, 1]]


def get_quadrant(angle):
    chk_angle = [0, 90, 180, 270]
    if angle in chk_angle:
        return -1
    else:
        if angle < 90:
            return 0
        elif angle < 180:
            return 1
        elif angle < 270:
            return 2
        elif angle < 360:
            return 3


def check_guadrant(angle, point):
    if angle == 0:
        return [0, point[1]]
    elif angle == 90:
        return [point[1], 0]
    elif angle == 180:
        return [0, point[1] * -1]
    elif angle == 270:
        return [point[1] * -1, 0]


def get_coord(data, detail=False):
    K = len(data)
    angles = np.array([x/float(K)*(2*mt.pi) for x in range(K)])
    non_zero_labels = data != 0

    x = angles[non_zero_labels]
    y = data[non_zero_labels]

    point = np.array([[x[i], y[i]] for i, _ in enumerate(x)])
    point = point.reshape(-1, 2)

    for idx, pt in enumerate(point):
        rad = pt[0]
        ang = rad / mt.pi * 180

        dis = pt[1]
        quad = get_quadrant(ang)
        if quad == -1:
            point[idx] = check_guadrant(ang, pt)
        else:
            if (ang < 90) or \
                    (ang > 180 and ang < 270):
                ang = 90 - (ang % 90)
            else:
                ang = ang % 90
            rad = ang * mt.pi / 180

            quad = quadrant_check[quad]
            x = dis * mt.cos(rad) * quad[0]  # get X
            y = dis * mt.sin(rad) * quad[1]  # get Y

            point[idx] = [x, y]

    if detail:
        return point, point.sum(axis=0)
    else:
        return point.sum(axis=0)


def _make_coords(mailbox):
    try:
        db = DB()
        K = db.cluster_zone.find().sort("version", -1)[0]['K']

        tracks = mailbox['tracks']
        label_cnt = np.zeros(K)
        for track in tracks:
            trackId = track['trackId']
            res = db.seed_zone.find_one({
                "trackId": trackId
            })
            label = res['label']
            label_cnt[label] += 1

        label_per = (label_cnt / label_cnt.sum()
                     * 100).round().astype("int")
        x, y = get_coord(label_per).astype("float64")

        label_percentages_ = label_per
        point = {
            "x": x,
            "y": y,
        }

        db.mailbox.update_one({
            "_id": mailbox["_id"],
        }, {
            "$set": {
                "point": point,
                "_labelPercentages": label_percentages_.tolist()
            }
        })

        return label_percentages_, point
    except:
        print(label_percentages_)
        print(track)


class CoordGenerator:
    def __init__(self, mailbox_id):
        self.db = DB()
        self.mailbox_id = ObjectId(mailbox_id)
        self.mailbox = self.db.mailbox.find_one({"_id": ObjectId(mailbox_id)})
        self.K = self.db.cluster_zone.find().sort("version", -1)[0]['K']

    @staticmethod
    def all_make_coords():
        db = DB()

        mailboxes = db.mailbox.find()
        for mailbox in mailboxes:
            _make_coords(mailbox)

    @staticmethod
    def all_make_coords_2():
        db = DB()

        mailboxes = db.mailbox.find()
        result = list()
        for mailbox in mailboxes:
            result.append(_make_coords(mailbox))

        return result

    def make_coords(self):
        label_percentages_, point = _make_coords(self.mailbox)

        self.label_percentages_ = label_percentages_
        self.point = point


CoordGenerator.draw_coord = draw_coord
CoordGenerator.save_draw_radar = save_draw_radar
CoordGenerator.save_draw_quadrant = save_draw_quadrant
CoordGenerator.draw_map = draw_map
CoordGenerator.get_map_table = get_map_table
CoordGenerator.draw_radar_map = draw_radar_map
CoordGenerator.radar_test = radar_test
