#!/usr/bin/env python
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
