#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman


def timel_hnd(type,source,parameters):
    if not parameters:
        reply(type,source,u'и?')
        return
    if parameters.count('@') and parameters.count('.'):
        jid=parameters.strip()
    else:
        if source[1] in GROUPCHATS:
            if parameters.strip() in GROUPCHATS[source[1]]:
                if GROUPCHATS[source[1]][parameters.strip()]['ishere']==1:
                    jid= source[1]+'/'+parameters.strip()
                else:
                    return
            else:
                return
        else:
            return
    q_iq = xmpp.Iq('get')
    id='time'+str(random.randrange(1000, 9999))
    q_iq.setID(id)
    q_iq.addChild('query', {}, [], 'jabber:iq:last');
    q_iq.setTo(jid)
    JCON.SendAndCallForResponse(q_iq, handler_timels, {'type': type, 'source': source})
    return

def handler_timels(coze, res, type, source):
    if res:
        if res.getType() == 'result':
            try:
                s=res.getTagAttr('query', 'seconds')
            except:
                reply(type,source,u'не получилось')
                return
            if int(s)==0:
                reply(type,source,u'он и сейчас активен')
                return
            reply(type,source,u'он заснул '+timeElapsed(int(s))+u' назад')
        else:
            reply(type,source,u'не получилось')

SC_L={}
SC_S={}
SC_W=[]
    
def scan_lt_start(type,source,parameters):
    if not source[1] in GROUPCHATS:
        return
    if not '1' in SC_W:
        SC_W.append('1')
    if SC_L:
        time.sleep(3)
        globals()['SC_L']=[]
    SP=[]
    n=0
    for x in GROUPCHATS[source[1]]:
        if GROUPCHATS[source[1]][x]['ishere']==1:
            if x != source[2] and x != get_bot_nick(source[1]):
                n+=1
                SP.append(x)
    if n<1:
        reply(type,source,u'а кто здесь еще?')
        return
    for x in SP:
        jid=source[1]+'/'+x
        q_iq = xmpp.Iq('get')
        id='time'+str(random.randrange(1000, 9999))
        q_iq.setID(id)
        q_iq.addChild('query', {}, [], 'jabber:iq:last');
        q_iq.setTo(jid)
        JCON.SendAndCallForResponse(q_iq, hnd_scan_get, {'type': type, 'source': source, 'x': x})
    time.sleep(3.5)
    if not source[1] in SC_L:
        reply(type,source,u'все спят походу')
        return
    rep=''
    ls=u'список живых:\n'
    l=''
    if source[1] in SC_L:
        for x in SC_L[source[1]]:
            l+=x+'; '
        del SC_L[source[1]]
    s=''
    rep+=ls+l
    if source[1] in SC_S:
        ss=u'\nспят:\n'
        for x in SC_S[source[1]]:
            s+=x+'; '
        del SC_S[source[1]]
        rep+=ss+s
    reply(type,source,rep)
    globals()['SC_W']=[]
    globals()['SC_L']={}
    globals()['SC_S']={}
        
def hnd_scan_get(coze, res, type, source, x):
    if res:
        if res.getType() == 'result':
            try:
                s=res.getTagAttr('query', 'seconds')
                if not SC_W:
                    return
                if int(s)<360:
                    if not source[1] in SC_L:
                        SC_L[source[1]]=[]
                        SC_L[source[1]].append(x)
                    else:
                        SC_L[source[1]].append(x)
                else:
                    if not source[1] in SC_S:
                        SC_S[source[1]]=[]
                        SC_S[source[1]].append(x)
                    else:
                        SC_S[source[1]].append(x)
            except:
                return

    
register_command_handler(timel_hnd, '!жив', ['мод','все'], 0, 'Показывает время простоя клиента.', '!жив <nick|jid>', ['!жив 40tman'])
register_command_handler(scan_lt_start, '!живые', ['мод','все'], 0, 'Показывавает кто жив', '!живые', ['!живые'])

