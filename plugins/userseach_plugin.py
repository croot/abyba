#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  userseach_plugin.py

# codded by Avinar (avinar@xmpp.ru)   v1.1
# fix by 40tman 

# thanks To:
#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>



from re import match

mdisco_pending=[]
inrooms=[]
suser=''
suserdef=''
skonfs=0
kir=1
reg=1
st=1
us_conn=0

def handler_disco_ext_nn(parameters):
	iq = xmpp.Iq('get')
	while 1:
		iqs = 'dis'+str(random.randrange(1000, 9999))
		if iqs not in globals()['mdisco_pending']:
			break
	globals()['mdisco_pending'].append(iqs)
	iq.setID(iqs)
	iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#items')
	if parameters:
		iq.setTo(parameters)
		JCON1.SendAndCallForResponse(iq, handler_disco_ext_n, {'parameters': parameters})
		return
	

def handler_disco_ext_n(coze, res, parameters):
	test1=string.split(parameters, ' ', 1)
	test2=string.split(test1[0], '@', 1)
	if len(test2)==2:
		trig=0
	else:
		trig=1
	discos=[]
	rep=0
	id=res.getID()
	if id in globals()['mdisco_pending']:
		globals()['mdisco_pending'].remove(id)
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
						
						globals()['skonfs']= globals()['skonfs'] + 1
						if globals()['reg']==2:
							globals()['suser']=globals()['suser'].lower()
							att['name']=att['name'].lower()
						if globals()['kir']==2:
							globals()['suser']=globals()['suser'].replace(u'a', u'а').replace(u'A', u'А').replace(u'e', u'е').replace(u'E', u'Е').replace(u'T', u'Т').replace(u'O', u'О').replace(u'o', u'о').replace(u'p', u'р').replace(u'P', u'Р').replace(u'H', u'Н').replace(u'k', u'к').replace(u'K', u'К').replace(u'X', u'Х').replace(u'x', u'х').replace(u'C', u'С').replace(u'c', u'с').replace(u'B', u'В').replace(u'M', u'М').replace(u'Y', u'У').replace(u'0', u'О')
							att['name']=att['name'].replace('a', u'а').replace('A', u'А').replace('e', u'е').replace('E', u'Е').replace('T', u'Т').replace('O', u'О').replace('o', u'о').replace('p', u'р').replace('P', u'Р').replace('H', u'Н').replace('k', u'к').replace('K', u'К').replace('X', u'Х').replace('x', u'х').replace('C', u'С').replace('c', u'с').replace('B', u'В').replace('M', u'М').replace('Y', u'У').replace('0', u'О')
						if globals()['st']==2:
							if globals()['suser']==att['name']:
								globals()['inrooms'].append(parameters + ' ('+defname+')')
								rep=1
						else:
							if att['name'].count(globals()['suser']):
								globals()['inrooms'].append(parameters + ' ('+defname+')')
								rep=1
								return

JCON1=None

def handler_mdisco(type, source, parameters):
	if parameters:
		if globals()['suser']:
			reply(type,source,u'На данный момент я выполняю другой запрос. Попробуйте повторить через 3 минуты.')
			return
		globals()['us_conn']=0
		globals()['confr']=0
		threading.Thread(None,start_finded_conference,'start_us_srch_bot'+str(random.randrange(1111,99999)),()).start()
		if type=='public':
			reply(type,source,u'Результат смотри у себя в привате через 3 минуты...')
		else:
			reply(type,source,u'Подожди 3 минутки...')
		t=0
		while not globals()['us_conn']:
                        t+=1
                        if t>100:
                                reply(type, source, u'попробуйте позже!')
                                break
                        time.sleep(0.1)
                        pass
                time.sleep(3)
		globals()['inrooms']=[]
		globals()['skonfs']=0
		globals()['suserdef']=''
		globals()['mdisco_pending']=[]
		globals()['reg']=1
		globals()['kir']=1
		globals()['st']=2
		parameters=parameters.split(' ')
		for line in parameters:
			if line == u'-k':
				globals()['kir']=2
			elif line == u'-r':
				globals()['reg']=2		
			elif line == u'-s':
				globals()['st']=1
			elif (len(line)==2) & (line.count('-')):
				continue
			else:
				if globals()['suser']=='':
					globals()['suser']+=line
					globals()['suserdef']+=line
				else:
					globals()['suser']+=' '+line
					globals()['suserdef']+=' '+line
		
		handler_mdiscoteco(type, source, parameters,'conference.jabber.ru',500)
		handler_mdiscoteco(type, source, parameters,'conference.qip.ru',135)
		threading.Thread(None,COMMAND_HANDLERS['disco_ans'],'command_user_search'+str(INFO['thr']),(type, source, parameters,)).start()
	else:
		reply(type,source,u'ииии?')
		return
			
			
			
