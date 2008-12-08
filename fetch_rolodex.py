import urllib
import sys
import simplejson
import pickle

if len(sys.argv) is not 3:
    print 'usage: ', sys.argv[0], 'url', 'some.dat'    
    sys.exit(-1)

url = sys.argv[1]
dat = sys.argv[2]

p = urllib.urlopen(url)
json_text = p.read()
p.close()

f = open(dat,'wb')
f.write(pickle.dumps(simplejson.loads(json_text)))
f.close()
