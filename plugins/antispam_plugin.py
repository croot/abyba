#===istalismanplugin===
# -*- coding: utf-8 -*-

GREEN_SERV = [u'myjabber.ru',u'jabber.ru',u'xmpp.ru',u'jabberon.ru',u'jabbus.org',u'jabber.kiev.ua',u'talkonaut.com',u'gtalk.com',u'qip.ru']


ANTI_BASE = {}

ANTI_CHAT = {}

ANTI_BD = {}

USRON = {}

THD_N = {}
    
    
def tell_admin_join(groupchat,nick,afl,role):
    if not groupchat in GROUPCHATS:
        return
    acc = int(user_level(groupchat+'/'+nick, groupchat))
    if acc<0:
        return
    if nick == get_bot_nick(groupchat):
        return
    jid = get_true_jid(groupchat+'/'+nick)
    if not check_file(groupchat,'tadmin.txt'):
        return
    if not ANTI_BASE:
        return
    txt = ANTI_BASE
    if groupchat in txt:
        if jid in txt[groupchat]:
            if not groupchat in USRON:
                USRON[groupchat]={}
            if not jid in USRON[groupchat]:
                USRON[groupchat][jid]={}
            print 'Tell admin join'
    else:
        return
    for x in txt[groupchat]:
        if txt[groupchat][x].has_key('time'):
            if time.time() - txt[groupchat][x]['time']>240000:
                TADMIN = 'dynamic/'+groupchat+'/tadmin.txt'
                fp = eval(read_file(TADMIN))
                if x in fp:
                    del fp[x]
                    write_file(TADMIN,str(fp))
                    continue
            if groupchat in USRON:
                if x in USRON[groupchat]:
                    continue
            if txt[groupchat][x].has_key('all'):
                body=nick[:19]+'='+jid[:25]
                if not body in txt[groupchat][x]['all']:
                    txt[groupchat][x]['all'].append(nick[:19]+'='+jid[:25])
                    txt[groupchat][x]['time']=time.time()
    user=''
    n=0
    if jid in txt[groupchat]:
        for x in txt[groupchat][jid]['all']:
            f=x
            if x.count('='):
                f=x.split('=')[0]
            if f in GROUPCHATS[groupchat]:
                if GROUPCHATS[groupchat][f]['ishere']==0:
                    if f != nick:
                        n+=1
                        if x.count('='):
                            if len(user)<900:
                                l=x.split('=')
                                if l[1].count(u'conference.'):
                                    l[1]=u'no JID'
                                user+=unicode(n)+'. '+l[0]+' : ['+l[1]+']\n'
                else:
                    try:
                        txt[groupchat][jid]['all'].remove(x)
                    except:
                        pass
            else:
                if f != nick:
                    n+=1
                    if x.count('='):
                        if len(user)<900:
                            l=x.split('=')
                            if l[1].count(u'conference.'):
                                l[1]=u'no JID'
                            user+=unicode(n)+'. '+l[0]+' : ['+l[1]+']\n'
        if n==0:
            return
        if n>0:
            info=u'Во время твоего отсутствия я здесь видел '+unicode(n)+u' юзеров:\n'
        kick=''
        if txt[groupchat][jid]['kick']:
            kick+=u'\nсписок киков '+str(len(txt[groupchat][jid]['kick']))+' :\n'
            ski=0
            for x in txt[groupchat][jid]['kick']:
                ski+=1
                kick+=unicode(ski)+'. '+x+';\n'
        ban=''
        if txt[groupchat][jid]['ban']:
            ban+=u'\nсписок бана '+str(len(txt[groupchat][jid]['ban']))+' :\n'
            sba=0
            for x in txt[groupchat][jid]['ban']:
                sba+=1
                if len(ban)<900:
                    ban+=unicode(sba)+'. '+x+';\n'
        th_day=''
        message=''
        if txt[groupchat][jid].has_key('msg'):
            message+=u'\nсообщений в чате '+str(txt[groupchat][jid]['msg'])
        if groupchat+jid not in THD_N:
            THD_N[groupchat+jid]={'time':time.time()}
            try:
                th_day=u'\nВ этот день в истории\n'+handler_history_day()
            except:
                pass
        else:
            if time.time() - THD_N[groupchat+jid]['time']>86400:
                THD_N[groupchat+jid]['time']=time.time()
                try:
                    th_day=u'\nВ этот день в истории\n'+handler_history_day()
                except:
                    pass
        msg(groupchat+'/'+nick,info+user[:900]+kick[:900]+ban[:900]+message+th_day)
        txt[groupchat][jid]['all']=[]
        txt[groupchat][jid]['kick']=[]
        txt[groupchat][jid]['ban']=[]
        txt[groupchat][jid]['time']=time.time()
        txt[groupchat][jid]['msg']=0

