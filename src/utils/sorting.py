import numpy as np
from sklearn.metrics.pairwise import euclidean_distances as euc


def sorting(self):
    k_pat = self.clusters_
    _label = self.labels_

    eucs = list()
    sort_scores = list()
    for idx in range(0, len(k_pat)):
        sel_k_pat = np.expand_dims(k_pat[idx], axis=0)

        euc_scores = euc(sel_k_pat, k_pat)[0]
        sort_scores.append(euc_scores.argsort())
        eucs.append(euc_scores)

    eucs = np.array(eucs)
    sort_scores = np.array(sort_scores)

    # 초기 셋팅 (가장 전체적으로 유사도가 높은 친구, euc를기반으로 하니까 제일 낮은 친구가 선정되어야 함)
    sorting_labels = np.zeros(len(sort_scores)) - 1
    sort_eucs = np.array(eucs).sum(axis=0).argsort()

    top_eucs_cluster = sort_eucs[0]
    sorting_labels[0] = top_eucs_cluster

    # 초기 기반으로 가장 가까운 애들을 양쪽에 배치
    first_idx = 1
    last_idx = len(sort_scores) - 1

    sorting_labels[first_idx] = sort_scores[top_eucs_cluster][1]
    sorting_labels[last_idx] = sort_scores[top_eucs_cluster][2]

    first_cnt = 0
    last_cnt = 0

    while True:
        # traiding
        entry_1_idx = int(sorting_labels[first_idx + first_cnt])
        entry_2_idx = int(sorting_labels[last_idx - last_cnt])

        entry_1 = sort_scores[entry_1_idx]
        entry_2 = sort_scores[entry_2_idx]

        entry_1_euc = eucs[entry_1_idx]
        entry_2_euc = eucs[entry_2_idx]

        entry_1_sel = np.where(
            np.isin(entry_1, sorting_labels) == False)[0]
        entry_2_sel = np.where(
            np.isin(entry_2, sorting_labels) == False)[0]

        entry_1_cnt = 0
        entry_2_cnt = 0

        while True:
            _entry_1_sel = entry_1[entry_1_sel[entry_1_cnt]]
            _entry_2_sel = entry_2[entry_2_sel[entry_2_cnt]]

            if entry_1_euc[_entry_1_sel] > entry_2_euc[_entry_1_sel]:
                _entry_1_sel = -1
                entry_1_cnt += 1
            if entry_1_euc[_entry_2_sel] < entry_2_euc[_entry_2_sel]:
                _entry_2_sel = -1
                entry_2_cnt += 1

            if len(entry_1_sel) == (entry_1_cnt):
                _entry_1_sel = "x"

            if len(entry_2_sel) == (entry_2_cnt):
                _entry_2_sel = "x"

            if (_entry_1_sel != -1) & (_entry_2_sel != -1):
                break

        if _entry_1_sel != "x":
            sorting_labels[first_idx + (first_cnt + 1)] = _entry_1_sel
            first_cnt += 1
        if _entry_2_sel != "x":
            sorting_labels[last_idx - (last_cnt + 1)] = _entry_2_sel
            last_cnt += 1

        if len(np.where(sorting_labels == -1)[0]) == 0:
            break

    change_index_info = list()
    for idx, _ in enumerate(sorting_labels):
        change_index_info.append({
            "idxes": np.where(_label == _)[0],
            "change": idx
        })

    for info in change_index_info:
        _label[info['idxes']] = info['change']

    self.clusters_ = k_pat[sorting_labels.astype("int")]
    self.labels_ = _label
