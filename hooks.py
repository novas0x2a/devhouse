## web hook dispatcher library
#
# Idea:
# - recipients are urls
# - events are special strings starting with reversed domain
# - args are arbitrary dicts to post to each recipient of an event
# - cooldown time is the wait after a failed post before trying again
# - retry time is to total time during which retries will continue

from twisted.internet import defer, reactor
from twisted.web import client
from twisted.python import log

import time
import urllib

class HookManager(object):
    """I manage a list of active recipients to which I will do my best to deliver payloads."""
    
    cooldownTime = 60 # between successive hooks
    retryTime = 3600 # stop retrying after this time

    def __init__(self):
        self.recipients = []
    
    def addRecipient(self, recipient):
        self.recipients.append(recipient)
        
    def dispatchEvent(self, event, args={}):
        entry = {"event": event}
        entry.update(args)
        
        now = time.time()
        for r in self.recipients:
            self.__dispatchEventToRecipient(entry, r, now)
        
    def __dispatchEventToRecipient(self, entry, recipient, ctime):
        
        def _good(page):
            log.msg(page)
            pass
        
        def _bad(reason):
            log.msg(reason)
            reactor.callLater(
                self.cooldownTime,
                self.__dispatchEventToRecipient,
                entry,
                recipient,
                ctime)
        
        now = time.time()
        if now < ctime + self.retryTime:
            data = urllib.urlencode(entry)
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'content-length': str(len(data)),
            }
            client.getPage(recipient, method='POST', postdata=data, headers=headers) \
                .addCallbacks(_good,_bad) 
        else:
            # silently drop this guy because it is past his retry time
            pass


if __name__ == "__main__":
    import sys
    log.startLogging(sys.stdout)
    hooker = HookManager()
    hooker.addRecipient("http://cacti.fihn.net/index.php")
    hooker.addRecipient("http://localhost:8181/echo")
    reactor.callLater(0,lambda: hooker.dispatchEvent("cats", {'x':'ex'}))
    reactor.run()