def handler_history_day():
        req = urllib2.Request('http://wapedia.mobi/ru/Wapedia:News?license=1')
        req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<ul>',target)
        h3 = target[od.end():]
        h3 = h3[:re.search('</ul>',h3).start()]
        message = h3
        try:
            message = decode(message)
        except:
            message = decode_s(message)
        message=message.strip()
        message = message.replace('Реклама',' ').replace('" target="_blank">','').replace('/','').replace('_','').replace('=','').replace('%','').replace('"','').replace('#','')
        return unicode(message,'UTF-8')
            
def tell_admin_subscribe(type,source,parameters):
    if not source[1] in GROUPCHATS:
        return
    TADMIN = 'dynamic/'+source[1]+'/tadmin.txt'
    txt = eval(read_file(TADMIN))
    jid = get_true_jid(source[1]+'/'+source[2])
    if parameters == '1':
        if jid in txt:
            reply(type,source,u'твой жид уже есть в базе!')
            return
        if len(txt)>5:
            reply(type,source,u'в чате больше 5-ти подписчиков!')
            return
        txt[jid]={'all':[],'kick':[],'ban':[],'time':time.time(),'msg':0}
        write_file(TADMIN,str(txt))
        reply(type,source,u'ok!')
        antispam_load(source[1])
        return
    else:
        if parameters == '0':
            if jid in txt:
                del txt[jid]
                write_file(TADMIN,str(txt))
                antispam_load(source[1])
                reply(type,source,u'delete!')
                if source[1] in ANTI_BASE:
                    if jid in ANTI_BASE[source[1]]:
                        del ANTI_BASE[source[1]][jid]

def tell_admin_leave(groupchat, nick, reason, code):
    if not groupchat in GROUPCHATS:
        return
    global USRON
    txt = ANTI_BASE
    if not groupchat in txt:
        return
    if not check_file(groupchat,'tadmin.txt'):
        return
    if not txt:
        return
    jid = get_true_jid(groupchat+'/'+nick)
    if groupchat in USRON:
        if jid in USRON[groupchat]:
            time.sleep(2)
            del USRON[groupchat][jid]
            print 'tell admin off'
    if code:
        if code == '307':
            if txt:
                for x in txt[groupchat]:
                    if txt[groupchat][x].has_key('kick'):
                        if reason:
                            txt[groupchat][x]['kick'].append(nick[:19]+' '+reason)
                        else:
                            txt[groupchat][x]['kick'].append(nick[:19])
	elif code == '301':
            if txt:
                for x in txt[groupchat]:
                    if txt[groupchat][x].has_key('ban'):
                        if reason:
                            txt[groupchat][x]['ban'].append(nick[:19]+' '+reason)
                        else:
                            txt[groupchat][x]['ban'].append(nick[:19])


