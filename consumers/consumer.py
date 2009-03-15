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
