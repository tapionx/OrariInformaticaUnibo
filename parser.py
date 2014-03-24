from bottle import route, run
import re
import urllib2
from BeautifulSoup import BeautifulSoup
import json
import pprint

@route('/<name>')
def index(name):
  
  if( name == 'primo' or name == 'secondo' or name == 'terzo'):
    contenturl = "http://orari.web.cs.unibo.it/cgi-bin/2013-2014/II-ciclo/inf/"
    contenturl = contenturl + name + '.php'
    soup = BeautifulSoup(urllib2.urlopen(contenturl).read())
    return parse_timetable(soup)
  else:
    abort(404, 'ERRORE')  

def parse_timetable(soup):

  out = []

  table = soup.find('table')
  rows = table.findAll('tr')
  for tr in rows:
    hour = []
    cols = tr.findAll('td')
    for col in cols:
      col = unicode(col)
      col = col.split('<br />')
      for i in range(len(col)):
        col[i] = re.sub('<[^<]+?>', '', col[i])
      if(len(col) == 1):
        col = col[0]
      hour.append(col)
    out.append(hour)

  return json.dumps(out)

#parse_timetable()
run(host='0.0.0.0', port=8080)
