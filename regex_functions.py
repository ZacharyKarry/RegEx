"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Zachary Karry 2013, 2014
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, Leaf, StarTree, DotTree, BarTree

# Do not change any of the class declarations above this comment
# Student code below this comment.


def regex_split(s: str) -> tuple:
    """
    Precondition: s begins with '(' and ends with ')'

    Splits a parenthesized regex into 3 parts: left child, operator and
    right child, then returns a tuple with those things in that order.
    Returns 'fail' for all three if there are mismatched parentheses.

    Note: Will return invalid operators and children for invalid regex
    formats.

    >>> regex_split('(()')
    ('fail', 'fail', 'fail')
    >>> regex_split('(())')
    ('()', ')', '')
    >>> regex_split('((0*|1*).e*)')
    ('(0*|1*)', '.', 'e*')
    >>> regex_split('((0|(0.2))|((0.1)|(1.2)))')
    ('(0|(0.2))', '|', '((0.1)|(1.2))')
    """
    if s[1] in "012e":
        if s[2] == "*":
            #to account for the case (something*|blahblah)
            i = 2
            while s[i] == '*':
                #in case we have 1** etc.
                i += 1
            return (s[1:i], s[i], s[i + 1:-1])
        else:
            return (s[1:2], s[2], s[3:-1])
    left = 1
    right = 0
    place = 1
    while left != right and place < len(s):
        #assuming that it is not a base case character, we will have brackets
        #so what this does is waits until we have an equal number of brackets
        #and then we know we have the left child.
        place += 1
        left = s[1:place].count('(')
        right = s[1:place].count(')')
    if place >= len(s):
        #this accounts for mismatched brackets
        return ("fail", "fail", "fail")
    if s[place] is not '*':
        #left child could also have stars, so we have to account for that
        return (s[1:place], s[place], s[place + 1:-1])
    else:
        while s[place] == '*':
            place += 1
        return (s[1:place], s[place], s[place + 1:-1])


def is_regex(s: str) -> bool:
    """
    Takes a string, and returns whether or not it is a valid
    regular expression.

    >>> is_regex('e')
    True
    >>> is_regex(")")
    False
    >>> is_regex("((0.1)|(1.2))(")
    False
    >>> is_regex("((0|(0.2)*)|((0.1)|(1p2)*))*")
    False
    >>> is_regex("(((0.0).0)***|(2.2))")
    True
    """
    #base case
    if len(s) == 1:
        return s in "012e"
    elif s == '':
        return False
    else:
        #if the end is a star, then it tests everything but that.
        if s[-1] == "*":
            return is_regex(s[:-1])
        elif s[0] == "(" and s[-1] == ")":
            #this is the more complicated one, essentially it uses a function
            #to pull out nested regex's, and tests that those as well as the
            #centre symbol are valid
            spl = regex_split(s)
            return spl[1] in ".|" and is_regex(spl[0]) and is_regex(spl[2])

    return False


def perm(s: str) -> {str, ...}:
    """
    Returns a set of all permutations of s.

    >>> perm("a") == {"a"}
    True
    >>> perm("ab") == {"ab", "ba"}
    True
    >>> perm("abc") == {"abc", "acb", "bac", "bca", "cab", "cba"}
    True
    """
    #from the lecture, copyright Danny Heap? or Dustin Wehr, either or.
    return (set(sum(  # gather from
                [  # list of

                    # list of permutations produced by prefixing s[i]
                    # for each permutation of s with s[i] removed
                    [s[i] + p for p in perm(s[:i] + s[i + 1:])]

                    # for each index in s
                    for i in range(len(s))],

                # pythonese to make sum gather (concatenate) lists
                []))  # (which it should have been designed to do, anyway!)

            # strings of length < 2 have just 1 permutation
            if len(s) > 1 else {s})


