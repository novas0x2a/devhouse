from twisted.web import server, resource
from twisted.internet import reactor

def consumer(f):
  class R(resource.Resource):
    isLeaf = True
  R.render = lambda res, req: f(req)
  R.tag = f.__name__
  return R()

def serve(res, port):
  if type(res) is dict:
    root = resource.Resource()
    for k,v in res.iteritems():
      root.putChild(k,v)
    res = root
  if type(res) is list:
    root = resource.Resource()
    for r in res:
      root.putChild(r.tag, r)
    res = root
  reactor.listenTCP(port, server.Site(res))
  reactor.run()

def easy_consume(port=80):
  return lambda f: serve(consumer(f),port)
