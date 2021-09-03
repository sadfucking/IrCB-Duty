import io
import re
import requests
from html import escape

from idm.objects import MySignalEvent, dp
from .template import delete_template


@dp.longpoll_event_register('+гс')
@dp.my_signal_event_register('+гс')
def voice_create(event: MySignalEvent) -> str:
    name = re.findall(r"([^|]+)\|?([^|]*)", ' '.join(event.args))
    if not name:
        event.msg_op(2, "❗ Не указано название")
        return "ok"
    category = name[0][1].lower().strip() or 'без категории'
    name = name[0][0].lower().strip()

    if category == 'все':
        event.msg_op(2, '❗ Невозможно создать голосовое сообщение ' +
                     'с категорией "все"')
        return "ok"

    try:
        if event.reply_message['attachments'][0]['type'] != 'audio_message':
            raise TypeError
    except (KeyError, IndexError, TypeError):
        event.msg_op(2, "❗ Необходим ответ на голосовое сообщение")
        return "ok"

    attach = event.reply_message['attachments'][0]['audio_message']
    data = requests.get(attach['link_mp3'])
    audio_msg = io.BytesIO(data.content)
    audio_msg.name = 'voice.mp3'
    upload_url = event.api('docs.getUploadServer',
                           type='audio_message')['upload_url']
    uploaded = requests.post(upload_url,
                             files={'file': audio_msg}).json()['file']
    audio = event.api('docs.save', file=uploaded)['audio_message']
    del(audio_msg)
    voice = f"audio_message{audio['owner_id']}_{audio['id']}_{audio['access_key']}"

    event.db.voices, exist = delete_template(name, event.db.voices)
    event.db.voices.append({
        "name": name,
        "cat": category,
        "attachments": voice
    })
    event.db.save()

    event.msg_op(2, f'{name}' +
                 ('+' if exist else '+') +
                 f'\nДлительность - {attach["duration"]} сек.')
    event.msg_op(3)
    return "ok"


@dp.longpoll_event_register('гсы')
@dp.my_signal_event_register('гсы')
def template_list(event: MySignalEvent) -> str:
    category = ' '.join(event.args)
    voices = event.db.voices
    if category == 'все':
        message = '📃 Список всех голосовых сообщений:'
        for i, v in enumerate(voices, 1):
            message += f"\n{i}. {v['name']} | {v['cat']}"
    elif not category:
        cats = {}
        for v in voices:
            cats[v['cat']] = cats.get(v['cat'], 0) + 1
        message = "📚 Категории голосовых сообщений:"
        for cat in cats:
            message += f"\n-- {cat} ({cats[cat]})"
    else:
        message = f'📖 Голосовые сообщения категории "{category}":'
        for v in voices:
            if v['cat'] == category:
                message += f"\n-- {v['name']}"
    if '\n' not in message:
        if voices == []:
            message = '👀 Нет ни одного голосового сообщения... Для создания используй команду "+гс"'  # noqa
        else:
            message = '⚠️ Голосовые сообщения по указанному запросу не найдены'
    event.msg_op(2, message)
    return "ok"


@dp.longpoll_event_register('-гс')
@dp.my_signal_event_register('-гс')
def voice_delete(event: MySignalEvent) -> str:
    name = ' '.join(event.args).lower()
    event.db.voices, exist = delete_template(name, event.db.voices)
    if exist:
        msg = f'{name}'
        event.db.save()
    else:
        msg = f'⚠️ Голосовое сообщение "{name}" не найдено'
    event.msg_op(2, msg, delete = 2)
    return "ok"


@dp.longpoll_event_register('гс')
@dp.my_signal_event_register('гс')
def voice_send(event: MySignalEvent) -> str:
    name = ' '.join(event.args).lower()
    voice = None
    for v in event.db.voices:
        if v['name'] == name:
            voice = v
            break
    if voice:
        event.msg_op(2, 'красный крестик')
        reply = str(event.reply_message['id']) if event.reply_message else ''
        att = voice['attachments']
        event.api.exe(
            'API.messages.delete({' +
            '"message_ids":'+str(event.msg['id'])+',"delete_for_all":1});' +
            'API.messages.send({'
                '"peer_id":%d,' % event.chat.peer_id +
                '"message":"%s",' % escape(event.payload).replace('\n', '<br>') +
                '"attachment":"%s",' % (att if type(att) == str else att[0]) +
                '"reply_to":"%s",' % reply +
                '"random_id":0});')
    else:
        event.msg_op(2, f'нету')
        event.msg_op(3)
    return "ok"
