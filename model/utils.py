import numpy as np
from enum import Enum


class AttrType(Enum):
    CATE = 0
    NUME = 1
    NONE = 2


class Attr:
    def __init__(self, index, type, name=None):
        self.index = index
        self.name = name if name is not None else self.index
        self.type = type
        self.values = None
    
    def print(self):
        print('Attr<%d, %s, %s>' % (self.index, self.name, self.type))
        if self.values is not None:
            print("values: ", self.values)


def hoeffing_bound(metric_func, n_class, delta, n):
    class_freq1 = {j: 1 for j in range(n_class)}
    bound1 = metric_func(class_freq1)
    class_freq2 = {j: n_class if j == 0 else 0 for j in range(n_class)}
    bound2 = metric_func(class_freq2)
    R = abs(bound1 - bound2)
    return np.sqrt(R * R * np.log(1 / delta) / (2 * n))
