# test solutions for A2, Part 2

from unittest import TestCase, main, TestLoader, TextTestRunner, TestResult
from regex_functions import is_regex, all_regex_permutations
from regex_functions import build_regex_tree, regex_match
from regextree import Leaf, DotTree, BarTree, StarTree, RegexTree


# brief aliases for regular expression tree classes
# and leaf instances
L, B, D, S = Leaf, BarTree, DotTree, StarTree
LE, L0, L1, L2 = L('e'), L('0'), L('1'), L('2')

class TestRegexMatch(TestCase):
    # TODO: separate 7 test methods for examples involving only the symbols from
    # one of the nonempty subsets of {*,|,.}
    # OK --- add fail test method for each ---> 14 methods
    # then add test match/non match for leaves --> 16 methods total
    # Perhaps methods for a single {*, |, .} should be separate from multiple ones?

    def setUp(self: 'TestRegexMatch') -> None:
        pass

    def tearDown(self: 'TestRegexMatch') -> None:
        """Clean up test case"""
        pass

    def test_leaf_ok(self: 'TestRegexMatch') -> None:
        """Correctly matches leaf regexes?"""
        leaf_list = [(LE, ''), (L0, '0'), (L1, '1'), (L2, '2')]
        for t in leaf_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_leaf_fail(self: 'TestRegexMatch') -> None:
        """Correct rejects near-leaves?"""
        nearly_leaf_list = [(LE, 'e'), (L0, '(0)'), (LE, '()'), (L1, '11'),
                            (L1, '3')]
        for t in nearly_leaf_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_edge_empty_ok(self: 'TestRegexMatch') -> None:
        """Correctly matches various matches of empty string?"""
        empty_string_list = [(D(LE, LE), ''), (B(L0, LE), ''), (S(L2), ''),
                             (S(LE), '')]
        for t in empty_string_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_dot_okay(self: 'TestRegexMatch') -> None:
        """Correctly matches dotted regexes?"""
        dot_list = [(D(L1, LE), '1'), (D(LE, L2), '2'), (D(L1, L1), '11'),
                    (D(L0, L2), '02')]
        for t in dot_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_dot_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near-dots?"""
        nearly_dot_list = [(D(L1, L0), '1'), (D(L1, L0), '102'),
                           (D(L1, L0), '1.0'), (D(L1, L2), '(12)'),
                           (D(L1, L2), '(1.2)')]
        for t in nearly_dot_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_bar_okay(self: 'TestRegexMatch') -> None:
        """Correctly matches barred regexes?"""
        bar_list = [(B(L1, LE), '1'), (B(LE, L2), '2'), (B(L1, L1), '1')]
        for t in bar_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_bar_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near-bars?"""
        nearly_bar_list = [(B(L1, L2), '12'), (B(L1, L2), '0'),
                           (B(L1, L2), '')]
        for t in nearly_bar_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_star_okay(self: 'TestRegexMatch') -> None:
        """Correctly matches starred regexes?"""
        star_list = [(S(L1), '1'), (S(L2), '222222')]
        for t in star_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_star_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near-stars?"""
        nearly_star_list = [(S(L1), '1 1'), (S(L2), '22212'),
                            (S(L0), '0000 0'), (S(L0), '3')]
        for t in nearly_star_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_dot_bar_ok(self: 'TestRegexMatch') -> None:
        """Correctly matches dot-bar regexes?"""
        dot_bar_list = [(D(B(L0, L1), B(L2, L0)),'12'),
                        (B(D(L0, L1), D(L2, L0)),'20'),
                        (D(B(L0, L1), D(L2, L1)), '121'),
                        (B(D(L0, L1), B(L2, L1)), '01')]
        for t in dot_bar_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_dot_bar_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near dot-bars?"""
        nearly_dot_bar_list = [(D(B(L0, L1), B(L2, L0)), '012'),
                        (B(D(L0, L1), D(L2, L0)), '02'),
                        (D(B(L0, L1), D(L2, L1)), '0121'),
                        (B(D(L0, L1), B(L2, L1)), '0121')]
        for t in nearly_dot_bar_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_dot_star_ok(self: 'TestRegexMatch') -> None:
        """Correctly matches dot-star regexes?"""
        dot_star_list = [(D(S(L1), S(L2)), '112'), (D(S(L1), S(L2)), '122'),
                         (D(S(L1), S(L2)), '2222'), (D(S(L1), S(L2)), '111'),
                         (S(D(L1, L0)), '101010'), (D(L1, S(D(L2, L0))), '1202020'),
                         (D(L1, S(D(L2, L0))), '1'), (S(D(L1, S(L0))), '100110')]
        for t in dot_star_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_dot_star_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near dot-stars?"""
        near_dot_star_list = [(D(L0, S(L1)), '(0.1*)'), (D(L0, S(L1)), '0101'),
                              (S(D(L1, L1)), '111'), (S(D(L1, L0)), '1100')]
        for t in near_dot_star_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_bar_star_ok(self: 'TestRegexMatch') -> None:
        """Correctly matches bar-star regexes?"""
        bar_star_list = [(B(S(L1), S(L0)), '000'), (S(B(L2, L1)), '11212212212'),
                         (S(B(L1, B(L0, L2))), '1002221102201')]
        for t in bar_star_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_bar_star_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near bar-stars?"""
        near_bar_star_list = [(B(L0, S(L1)), '(0|1*)'), (B(L0, S(L1)), '01'),
                              (S(B(L0, L1)), '(0|1)*'), (S(B(L0, L1)), '00 1')]
        for t in near_bar_star_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_bar_star_dot_ok(self: 'TestRegexMatch') -> None:
        """Correctly matches bar-star-dot regexes?"""
        bar_star_dot_list = [(B(S(L2), D(L1, L0)), '10'), (B(S(L2), D(L1, L0)), '222'),
                             (D(B(L0, L2), S(L1)), '0111'),
                             (S(D(B(L0, L2), S(L1))), '0121210121'),
                             (S(S(L2)), '22222')]
        for t in bar_star_dot_list:
            self.assertTrue(regex_match(t[0], t[1]),
                            "Rejects valid match: {}".format(t))

    def test_bar_star_dot_fail(self: 'TestRegexMatch') -> None:
        """Correctly rejects near bar-star-dots?"""
        near_bar_star_dot_list = [(B(S(L2), D(L1, L0)), '210'), (B(S(L2), D(L1, L0)), '1'),
                             (D(B(L0, L2), S(L1)), '02111'),
                             (S(D(B(L0, L2), S(L1))), '102102'),
                             (S(S(L2)), '2 2222')]
        for t in near_bar_star_dot_list:
            self.assertFalse(regex_match(t[0], t[1]),
                             "Accepts invalid match: {}".format(t))

    def test_difficult_star(self: 'TestRegexMatch') -> None:
        """Correct on difficult case for star (1|(1.2))*?
        Almost-correct implementation of * will fail this test, in particular
        will not get accept enough strings."""
        r = S(B(L1,D(L1,L2)))
        yes = ["11212","12121","112112"]
        no = ["1221","11221"]
        for s in yes:
            self.assertTrue(regex_match(r,s),
                       "Rejects valid match: {}".format((r,s)))
        for s in no:
            self.assertFalse(regex_match(r, s),
                       "Accepts invalid match: {}".format((r,s)))


