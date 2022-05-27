from pymongo import MongoClient as mc
from bson import ObjectId
import datetime as dt


class DB:
    def __init__(self):
        mongo_uri = "mongodb://localhost:27017"
        self.conn = mc(mongo_uri).TestMuLetter
        self.mail = self.conn.Mail
        self.mail_box = self.conn.MailBox
        self.seed_zone = self.conn.SeedZone

    # Test 저장용
    def save_mailbox(self, sel_tracks):
        mail_box = {
            "title": "Test",
            "description": "Test",
            "imagePath": "",
            "tracks": [row.to_dict() for idx, row in sel_tracks.iterrows()],
            "createdAt": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "updatedAt": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }

        return self.mail_box.insert_one(mail_box)

    def get_mailbox(self, _obj_id):
        obj_id = ObjectId(_obj_id)

        mail_box = self.mail_box.find_one({
            "_id": obj_id
        })

        return mail_box

    def save_mail(self, recommender):
        mail = {
            "mailBoxId": ObjectId(recommender.mailbox_id),
            "tracks": [row.to_dict() for idx, row in recommender.reco['tracks'].iterrows()],
            "isRead": False,
            "createdAt": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

        return self.mail.insert_one(mail)
