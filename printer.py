## print queue library
#
# Idea:
# - cards are dicts that will be given to the print binary
# - the print binary returns when printing is completed
# - outstanding jobs can tracked for status
# - failed jobs can be easily relaunched

from twisted.internet import protocol, reactor, defer
from twisted.python import log
import demjson

class SpamProtocol(protocol.ProcessProtocol):
    """I take some prepackaged spam and feed it to some process."""

    def __init__(self, spam):
        self.spam = spam
        self.d = defer.Deferred()
    
    def connectionMade(self):
        self.transport.write(self.spam)
        self.transport.closeStdin()
    
    def processEnded(self, reason):
        if reason.value.exitCode is 0:
            self.d.callback(reason.value.exitCode)
        else:
            self.d.errback(reason.value.exitCode)

class PrinterManager(object):
    """I implement a fancy print queue."""

    commandLine = ["./print_badge"]

    def __init__(self):
        self.lastJobId = 0
        self.outstandingJobs = {}
        self.failedJobs = {}    

    def __makeJob(self):
        jobId = self.lastJobId
        self.lastJobId += 1
        return jobId

    def printCard(self, card):
        jobId = self.__makeJob()
        log.msg('Starting print job %d.' % jobId)
        self.outstandingJobs[jobId] = card
        def _done(result):
            log.msg('Finished print job %d.' % jobId)
            del self.outstandingJobs[jobId]
            return True
        def _failed(failure):
            log.msg('Failed print job %d.' % jobId)
            del self.outstandingJobs[jobId]
            self.failedJobs[jobId] = card
            return False
        spam = demjson.encode(card).encode('utf8')
        spamProto = SpamProtocol(str(spam)+"\n")
        spamProto.d.addCallbacks(_done, _failed)
        
        reactor.spawnProcess(spamProto, self.commandLine[0], self.commandLine)
        
        return (jobId, spamProto.d)
        
    def getOutstandingJobs(self):
        return self.outstandingJobs
    
    def getFailedJobs(self):
        return self.failedJobs
    
    def retryFailedJob(self, jobId):
        if jobId in self.failedJobs.keys():
            card = self.failedJobs[jobId]
            del self.failedJobs[jobId]
            return self.printCard(card)
            
    def deleteFailedJob(self, jobId):
        if jobId in self.failedJobs.keys():
            del self.failedJobs[jobId]

