import json
import os
import sys
from gevent import monkey

monkey.patch_all()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from pymongo import MongoClient
from flask import render_template, Flask
from werkzeug.debug import DebuggedApplication

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

from mechat.blueprints.ai_baidu import Baidu_AI

baidu_ai = Baidu_AI()

mgclient = MongoClient("127.0.0.1", 27017)
MONGO_DB = mgclient["chat_mess_room"]

flask_app = Flask(__name__)
flask_app.debug = True


class ChatApplication(WebSocketApplication):
    def on_open(self):
        print('connect')

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)
        # a = {'msg_type': 'message', 'nickname': 'unknown', 'message': '你啊'}

        if message['msg_type'] == 'message':
            im = message['message']
            tuningre = baidu_ai.tuning(im)
            cur_time = message.get('cur_time')
            the_robot = {'msg_type': 'message', 'nickname': '图灵机器人的爸爸', 'message': tuningre, 'the_robot': "robot",
                         'cur_time': cur_time}

            self.broadcast(message)
            self.broadcast(the_robot)
            MONGO_DB.groups.insert_many([message, the_robot])



        elif message['msg_type'] == 'update_clients':
            self.send_client_list(message)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            # client.ws.send(json.dumps({
            #     'msg_type': 'message',
            #     'nickname': message['nickname'],
            #     'message': message['message']
            # }))
            client.ws.send(json.dumps(message))

    def on_close(self, reason):
        print('Connectiion closed')


@flask_app.route('/')
def home():
    te = [{"nickname": "baozi", "body": '你的名字叫啥'},
          {"nickname": "baozi", "body": '做个自我介绍啊'},
          {"nickname": "baozi", "body": '发图啊'}]

    re = list(MONGO_DB.groups.find({}, {"_id": 0}))

    # return render_template("home2.html")
    return render_template("home2.html", messages=re)


if __name__ == '__main__':
    WebSocketServer(('192.168.1.2', 9999), Resource([
        ('^/chat', ChatApplication),
        ('^/.*', DebuggedApplication(flask_app))
    ]), debug=False).serve_forever()