def all_regex_permutations(s: str) -> set:
    """
    Takes a string and returns a set of all permutations of that string that
    are valid regex's.

    >>> d =  all_regex_permutations(')(1.2')
    >>> d == {'(2.1)', '(1.2)'}
    True
    >>> j =  all_regex_permutations(')(1.p')
    >>> j == set()
    True
    >>> q = all_regex_permutations('**(|)12')
    >>> u = {'(1*|2)*', '(1*|2*)', '(1|2)**', '(1|2*)*', '(1|2**)',
    ... '(2*|1)*', '(2*|1*)', '(2|1)**', '(2|1*)*', '(2|1**)',
    ... '(2**|1)', '(1**|2)'}
    >>> q == u
    True
    >>> e = all_regex_permutations('**(p)12')
    >>> e == set()
    True
    """
    return set(filter(is_regex, perm(s)))


def least_star(r: "StarTree") -> "RegexTree":
    """
    Recursively goes in and returns the first non-star in a nested StarTree
    regex.

    >>> test = StarTree(StarTree(StarTree(Leaf('e'))))
    >>> least_star(test)
    Leaf('e')
    """
    if not isinstance(r.children[0], StarTree):
        return r.children[0]
    else:
        return least_star(r.children[0])


def regex_match(r: "RegexTree", s: str) -> bool:
    """
    Determines whether a RegexTree matches a string.

    >>> regex_match(Leaf('1'), '1')
    True
    >>> regex_match(Leaf('e'), '')
    True
    >>> test = build_regex_tree('((0.1)|(0.2))*')
    >>> regex_match(test, '01020101020101020202')
    True
    >>> regex_match(test, '010201010201010202102')
    False
    >>> test2 = build_regex_tree('((0|1)|(0.2))*')
    >>> regex_match(test2, '')
    True
    >>> regex_match(test2, '0000001110010211')
    True
    >>> regex_match(test2, '000000111001211')
    False
    """
    if isinstance(r, Leaf):
        return (s == r.symbol and s != 'e') or (s == '' and r.symbol == 'e')
    elif isinstance(r, StarTree):
        if s == '':
            return True
        child_match = least_star(r)
        for i in range(1, len(s) + 1):
            #what this is doing is searching for a slice that matches
            #the child, and if the ENTIRE regex also matches the rest
            #then it must be true.
            if regex_match(child_match, s[:i]) and regex_match(r, s[i:]):
                return True
        return False
    elif isinstance(r, BarTree):
        return regex_match(r.children[0], s) or regex_match(r.children[1], s)
    elif isinstance(r, DotTree):
        #this one iterates over all possible different slices of
        #the inputted string to see if they match the characterization.
        for index in range(len(s) + 1):
            if (regex_match(r.children[0], s[:index]) and
                    regex_match(r.children[1], s[index:])):
                return True
        return False


def build_regex_tree(regex: str) -> "RegexTree":
    """
    Takes a valid string form regex, and returns the RegexTree that
    corresponds to it.

    >>> build_regex_tree('0')
    Leaf('0')
    >>> build_regex_tree('0*')
    StarTree(Leaf('0'))
    >>> build_regex_tree('(0.1)')
    DotTree(Leaf('0'), Leaf('1'))
    >>> build_regex_tree('(1|0)')
    BarTree(Leaf('1'), Leaf('0'))
    >>> build_regex_tree('(0*|1*)')
    BarTree(StarTree(Leaf('0')), StarTree(Leaf('1')))
    >>> build_regex_tree('((0.1).0)')
    DotTree(DotTree(Leaf('0'), Leaf('1')), Leaf('0'))
    """
    if len(regex) == 1:
        return Leaf(regex)
    else:
        if regex[-1] == "*":
            return StarTree(build_regex_tree(regex[:-1]))
        else:
            #this then builds either a bar or a star using the regex_split
            #function used eariler in is_regex
            spl = regex_split(regex)
            if spl[1] == "|":
                return BarTree(build_regex_tree(spl[0]),
                               build_regex_tree(spl[2]))
            else:
                return DotTree(build_regex_tree(spl[0]),
                               build_regex_tree(spl[2]))