class TestBuildRegexTree(TestCase):

    def setUp(self: 'TestBuildRegexTree') -> None:
        pass

    def tearDown(self: 'TestBuildRegexTree') -> None:
        pass

    def test_leaf(self: 'TestBuildRegexTree') -> None:
        """Correctly builds leaves?"""
        leaf_list = [(LE, 'e'), (L0, '0'), (L1, '1'), (L2, '2')]
        for t in leaf_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_dot(self: 'TestBuildRegexTree') -> None:
        """Correctly builds dot trees?"""
        dot_list = [(D(L0, L1), '(0.1)'), (D(LE, L1), '(e.1)'),
                    (D(L1, LE), '(1.e)'), (D(L2, L2), '(2.2)')]
        for t in dot_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_bar(self: 'TestBuildRegexTree') -> None:
        """Correctly builds bar trees?"""
        bar_list = [(B(L0, L1), '(0|1)'), (B(LE, L1), '(e|1)'),
                    (B(L1, LE), '(1|e)'), (B(L2, L2), '(2|2)')]
        for t in bar_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_star(self: 'TestBuildRegexTree') -> None:
        """Correctly builds star trees?"""
        star_list = [(S(L1), '1*'), (S(LE), 'e*'), (S(L0), '0*'), (S(L2), '2*')]
        for t in star_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_bar_dot(self: 'TestBuildRegexTree') -> None:
        """Correctly builds bar-dot trees?"""
        bar_dot_list = [(B(D(L0, L1), D(L2, LE)), '((0.1)|(2.e))'),
                        (B(B(L0, L1), D(L2, LE)), '((0|1)|(2.e))'),
                        (B(D(L0, L1), B(L2, LE)), '((0.1)|(2|e))'),
                        (B(D(L1, L2), L0), '((1.2)|0)'),
                        (B(L1, D(L2, L0)), '(1|(2.0))'),
                        (D(B(L0, L1), B(L2, LE)), '((0|1).(2|e))'),
                        (D(D(L0, L1), B(L2, LE)), '((0.1).(2|e))'),
                        (D(B(L0, L1), D(L2, LE)), '((0|1).(2.e))')]
        for t in bar_dot_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_bar_star(self: 'TestBuildRegexTree') -> None:
        """Correctly builds bar-star trees?"""
        bar_star_list = [(B(L0, S(L1)), '(0|1*)'), (B(S(L0), L1), '(0*|1)'),
                         (B(S(L1), S(L2)), '(1*|2*)'),
                         (S(B(L0, L1)), '(0|1)*'), (S(B(S(L0), L1)), '(0*|1)*'),
                         (S(B(S(L0), B(L1, S(L2)))), '(0*|(1|2*))*')]
        for t in bar_star_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_dot_star(self: 'TestBuildRegexTree') -> None:
        """Correctly builds dot-star trees?"""
        dot_star_list = [(D(L0, S(L1)), '(0.1*)'), (D(S(L0), L1), '(0*.1)'),
                         (D(S(L1), S(L2)), '(1*.2*)'),
                         (S(D(L0, L1)), '(0.1)*'), (S(D(S(L0), L1)), '(0*.1)*'),
                         (S(D(S(L0), D(L1, S(L2)))), '(0*.(1.2*))*')]
        for t in dot_star_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))

    def test_bar_dot_star(self: 'TestBuildRegexTree') -> None:
        """Correctly builds bar-dot-star trees?"""
        bar_dot_star_list = [(B(D(L0, L1), D(S(L2), LE)), '((0.1)|(2*.e))'),
                             (D(B(L0, L1), B(S(L2), LE)), '((0|1).(2*|e))'),
                             (S(D(B(L0, L1), D(S(L2), LE))),
                              '((0|1).(2*.e))*'),
                             (S(B(D(L0, L1), B(S(L2), LE))),
                              '((0.1)|(2*|e))*'),
                             (S(D((L0), B(S(L2), LE))),
                              '(0.(2*|e))*'),]
        for t in bar_dot_star_list:
            self.assertEqual(t[0], build_regex_tree(t[1]),
                             "Regex tree {} doesn't match {}.".format(
                                 t[0], t[1]))


