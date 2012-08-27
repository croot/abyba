#===istalismanplugin===
# -*- coding: utf-8 -*-

TURBO_PING = {}
TURBO_LIM = {}

def handler_turbo_ping(t, s, p):
        global TURBO_PING
        global TURBO_LIM
        jid = s[1]+'/'+s[2]
        if p:
                if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
                        if p==get_bot_nick(s[1]):
                                reply(t, s, u'Мой понг отменный! А ваш?')
                                return
                        jid = s[1]+'/'+p
                else:
                        jid = p
        i = s[1]+'/'+s[2]
        if i in TURBO_PING.keys() and p=='??':
                reply(t, s, i+':\n'+'; '.join([str(x) for x in TURBO_PING[i]]))
                return
        if jid in TURBO_LIM.keys():
                if time.time()-TURBO_LIM[jid]<60:
                        reply(t, s, u'Данный адрес сейчас проверяется!')
                        return
        TURBO_LIM[jid]=time.time()
        TURBO_PING[jid]=[]
        reply(t, s, u'Тестирование начато..')
        for x in range(10):
                iq = xmpp.Iq('get')
                id = str(random.randrange(1, 1000))
                iq.setID(id)
                iq.setTo(jid)
                iq.addChild('query', {}, [], 'jabber:iq:version');
                JCON.SendAndCallForResponse(iq, handler_turboping_answ,{'tt': time.time(), 'jid': jid})
                time.sleep(6)
        tt=time.time()
        while not len(TURBO_PING[jid])!=9:
                if time.time()-tt>120:
                        break
                time.sleep(1)
                pass
        if len(TURBO_PING[jid])<3:
                reply(t, s, u'Понг хреновый, либо адрес указан неверно!Часть пакетов утеряна!')
                return
        l = getMedian(TURBO_PING[jid])
        reply(t, s, u'Минимальное время '+str(min(TURBO_PING[jid]))+u' секунд, макс. '+str(max(TURBO_PING[jid]))+u' секунд.\nВ среднем, из '+str(len(TURBO_PING[jid]))+u' отправленных пакетов понг составляет '+str(round(l,3))+u' секунд.')

def handler_turboping_answ(cl, res, tt, jid):
        global TURBO_PING
        if res:
                if res.getType() == 'result':
                        t = time.time()
                        TURBO_PING[jid].append(round(t-tt, 3))

def getMedian(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
    return (float(lower + upper)) / 2
                        
register_command_handler(handler_turbo_ping, 'турбопинг', ['все'], 0, 'Проверяет пинг указаного адреса в течении минуты, выводит медиану, максимальное и минимально значение. Дополнительный ключ ?? может использоватся после проверки вашего пинга для вывода полного результата, при условии что не проверялся отдельный адрес!\n(c)write by 40tman', 'турбопинг', ['турбопинг'])
