#===istalismanplugin===
# -*- coding: utf-8 -*-

#UPDATE 27. 10. 2012

import urllib2,re,urllib

MAFIA_REMOTE = {}

MF_GET_RES = {}

MAFIA_MEM = {}

RESULT_MAF = []

RBOT=[u'mafia_bot@jabber.cz/JabberBot', u'mafiozo@worldskynet.net/pybot', u'mafia@oneteam.im/JabberBot','bot@oneteam.im/JabberBot']

MAFIA_REMOTE_CALC = 0

def mr_send_iq(botjid=None, body='text', id=None, jid=None, typ=None, nick=None):
    if not botjid or not isinstance(botjid, basestring):
        print 'return'
        return
    iq = xmpp.Iq('set')
    iq.setTo(botjid)
    iq.setID(id)
    i = xmpp.Node('query')
    i.setNamespace('xmpp:iq:mafia')
    if jid:
        i.setAttr('jid', jid)
    if typ:
        i.setAttr('typ', typ)
    if nick:
        i.setAttr('nick', nick)
    i.addData(body)
    iq.addChild(node=i)
    #print unicode(iq)
    JCON.send(iq)



def hnd_getiqmaf(con, iq):
    global MAFIA_MEM
    global MAFIA_REMOTE
    global MF_GET_RES
    global MAFIA_REMOTE_CALC
    
    
    fromjid = iq.getFrom()
    log = fromjid.getStripped()
    name = fromjid.getResource()
    fromjid = log+'/'+name
    if fromjid == JID+'/'+RESOURCE: return
    id = iq.getID()
    
    if not fromjid in RBOT: return

    if iq.getType() == 'result':
        if iq.getTags('query', {}, 'xmpp:iq:mafia'):
            #RESULT_MAF.append(id)
            #if len(RESULT_MAF)>30:
            #    RESULT_MAF.pop(0)
            if id in MAFIA_REMOTE and 'spec' in MAFIA_REMOTE[id]:# and MAFIA_REMOTE[id]['bot']==fromjid:
                MAFIA_REMOTE[id]['spec']=1
            return
    
    elif iq.getType() == 'set':
        if iq.getTags('query', {}, 'xmpp:iq:mafia'):
            #print unicode(iq)
            body = iq.getTag("query").getPayload()[0]
            ch = iq.getChildren()

            if not ch: return
            
            jid = ch[0].getAttrs().get('jid',None)
            typ = ch[0].getAttrs().get('typ',None)
            cityid = ch[0].getAttrs().get('cityid',None)
            try:
                if id == u'info':
                    i = len(MF_GET_RES)+1
                    MF_GET_RES[i] = {'jid':fromjid,'body':body,'id':cityid}
                    return

                if id == u'game_over' or id.count('game_over'):
                    for x in MAFIA_REMOTE.keys():
                        if 'private' in MAFIA_REMOTE[x]:
                            msg(MAFIA_REMOTE[x]['private'], u'Для повторного входа в игру отправьте 1 или #')
                            MAFIA_MEM[x] = MAFIA_REMOTE[x]['bot']
                    MAFIA_REMOTE.clear()
                    return
                if not typ or typ == 'public':
                    for x in [c for c in MAFIA_REMOTE.keys() if MAFIA_REMOTE[c].get('bot')==fromjid]:
                        jj = MAFIA_REMOTE[x]['private']
                        msg(jj, body)
                    return
                if jid in MAFIA_REMOTE.keys():
                    try:
                        if time.time()-MAFIA_REMOTE_CALC>60:
                            MAFIA_REMOTE_CALC = time.time()
                            write_file('dynamic/mrecovery.txt',str(MAFIA_REMOTE))
                    except: pass
                    jj = MAFIA_REMOTE[jid]['private']
                    msg(jj, body)
            except: print 'exception in mafia iq'

def hnd_botremotemaf(con, raw):
    global MAFIA_MEM
    global MAFIA_REMOTE
    global MF_GET_RES
    global MAFIA_REMOTE_CALC
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
            if id==u'game_over' or id.count('game_over'):
                for x in MAFIA_REMOTE.keys():
                    if 'private' in MAFIA_REMOTE[x]:
                        msg(MAFIA_REMOTE[x]['private'], u'Для повторного входа в игру отправьте 1 или #')
                        MAFIA_MEM[x]=MAFIA_REMOTE[x]['bot']
                MAFIA_REMOTE.clear()
                return
            if sp[0] in MAFIA_REMOTE.keys():
                try:
                    if time.time()-MAFIA_REMOTE_CALC>60:
                        MAFIA_REMOTE_CALC = time.time()
                        write_file('dynamic/mrecovery.txt',str(MAFIA_REMOTE))
                except: pass
                jj = MAFIA_REMOTE[sp[0]]['private']
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
    try: mafia_url_get_jid()
    except: pass
    ###JCON.RegisterHandler('message', hnd_botremotemaf)
    JCON.RegisterHandler('iq', hnd_getiqmaf)