def tell_admin_mes(raw, type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if type in ['private']:
        return
    if not check_file(source[1],'tadmin.txt'):
        return
    txt = ANTI_BASE
    if not txt:
        return
    if not source[1] in txt:
        return
    for x in txt[source[1]]:
        if not txt[source[1]][x].has_key('msg'):
            return
        if source[1] in USRON:
            if x in USRON[source[1]]:
                return
        txt[source[1]][x]['msg']+=1
    
register_join_handler(tell_admin_join)
register_command_handler(tell_admin_subscribe, 'подписка', ['мод','админ'], 20, 'Показывает все визиты юзеров во время вашего отсутствия,баны и список киков', 'подписка <0|1>', ['подписка 0','подписка 1'])
register_leave_handler(tell_admin_leave)
register_message_handler(tell_admin_mes)


            
def anti_bot_goon(groupchat, nick, afl, role):
    anti = aspam_file(groupchat,'anti')
    anticonf = aspam_file(groupchat,'anticonf')
    jid = get_true_jid(groupchat+'/'+nick)
    if not nick or nick.isspace():
        return
    if nick == get_bot_nick(groupchat):
        return
    if len(nick)>20:
        return
    acc=int(user_level(groupchat+'/'+nick, groupchat))
    if acc>16 or acc<0:
        return
    if jid in anti:
        if not anti_conn:
            chenge_role(groupchat, nick, 'visitor')
            threading.Thread(None, antispam_private_flood, 'antispam_bot'+str(random.randrange(0, 999)), (groupchat,nick)).start()
            return
    if nick in anti:
        chenge_role(groupchat,nick,'visitor')
        if not anti_conn:
            threading.Thread(None, antispam_private_flood, 'antispam_bot'+str(random.randrange(0, 999)), (groupchat,nick)).start()
        if not jid in anti:
            bs='dynamic/'+groupchat+'/anti.txt'
            anti=eval(read_file(bs))
            anti[jid]={}
            write_file(bs, str(anti))
            antispam_load(groupchat)
            return
    if 'avi' in anticonf:
        if time.time() - anticonf['avi']['time']<1800:
            chenge_role(groupchat, nick,'visitor')
    

register_join_handler(anti_bot_goon)


def aspam_file(groupchat,file):
    if not groupchat in GROUPCHATS:
        return
    if file=='tadmin':
        return ANTI_BASE
    if groupchat in ANTI_BD:
        if file+'.txt' in ANTI_BD[groupchat]:
            return ANTI_BD[groupchat][file+'.txt']
    return '{}'

def handler_anti_lennick(groupchat, nick, afl, role):
    jid=get_true_jid(groupchat+'/'+nick)
    if not jid or jid==None:
        return
    serv = jid.split('@')[1]
    if nick == get_bot_nick(groupchat):
        return
    if len(nick)>20:
        chenge_afl(groupchat, jid, 'outcast')
        time.sleep(0.1)
        if len(nick)<100:
            chenge_role(groupchat, nick, 'none')
        if serv not in GREEN_SERV:
            chenge_afl(groupchat, serv, 'outcast')
            if ANTI_BASE:
                for x in ANTI_BASE:
                    if x.count(groupchat) and 'ban' in ANTI_BASE[x]:
                        ANTI_BASE[x]['ban'].append(serv+u' подозрение на вайп!')

def chenge_afl(groupchat, nick, afl):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    iq.setID('kick'+str(random.randrange(1000, 9999)))
    query = xmpp.Node('query')
    query.setNamespace('http://jabber.org/protocol/muc#admin')
    query.addChild('item', {'jid':nick, 'affiliation':afl})
    iq.addChild(node=query)
    JCON.send(iq)

def chenge_role(groupchat, jid, role):
    reason=u'antispam work'
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    iq.setID('kick'+str(random.randrange(1000, 9999)))
    query = xmpp.Node('query')
    query.setNamespace('http://jabber.org/protocol/muc#admin')
    kick=query.addChild('item', {'jid':jid, 'role':role})
    kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
    iq.addChild(node=query)
    JCON.send(iq)

def handler_antispam_msg(raw, type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if type == 'private':
        return
    if not source[2] or source[2].isspace():
        return
    if source[2]==get_bot_nick(source[1]):
        return
    acc=int(user_level(source[1]+'/'+source[2], source[1]))
    if (acc in [-10,'-10']) | (acc > 16) | (acc < 0):
        return
    jid = get_true_jid(source[1]+'/'+source[2])
    anti = aspam_file(source[1],'anti')
    tadmin = aspam_file(source[1],'tadmin')
    anticonf = aspam_file(source[1],'anticonf')
    if jid in anti:
        chenge_role(source[1], jid, 'visitor')
        if not anti_conn:
            threading.Thread(None, antispam_private_flood, 'antispam_bot'+str(random.randrange(0, 999)), (source[1],source[2])).start()
    if source[2] in anti:
        chenge_role(source[1], jid, 'visitor')
        if not jid in anti:
            fp=open('dynamic/'+source[1]+'/anti.txt','r')
            anti=eval(fp.read())
            fp.close()
            anti[jid]={}
            write_file('dynamic/'+source[1]+'/anti.txt',str(anti))
    if len(parameters)>1150:
        if 'on' in anticonf:
            if not 'avi' in anticonf:
                fp=open('dynamic/'+source[1]+'/anticonf.txt','r')
                anticonf=eval(fp.read())
                fp.close()
                anticonf['avi']={'time':time.time()}
                write_file('dynamic/'+source[1]+'/anticonf.txt',str(anticonf))
                antispam_load(source[1])
                msg(source[1],u'Временно включен авизитор, для отключения наберите avi 0')
            if 'avi' in anticonf:
                if time.time() - anticonf['avi']['time']<360:
                    for x in GROUPCHATS[source[1]]:
                        try:
                            chenge_role(source[1], get_true_jid(source[1]+'/'+x), 'visitor')
                        except:
                            pass
                else:
                    fp=open('dynamic/'+source[1]+'/anticonf.txt','r')
                    anticonf=eval(fp.read())
                    fp.close()
                    anticonf['avi']['time']=time.time()
                    write_file('dynamic/'+source[1]+'/anticonf.txt',str(anticonf))
                    antispam_load(source[1])
            if not jid in anti and not source[2] in anti:
                if anti_auto_add(source[1],jid,u' занесен в антилист:большая мессага.'):
                    chenge_role(source[1], nick, 'visitor')
                    if not anti_conn:
                        threading.Thread(None, antispam_private_flood, 'antispam_bot'+str(random.randrange(0, 999)), (source[1],source[2])).start()
        else:
            msg(source[1],u'/me может включить антиспам (антиспам 1)?')
                    
    if len(parameters)<1150:
        if not 'on' in anticonf:
            return
        if check_count(source[1], parameters):
            anti_auto_add(source[1],jid,u' занесен в антилист:реклама')
            chenge_role(source[1], source[2], 'visitor')
            threading.Thread(None, antispam_private_flood, 'antispam_bot'+str(random.randrange(0, 999)), (source[1],source[2])).start()
        

                
def anti_auto_add(groupchat,user,mess):
    if not groupchat in GROUPCHATS:
        return 0
    tadmin = aspam_file(groupchat,'tadmin')
    fp=open('dynamic/'+groupchat+'/anti.txt','r')
    anti=eval(fp.read())
    fp.close()
    if not user in anti:
        anti[user]={}
        write_file('dynamic/'+groupchat+'/anti.txt',str(anti))
        antispam_load(groupchat)
        msg(groupchat,user[:20]+u' add to antispam base!')
        if tadmin:
            for x in tadmin:
                if x.count(groupchat) and 'ban' in tadmin[x]:
                    tadmin[x]['ban'].append(user[:20]+mess)
        return 1
    return 0


def check_count(groupchat, parameters):
    if not groupchat in GROUPCHATS:
        return
    body=parameters.lower()
    s= body
    if s.count(' ')>0:
        s=parameters.split()[0]
    if not s in COMMANDS:
        if body.count(u'заходите в') | body.count(u'@con') | body.count(u'@c.j.r') | body.count(u'conference.jabber'):
            return 1
    return 0


def antispame_subscribe(type, source, parameters):
    if not parameters or parameters.isspace():
        return
    if not source[1] in GROUPCHATS:
        return
    FILE = 'dynamic/'+source[1]+'/anticonf.txt'
    anti = aspam_file(source[1],'anti')
    tadmin = aspam_file(source[1],'tadmin')
    anticonf=eval(read_file(FILE))
    if parameters == '1':
        if not 'on' in anticonf:
            anticonf['on']={}
            write_file(FILE, str(anticonf))
            reply(type,source,u'Авто-антиспам включен!')
            antispam_load(source[1])
            return
        else:
            reply(type,source,u'Уже работает!')
            return
    if parameters == '0':
        if 'on' in anticonf:
            del anticonf['on']
            write_file(FILE, str(anticonf))
            reply(type,source,u'Авто-антиспам отключен!')
            antispam_load(source[1])
            return
        else:
            reply(type,source,u'Уже отключен!')
            return
    if parameters in anti:
        reply(type, source, u'такой ник/JID в базе уже есть')
        return
    else:
        if parameters:
            fp='dynamic/'+source[1]+'/anti.txt'
            anti=eval(read_file(fp))
            anti[parameters] = {}
            write_file('dynamic/'+source[1]+'/anti.txt',str(anti))
            antispam_load(source[1])
            if tadmin:
                for x in tadmin:
                    if x.count(source[1]) and 'ban' in tadmin[x]:
                        tadmin[x]['ban'].append(u'в антилист занесен '+parameters+u': добавил - '+source[2])
            reply(type, source, parameters+u' добавлен')
            nick = parameters
            tojid = source[1]+'/'+parameters
            acc = int(user_level(source[1]+'/'+parameters, source[1]))
            if acc<16 and acc> -1:
                if parameters in GROUPCHATS[source[1]]:
                    if GROUPCHATS[source[1]][parameters]['ishere']:
                        chenge_role(source[1], get_true_jid(source[1]+'/'+parameters), 'visitor')
                        if not anti_conn:
                            threading.Thread(None, antispam_private_flood, 'antispam_bot'+str(random.randrange(0, 999)), (source[1],parameters)).start()
        
                    



def antispame_show(type, source, parameters):
    ANTIUSER = 'dynamic/'+source[1]+'/anti.txt'
    fp = open(ANTIUSER, 'r')
    txt = eval(fp.read())
    fp.close()
    if len(txt) == 0:
      reply(type, source, u'База пуста!')
      return
    p =1
    spisok = ''
    for usr in txt:
          spisok += str(p)+'. '+usr+'\n'
          p +=1
    reply(type, source, u'(всего '+str(len(txt))+u'):\n'+spisok)


def antispam_unsubscribe(type, source, parameters):
    ANTIUSER = 'dynamic/'+source[1]+'/anti.txt'
    if parameters:
        fp = open(ANTIUSER, 'r')
        ftr = eval(read_file(ANTIUSER))
        fp.close()
        if parameters in ftr:
            del ftr[parameters]
        else:
            reply(type, source, u'ты видишь такой ник или jid в списке? я - нет!')
            return
        write_file(ANTIUSER,str(ftr))
        reply(type, source, parameters+u' удален из антиспама')
        antispam_load(source[1])
        ANTI_BOT['off']=0
        time.sleep(5)
        ANTI_BOT['off']=1

def antispam_clear(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    ANTIUSER = 'dynamic/'+source[1]+'/anti.txt'
    write_file(ANTIUSER,str('{}'))
    antispam_load(source[1])
    reply(type, source, u'done')
    ANTI_BOT['off']=0
    time.sleep(5)
    ANTI_BOT['off']=1

ANTISPAM_JCON = None

anti_conn = 0

def anti_timer():
    time.sleep(60)
    try:
        if ANTISPAM_JCON.isConnected():
            ANTISPAM_JCON.disconnect()
            anti_conn = 0
    except:
        pass

ANTI_LAST = 0


def antispam_private_flood(groupchat, nick):
    if nick.isspace():
        return
    if not groupchat in GROUPCHATS:
        return
    if time.time() - INFO['start'] < 120:
        return
    global ANTI_LAST
    global anti_conn
    if not ANTI_LAST:
        ANTI_LAST=time.time()
    else:
        if time.time() - ANTI_LAST<3600:
            return
        else:
            ANTI_LAST=time.time()
    if not anti_conn:
        antispam_bot()
    tim=time.time()
    while not anti_conn and time.time() - tim<15:
        time.sleep(1)
        pass
    if not anti_conn:
        return
    prs=xmpp.protocol.Presence(groupchat+'/Antispam'+str(random.randrange(100,9999)))
    try:
        ANTISPAM_JCON.send(prs)
    except:
        pass
    time.sleep(2)
    n=0
    s=time.time()
    while time.time() - s < 60:
        n+=1
        try:
            ANTISPAM_JCON.send(xmpp.Message(groupchat+'/'+nick,str(n),'chat'))
        except:
            pass
    time.sleep(2)
    try:
        ANTISPAM_JCON.disconnect()
    except:
        pass
        

def antispam_bot():
    global anti_conn
    if anti_conn:
        print 'Antispam BOT is work now!'
        return
    print '-= Antispam BOT start! =-\n'
    try:
        (USERNAME, SERVER) = JID.split("/")[0].split("@")
    except:
        print 'Wrong, wrong JID %s' % JID
        return
    global ANTISPAM_JCON
    ANTISPAM_JCON = xmpp.Client(server=SERVER, port=PORT, debug=[])
    con=ANTISPAM_JCON.connect(server=(CONNECT_SERVER, PORT), secure=0,use_srv=True)
    if not con:
        print 'Do not connected, return'
        return
    else:
        print 'Connection Established'
    auth=ANTISPAM_JCON.auth(USERNAME, PASSWORD, str(random.randrange(010,999)))
    if not auth:
        print 'Do not auth, return'
        return
    else:
        print 'Connected!'
    ANTISPAM_JCON.sendInitPresence()
    anti_conn=1
    #while ANTISPAM_JCON.isConnected():
    #    ANTISPAM_JCON.Process(1)

def hnd_avi_work(type,source,parameters):
    if not source[1] in GROUPCHATS:
        return
    FILE = 'dynamic/'+source[1]+'/anticonf.txt'
    anticonf=eval(read_file(FILE))
    if parameters in ['0']:
        if 'avi' in anticonf:
            del anticonf['avi']
            write_file(FILE,str(anticonf))
            reply(type,source,u'Отключил авто-девойс!')
            return
        else:
            reply(type,source,u'Уже отключен!')
            return
    if parameters=='1':
        if not 'avi' in anticonf:
            anticonf['avi']={'time':time.time()}
            write_file(FILE,str(anticonf))
            reply(type,source,u'Включен авто-девойс на 30 минут!!!')
            return
        else:
            anticonf['avi']['time']=time.time()
            write_file(FILE,str(anticonf))
            reply(type,source,u'Уже Включен авто-девойс!')


AN_LIST=[u'anti.txt',u'tadmin.txt',u'anticonf.txt']

def antispam_load(groupchat):
    if (check_file(groupchat,'anti.txt')) | (check_file(groupchat,'tadmin.txt')) | (check_file(groupchat,'anticonf.txt')):
        for x in AN_LIST:
            if groupchat in ANTI_BD:
                if x in ANTI_BD[groupchat]:
                    del ANTI_BD[groupchat][x]
            try:
                file='dynamic/'+groupchat+'/'+x
            except:
                continue
            fp=open(file,'r')
            txt=eval(fp.read())
            fp.close()
            if not groupchat in ANTI_BD:
                ANTI_BD[groupchat]={}
            if not groupchat in ANTI_BASE:
                ANTI_BASE[groupchat]={}
            if x=='tadmin.txt':
                for c in txt:
                    if not c in ANTI_BASE[groupchat]:
                        ANTI_BASE[groupchat][c]=txt[c]
                return
            if txt:
                for i in txt:
                    if not x in ANTI_BD[groupchat]:
                        ANTI_BD[groupchat][x]=[]
                    if not i in ANTI_BD[groupchat][x]:
                        ANTI_BD[groupchat][x].append(i)

AUTO_SUB_L={}

def hand_autosub(groupchat, nick, role, afl):
    if time.time() - INFO['start'] < 70:	
		return
    if groupchat in GROUPCHATS:
        if role=='owner':
            if check_file(groupchat,'autosub.txt'):
                try:
                    txt=eval(read_file('dynamic/'+groupchat+'/autosub.txt'))
                except:
                    write_file('dynamic/'+groupchat+'/autosub.txt', '{}')
                    txt=eval(read_file('dynamic/'+groupchat+'/autosub.txt'))
                jid=get_true_jid(groupchat+'/'+nick)
                if groupchat in ANTI_BASE:
                    if jid in ANTI_BASE[groupchat]:
                        return
                if jid not in txt:
                    if get_bot_nick(groupchat) in GROUPCHATS[groupchat]:
                        if not GROUPCHATS[groupchat][get_bot_nick(groupchat)]['ismoder']:
                            return
                    msg(groupchat+'/'+nick,u'Ув. Владелец '+groupchat+u',\n при входе вы можете автоматически получать всю необходимую статистику включая посещаемость (ники, количество сообщений), список банов и киков в вашей конференции.\n Для подписки напешите мне <да> без кавычек,\nлибо просто проигнорируйте это сообщение.\nтаймер 3 минуты.')
                    AUTO_SUB_L[jid]=groupchat
                    hand_autosub_timer(groupchat,jid)
                         

def hand_autosub_answ(raw, type , source, parameters):
    jid=get_true_jid(source[1]+'/'+source[2])
    if jid in AUTO_SUB_L:
        if parameters.lower() in [u'да',u'да!',u'lf'] and type=='private':
            if AUTO_SUB_L[jid]==source[1]:
                tell_admin_subscribe(type,source,u'1')


def hand_autosub_timer(groupchat,jid):
    time.sleep(180)
    if jid in AUTO_SUB_L:
        try:
            del AUTO_SUB_L[jid]
        except:
            pass
        if check_file(groupchat,'autosub.txt'):
            txt=eval(read_file('dynamic/'+groupchat+'/autosub.txt'))
            txt[jid]={}
            write_file('dynamic/'+groupchat+'/autosub.txt',str(txt))
            
    
    
                         
register_message_handler(hand_autosub_answ)
register_join_handler(hand_autosub)
register_stage1_init(antispam_load)    
register_join_handler(handler_anti_lennick)
register_message_handler(handler_antispam_msg)
register_command_handler(antispame_subscribe, 'антиспам', ['мод','антиспам','админ','антивайп'], 20, 'Включить/отключить авто-антиспам(антиспам 0/антиспам1), либо добавить чейто ник в antilist,после чего бот будет спамить приват этого юзера.Авто-антиспам заносит ники за рекламу и спам самостоятельно,и чистит конфу после отакэ)', 'антиспам <ник>', ['антиспам vasya','антиспам 1','антиспам 0'])
register_command_handler(antispame_show, 'antilist', ['мод','антиспам','антивайп'], 0, 'показывает базу антиспама', 'antilist', ['antilist'])
register_command_handler(antispam_unsubscribe, 'antilist-', ['мод','антиспам','антивайп'], 20, 'удаляет ник или JID из базы антиспама', 'antilist- <ник>', ['antilist- vasya'])
register_command_handler(antispam_clear, 'anti_clean', ['мод','админ','антивайп'], 20, 'удаляет все ники и джиды из базы антиспама', 'anti_clear', ['anti_clear'])
register_command_handler(hnd_avi_work, 'avi', ['антиспам','мод','антивайп'], 20, 'Временной авизитор на 30 минут! Команда не эффективна если другие функции настроены на выдачу голоса или в конференции есть другие боты и они настроены выдавать голос!', 'avi <0|1>', ['avi 1'])

