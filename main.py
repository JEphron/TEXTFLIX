from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import sys
import ansi.colour.rgb
import ansi.colour.fx
def range_map(x, imi, ima, omi, oma):
  return (x-imi)*(oma-omi)/(ima-imi)+omi;
chars = [' ','M','@','F','P','2','Q','O','7','l',';',',','.',' ']
def pa(img):
  width, height = img.size
  width, height = width/2, height/4
  img = img.resize((width, height), Image.ANTIALIAS)
  img_array = np.array(img)
  def f(x):
      lightness = int(x[0]) + int(x[1]) + int(x[2])
      index = int(range_map(lightness, 0, 755, 0, len(chars)-1))
      msg = (rgb256(int(x[0]), int(x[1]), int(x[2])), chars[index], reset)
      return ''.join(map(str, msg))
  img_array = np.apply_along_axis(f, 2, img_array)
  print '\n'.join(''.join(str(cell) for cell in row) for row in img_array)+'\r'
class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
    def onOpen(self):
        print("WebSocket connection open.")
    def onMessage(self, payload, isbin):
        if not isbin:
          data = payload.decode('utf8')[22:]
          im = Image.open(BytesIO(base64.b64decode(data)))
          pa(im)
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
if __name__ == '__main__':
    from twisted.python import log
    from twisted.internet import reactor
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8088", debug=False)
    factory.protocol = MyServerProtocol
    reactor.listenTCP(8088, factory)
    reactor.run()