def mafia_get_info():
    if RBOT:
        for x in [c for c in RBOT if c!=JID]:
            ###mr_send(x,u'info','1','none@tld:x:public')
            mr_send_iq(x, u'info', u'info')

def mafremote_register(type, source, parameters):
    global MAFIA_REMOTE
    rep = ''
    jid = get_true_jid(source[1]+'/'+source[2])
    jid = jid.lower()
    nick = ''
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
        if 'spec' in MAFIA_REMOTE[jid] and MAFIA_REMOTE[jid]['spec']:
            ###mr_send(MAFIA_REMOTE[jid]['bot'],'1','off',jid+':x:public')
            mr_send_iq(MAFIA_REMOTE[jid]['bot'], 'off', 'off', jid, 'public')
            time.sleep(1.5)
            del MAFIA_REMOTE[jid]
            return
    if parameters.isdigit():
        if int(parameters) in range(1, 9):
            if int(parameters) in MF_GET_RES:
                MAFIA_REMOTE[jid]={'bot':MF_GET_RES[int(parameters)]['jid'],'private':source[1]+'/'+source[2],'spec':None}
                ###mr_send(MF_GET_RES[int(parameters)]['jid'],'1234','1',jid+':x:'+nick)
                mr_send_iq(MF_GET_RES[int(parameters)]['jid'], '1234', str(), jid, 'public', nick)
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
    cid = []
    for x in MF_GET_RES.keys():
        try:
            if MF_GET_RES[x].get('id',None):
                if MF_GET_RES[x].get('id',None) in cid:
                    continue
                else: cid.append(MF_GET_RES[x].get('id',None))
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
        ###mr_send(MAFIA_REMOTE[jid]['bot'], parameters, random.randrange(0,222), jid+':x:'+t)
        mr_send_iq(MAFIA_REMOTE[jid]['bot'], parameters, str(random.randrange(0,222)), jid, t)

def mfremote_leave(groupchat, nick, nw, nr):
    jid=get_true_jid(groupchat+'/'+nick)
    if jid in MAFIA_REMOTE.keys():
        if MAFIA_REMOTE[jid]['private']==groupchat+'/'+nick:
            ###mr_send(MAFIA_REMOTE[jid]['bot'],'1','off',jid+':x:public')
            mr_send_iq(MAFIA_REMOTE[jid]['bot'], 'off', 'off', str(random.randrange(0,222)), jid)

def mafia_url_get_jid():
    for x in [u'http://mafiozo.in/mafia.txt',u'http://talisman.wen.ru/mafia.txt']:
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

def mrem_memory(r, t, s, p):
    global MAFIA_MEM
    global MAFIA_REMOTE
    if not p or not p in ['1','#']: return
    jid = get_true_jid(s)
    if 'MAFIA' in globals().keys() and jid in MAFIA.keys(): return
    nick = ''
    if s[1] in GROUPCHATS.keys(): nick = s[2]
    else: nick = jid.split('@')[0]
    nick = nick[:20]
    if jid in MAFIA_MEM.keys() and not jid in MAFIA_REMOTE.keys():
        botjid = MAFIA_MEM[jid]
        if not isinstance(botjid, basestring): return
        MAFIA_REMOTE[jid]={'bot':botjid, 'private':s[1]+'/'+s[2], 'spec':0}
        ###mr_send(botjid, '1234', '1', jid+':x:'+nick)
        mr_send_iq(MAFIA_REMOTE[jid]['bot'], '1234', str(random.randrange(0,222)), jid, 'public', nick)

def mafia_rm_recovery():
    if check_file(file='mrecovery.txt'):
        file='dynamic/mrecovery.txt'
        try: db=eval(read_file(file))
        except:
            db = {}
            write_file(file, '{}')
        global MAFIA_REMOTE
        MAFIA_REMOTE = db.copy()

register_stage0_init(mafia_rm_recovery)
register_message_handler(mrem_memory)
register_leave_handler(mfremote_leave)        
register_message_handler(mremote_msg)
register_stage0_init(mf_remote_proc)
register_command_handler(mafremote_register, '.мафия', ['все','игры'], 0, 'Игра мафия (UPDATE 18. 12. 2012)', '.мафия', ['.мафия'])
if not u'!мафия' in COMMANDS.keys():
    register_command_handler(mafremote_register, '!мафия', ['все','игры'], 0, 'Игра мафия (UPDATE 18. 12. 2012)', '!мафия', ['!мафия'])
