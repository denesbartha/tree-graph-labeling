#!/usr/bin/env python
# coding: utf-8
"""
    Unit Tests for  tree-graph-labeling
    ~~~~~~~~~~~~~~~~~~~

    :copyright: 2017, Dénes Bartha
    :license: MIT, see LICENSE for more details
    :version: 1.0.1
    :email: denesb@gmail.com
    :maintainer: Dénes Bartha
"""
import unittest
import tree_labeling


class TestTreeLabeling(unittest.TestCase):
    @staticmethod
    def gen_colour_lst(labeling_generator):
        return [lbl for lbl in labeling_generator]

    @staticmethod
    def check_lst_equal(l1, l2):
        return len(l1) == len(l2) and l1 == l2

    def test_get_labeled_graphs(self):
        # tests for malformed / bad inputs
        with self.assertRaises(ValueError):
            self.gen_colour_lst(tree_labeling.get_labeled_graphs([]))
        with self.assertRaises(ValueError):
            self.gen_colour_lst(tree_labeling.get_labeled_graphs(42))
        with self.assertRaises(ValueError):
            self.gen_colour_lst(tree_labeling.get_labeled_graphs([3, 4]))
        with self.assertRaises(ValueError):
            self.gen_colour_lst(tree_labeling.get_labeled_graphs([1, 2, 3]))
        with self.assertRaises(ValueError):
            self.gen_colour_lst(tree_labeling.get_labeled_graphs([42, 43]))
        with self.assertRaises(ValueError):
            self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 2, 3], ""))

        # check for some trivial examples
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0])), [(0,), (1,)])
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0], max_label=3)),
                                    [(0,), (1,), (2,)])
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0], max_label=5)),
                                    [(0,), (1,), (2,), (3,), (4,)])
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1], max_label=1)),
                                    [(0, 0)])

        # check for "easy" examples
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1])),
                                    [(0, 0), (1, 0), (1, 1)])
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 2])),
                                    [(0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1)])
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 1])),
                                    [(0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1)])
        assert self.check_lst_equal(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 1, 2])),
                                    [(0, 0, 0, 0), (0, 0, 0, 1), (1, 0, 0, 0), (1, 0, 0, 1), (0, 0, 1, 1), (1, 0, 1, 0),
                                     (1, 0, 1, 1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 1)])

        # check for more complex examples - asymmetric
        assert len(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 2, 3, 4, 4, 5, 5, 3, 4]))) == 480
        # check for more complex examples - symmetric
        assert len(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 1, 2]))) == 10
        assert len(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 1, 2], max_label=3))) == 45
        assert len(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 2, 3, 1, 2, 3]))) == 72

        # edge labelings
        assert len(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 2, 2, 1, 1], 2, True))) == 12
        assert len(self.gen_colour_lst(tree_labeling.get_labeled_graphs([0, 1, 2, 2, 1, 1], 3, True))) == 99

if __name__ == '__main__':
    unittest.main()
