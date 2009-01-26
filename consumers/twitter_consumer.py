from consumer import easy_consume
from twitter import api

desired_event_type = "org.superhappydevhouse.event.Attendance"

email = "shdhbot"
password = "iz4robotmeow"
twitter = api.Twitter(email, password)

@easy_consume(10100)
def tweet(request):
  d = dict([(k,vs[0])for (k,vs) in request.args.items()])
  if not d['event'] == desired_event_type:
    return ""
  else:
    f = d['first_name']
    l = d['last_name'][0] + '.'
    e = d['event_key'].replace("_","")
    msg = "%s %s just arrived #%s" % (f, l, e)
    twitter.statuses.update(status=msg)
    return msg
