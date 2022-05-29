import pandas as pd
from ..lib import DB


@staticmethod
def get_map_table():
    db = DB()

    mailbox_docs = db.mailbox.find({})
    mailboxes = [_ for _ in mailbox_docs]

    K = db.cluster_zone.find({}).sort("createdAt", -1)[0]['K']

    points = pd.DataFrame([[_['point']['x'], _['point']['y']] for _ in mailboxes],
                          columns=['x', 'y'],
                          index=pd.Series([_['_id'] for _ in mailboxes], name='우체통 고유 ID'))
    label_percentages = pd.DataFrame([_['_labelPercentages'] for _ in mailboxes],
                                     index=pd.Series(
                                         [_['_id'] for _ in mailboxes], name='우체통 고유 ID'),
                                     columns=pd.Series(range(0, K), name='클러스터 번호'))

    return points, label_percentages
