## print queue library
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
#
# Idea:
# - cards are dicts that will be given to the print binary
# - the print binary returns when printing is completed
# - outstanding jobs can tracked for status
# - failed jobs can be easily relaunched

from twisted.internet import protocol, reactor, defer
from twisted.python import log
import simplejson
import copy

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
    updates = {}

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
        fullCard = copy.copy(card)
        fullCard.update(self.updates)
        spam = simplejson.dumps(fullCard)
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

