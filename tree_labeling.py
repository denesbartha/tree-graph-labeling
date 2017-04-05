#!/usr/bin/env python
# coding: utf-8
"""
    tree-graph-labeling
    ~~~~~~~~~~~~~~~~~~~

    Generates all labelings of a given free tree with the specified alphabet.

    :copyright: 2017, Dénes Bartha
    :license: MIT, see LICENSE for more details
    :version: 1.0.1
    :email: denesb@gmail.com
    :maintainer: Dénes Bartha
"""
from collections import deque


class Node(object):
    """Represents a node of a tree."""

    def __init__(self, parent, distance):
        """Initializes the node object.

        Args:
            parent: the parent node of the node
            distance: the distance from the root node
        """
        self.parent = parent
        self.symm = False
        self.distance = distance
        self.children_list = []
        self.ordervect = []
        self.m = 1

    def __str__(self):
        """Makes a string object from the node."""

        return "parent: %s, multiplicity: %s, distance: %s children_list: %s, ordervect: %s" \
               % (self.parent, self.m, self.distance, self.children_list, self.ordervect)


def sort_tree(t, node):
    """Sorts the given directed tree's branch.

    Sorting here means that at every level (starting from the root node) the nodes should follow an increasing order
    at the count of their children.

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        node: the actual node of the tree (Node object)
    """
    node.ordervect = [len(node.children_list)]
    if node.children_list:
        # iterate through the children
        for n in node.children_list:
            sort_tree(t, t[n])
            node.ordervect.append(t[n].ordervect)

        # if there is more then one children, sort the children list and the ordervect at the same time (the keys are
        # the elements of the ordervect)
        if len(node.children_list) > 1:
            node.children_list, node.ordervect[1:] = (list(x) for x in zip(
                *sorted(zip(node.children_list, node.ordervect[1:]), key=lambda pair: t[pair[0]].ordervect)))


def reset_labeling(t, s):
    """Resets the labeling of given branch of the tree.

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        s: the actual node of the tree
    """
    t[s].label = 0
    for n in t[s].children_list:
        reset_labeling(t, n)


def copy_branch_labeling(t, source_node, dest_node):
    """Copies a branch's labeling of the given tree from one node to another.

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        source_node: the source node
        dest_node: the destination node
    """
    t[dest_node].label = t[source_node].label
    for i in xrange(len(t[source_node].children_list)):
        copy_branch_labeling(t, t[source_node].children_list[i], t[dest_node].children_list[i])


def _next_labeling(t, et, n, en, max_label):
    """

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        et: a dictionary that contains the nodes of the "equivalence-tree" created from the given tree
        n: the actual node of the given t tree
        en: the actual node of the given et "equivalence-tree"
        max_label: an int that specifies the labeling alphabet's size (the labels come from the set 0..maxlabel)

    Returns:
        bool: true if it generated all the labelings for the actual branch
    """

    nind = 0
    for eqnode in et[en].children_list:
        for j in xrange(et[eqnode].m):
            anode = t[n].children_list[nind + j]
            # if the label of the actual node is a valid labeling and the next labeling of the given node is also
            # valid (we are not at the end of the labeling if the current branch)
            if t[anode].label < max_label and _next_labeling(t, et, anode, eqnode, max_label):
                # for every equivalent siblings of the node till the actual equivalent index (j)
                for k in xrange(j):
                    # the equivalent branches should be the same
                    copy_branch_labeling(t, anode, t[n].children_list[nind + k])
                # returns True, because there was a valid labeling of the current branch
                return True
        # increase nind with the current equivalent node's multiplicity
        nind += et[eqnode].m
    # if we are at the end of the actual node's children's labeling
    else:
        # increase the actual node's labeling
        t[n].label += 1
        # if the actual label is a valid labeling => reset the node's children's labeling
        if t[n].label < max_label:
            for an in t[n].children_list:
                reset_labeling(t, an)
        # otherwise reset the actual node's labeling and return False (it means that the current node's labeling is
        # not valid)
        else:
            t[n].label = 0
            return False
    return True


def is_symmetric(t):
    """Finds out whether the given tree is symmetric or not.

    A tree is symmetric iff traversing through the centers children (by breadth-first traversal) at every level
    we got the same amount of nodes. It requires that the t must be ordered.

    Args:
        t: a dictionary that contains the nodes of a labeled tree

    Returns:
        bool: the tree is symmetric or not
    """
    if len(t) == 1:
        return False

    # queues for the center nodes
    q1, q2 = deque([c for c in t[0].children_list]), deque([c for c in t[1].children_list])
    q1.remove(1)
    # loop that goes while at every level we have the same amount of nodes
    while len(q1) == len(q2) and len(q1) > 0:
        c1, c2 = q1.popleft(), q2.popleft()
        q1 += deque([c for c in t[c1].children_list])
        q2 += deque([c for c in t[c2].children_list])
    return len(q1) == 0


