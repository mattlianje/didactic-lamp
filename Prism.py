#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from util2 import Arff2Skl

"""

Input data:
   The input of the program has to be an .arff file.
   During initialization, this implementation loads the .arff file and
   coverts it into a suitable representation. This is done by using the
   Arff2Skl() class defined in util2.py (self._cvt in code).  The
   convertion of the dataset is done by calling the .to_dict() method.
   By calling this method we translate the dataset from the .arff format:

   age	 spectacle-prescrip   astigmatism   tear-prod-rate  contact-lenses
   --------------------------------------------------------------------------
   young	myope               no	                  reduced         none
   young	myope               no      	normal	       soft
   young	myope               yes     	reduced         none
   ...

   to our representation that is a list of dictionaries:

   data = [{'age': 'young', 'spectactle-prescrip': 'myope',
            'astigmatism': 'no', 'tear-prod-rate': reduced,
            'contact-lenses': 'none'},
           {'age': 'young', 'spectactle-prescrip': 'myope',
            'astigmatism': 'no', 'tear-prod-rate': 'normal',
            'contact-lenses': 'none'}, ..., ]

   Other information such as: attributes and label are extracted from
   the metadata of the .arff. These are obtaned by:

   attributes = self._cvt.meta.names() # ['age', 'spectact-prescrip', ..., ]
   label = attributes[-1]  # 'contact-lenses' (what we want to predict)
   classes = self._cvt.meta[label][1] # ['none', 'soft', 'hard']

Rule encoding:
   A rule is encoded as a list of one or more predicates.
   In the case of the contact-lenses dataset,
   a rule for the 'hard' class is:

   'astigmatism'=='yes' and
   'tear-prod-rate'=='normal' and
   'spectacle-prescrip', 'myope'

   Here the rule is encoded as list of tuples of the form:

   rule = [('astigmatism', 'yes'), ('tear-prod-rate', 'normal'),
           ('spectacle-prescrip', 'myope)]

Output format:
   The output of the program is the set of rules returned
   by the fit() method of the Prism class. The set of all rules are
   represented as a list of dictionaries indexed by all the possible
   classes. For example, in the case of contact-lenses dataset the
   output would be something like:

   R = [{'soft': [('astigmatism', 'no'), ('tear-prod-rate', 'normal'),
                          ('spectacle-prescrip', 'hypermetrope')]},
                {'soft': [('astigmatism', 'no'), ('tear-prod-rate', 'normal'),
                          ('age', 'pre-presbyopic')]},
                ...,
                {'hard': [('astigmatism', 'yes'), ('tear-prod-rate', 'normal'),
                          ('spectacle-prescrip', 'myope')]},
                ...,
                {'none': [....]}, ...]

"""


class Prism():

    def __init__(self, dataf):
        assert (os.path.exists(dataf))
        self._cvt = Arff2Skl(dataf)

    def fit(self, label=[]):
        data, attributes = (self._cvt.to_dict(),
                            self._cvt.meta.names())
        if not label:
            label = attributes[-1]

        # classes stores all possible values for the class
        # ex: class 'contact-lenses' can be 'none', 'soft' or 'hard', so classes = ['none','soft','hard']
        classes = self._cvt.meta[label][1]  # C

        # R is a list that stores all the rules
        R = []
        for cls in classes:
            # instances are the rows of the dataset
            instances = data[:]  # E
            while self.__has_class_value(instances, label, cls):
                rule, covered = self.__build_rule(instances, attributes,
                                                  label, cls)
                R.append({cls: rule})
                instances = self.__remove_covered_instances(instances, covered)
        return R, label

    def __build_rule(self, instances, attributes, label, cls):
        R, accuracy = [], -1.0
        rule_instances = instances[:]
        avail_attr = [a for a in attributes if a != label]
        # -----------------------------------------------------------------------------------
        # THE BELOW CODE COMPLETED BY DAHV REINHART - V00735279
        # -----------------------------------------------------------------------------------
        while True:
            allRules = []
            for A in self.__attr_not_in_R(avail_attr, R):
                for X in self.__get_attr_values(rule_instances, A):
                    coverage = self.__apply_rule(rule_instances, [[A, X]])
                    accuracy = self.__rule_accuracy(coverage, label, cls)
                    allRules.append([A, X, accuracy[0], accuracy[1]])

            bestRule = self.__get_best_rule(allRules)

            R.append((bestRule[0][0], bestRule[0][1]))

            rule_instances = self.__apply_rule(rule_instances, R)

            if bestRule[0][2] == 1.0 or bestRule[0][3] < 1:
                break

        return R, rule_instances

    def __get_best_rule(self, rules):
        rule = []

        runningBest = []
        maxAcc = 0
        maxCov = 0
        for potentRule in rules:
            if potentRule[2] > maxAcc:
                maxAcc = potentRule[2]
                maxCov = potentRule[3]
                runningBest.append(potentRule)

            elif potentRule[2] == maxAcc:
                if potentRule[3] > maxCov:
                    runningBest.append(potentRule)

        rule.append(runningBest[-1])
        # ---------------------------------------------------------------------------------
        # THE ABOVE CODE COMPLETED BY DAHV REINHART - V00735279
        # ---------------------------------------------------------------------------------
        return rule

    def predict(test_data_file, rules):
        test_data = pickle.load(open(test_data_file, 'rb'))
        p = []
        return p

    # This method returns the instances covered by the set of rules
    def __apply_rule(self, data, R):
        coverage = data[:]
        for r in R:
            coverage = [i for i in coverage if i[r[0]] == r[1]]
        return coverage

    # This method remove all instances covered by the set of rules
    def __remove_covered_instances(self, instances, covered):
        return [i for i in instances if i not in covered]

    # Computes p/t
    def __rule_accuracy(self, coverage, label, cls):
        accuracy = [i for i in coverage if i[label] == cls]
        return float(len(accuracy)) / len(coverage), len(accuracy)

    # Counts how many instances of a given label have the specified class
    # ex: how many 'contact-lenses' = 'hard'
    def __has_class_value(self, instances, label, cls):
        asd = [i for i in instances if i[label] == cls]
        return len(asd)

    # Returns a list of all possible values of a given attribute
    def __get_attr_values(self, instances, attr):
        return self.__unique([a[attr] for a in instances])

    # Returns a list of all unique values of a list
    def __unique(self, l):
        return list(set(l))

    # Returns list of attributes not present in the rules
    def __attr_not_in_R(self, attr, R):
        return [a for a in attr if a not in [r[0] for r in R]]


# Debugging function printing the set of rules in english
def printRules(rules, label):
    for rule in rules:
        k = rule.keys()[0]
        nbr = len(rule[k])

        theRule = " IF "
        for subrules in rule[k]:
            nbr -= 1
            theRule = theRule + str(subrules[0]) + " = " + subrules[1]
            if nbr > 0:
                theRule = theRule + "\n\t AND "
            else:
                theRule = theRule + "\n\t THEN " + label + " = " + k

        print
        theRule + "\n"


if __name__ == '__main__':
    import sys

    prism = Prism(sys.argv[1])
    rules, label = prism.fit()

    # printRules(rules,label)
    print
    rules
    # print p
