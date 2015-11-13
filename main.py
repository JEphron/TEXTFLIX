# -*- coding: utf-8 -*-

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.conch.telnet import TelnetTransport, TelnetProtocol
import base64
from PIL import Image
from io import BytesIO
import math
import numpy as np
import numpy.ma as ma
import sys
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
import time

"""
    todo: faster update speed
                implement mp4 style diffing 
                do a speed test to see what's so slow

"""


def range_map(x, in_min, in_max, out_min, out_max):
    # maps an input value in a given range to a new range
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# character set from heaviest to lightest
chars = [' ', 'M', '@', 'F', 'P', '2', 'Q', 'O', '7', 'l', ';', ',', '.', '*']

# previous_image = None


def ascii_frame(img):
    # the algorithm itself
    # takes the lightness of each pixel and maps it to a character in the set

    width, height = img.size
    width, height = width / 2, height / 4
    img = img.resize((width, height), Image.ANTIALIAS)
    img_array = np.array(img)

    def f(x):
        brightness = int(x[0]) + int(x[1]) + int(x[2])
        index = int(range_map(brightness, 0, 755, 0, len(chars) - 1))
        # rbg256 and reset are from the ansi package and are for color
        msg = (rgb256(int(x[0]), int(x[1]), int(x[2])), chars[index], reset)
        return ''.join(map(str, msg))

    img_array = np.apply_along_axis(f, 2, img_array)
    start_time = time.clock()
    rendered_string = '\n'.join(''.join(str(cell)
                                        for cell in row) for row in img_array)
    return rendered_string
    #
    # fin_time = time.clock()
    # print '%.2f' % (fin_time - start_time)
    # sys.stdout.write(rendered_string)


clients = []


class TelnetRelay(TelnetProtocol):

    def connectionMade(self):
        clients.append(self)

    def connectionLost(self, reason):
        clients.remove(self)

class ChromeExtWebSockProtocol(WebSocketServerProtocol):

    def onMessage(self, payload, isBinary):
        data = payload.decode('utf8')[22:]
        im = Image.open(BytesIO(base64.b64decode(data)))
        frame = ascii_frame(im)
        for i in clients:
            i.transport.write("\x1b[2J\x1b[1;1H")
            i.transport.write(frame)

if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.internet.protocol import ServerFactory

    # log.startLogging(sys.stdout)

    wsfactory = WebSocketServerFactory(u"ws://127.0.0.1:8088", debug=False)
    wsfactory.protocol = ChromeExtWebSockProtocol

    tnfactory = ServerFactory()
    tnfactory.protocol = lambda: TelnetTransport(TelnetRelay)

    reactor.listenTCP(8088, wsfactory)
    reactor.listenTCP(8077, tnfactory)
    reactor.run()
