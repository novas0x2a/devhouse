## welcome system core
#
# Idea:
# - run a web server for serving misc welcome system related pages
#   - GET /prefill/{key} gets a view of known details for {key}
#   - POST /attend/{key} updates card store, notices new attendees, and prints
#   - GET /print/{id} gets a print job's status
#
# - new attendees have their cards hooked out to any registered recipients

from twisted.internet import reactor
from twisted.python import log
from twisted.web import server, resource, static, http

import demjson

import cards
import attendance
import printer
import hooks

# helpers to turn python objs into transport strings
def enjson(d): return demjson.encode(d).encode('utf8')
def dejson(str): return demjson.decode(str.decode('utf8'))

####
#### Web Resources (like pages)
####

class Printer(resource.Resource):
    isLeaf = True
    def __init__(self, printerManager):
        resource.Resource.__init__(self)
        self.printerManager = printerManager
    
    def render_GET(self, request):
        if len(request.postpath) is not 1:
            request.setResponseCode(http.NOT_FOUND)
            return ""
            
        jobId = int(request.postpath[0])
        jobStatus = "finished"
        if jobId in printerManager.getOutstandingJobs():
            jobStatus = "outstanding"
        elif jobId in printerManager.getFailedJobs():
            jobStatus = "failed"
        return enjson(dict(status=jobStatus))
        
class Prefill(resource.Resource):
    isLeaf = True
    def __init__(self, attendanceManager):
        resource.Resource.__init__(self)
        self.attendanceManager = attendanceManager

    def render_GET(self, request):
        key = request.postpath[0]
        prefill = attendanceManager.prefill(key)
        request.setHeader("content-type", "application/json")
        return enjson(prefill)
                
class Attend(resource.Resource):
    isLeaf = True
    def __init__(self, attendanceManager, printerManager, cardStore):
        resource.Resource.__init__(self)
        self.attendanceManager = attendanceManager
        self.printerManager = printerManager
        self.cardManager = cardStore

    def render_POST(self, request):
        key = request.postpath[0]
        updates = dict([(k,vs[0])for (k,vs) in request.args.items()])
        attendanceManager.attend(key, updates)
        fullCard = cardStore.getCard(key)
        printJobId, d = printerManager.printCard(fullCard)
        request.setHeader("content-type", "application/json")
        return enjson(dict(printJobId=printJobId))

###
### Top Level
###

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "%s cards.dat event_0" % sys.argv[0]
        sys.exit(1)
    dat = sys.argv[1] # pickle'd dict for backing the card store
    eventKey = sys.argv[2] # keyable name for identifying the CURRENT event

    log.startLogging(sys.stdout)
    
    hookManager = hooks.HookManager()
    hookManager.addRecipient("http://cacti.fihn.net/")
    
    cardStore = cards.CardStore(dat)

    def onAttend(key):
        fullCard = cardStore.getCard(key)
        hookManager.dispatchEvent("org.devhouse.event.Attendance", fullCard)
        log.msg("looks like %s arrived." % key)

    attendanceManager = \
        attendance.AttendanceManager(cardStore, eventKey, onAttend)
    
    printerManager = printer.PrinterManager()

    # welcome root resource
    root = resource.Resource()
    root.putChild('static', static.File('static'))
    root.putChild('printer', Printer(printerManager))
    root.putChild('prefill', Prefill(attendanceManager))
    root.putChild('attend', \
        Attend(attendanceManager, printerManager, cardStore))

    # reactor setup
    reactor.listenTCP(8181, server.Site(root))
    log.msg("It's a piece of cake to break a pretty snake. [SYSTEM ONLINE]")
    reactor.run()