def find_center(lst):
    """Finds the center of a given free-tree.

    A center of a tree is a node whose distance from every node is minimal, therefore a tree could have at most
    two centers.

    Args:
        lst: a list that contains a pre-order traversal of a free-tree

    Returns:
        list: contains one or two centers of the tree
    """
    # create a list that contains the original indexes as well
    ind_lst = zip(lst, range(len(lst)))
    while True:
        # the actual root's children count and distance
        cnt_root_children, root_children_distance = 0, ind_lst[0][0] + 1
        i = 0
        while i < len(ind_lst):
            # if the node is the children of the actual root
            if ind_lst[i][0] == root_children_distance:
                cnt_root_children += 1
            # if it is a leaf => delete it from the list
            if i == len(ind_lst) - 1 or ind_lst[i + 1][0] <= ind_lst[i][0]:
                del ind_lst[i]
            else:
                i += 1
        # if the root has only one child => it is a leaf too
        if cnt_root_children < 2:
            del ind_lst[0]
        # if there are only 1 or 2 node remained => it is / those are the centers of the tree
        if len(ind_lst) <= 2:
            return ind_lst


def find_branch(lst, i):
    """Finds the whole branch that is rooted from the given node.
    
    Args:
        lst: a list that contains a pre-order traversal of a free-tree
        i: the index of the actual node

    Returns:
        int: the given i value
        int: the index of the end of the branch + 1
    """
    pi = i
    i += 1
    while i < len(lst):
        if lst[i] <= lst[pi]:
            break
        i += 1
    return pi, i


def find_parent(lst, i, dist):
    """Finds the parent node of the given node in a pre-order traversal list.

    Args:
        lst: a list that contains a pre-order traversal of a free-tree
        i: the index of the actual node
        dist: the distance of the actual node

    Returns:
        int: the index of the node's parent (-1 if it has no parent)
    """
    while i >= 0:
        if lst[i] < dist:
            break
        i -= 1
    return i


def balance_tree_list(lst, centers):
    """Returns a tree's pre-order traversal that is balanced.

    A balanced tree is a rooted tree whose root is the same as one of the tree's centers.

    Args:
        lst: a list that contains a pre-order traversal of a free-tree
        centers: the center nodes (one or two) of the given tree

    Returns:
        list: a pre-order traversal of the balanced tree
    """
    (distance, index) = min(centers, key=lambda c: c[1])
    # if the center is the original root node => we don't need to balance the tree
    if len(centers) == 1 and index == 0:
        return lst

    # find all the elements that are under the center node
    (pmi, mi) = find_branch(lst, index)
    if len(centers) == 1:
        # if there is only one center => the center's branch will be the first part of the balanced tree
        balanced_list = [d - distance for d in lst[pmi:mi]]
    else:
        # if there are two centers => the node that has the lower index will be the center and the higher indexed node
        # branch will be the first part of the reordered tree
        index2 = max(centers, key=lambda c: c[1])[1]
        balanced_list = [0] + [d - distance for d in lst[index2: mi]] + [d - distance for d in lst[pmi + 1:index2]]

    # take every branch that is located in the list after the center's branch
    parent_index = index - 1
    while mi < len(lst):
        (pmi, mi) = find_branch(lst, mi)
        parent_index = find_parent(lst, parent_index, lst[pmi])
        # rearrange the list => copy the actual branch to its parent's location
        lst = lst[:parent_index + 1] + lst[pmi:mi] + lst[parent_index + 1:]
        index += mi - pmi
        mi += mi - pmi

    # copy the remaining branches from the list by going upper in the center's parents
    parent_index = index
    parent_dist = 1
    while True:
        child_index = parent_index
        parent_index = find_parent(lst, parent_index - 1, lst[parent_index])
        # if we hit the previous root node (the beginning of the list) => we break from the loop
        if parent_index < 0:
            break
        diff = lst[parent_index] - parent_dist
        # append the corrected distances from the current branch
        for i in xrange(parent_index, child_index):
            balanced_list.append(lst[i] - diff)
        parent_dist += 1

    # return the newly created balanced list
    return balanced_list


def eq_subtree(t, et, n, en):
    """Generates the "equivalence-tree" from the given rooted tree.

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        et: a dictionary that contains the nodes of the "equivalence-tree" created from the given tree
        n: the actual node of the given t tree
        en: the actual node of the given et "equivalence-tree"
    """
    i = 0
    while i < len(t[n].children_list):
        eq_cnt = 1
        j = i + 1
        while j < len(t[n].children_list) and t[t[n].children_list[j]].ordervect == t[t[n].children_list[i]].ordervect:
            j += 1
            eq_cnt += 1
        # create a node in the equvivalance tree
        an = len(et)
        et[an] = Node(en, 0)
        # set the multiplicity of the new node
        et[an].m = eq_cnt
        # append to its parent's children list
        et[en].children_list.append(an)
        # call the eq_subtree recursively
        eq_subtree(t, et, t[n].children_list[i], an)
        i = j


