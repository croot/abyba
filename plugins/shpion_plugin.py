#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman


SHPIONA_SEND={}

def shpion_hnd(type,source,parameters):
    jid=get_true_jid(source[1]+'/'+source[2])
    if parameters in GROUPCHATS:
        n=str(random.randrange(01, 99))
        if n in SHPIONA_SEND:
            n=str(random.randrange(01, 99))
        SHPIONA_SEND[n]={'jid':jid,'from':parameters,'prs':0}
        reply(type,source,u'id ='+n)
        return
    if parameters in SHPIONA_SEND:
        del SHPIONA_SEND[parameters]
        reply(type,source,u'id '+parameters+' unregister')
        return
    if parameters=='prs':
        for x in SHPIONA_SEND:
            if SHPIONA_SEND[x]['jid']==jid:
                if SHPIONA_SEND[x]['prs']==0:
                    SHPIONA_SEND[x]['prs']=1
                    reply(type,source,u'ok')
                    return
                else:
                    SHPIONA_SEND[x]['prs']=0
                    reply(type,source,u'ok')
    


def shpion_msg(raw,type,source,parameters):
    jid=get_true_jid(source[1]+'/'+source[2])
    if parameters.count(' ') and source[1] not in GROUPCHATS:
        s=parameters.split()
        if s[0] in SHPIONA_SEND:
            if SHPIONA_SEND[s[0]]['jid']==jid:
                parameters=' '.join(s[1:])
                msg(SHPIONA_SEND[s[0]]['from'],parameters[:500])
    else:
        if source[1] in GROUPCHATS and parameters.count(' '):
            for c in SHPIONA_SEND:
                if source[1]==SHPIONA_SEND[c]['from']:
                    JCON.send(xmpp.Message(SHPIONA_SEND[c]['jid'],source[1]+'/'+source[2]+'\nid='+unicode(c)+'\n'+parameters[:250],'chat'))

def shpion_join(groupchat,nick,afl,role):
    if SHPIONA_SEND:
        for x in SHPIONA_SEND:
            if SHPIONA_SEND[x]['from']==groupchat:
                if SHPIONA_SEND[x]['prs']==1:
                    msg(SHPIONA_SEND[x]['jid'],groupchat+' new presence from '+nick[:20]+'\nid ='+x)
                    
register_join_handler(shpion_join)
register_message_handler(shpion_msg)        
register_command_handler(shpion_hnd, 'шпийон', ['мод'], 40, 'Выдает вам уникальный id позволяющий получать/отправлять мессаги с выбранных конференций на свой jid, и писать ответ указывая в начале id,чтобы убить какойто id небераем шпийон и ваш id', 'шпийон <чат>, шпийон <ключ>', ['шпийон cool@conference.jabber.ru','шпийон prs'])

