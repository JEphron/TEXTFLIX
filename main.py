from autobahn.twisted.websocket import *
import base64
from PIL import Image
import io
import numpy as np
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
def range_map(x, imi, ima, omi, oma):
  return (x-imi)*(oma-omi)/(ima-imi)+omi;
chars = [' ','M','@','F','P','2','Q','O','7','l',';',',','.',' ']
def pa(i):
  w,h=i.size
  w,h=w/2,h/4
  i=i.resize((w,h),Image.ANTIALIAS)
  ia=np.array(i)
  def f(x):
      li=int(x[0])+int(x[1])+int(x[2])
      ix=int(range_map(li,0,755,0,len(chars)-1))
      msg=(rgb256(int(x[0]),int(x[1]),int(x[2])),chars[ix],reset)
      return ''.join(map(str,msg))
  ia = np.apply_along_axis(f,2,ia)
  print '\n'.join(''.join(str(c) for c in r) for r in ia)+'\r'
class MyServerProtocol(WebSocketServerProtocol):
    def onMessage(s,p,b):
        if not b:
          d=p.decode('utf8')[22:]
          im=Image.open(io.BytesIO(base64.b64decode(d)))
          pa(im)
from twisted.internet import reactor as rc
fc=WebSocketServerFactory(u"ws://127.0.0.1:8088",debug=False)
fc.protocol=MyServerProtocol
rc.listenTCP(8088, fc)
rc.run()