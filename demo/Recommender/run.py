from ..lib import KMeans


def run(self):
    if hasattr(self, "parsed_labels_"):
        del self.parsed_labels_
    kmeans = KMeans(datas=self.features['norm'])
    kmeans.init_setting()
    kmeans.fit()

    self.kmeans = kmeans
