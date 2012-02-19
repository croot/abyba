#===istalismanplugin===
# -*- coding: utf-8 -*-

SECURITY = {}

SECURITY_MSG = {}

SECURITY_BUF = {}

SECURITY_FILE = 'dynamic/SECURITY.txt'

def security_set(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    jid = get_true_jid(source[1]+'/'+source[2])
    SECURITY_MSG[jid]={}
    SECURITY_MSG[jid]['step1']={}
    reply(type, source, u'Вы в меню настройки безопасности конференции, выберите дейстивие:\n1-включить/настроить лимит новых пользователей,\n0-отключить')


def security_prs(prs):
    ptype = prs.getType()
    if ptype == 'unavailable' and prs.getStatusCode() == '303':
        nick = prs.getNick()
	fromjid = prs.getFrom()
	groupchat = fromjid.getStripped()		
	afl=prs.getAffiliation()
	role=prs.getRole()
	security_join(groupchat, nick, afl, role)

register_presence_handler(security_prs)

LIM_GUEST_M=0
		
def security_join(g, n, r, a):
    if time.time() - INFO['start']<60:
        return
    global SECURITY
    global LIM_GUEST_M
    if not g in SECURITY:
        return
    if not 'time' in SECURITY[g] or not 'n' in SECURITY[g]:
        return
    global SECURITY_BUF
    list=[u'jabbrik.ru',u'jabber.ru',u'talkonaut.com',u'xmpp.ru',u'jabber.ua',u'qip.ru',u'jabberon.ru']
    jid=get_true_jid(g+'/'+n)
    if not jid or jid==None: return
    if jid.count('@con'): return
    if jid.split('@')[1] in list: return
    acc = int(user_level(g+'/'+n, g))
    if acc>=11: return
    if not g in SECURITY_BUF.keys():
        SECURITY_BUF[g]={'time':time.time(),'n':1,'tban':0}
    else:
        if time.time()-SECURITY_BUF[g]['time']<SECURITY[g]['time']:
            SECURITY_BUF[g]['n']+=1
            if SECURITY_BUF[g]['n']==SECURITY[g]['n']:
                SECURITY_BUF[g]['tban']=time.time()
                if time.time()-LIM_GUEST_M>2800:
                    msg(g, u'/me Достигнут установленный лимит Гостей '+str(SECURITY[g]['n']))
                    LIM_GUEST_M=time.time()
            if SECURITY_BUF[g]['n']>SECURITY[g]['n']:
                security_ban(g, jid.split('@')[1])
                security_ban(g, jid)
                SECURITY_BUF[g]['time']=time.time()
        else:
            SECURITY_BUF[g]['n']=1
            SECURITY_BUF[g]['tban']=0
            SECURITY_BUF[g]['time']=time.time()

register_join_handler(security_join)

def security_ban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', u'security <лимит пользователей>')
	iq.addChild(node=query)
	JCON.send(iq)


def security_msg(raw, type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    jid=get_true_jid(source[1]+'/'+source[2])
    if not jid in SECURITY_MSG or not parameters.isdigit():
        return
    db=eval(read_file(SECURITY_FILE))
    if 'step1' in SECURITY_MSG[jid]:
        if int(parameters)==1:
            del SECURITY_MSG[jid]['step1']
            SECURITY_MSG[jid]['step2']={}
            if not source[1] in db:
                db[source[1]]={}
                write_file(SECURITY_FILE,str(db))
            reply(type, source, u'Ок. Выберите промежуток во времени в секундах, за который будет вестись подщет вошедших Гостей')
            return
        if int(parameters)==0:
            del SECURITY_MSG[jid]
            if source[1] in SECURITY:
                del SECURITY[source[1]]
            if source[1] in db:
                del db[source[1]]
                write_file(SECURITY_FILE,str(db))
            reply(type, source, u'Отключено')
            return
    elif 'step2' in SECURITY_MSG[jid]:
        if int(parameters)<2:
            reply(type, source, u'Меньше двух секунд нельзя!')
            return
        if source[1] in db.keys():
            db[source[1]]['time']=int(parameters)
            write_file(SECURITY_FILE,str(db))
        del SECURITY_MSG[jid]['step2']
        SECURITY_MSG[jid]['step3']={}
        reply(type, source, u'Ок. Введите количество вошедших Гостей за '+parameters+u' секунд, после превышения которого будет включен временный автобан подозрительных серверов.')
        return
    elif 'step3' in SECURITY_MSG[jid]:
        if source[1] in db.keys():
            db[source[1]]['n']=int(parameters)
            write_file(SECURITY_FILE,str(db))
            for x in db.keys():
                SECURITY[x]=db[x]
        del SECURITY_MSG[jid]
        reply(type, source, u'Ок. Настройка завершена!')

register_message_handler(security_msg)

def security_load():
    global SECURITY
    global SECURITY_FILE
    if not os.path.exists(SECURITY_FILE) or not isinstance(read_file(SECURITY_FILE),dict):
        new=open(SECURITY_FILE, 'w')
        new.write('{}')
        new.close()
    db=eval(read_file(SECURITY_FILE))
    for x in db:
        SECURITY[x]=db[x]

register_stage0_init(security_load)
register_command_handler(security_set, 'security', ['все','антивайп'], 20, 'Настройка лимита новых пользователей в конференции.', 'security', ['security'])		

