## attendance tracking library
#
# Copyright (c) 2008, 2009 Adam Marshall Smith
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Idea:
# - prefill gets a view of a person's card (to the best of our knowledge)
# - attend updates their card and if they are new calls onAttend
# - attended_{event} is added to the card on first attend call

import time

class AttendanceManager(object):
    prefillKeys = ["first_name", "last_name", "tags", "badge_icons"]
    
    def __init__(self, cardStore, eventKey, onAttend):
        self.cardStore = cardStore
        self.onAttend = onAttend
        self.attendKey = "attended_"+eventKey
    
    def prefill(self, key):
        return self.cardStore.getCard(key, self.prefillKeys)
    
    def attend(self, key, updates):
        justAttended = self.cardStore.getCard(key, [self.attendKey])
        itsANewKid = justAttended[self.attendKey] is None

        filteredUpdates = \
          dict([(k, updates.get(k,None)) for k in self.prefillKeys])
        filteredUpdates[self.attendKey] = int(time.time())

        self.cardStore.updateCard(key, filteredUpdates)

        if itsANewKid: self.onAttend(key)
