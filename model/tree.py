from collections import Counter
import numpy as np

from model.utils import AttrType, Attr
from metrics.utils import splitting_metric

from copy import deepcopy


class ClsNode:
    def __init__(self, candidate_attr, parent):
        self.parent = parent
        self.children = []

        self.candidate_attr = candidate_attr

        self.depth = parent.depth + 1 if parent is not None else 0

        self.split_attr = None
        self.split_value = None

        self.total_sample = 0
        self.class_freq = {}

        self.prediction = None

    @staticmethod
    # build a nume dict to simulate categorical variable. The output should be like
    # {'float('-inf')/10':10, '10/30': 30, '10/float('inf')': 50}
    def build_nume_dict(nume_list, max_class):
        value_list = nume_list['value']
        label_list = nume_list['label']

        nume_dict = {}

        sort_idx = np.argsort(value_list)
        sorted_value_list = np.array(value_list)[sort_idx]
        sorted_label_list = np.array(label_list)[sort_idx]

        max_class = min(max_class, len(set(value_list)))
        step = len(sorted_value_list) // max_class

        sparse_value_list = sorted_value_list[::step]
        if len(sparse_value_list) == 1:
            return {f'float(\'-inf\')/float(\'inf\')': dict(Counter(sorted_label_list))}

        for i, val in enumerate(sparse_value_list):
            if i == 0:
                pass
            elif i == 1:
                nume_dict[f'float(\'-inf\')/{val}'] = dict(Counter(sorted_label_list[:step*i]))
            else:
                temp = sparse_value_list[i-1]
                nume_dict[f'{temp}/{val}'] = dict(Counter(sorted_label_list[step*(i-1):step*i]))
        nume_dict[f'{val}/float(\'inf\')'] = dict(Counter(sorted_label_list[step*i:]))
        return nume_dict

    @staticmethod
    # return a key of num from the nume_dict,
    # supppose the nume dict is {'float('-inf')/10':10, '10/30': 30, '10/float('inf')': 50}
    # then num=5 will produces 'float('-inf')/10'
    def get_nume_key(num, dict_keys):
        for idx, key in enumerate(dict_keys):
            start, end = key.split('/')
            start, end = eval(start), eval(end)
            if start <= num < end:
                return idx, key

    # given example x, trace down to child
    def trace_down(self, x):
        if self.is_leaf():
            return self

        value = x[self.split_attr.index]
        if self.split_attr.type == AttrType.CATE:
            return self.children[self.split_attr.values.index(value)]
        elif self.split_attr.type == AttrType.NUME:
            if value <= self.split_value:
                return self.children[0]
            else:
                return self.children[1]
        else:
            raise RuntimeError

    # trace all the way down to leaf
    def trace_down_to_leaf(self, x):
        node = self
        while not node.is_leaf():
            node = node.trace_down(x)
        return node

    def is_leaf(self):
        return len(self.children) == 0

    def most_freq(self):
        try:
            return max(self.class_freq, key=self.class_freq.get)
        except ValueError:
            if self.parent is not None:
                return self.parent.most_freq()
            else:
                return None

    def recur_splitting(self, X, y, metric_func, max_depth, min_sample):
        self.total_sample = len(y)
        self.class_freq = Counter(y)

        if self.depth is not None and self.depth > max_depth:
            return

        if self.total_sample < min_sample:
            return

        if len(self.class_freq) == 1:
            return

        metric0 = metric_func(self.class_freq)

        best_split_attr = None
        best_split_value = None
        best_metric_val = float('-inf')

        # TODO: optimization
        for attr in self.candidate_attr:
            if attr.type == AttrType.NONE:
                continue

            njk = {}
            for (_x, k) in zip(X, y):
                j = _x[attr.index]
                if j not in njk:
                    njk[j] = {k: 1}
                else:
                    if k not in njk[j]:
                        njk[j][k] = 1
                    else:
                        njk[j][k] += 1

            split_metric, split_value = splitting_metric(
                attr.type, njk, metric_func, self.total_sample, self.class_freq)
            # TODO: we can also use hoeffding bound to split ?
            if split_metric > best_metric_val:
                best_metric_val = split_metric
                best_split_attr = attr
                best_split_value = split_value

        if best_metric_val < metric0:
            return

        self.split_attr = best_split_attr
        self.split_value = best_split_value

        if best_split_attr.type == AttrType.CATE:
            self.children = []
            for v in best_split_attr.values:
                index = np.array(X[:, best_split_attr.index]) == v
                candidate_attr = deepcopy(self.candidate_attr)
                candidate_attr.pop(self.candidate_attr.index(best_split_attr))
                self.children.append(ClsNode(candidate_attr, self))
                self.children[-1].recur_splitting(X[index], y[index], metric_func, max_depth, min_sample)

        elif best_split_attr.type == AttrType.NUME:
            left_index = np.array(
                X[:, best_split_attr.index]) < best_split_value
            right_index = ~left_index
            X_left, X_right, y_left, y_right = X[left_index], X[right_index], y[left_index], y[right_index]
            self.children = [ClsNode(deepcopy(self.candidate_attr), self), ClsNode(
                deepcopy(self.candidate_attr), self)]
            self.children[0].recur_splitting(
                X_left, y_left, metric_func, max_depth, min_sample)
            self.children[1].recur_splitting(
                X_right, y_right, metric_func, max_depth, min_sample)
        else:
            raise NotImplementedError

    def print(self):
        tree_plot = ''
        head = '    ' * self.depth
        if self.is_leaf():
            tree_plot += head + str(self.most_freq()) + str(self.class_freq) + '\n'
        else:
            if self.split_attr.type == AttrType.NUME:
                tree_plot += head + str(self.split_attr.name) + '<' + str(self.split_value) + '\n'
                tree_plot += self.children[0].print()
                tree_plot += head + str(self.split_attr.name) + '>=' + str(self.split_value) + '\n'
                tree_plot += self.children[1].print()

            elif self.split_attr.type == AttrType.CATE:
                for i, c in enumerate(self.children):
                    tree_plot += head + str(self.split_attr.name) + '==' + str(self.split_attr.values[i]) + '\n'
                    tree_plot += c.print()
        return tree_plot


class ClsTree:
    """Classifier Tree: Base class for VFDT and EFDT

    Parameters
    ----------
    max_depth: 
        Maximum depth of a tree
    min_sample:
        Minimum sample observed for a node to attempt split 
    """
    def __init__(self, candidate_attr=None, max_depth=100, min_sample=5):
        self.root = ClsNode(candidate_attr, parent=None)
        self.max_depth = max_depth
        self.min_sample = min_sample

    def fit(self, X, y, metric_func):
        self.root.recur_splitting(
            X, y, metric_func, self.max_depth, self.min_sample)

    def predict(self, X):
        return [self._predict(x) for x in X]

    def _predict(self, x):
        return self.root.trace_down_to_leaf(x).most_freq()

    def predict_one(self, x):
        return self._predict(x)

    def print(self):
        return self.root.print()
