from twisted.web import server, resource
from twisted.internet import reactor
from twitter import api

email = "shdhbot"
password = "iz4robotmeow"
twitter = api.Twitter(email, password)

# example:
# {'attended_shdh_00': '1232938414', 'last_name': 'Smith', 'badge_icons':
# 'None', 'tags': "taggity, tag, tag'", 'first_name': 'Adam', 'key':
# 'adam@adamsmith.as', 'event': 'org.superhappydevhouse.event.Attendance'}

desired_event_type = "org.superhappydevhouse.event.Attendance"

class Tweet(resource.Resource):
  isLeaf = True
  def render(self,request):
    d = dict([(k,vs[0])for (k,vs) in request.args.items()])
    print d
    if not d['event'] == desired_event_type:
      return ""
    else:
      f = d['first_name']
      l = d['last_name'][0] + '.'
      e = d['event_key'].replace("_","")
      msg = "%s %s just arrived #%s" % (f, l, e)
      twitter.statuses.update(status=msg)
      return msg

reactor.listenTCP(10100, server.Site(Tweet()))
reactor.run()
