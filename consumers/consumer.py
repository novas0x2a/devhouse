from twisted.web import server, resource
from twisted.internet import reactor

def consumer(f):
  class R(resource.Resource):
    isLeaf = True
  R.render = lambda res, req: f(req)
  return R()

def serve(res, port=10100):
  reactor.listenTCP(port, server.Site(res))
  reactor.run()