class TestIsRegex(TestCase):
    def setUp(self: 'TestIsRegex') -> None:
        pass

    def tearDown(self: 'TestIsRegex') -> None:
        """Clean up test case"""
        pass

    def test_leaf_ok(self: 'TestIsRegex') -> None:
        """Leaf regular expressions accepted?"""
        leaf_list = ['0', '1', '2', 'e']
        for r in leaf_list:
            self.assertTrue(is_regex(r),
                                "Rejects valid regex: {}".format(r))

    def test_leaf_fail(self: 'TestIsRegex') -> None:
        """Leaf non-regexes rejected?"""
        bad_leaf_list = ['3', '00', '', '(1)']
        for r in bad_leaf_list:
            self.assertFalse(is_regex(r),
                            "Accepts invalid regex: {}".format(r))

    def test_bar(self: 'TestIsRegex') -> None:
        """Bar regexes accepted?"""
        bar_regex_list = ['(0|1)', '(0|e)', '(1|1)', '(1|e)', '(2|1)']
        for r in bar_regex_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_bar_fail(self: 'TestIsRegex') -> None:
        """Bar-like non-regexes rejected?"""
        bad_bar_list = ['0|1', '(0|1|2)', '|', '(|)', '(00|1)']
        for r in bad_bar_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

    def test_dot(self: 'TestIsRegex') -> None:
        """Dot regexes accepted?"""
        dot_regex_list = ['(0.1)', '(0.e)', '(1.1)', '(1.e)', '(2.1)']
        for r in dot_regex_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_dot_fail(self: 'TestIsRegex') -> None:
        """Dot-like non-regexes rejected?"""
        bad_dot_list = ['0.1', '(0.1.2)', '.', '(.)', '(00.1)']
        for r in bad_dot_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

    def test_star_ok(self: 'TestIsRegex') -> None:
        """Star regexes accepted?"""
        star_list = ['e*', '0*', '1*', '2*']
        for r in star_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_star_fail(self: 'TestIsRegex') -> None:
        """Star-like non-regexes rejected?"""
        bad_star_list = ['*1', '*', '(2*)', '0*1', '(1)*']
        for r in bad_star_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

    def test_bar_dot_ok(self: 'TestIsRegex') -> None:
        """Bar-dot regexes accepted?"""
        bar_dot_list = ['((0.1)|(2.e))', '((0|1).(2|e))', '((0|1).e)',
                         '(0.(2|e))', '((0.1)|e)', '(1|(2.e))', '((0.1)|(2|e))',
                         '((0|1).(2.e))']
        for r in bar_dot_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_bar_dot_fail(self: 'TestIsRegex') -> None:
        """Bar-dot-line non-regexes rejected?"""
        bad_bar_dot_list = ['(0.1|2.e)', '(.2|e)', '((0.1)|(1.2.0))', '(.|)']
        for r in bad_bar_dot_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

    def test_bar_star_ok(self: 'TestIsRegex') -> None:
        """Bar-star regexes accepted?"""
        bar_star_list = ['(0|1)*', '(0*|1)', '(1|0*)', '(0|(1|2*))*',
                         '((0|1)*|2)*']
        for r in bar_star_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_bar_star_fail(self: 'TestIsRegex') -> None:
        """Bar-star-like non-regexes rejected?"""
        bad_bar_star_list = ['0|1*', '*(0|1)', '(*0|1)', '(1|*0)', '(|0(1|2*)']
        for r in bad_bar_star_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

    def test_dot_star_ok(self: 'TestIsRegex') -> None:
        """Dot-star regexes accepted?"""
        dot_star_list = ['(0.1)*', '(0*.1)', '(1.0*)', '(0.(1.2*))*',
                         '((0.1)*.2)*']
        for r in dot_star_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_dot_star_fail(self: 'TestIsRegex') -> None:
        """Dot-star-like non-regexes rejected?"""
        bad_dot_star_list = ['0.1*', '*(0.1)', '(*0.1)', '(1.*0)', '(.0(1.2*)']
        for r in bad_dot_star_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

    def test_bar_star_dot_ok(self: 'TestIsRegex') -> None:
        """Bar-star-dot regexes accepted?"""
        bar_star_dot_list = ['((0.e)|(1*.2))*', '((0|e).(1*|2))*',
                             '(0|(1*.2))*', '((0|1)|(2*.(e|0)))*',
                             '((0.1).(2*|(e.0)))*']
        for r in bar_star_dot_list:
            self.assertTrue(is_regex(r),
                            "Rejects valid regex: {}".format(r))

    def test_bar_star_dot_fail(self: 'TestIsRegex') -> None:
        """Bar-star-dot non-regexes rejected?"""
        bad_bar_star_dot_list = ['0*|1.2', '((0*)|(1).(2))', '(0.1|2*)',
                                 '((0*|(1.2)))', '((0.1*)|(2*)',
                                 '((0|1).(2|((1.0))))*', '((0.1)|(2.((1|0))))*']
        for r in bad_bar_star_dot_list:
            self.assertFalse(is_regex(r),
                             "Accepts invalid regex: {}".format(r))

