from ..lib import KMeans


def run(self):
    kmeans = KMeans(datas=self.features['norm'])
    kmeans.init_setting()
    kmeans.fit()

    self.kmeans = kmeans
