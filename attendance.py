## attendance tracking library
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
        fullUpdates = {self.attendKey: int(time.time())}
        fullUpdates.update(updates)
        self.cardStore.updateCard(key, fullUpdates)
        if itsANewKid: self.onAttend(key)
