#!/usr/bin/env python

import pprint
import pickle

cards = pickle.load(file('rolodex.dat', 'r+b'))
pprint.pprint(cards)
