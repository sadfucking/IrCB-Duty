from idm.objects import dp, MySignalEvent
import random
@dp.longpoll_event_register('фото')
@dp.my_signal_event_register('фото')
def lo(event:MySignalEvent) -> str:
#    if event.args[0] == 'хз':
#    hz=event.api
#    iid=-196431814
#    fo=[]
#    fo1=hz.photos.get(owner_id=iid, album_id=271467921, count=30)["items"]
#for i in fo1:
#    fo.append(f'photo{iid}_{i["items"]}')
#    cr=random.choice(foto)
#    event.msg_op(2, attachment=cr)
#    else:
    att=["photo-36592437_308515972", "photo-36592437_320526953", "photo-36592437_321368100", "photo-36592437_334894262", "photo-171587644_457239353", "photo-171587644_457239354", "photo-55673870_456245288", "photo-122559935_436625438", "photo-36592437_309686753", "photo-36592437_314106457", "photo-36592437_456247409"]
    ctr=random.choice(att)
    event.msg_op(2, attachment=ctr)
    return "ok"
