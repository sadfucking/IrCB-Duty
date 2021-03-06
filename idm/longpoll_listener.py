from idm.objects import LongpollEvent, DB, dp, db_gen
from microvk import VkApi, VkApiResponseException
from idm.utils import gen_secret
from wtflog import warden
from .app import app
from flask import request
import traceback
import json

logger = warden.get_boy('Приемник сигналов LP модуля')


@app.route('/ping', methods=["POST"])
def ping():
    return "ok"


@app.route('/longpoll/event', methods=["POST"])
def longpoll():
    event = LongpollEvent(request.json)

    if event.data['access_key'] != event.db.lp_settings['key']:
        return "?"

    d = dp.longpoll_event_run(event)
    if type(d) == dict:
        return json.dumps(d, ensure_ascii=False)
    return json.dumps({"response": "ok"}, ensure_ascii=False)


class error:
    AuthFail = 0


@app.route('/longpoll/start', methods=["POST"])
def get_data():
    token = json.loads(request.data)['token']

    try:
        if VkApi(token)('users.get')[0]['id'] != db_gen.owner_id:
            raise ValueError
    except (KeyError, IndexError, ValueError):
        return json.dumps({'error': error.AuthFail})

    db = DB()
    db.lp_settings['key'] = gen_secret(length=20)
    db.save()
    return json.dumps({
            'chats': db.chats,
            'deleter': db.responses['del_self'],
            'settings': db.lp_settings,
            'self_id': db.duty_id
        })


@app.route('/longpoll/sync', methods=["POST"])
def sync_settings():
    data = request.json

    db = DB()

    if data['access_key'] != db.lp_settings['key']:
        return "?"

    db.lp_settings.update(data['settings'])
    db.save()
    return "ok"
