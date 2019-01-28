# =====================================================================
# EXAMPLE 
# =====================================================================
# test_iter = MyIterator(5, 6)
#
# for val in test_iter:
#     print val
# =====================================================================

import numpy


class MyIterator(object):
    def __init__(self, h_res, v_res):
        self._h_res = h_res
        self._v_res = v_res
        self._current_h = 0
        self._current_v = 0
        self._step = 1
        self._matrix = numpy.random.rand(h_res, v_res)

    def __iter__(self):
        return self

    def next(self):
        if self._current_v >= self._v_res:
            raise StopIteration

        current_value = self._matrix[self._current_h][self._current_v]
        result = (self._current_h, self._current_v), current_value

        self._current_h = (self._current_h + self._step) % self._h_res
        if self._current_h == 0:
            self._current_v += self._step

        return result
