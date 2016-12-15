#!/usr/bin/env python

"""
Command-line script for generating embeddings
Useful if you want to generate larger embeddings for some models
"""

from __future__ import print_function

import os
import sys
import random
import pickle
import argparse
import logging

random.seed(42)


def load(path, name):
    return pickle.load(open(os.path.join(path, name), 'rb'))


def revert(vocab, indices):
    return [vocab.get(i, 'X') for i in indices]

try:
    data_path = os.environ['INSURANCE_QA']
except KeyError:
    print('INSURANCE_QA is not set. Set it to your clone of https://github.com/codekansas/insurance_qa_python')
    sys.exit(1)


vocab = load(data_path, 'vocabulary')
#print(vocab)

train = load(data_path, 'train')
teste = [revert(vocab, q['question']) for q in train]
#print(train)

answers = load(data_path, 'answers')
sentences = [revert(vocab, txt) for txt in answers.values()]
print(answers)
#mdict = { 1: 'Zara', 2: '7', 3: 'First'}
#print(mdict)