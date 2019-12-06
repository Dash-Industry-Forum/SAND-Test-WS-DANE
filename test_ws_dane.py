#!/usr/bin/env python

"""
SAND WS Test DANE.

This implements a DANE for testing purposes according to ISO/IEC 23009-5 SAND.
It implementes a WebSocket SAND Channel that a DASH client can connect to.
SAND messages that may be sent and received by this test DANE do not reflect
real operations but merely serve as example behaviour.

Copyright (c) 2019-, TNO
All rights reserved.

See AUTHORS for a full list of authors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import sys

from autobahn.twisted.websocket import WebSocketServerProtocol
import logging

MESSAGES = {
    "DaneCapabilitiesNA": 
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<SANDMessage xmlns="urn:mpeg:dash:schema:sandmessage:2016" senderId="abc1234" generationTime="2016-02-21T11:20:52-08:00">'
          '<DaneCapabilities messageId="45678" messageSetUri="http://dashif.org/guidelines/sand/modes/na"></DaneCapabilities>'
        '</SANDMessage>'
}

class TestDANE(WebSocketServerProtocol):
    """
    Implements a WebSocket Test DANE.
    """

    def onConnect(self, request):
        logging.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        logging.debug("WebSocket connection open.")
        self.sendMessage(MESSAGES["DaneCapabilitiesNA"], False)

    def onMessage(self, payload, isBinary):
        # Check Data frame type
        if isBinary:
            logging.debug(
                "Binary message received: {0} bytes".format(len(payload)))

        else:
            logging.debug(
                "Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        logging.info("WebSocket connection closed: {0}".format(reason))

def run():
    """
    Runs the server.
    """
    from twisted.python import log
    from twisted.internet import reactor
    file_handler = logging.FileHandler(filename='debug.log')
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(handlers=handlers, level=logging.DEBUG)
    log.startLogging(sys.stdout)

    from autobahn.twisted.websocket import WebSocketServerFactory
    factory = WebSocketServerFactory()
    factory.protocol = TestDANE

    import os
    port = 9000
    if os.environ.get('PORT') is not None:
        port = int(os.environ['PORT'])

    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == '__main__':
    run()