students_arp = all_regex_permutations
def all_regex_permutations(s:str):
    rv = students_arp(s)
    set_rv = set(rv)
    if len(set_rv) != len(rv):
        raise Exception("Student returned a list with duplicates")
    return set_rv

class TestAllRegexPermutations(TestCase):
    # Some students will return lists
    # len() works on both lists and sets
    # otherwise, just convert to a set.



    def test_empty_results(self) -> None:
        ex = ['0221','||(011)','0*.1*','0*1']
        for s in ex:
            self.assertTrue(len(set(all_regex_permutations(s))) == 0,
                            ("No regular expressions can be formed from {}" +
                             " but returned a non-empty collection").format(s))

    def test_leaf(self: 'TestAllRegexPermutations') -> None:
        """Correctly produces unique permutation of leaf?"""
        leaf_list = ['e', '0', '1', '2']
        for s in leaf_list:
            self.assertEqual(set(s), all_regex_permutations(s),
                             "Different permutation set: {}, {}".format(
                                 set(s), all_regex_permutations(s)))

    def test_binary(self: 'TestAllRegexPermutations') -> None:
        """Correctly produces permutations of binary regexes?"""
        binary_list = [('(0.1)', {'(0.1)', '(1.0)'}),
                       ('(1|2)', {'(1|2)', '(2|1)'}),
                       ('(1|2*)', {'(1|2*)', '(2*|1)', '(1*|2)', '(2|1*)',
                                   '(1|2)*', '(2|1)*'})]
        for t in binary_list:
            self.assertEqual(all_regex_permutations(t[0]), t[1],
                             "Different permutation sets: {}, {}".format(
                                 set(all_regex_permutations(t[0])), t[1]))

    def test_long(self: 'TestAllRegexPermutations') -> None:
        """Correctly produces permutations of long regex?"""
        # naive generation of permutations not practical for much longer strings
        s = '(0*.1)*'
        p = {'(0*.1)*', '(0*.1*)', '(0.1*)*', '(1*.0)*', '(1*.0*)',
             '(1.0*)*', '(0.1)**', '(1.0)**', '(1**.0)', '(1.0**)',
             '(0**.1)', '(0.1**)'}
        self.assertEqual(set(all_regex_permutations(s)), p)

