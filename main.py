# -*- coding: utf-8 -*-

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import base64
from PIL import Image
from io import BytesIO
import math
import numpy as np
import sys
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset

def range_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

chars = [' ', 'M', '@', 'F', 'P', '2', 'Q', 'O', '7', 'l', ';', ',', '.', ' ']

# 204 x 57

def print_ascii_frame(img):

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
  # img_array = np.swapaxes(img_array, 0, 1)
  # outstring = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
  print '\n'.join(''.join(str(cell) for cell in row) for row in img_array)+'\r'
  # loops are really slow

  # for y in range(0, height):
  #     for x in range(0, width):
  #       outstring = outstring + img_array[x][y]
  #         # sys.stdout.write(img_array[x][y])
  #     # sys.stdout.write('\n')    
  #     outstring = outstring + '\n'
  # for x in range(10):
  #   sys.stdout.write('{}\r'.format(outstring))



class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
    ind = 0

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
          # print("received {0} bytes".format(len(payload.decode('utf8'))))
          # self.ind = self.ind + 1
          # data:image/png;base64,
          data = payload.decode('utf8')[22:]
          im = Image.open(BytesIO(base64.b64decode(data)))
          print_ascii_frame(im)
          print(len(payload.decode('utf8')))

        # echo back message verbatim
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    # log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8088", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(8088, factory)
    reactor.run()