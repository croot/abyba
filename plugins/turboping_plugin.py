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
        srv, rep = '', ''
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
        
        rep = u'- Минимальный '+str(min(TURBO_PING[jid]['jid']))+u'с. ;\n - Mаксимальный '+str(max(TURBO_PING[jid]['jid']))+u'с. ;\n - Cредний результат '
        rep += u' из '+str(len(TURBO_PING[jid]['jid']))+u' запросов '+str(round(l, 3))+u' с. ;\n'
        rep += u'- Ботпинг '+str(bot)+u'c. ;\n'
        rep += u'- Понг от сервера '+JID.split('@')[1]+u' до сервера '+srv+' '+str(round(s2s, 2))+u'c. ;\n'
        rep += u'- Результат с учетом всех параметров '+str(round((l-bot)-s2s, 3))+u' секунд.\n'
        res = (l-bot)-s2s
        rep +=u'- Оценка понга по шкале от 0 до 5-ти '
        if res< 0.1: rep+=u' 5+'
        if res< 0.6 and res> 0.1: rep+=u' 5'
        if res<1.1 and res>0.5: rep+=u' 4'
        if res<2.2 and res>1: rep+=u' 3'
        if res<5.5 and res>2.1: rep+=u' 2'
        if res<8.8 and res>5.4: rep+=u' 1'
        if res>=8.8: rep+=u' 0'
        reply(t, s, rep)
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
