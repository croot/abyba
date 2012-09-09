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
        srv = ''
        #if i in TURBO_PING.keys() and p=='??':
        #        reply(t, s, i+':\n'+'; '.join([str(x) for x in TURBO_PING[i]]))
        #        return
        if TURBO_PING:
                reply(t, s, u'Подождите пару минут!')
                return
        TURBO_LIM[jid]=time.time()
        TURBO_PING[jid]={'jid':[],'s2s':[],'bot':[]}
        reply(t, s, u'Тестирование начато..')
        for x in range(20):
                tojid = jid
                if x in range(11, 16):
                        if jid.count('@'):
                                spl='@'
                                if jid.count('@conference.'):
                                        spl='@conference.'
                                tojid = jid.split(spl)[1]
                                if tojid.count('/'):
                                        tojid = tojid.split('/')[0]
                        srv = tojid
                if x in range(16, 21):
                        tojid = JID.split('@')[1]
                iq = xmpp.Iq('get')
                id = str(x)
                iq.setID(id)
                iq.setTo(tojid)
                iq.addChild('query', {}, [], 'jabber:iq:version');
                JCON.SendAndCallForResponse(iq, handler_turboping_answ,{'tt': time.time(), 'jid': jid})
                time.sleep(3)
        tt=time.time()
        while (len(TURBO_PING[jid]['jid'])+len(TURBO_PING[jid]['s2s'])+len(TURBO_PING[jid]['bot']))!=20:
                if time.time()-tt>120:
                        break
                time.sleep(1)
                pass
        if len(TURBO_PING[jid]['jid'])<3:
                reply(t, s, u'Понг хреновый, либо адрес указан неверно!Часть пакетов утеряна!')
                return
        l = getMedian(TURBO_PING[jid]['jid'])
        bot = getMedian(TURBO_PING[jid]['bot'])
        s2s = getMedian(TURBO_PING[jid]['s2s']) - bot
        
        reply(t, s, u'Минимальное время '+str(min(TURBO_PING[jid]['jid']))+u' секунд, макс. '+str(max(TURBO_PING[jid]['jid']))+u' секунд.\nВ среднем, из '+str(len(TURBO_PING[jid]['jid']))+u' отправленных пакетов понг составляет '+str(round(l,3))+u' секунд.\nОтнимаем разность понга s2s & botping-a \"'+str(round(l,3))+' - ('+str(getMedian(TURBO_PING[jid]['s2s']))+' - '+str(bot)+u')\" получаем '+str((round(l,3))-s2s)+u' секунд!')
        TURBO_PING.clear()
        
def handler_turboping_answ(cl, res, tt, jid):
        global TURBO_PING
        if res:
                if res.getType() == 'result':
                        t = time.time()
                        if int(res.getID()) in range(11, 16):
                                TURBO_PING[jid]['s2s'].append(round(t-tt, 3))
                                return
                        if int(res.getID()) in range(16, 21):
                                TURBO_PING[jid]['bot'].append(round(t-tt, 3))
                                return
                        TURBO_PING[jid]['jid'].append(round(t-tt, 3))

def getMedian(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
    return (float(lower + upper)) / 2
                        
register_command_handler(handler_turbo_ping, 'турбопинг', ['все'], 0, 'Проверяет пинг указаного адреса в течении минуты, выводит медиану, максимальное и минимально значение.\n(c)write by 40tman', 'турбопинг', ['турбопинг'])