def handler_mdiscoteco(type, source, parameters,server,stop):
	iq = xmpp.Iq('get')
	
	while 1:
		iqs = 'dis'+str(random.randrange(1000, 9999))
		if iqs not in globals()['mdisco_pending']:
			break		
	
	globals()['mdisco_pending'].append(iqs)
	iq.setID(iqs)
	iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#items')
	iq.setTo(server)
	JCON1.SendAndCallForResponse(iq, handler_mdisco_ext, {'type': type, 'source': source, 'stop': stop, 'parameters': server})
	return

confr=0	

def handler_mdisco_ext(coze, res, type, source, stop, parameters):
	test1=string.split(parameters, ' ', 1)
	test2=string.split(test1[0], '@', 1)
	if len(test2)==2:
		trig=0
	else:
		trig=1
	mdisco=[]
	rep=''
	id=res.getID()
	if id in globals()['mdisco_pending']:
		globals()['mdisco_pending'].remove(id)
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
							globals()['confr']+=1
							mdisco.append([st[0],att['jid'],int(st[1])])
							trig=1
					else:
						mdisco.append(att['jid'])
						trig=2
				else:
					if att.has_key('name'):
						mdisco.append(att['name'])
						trig=0
			handler_1mdisco_answ(type,source,trig,stop,mdisco,parameters)
			return
		else:
			print parameters + u' лежит'
	else:
		print u'o_O'
	
	
def handler_1mdisco_answ(type,source,trig,stop,mdisco,parameters):
	total=0
	if str(total)==stop:
		reply(type, source, u'всего '+str(len(mdisco))+u' пунктов')
		return
	if trig:
		mdisco.sort(lambda x,y: x[2] - y[2])
		mdisco.reverse()
		for x in mdisco:
			total=total+1
			handler_disco_ext_nn(x[1])
			if total==stop:
				break


	
def handler_disco_an_nnn(type, source, parameters):
	time.sleep(110)
	if not globals()['skonfs']:
                time.sleep(60)
	try:
                globals()['us_conn']=0
                JCON1.disconnect()
        except:
                pass
	rep=u'Пользователь с никнеймом ' + globals()['suserdef'] + u' сейчас находится в:\n '
	gg=''
	if len(globals()['inrooms']) > 0:
		for g in globals()['inrooms']:
			gg= gg + g + u'\n '
		rep= rep + gg + u'\n Конференций: '+str(globals()['confr'])+u' всего пользователей найдено: ' + str(globals()['skonfs'])
	else:
		rep=u'Пользователь с никнеймом ' + globals()['suserdef'] + u' не найден. Конференций: '+str(globals()['confr'])+u' Всего пользователей найдено: ' + str(globals()['skonfs'])
	globals()['suser']=''
	reply('private',source,rep.strip())
	
mdisco=[]



def start_finded_conference():
	try:
		(USERNAME, SERVER) = JID.split("/")[0].split("@")
	except:
		print 'Wrong, wrong JID %s' % JID
		os.abort()
	global JCON1
	JCON1 = xmpp.Client(server=SERVER, port=PORT, debug=[])


	con=JCON1.connect(server=(CONNECT_SERVER, PORT), secure=0,use_srv=True)
	if not con:
                return
	else:
		print 'Connection Established'

	print 'Using',JCON1.isConnected()


	auth=JCON1.auth(USERNAME, PASSWORD, str(random.randrange(010,999)))
	if not auth:
                return
	else:
		print 'Connected!'
	global us_conn
	us_conn+=1
	if auth!='sasl':
		print 'Warning: unable to perform SASL auth. Old authentication method used!'

	while JCON1.isConnected():
                JCON1.Process(1)


register_command_handler(handler_disco_an_nnn, 'disco_ans', [], 100, 'служебная команда', 'не заморачивайтесь на ней', ['НЕ КОМЕНТИТЬ'])			
register_command_handler(handler_mdisco, 'отыскать', ['мук','инфо','все'], 0, 'Ищет указанный никнейм в 1000 лучших конференций русской сети Jabber.\nДоп. Параметры:\n -s НЕстрогое соответствие по количеству символов;\n -r игногировать регистр символов;\n -k игнорировать отличие русских букв от английских. (англ А = Русская А);\n\nБольше параметров - обширней результат', 'отыскать <ник> [<-s -k -r>]', ['отыскать Avinar','отыскать Avinar -r','отыскать Avinar -s -k','отыскать Avinar -k -s -r'])
