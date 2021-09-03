from idm.objects import dp, MySignalEvent
import random, time
@dp.longpoll_event_register('!!')
@dp.my_signal_event_register('!!')
def lo(event:MySignalEvent) -> str:
    event.msg_op(2, '+', attachment = '')
    event.msg_op(3)
    return "ok"
#файлы
@dp.longpoll_event_register('файлы', '!файлы')
@dp.my_signal_event_register('файлы')
def lo(event:MySignalEvent) -> str:
    event.msg_op(2, 'https://vk.cc/c1t66s', attachment = '')
    return "ok"


@dp.longpoll_event_register('мкмд')
@dp.my_signal_event_register('мкмд')
def kmd(event: MySignalEvent) -> str:
    event.msg_op(2, 'https://vk.cc/c4zWm3')
    return "ok"

#инфинити
@dp.longpoll_event_register('токенинф')
@dp.my_signal_event_register('токенинф')
def tok(event: MySignalEvent) -> str:
    event.msg_op(2, 'https://vk.cc/c5lnrD')
    return "ok"

@dp.longpoll_event_register('кмдинф')
@dp.my_signal_event_register('кмдинф')
def kmd(event: MySignalEvent) -> str:
    event.msg_op(2, 'https://vk.cc/c5moTw')
    return "ok"

@dp.longpoll_event_register('!рестарт')
@dp.my_signal_event_register('!рестарт')
def lo(event:MySignalEvent) -> str:
    event.msg_op(3)
    event.msg_op(1, """.влс @shizu_l_p
рестарт""")
    return "ok"

#рандом
@dp.longpoll_event_register('выбери')
@dp.my_signal_event_register('выбери')
def lo(event:MySignalEvent) -> str:
    text1=[*event.args]
    text=[f'{text1}']
    out=random.choice(text)
    rep=out.replace("'", '').replace(",", '').replace("]", '')
    event.msg_op(2, rep.partition('или'))
    return "ok"

#вкапи док
@dp.longpoll_event_register('вкапи')
@dp.my_signal_event_register('вкапи')
def lo(event:MySignalEvent) -> str:
    event.msg_op(2, 'https://vk.cc/8m6dG8', attachment = '')
    time.sleep(20)
    event.msg_op(3)
    return "ok"
