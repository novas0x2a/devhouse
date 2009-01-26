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

import simplejson

import cards
import attendance
import printer
import hooks
import secure

####
#### Web Resources (like pages)
####

class RootRedirector(resource.Resource):
    def render(self, request):
        request.redirect("/static/welcome.html")
        return ""

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
        return simplejson.dumps(dict(status=jobStatus))
        
class Prefill(resource.Resource):
    isLeaf = True
    def __init__(self, attendanceManager):
        resource.Resource.__init__(self)
        self.attendanceManager = attendanceManager

    def render_GET(self, request):
        key = request.postpath[0]
        prefill = attendanceManager.prefill(key)
        request.setHeader("content-type", "application/json")
        return simplejson.dumps(prefill)
                
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
        return simplejson.dumps(dict(printJobId=printJobId))

###
### Top Level
###

if __name__ == "__main__":
    import sys, os
    if len(sys.argv) != 3:
        print "%s cards.dat event_0" % sys.argv[0]
        sys.exit(1)
    dat = sys.argv[1] # pickle'd dict for backing the card store
    eventKey = sys.argv[2] # keyable name for identifying the CURRENT event

    log.startLogging(sys.stdout)
    
    hookManager = hooks.HookManager()
    # example: hookManager.addRecipient("http://cacti.fihn.net/")
    
    cardStore = cards.CardStore(dat)

    def onAttend(key):
        fullCard = cardStore.getCard(key)
        hookManager.dispatchEvent("org.superhappydevhouse.event.Attendance", fullCard)
        log.msg("ARRIVAL: looks like %s arrived." % key)

    attendanceManager = \
        attendance.AttendanceManager(cardStore, eventKey, onAttend)
    
    printerManager = printer.PrinterManager()
    printerManager.updates.update(event_key=eventKey)

    # XXX: adding shdh_number for badge print compatibility
    parts = eventKey.split("_")
    if len(parts) < 2:
      print "Event key SHOULD REALLY look like \"shdh_99\"!!"
      sys.exit(2)
    printerManager.updates.update(shdh_number=parts[1])

    # secure welcome root resource
    sroot = resource.Resource()
    sroot.putChild('', RootRedirector())
    sroot.putChild('static', static.File('static'))
    sroot.putChild('printer', Printer(printerManager))
    sroot.putChild('prefill', Prefill(attendanceManager))
    sroot.putChild('attend', \
        Attend(attendanceManager, printerManager, cardStore))
    
    # insecure root
    iroot = static.File('bootstrap')

    # reactor setup

    if os.environ.get('INSECURE',False):
        reactor.listenTCP(10081, server.Site(sroot))

    reactor.listenSSL(10443, server.Site(sroot), \
        secure.ServerContextFactory(myKey='certs/server.pem', trustedCA='certs/ca-cert.pem'))
        
    reactor.listenTCP(10080, server.Site(iroot)) 
    
    log.msg("It's a piece of cake to break a pretty snake. [SYSTEM ONLINE]")
    reactor.run()