def gen_eq_tree(t, centers):
    """Returns the "equivalence-tree" from the given rooted tree.

   An "equivalence-tree" of a tree is a tree that contains all the automorphisms of the given tree with the proper
   multiplicity (it stores an equivalent part only once).

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        centers: the center nodes (one or two) of the given tree

    Returns:
        dictionary: contains the nodes of a labeled tree
        dictionary: the nodes of the "equivalence-tree" created from the given tree
    """
    # sort the tree
    sort_tree(t, t[0])
    # if the tree is symmetric (it must have 2 centers)
    if len(centers) == 2 and is_symmetric(t):
        t[0].symm = True
        # if the graph is symmetric => add a new node that has two children: the previous root node and the first child
        # of the root
        root_id = -1
        t[-1] = Node(None, 0)
        t[-1].children_list = [0, 1]
        t[0].parent = -1
        # remove the edge between the old root and it's first child
        t[0].children_list.remove(1)
        # sort the tree again
        sort_tree(t, t[-1])
    else:
        root_id = 0

    # create the equvivalance tree
    et = {root_id: Node(None, 0)}
    et[root_id].m = 1
    eq_subtree(t, et, root_id, root_id)
    # reset the labels of the tree
    reset_labeling(t, root_id)
    return t, et


def gen_tree_from_list(lst):
    """Generates a directed, labeled tree from the given list.

    Args:
        lst: a list that contains a pre-order traversal of a free-tree

    Returns:
        list: a list that contains a pre-order traversal of a balanced tree (according to the given tree)
        dictionary: contains the nodes of a labeled tree
        dictionary: the nodes of the "equivalence-tree" created from the given tree
    """

    if len(lst) > 2:
        centers = find_center(lst)
        lst = balance_tree_list(lst, centers)
    else:
        centers = []

    # start node (parent, children list, path list, distance from the root node)
    t = {0: Node(None, 0)}
    node = 1
    pnode = 0
    for i in xrange(1, len(lst)):
        if lst[i] <= lst[i - 1]:
            pnode = t[pnode].parent
            while t[pnode].distance >= lst[i]:
                pnode = t[pnode].parent

        t[node] = Node(pnode, lst[i])
        t[pnode].children_list.append(node)
        pnode = node
        node += 1

    (t, et) = gen_eq_tree(t, centers)
    return lst, t, et


def graph_labeling_to_list(t, keys):
    """Creates a list that contains the tree's labels (according to the pre-order traversal).

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        keys: sorted keys of the given t

    Returns:
        list: contains the tree's labels
    """

    label_list = []
    for i in keys:
        label_list.append(t[i].label)
    return label_list


def next_labeling(t, et, max_label):
    """Yields all the labelings of a tree.

    Args:
        t: a dictionary that contains the nodes of a labeled tree
        et: a dictionary that contains the nodes of the "equivalence-tree" created from the given tree
        max_label: an int that specifies the labeling alphabet's size

    Yields:
        list: the next labeling of the given tree
    """

    keys = sorted(t)
    if t[0].symm:
        keys.remove(-1)
        yield graph_labeling_to_list(t, keys)
        while _next_labeling(t, et, -1, -1, max_label):
            # if the tree is symmetric => the whole process ends when the "fictive" center node's labeling changes
            if t[-1].label != 0:
                break
            yield graph_labeling_to_list(t, keys)
    else:
        yield graph_labeling_to_list(t, keys)
        while _next_labeling(t, et, 0, 0, max_label):
            yield graph_labeling_to_list(t, keys)


def is_proper_traversal(lst):
    """Determines whether the given list is a valid nonempty pre-order traversal of a tree or not.

    Args:
        lst: a list that contains integers

    Returns:
        bool: the given list is valid or not
    """

    if len(lst) == 0 or lst[0] != 0:
        return False
    for i in xrange(len(lst) - 1):
        # if the actual element of the list is not an integer or the next number (distance) is greater than the current
        # number (distance) + 1 => it is not a valid list
        if type(lst[i]) != int or lst[i + 1] > lst[i] + 1:
            return False
    return type(lst[-1]) == int


def get_labeled_graphs(lst, max_label=2):
    """Prints out all the given free-tree's labelings.

    Args:
        lst: a list that contains a pre-order traversal of a free-tree
        max_label: an int that specifies the labeling alphabet's size
    """

    if type(lst) is not list or not is_proper_traversal(lst):
        raise ValueError("The given object should be a nonempty list that contains a valid pre-order traversal of a "
                         "free-tree...")
    if type(max_label) is not int or max_label <= 0:
        raise ValueError("maxlabel should be a positive integer...")

    (lst, t, et) = gen_tree_from_list(lst)
    print lst, "\n"
    labeling_cnt = 0
    for lblvect in next_labeling(t, et, max_label):
        labeling_cnt += 1
        print lblvect
    print "Count of possible labelings:", labeling_cnt