is_regex_suite = TestLoader().loadTestsFromTestCase(TestIsRegex)
all_regex_permutations_suite = TestLoader().loadTestsFromTestCase(TestAllRegexPermutations)
match_regex_suite = TestLoader().loadTestsFromTestCase(TestRegexMatch)
build_regex_tree_suite = TestLoader().loadTestsFromTestCase(TestBuildRegexTree)


def show_failures_and_errors() -> TestResult:
    results = {}
    results['is_regex'] = TestResult()
    results['all_regex_permutations'] = TestResult()
    results['match_regex'] = TestResult()
    results['build_regex_tree'] = TestResult()

    is_regex_suite.run(results['is_regex'])
    all_regex_permutations_suite.run(results['all_regex_permutations'])
    match_regex_suite.run(results['match_regex'])
    build_regex_tree_suite.run(results['build_regex_tree'])

    failures = {}
    for case in results.keys():
        failures[case] = [e[0]._testMethodName for
                          e in results[case].failures]
    errors = {}
    for case in results.keys():
        errors[case] = [e[0]._testMethodName for
                        e in results[case].errors]


    for (case,methods) in failures.items():
        for m in methods:
            print("failure:{}.{}".format(case,m))
    for (case,methods) in errors.items():
        for m in methods:
            print("error:  {}.{}".format(case,m))


if __name__ == '__main__':
    OUTPUT_FOR_COMPUTING_STATS = False
    if OUTPUT_FOR_COMPUTING_STATS:
        results = show_failures_and_errors()
    else:
        TextTestRunner().run(is_regex_suite)
        TextTestRunner().run(all_regex_permutations_suite)
        TextTestRunner().run(match_regex_suite)
        TextTestRunner().run(build_regex_tree_suite)
    #main(exit=False, verbosity=2)
