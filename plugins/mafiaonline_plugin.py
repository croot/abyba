#===istalismanplugin===
# -*- coding: utf-8 -*-

import urllib2,re,urllib

MAFIA_REMOTE={}

MF_GET_RES={}

RBOT=[u'mafia_bot@jabber.cz']

def hnd_botremotemaf(con, raw):
    try:
        body=raw.getBody()
        fromjid=raw.getFrom()
        groupchat = fromjid.getStripped()
	nick = fromjid.getResource()
	if raw.getType()==u'error':
            return
        if body!=u'[no text]':
            return
        id=raw.getID()
        jid=get_true_jid(groupchat+'/'+nick)
        if not jid in RBOT: return
        p=raw.getTagData('x')
        z=raw.getChildren()
        for x in z:
            ns=x.getNamespace()
            sp=ns.split(':')
            jj=sp[0]
            if id==u'info':
                i=len(MF_GET_RES)+1
                MF_GET_RES[i]={'jid':jid,'body':p}
                return
            if sp[0] in MAFIA_REMOTE.keys():
                jj=MAFIA_REMOTE[sp[0]]['private']
                msg(jj, p)
    except: pass

                    
def mr_send(jid, x, id, ns):
    msg=xmpp.Message(jid,u'[no text]','chat')
    msg.setID(id)
    m=msg.setTag('x',namespace=ns)
    m.setData(x)
    try:
        JCON.send(msg)
    except:
        pass

def mf_remote_proc():
    try:
        mafia_url_get_jid()
    except:
        pass
    JCON.RegisterHandler('message', hnd_botremotemaf)

def mafia_get_info():
    if RBOT:
        for x in RBOT:
            if x!=JID:
                mr_send(x,u'info','1','none@tld:x:public')

def mafremote_register(type, source, parameters):
    global MAFIA_REMOTE
    rep=''
    jid=get_true_jid(source[1]+'/'+source[2])
    nick=''
    if source[1] in GROUPCHATS.keys():
        nick=source[2]
    else:
        nick=jid.split('@')[0]
    try:
        if jid in MAFIA.keys():
            reply(type, source, u'you must leave from game to do this!')
            return
    except:
        pass
    if jid in MAFIA_REMOTE.keys():
        mr_send(MAFIA_REMOTE[jid]['bot'],'1','off',jid+':x:public')
        del MAFIA_REMOTE[jid]
        return
    if parameters.isdigit():
        if int(parameters) in range(1, 9):
            if int(parameters) in MF_GET_RES:
                MAFIA_REMOTE[jid]={'bot':MF_GET_RES[int(parameters)]['jid'],'private':source[1]+'/'+source[2]}
                mr_send(MF_GET_RES[int(parameters)]['jid'],'1234','1',jid+':x:'+nick)
                return
            else:
                reply(type, source, u'Партия с таким номером не найденa!')
                return
    if not RBOT:
        reply(type, source, u'При инициализации небыло загружено ни одного jabberID игровых ботов!Повторите попытку через минуту!')
        mafia_url_get_jid()
        return
    MF_GET_RES.clear()
    mafia_get_info()
    t=time.time()
    while time.time() - t<3:
        time.sleep(1)
        pass
    if not MF_GET_RES:
        reply(type, source, u'извините, на данный момент сервер недоступен!')
        return
    SP=[]
    for x in MF_GET_RES.keys():
        try:
            if not MF_GET_RES[x]['jid'] in SP:
                SP.append(MF_GET_RES[x]['jid'])
            else:
                continue
            rep+=str(x)+'. '+MF_GET_RES[x]['body']+'\n'
        except:
            pass
    reply(type, source, u'Вот че я нашел:\n'+rep+u'\nВыберите номер партии, например:\n .мафия 1')

def mremote_msg(raw, type, source, parameters):
    if parameters.lower() in COMMANDS.keys() or type!='private':
        return
    if parameters.count(' '):
        s=parameters.split()
        if s[0].lower() in COMMANDS.keys():
            return
    jid=get_true_jid(source[1]+'/'+source[2])
    t='public'
    if jid in MAFIA_REMOTE.keys():
        mr_send(MAFIA_REMOTE[jid]['bot'], parameters, random.randrange(0,222), jid+':x:'+t)

def mfremote_leave(groupchat, nick, nw, nr):
    jid=get_true_jid(groupchat+'/'+nick)
    if jid in MAFIA_REMOTE.keys():
        if MAFIA_REMOTE[jid]['private']==groupchat+'/'+nick:
            mr_send(MAFIA_REMOTE[jid]['bot'],'1','off',jid+':x:public')

def mafia_url_get_jid():
    for x in [u'http://tysa.1gb.ru/mafia.txt',u'http://talisman.wen.ru/mafia.txt']:
        try:
            req = urllib2.Request(x)
            r = urllib2.urlopen(req)
            page = r.read().replace('\r','').split('\n')
            if page:
                for c in page:
                    c=c.strip()
                    if not c in RBOT and c.count('@'):
                        RBOT.append(c)
        except:
            pass

register_leave_handler(mfremote_leave)        
register_message_handler(mremote_msg)
register_stage0_init(mf_remote_proc)
register_command_handler(mafremote_register, '.мафия', ['все','игры'], 0, 'Игра мафия, ключ 0 чтобы выйти', '.мафия', ['.мафия'])
register_command_handler(mafremote_register, '!мафия', ['все','игры'], 0, 'Игра мафия, ключ 0 чтобы выйти', '.мафия', ['.мафия'])
