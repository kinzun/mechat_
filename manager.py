from mechat import create_app

from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer

app = create_app()
app.debug = True

if __name__ == '__main__':
    wb_socket = WSGIServer(("127.0.0.1", 9999), app, handler_class=WebSocketHandler)
    wb_socket.serve_forever()
