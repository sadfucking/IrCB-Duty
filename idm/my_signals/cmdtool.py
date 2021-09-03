from idm.objects import dp, MySignalEvent
import subprocess, os, psutil
@dp.longpoll_event_register('к')
@dp.my_signal_event_register('к')
def run(event: MySignalEvent) -> str:
    try:
        if event.args[0] == 'помощь':
            event.msg_op(2, 'тут будет список команд')
        else:
            ct=subprocess.run([*event.args], capture_output=True)
            event.msg_op(2, ct)
    except:
        event.msg_op(2, 'arguments entered incorrectly')
    return "ok"

#subprocess.popen

@dp.longpoll_event_register('popen')
@dp.my_signal_event_register('popen')
def popen(event: MySignalEvent) -> str:
    try:
        if event.args[0] == 'помощь':
            event.msg_op(2, """ls (просмотр сожержимого каталогов)
cat (просмотр содержимого файла)
mkdir (создать каталог)
file (тип файла)
rm (удаление файлов)
rmdir (удалить папку)
df (анализатор дискового пространства)
top (список процессов)
uname (основная информация о системе)
uptime (время работы системы)
cal (календарь)
date (дата, время)
dig (посмотреть информацию о DNS)
free (отобразить ОЗУ)
ps (запущенные процессы)
touch (создать файл)
wget (загрузка файлов)""")
        else:
            proc = subprocess.Popen([*event.args], stdout=subprocess.PIPE)
            output = proc.stdout.read()
            event.msg_op(2, output)
    except:
        event.msg(2, "arguments entered incorrectly")
    return "ok"

#exec

@dp.longpoll_event_register('eval')
@dp.my_signal_event_register('eval')
def lo(event: MySignalEvent) -> str:
    try:
        ex=eval(*event.args)
        event.msg_op(2, ex)
    except:
        event.msg_op(2, 'error input')
    return "ok"

#test

@dp.longpoll_event_register('о')
@dp.my_signal_event_register('о')
def o(event: MySignalEvent) -> str:
    ct=subprocess.run([*event.args], capture_output=True, shell=True).stdout
    out = ct.decode('utf-8').splitlines()
    event.msg_op(2, out)
    return "ok"

#os

@dp.longpoll_event_register('os')
@dp.my_signal_event_register('os')
def oss(event: MySignalEvent) -> str:
    oss=os.system(*event.args, capture_output=True)
    event.msg_op(2, oss)
    return "ok"

#цпу
@dp.longpoll_event_register('цпу')
@dp.my_signal_event_register('цпу')
def lo(event: MySignalEvent) -> str:
    cr=psutil.cpu_percent()
    event.msg_op(2, ('cpu: ') + f'{cr}' + ('%'))
    return "ok"
