#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman
#ver 5.0 (NEW!)

import os, xmpp, time, sys, time, pdb, urllib, threading, types, random

BOT_VER1 = {'botver': {'name': 'Tkabber', 'ver': '0.11.1-svn-20101220 (Tcl/Tk 8.5.5)', 'os': ''}}

ob_pd=[]
OB_MSG={'num':0,'nick':'','reg':0}
OB_NT={}
OB_SEND={}
OB_USER={}
OB_ROOM=[]
JJJ=[]
OB_SE='conference.jabber.ru'

def hd_ob_join(cl,groupchat):
  nick = gen_ob(random.Random().randint(10,15))
  if len(OB_MSG['nick'])>2:
    nick=OB_MSG['nick']
  mess = xmpp.protocol.Presence(groupchat+'/'+nick)
  mess.setTag('x', namespace=xmpp.NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
  try:
    cl.send(mess)
  except:
    pass

def ob_leave(cl,groupchat,status=''):
  prs=xmpp.Presence(groupchat, 'unavailable')
  try:
    cl.send(prs)
    return
  except:
    pass
	
def gen_ob(_len = None, sg = None):
  if sg == None:
    sg = 'aoeuizxcvbn.msdfghjklqwrtyp1234567890'
  if _len == None:
    _len = random.Random().randint(1, 100)
  s = ''
  l = len(sg)
  while _len > 0:
    s += sg[random.Random().randint(0, l - 1)]
    _len -= 1
  return s

OB_L_ERR={}

def get_prs_ob(cl,mess):
  try:
    try_get_prs_ob(cl, mess)
  except:
    pass

def try_get_prs_ob(cl, mess):
  fromjid=mess.getFrom()
  scode=1
  try:
    scode = mess.getStatusCode()
  except:
    pass
  ptype = mess.getType()
  print scode
  if ptype=='error':
    ecode = mess.getErrorCode()
    if ecode=='401' or ecode=='307':
      return
    if not OB_L_ERR:
      OB_L_ERR['1']={'time':time.time(),'n':0}
    else:
      if time.time()-OB_L_ERR['1']['time']<3:
        OB_L_ERR['1']['n']+=1
        if OB_L_ERR['1']['n']>10:
          print 'obyava bot disconnect'
          try:
            cl.disconnect()
          except:
            pass
      else:
        OB_L_ERR['1']['time']=time.time()
        OB_L_ERR['1']['n']=0
    return
  rep=''
  for x in OB_SEND:
    rep+=x
  if fromjid and ptype != 'unavailable':
    try:
      spisok =xmpp.protocol.Message(fromjid,rep,'chat')
      cl.send(spisok)
    except:
      pass
	
def iq_ob(cl,iq):
	fromjid = iq.getFrom()
	global BOT_VER1
	if not iq.getType() == 'error':
		if iq.getTags('query', {}, xmpp.NS_VERSION):
			if not BOT_VER1['botver']['os']:
				osver=''
				if os.name=='nt':
					osname=os.popen("ver")
					osver=osname.read().strip().decode('cp866')+'\n'
					osname.close()			
				else:
					osname=os.popen("uname -sr", 'r')
					osver=osname.read().strip()+'\n'
					osname.close()			
				pyver = 'Windows XP'
				BOT_VER1['botver']['os'] = pyver
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setTagData('name', BOT_VER1['botver']['name'])
			query.setTagData('version', BOT_VER1['botver']['ver'])
			query.setTagData('os', BOT_VER1['botver']['os'])
			try:
                          cl.send(result)
                        except:
                          pass
		      
def handler_ob_start(type, source, parameters):
        stop,tojid,srch='500',OB_SE,''#'conference.jabber.ru',''
        if not OB_SEND:
          reply(type,source,u'а объяву добавить?')
          return
        iq = xmpp.Iq('get')
        id='dis'+str(random.randrange(1, 9999))
	globals()['ob_pd'].append(id)
	iq.setID(id)
	query=iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
	if len(tojid.split('#'))==2:
                query.setAttr('node',tojid.split('#')[1])
                iq.setTo(tojid.split('#')[0])
        else:
                iq.setTo(tojid)
                JCON.SendAndCallForResponse(iq, handler_getob_allconf, {'type': type, 'source': source, 'stop': stop, 'srch': srch, 'tojid': tojid})

def handler_getob_allconf(coze, res, type, source, stop, srch, tojid):
	disco=[]
	rep,trig='',0
	id=res.getID()
	if id in globals()['ob_pd']:
		globals()['ob_pd'].remove(id)
	else:
		print 'someone is doing wrong...(obyava_plugin.py)'
		reply(type, source, u'вглюкнуло...')
		return
	if res:
		if res.getType() == 'result':
			props=res.getQueryChildren()
			for x in props:
				att=x.getAttrs()
				if att.has_key('name'):
					try:
						st=re.search('^(.*) \((.*)\)$', att['name']).groups()
						disco.append([st[0],att['jid'],st[1]])
						trig=1
					except:
						if not trig:
							temp=[]
							if att.has_key('name'):
								temp.append(att['name'])
							if att.has_key('jid') and not tojid.count('@'):
								temp.append(att['jid'])
							if att.has_key('node'):
								temp.append(att['node'])
							disco.append(temp)
				else:
					disco.append([att['jid']])
			if disco:
				handler_ob_answ11(type,source,stop,disco,srch)
			else:
				reply(type, source, u'пустое диско')
			return
		else:
			rep = u'не могу'
	else:
		rep = u'аблом...'
	reply(type, source, rep)
	
	
def handler_ob_answ11(type,source,stop,disco,srch):
	total=0
	if total==stop:
		reply(type, source, u'всего '+str(len(disco))+u' пунктов')
		return
	rep,dis,disco = u'',[],sortdis_ob(disco)
	for item in disco:
		if len(item)==3:
			total+=1
			if srch:
				if srch.endswith('@'):
					if item[1].startswith(srch):
						dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']: '+str(item[2]))
						break
					else:
						continue
				else:
					if not item[0].count(srch) and not item[1].count(srch):
						continue
			dis.append(item[1]+u'')
			if len(dis)==stop:
				break
		elif len(item)==2:
			total+=1
			if srch:
				if not item[0].count(srch) and not item[1].count(srch):
					continue
			dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']')
			if len(dis)==stop:
				break
		else:
			total+=1
			if srch:
				if not item[0].count(srch):
					continue
			dis.append(str(total)+u') '+item[0])
			if len(dis)==stop:
				break
	if dis:
		if len(disco)!=len(dis):
			dis.append(u'')
	else:
		rep=u'пустое диско'
	ger = (u' '.join(dis))
	try:
          LISTCON = 'dynamic/oban.txt'
          fp = open(LISTCON, 'r')
          txt = eval(read_file(LISTCON))
        except:
          print u'no file oban.txt in /dynamic direcrotory'
          txt='{}'
        ddt = ger.split()
        OB_ROOM.extend(ddt)
        for x in OB_ROOM:
          if x in txt:
            OB_ROOM.remove(x)
        reply(type, source, 'список комнат получен, всего '+str(len(OB_ROOM)))
        lencon=len(OB_ROOM)
        handler_reg_jid(type,source,lencon)

def Step_Ob_On(cl):
  try:
    if cl.isConnected():
      cl.Process(1)
  except:
    pass
    return 0
  return 1
    

def ob_privacy_action(cl):
    type,source=0,0
    od=str(random.randrange(1, 999))
    iq = xmpp.Iq('set')
    id='privacy'+str(random.randrange(1000, 9999))
    iq.setID(id)
    query = xmpp.Node('query')
    query.setNamespace('jabber:iq:privacy')
    pri=query.addChild('list', {'name':"1"})
    zc=OB_SE
    var2=pri.addChild('item', {'action':"allow", 'order':'1', 'type':"jid", 'value':zc})
    n=n+1
    var3=pri.addChild('item', {'action':"deny", 'order':'2', 'type':"subscription", 'value':'none'})
    iq.addChild(node=query)
    try:
      cl.send(iq)
    except:
      pass
    default = xmpp.Iq('set')
    q = xmpp.Node('query')
    q.setNamespace('jabber:iq:privacy')
    v = q.addChild('active', {'name':"1"})
    default.addChild(node=q)
    try:
        cl.send(default)
    except:
        pass

def Ob_On(cl,psw):
    while Step_Ob_On(cl) and cl.isConnected(): pass

def get_msg_ob(cl, msg):
  txt=msg.getBody()
  if txt.count(u'cap') and txt.count(u'http'):
    print u'CAPTCHA'
    JCON.send(xmpp.Message(u'some_user@talkonaut.com',txt,'chat'))
    #par=txt.split()
    #for x in par:
    #  if x.count(u'http'):
    #    ANTIBAN['url']=x
    #    antiban_cap_detect(x)
    
def handler_reg_jid(type,source,lencon):
  try:
    lencon=str(len(OB_ROOM))
    bvc = gen_ob(random.Random().randint(6,11))
    try:
      file='dynamic/oserver.txt'
      fp=open(file,'r')
      srvl=eval(fp.read())
      fp.close()
    except:
      srvl=[u'talkonaut.com',u'jabberon.ru',u'jabber.perm.ru']
    gserv = random.choice(srvl)
    name, domain, password, newBotJid, mainRes = bvc, gserv, gen_ob(random.Random().randint(6,11)), 0,'Tkabber'
    print u'START'
    node = unicode(name)
    lastnick = name
    jid = xmpp.JID(node=node, domain=domain, resource=mainRes)
    print u'bot jid: '+unicode(jid)
    psw = u''
    cl = xmpp.Client(jid.getDomain(), debug=[])
    con = cl.connect()
    if not con:
      OB_MSG['reg']+=1
      if OB_MSG['reg']>10:
        reply(type,source,u'Превышен лимит ошибок.\nНе удалось подключиться к '+gserv+u' для повторной попытки наберите объява_ак')
        OB_MSG['reg']=0
        return
      else:
        handler_reg_jid(type,source,lencon)
        return
    cl.RegisterHandler('iq',iq_ob)
    cl.RegisterHandler('presence',get_prs_ob)
    cl.RegisterHandler('message',get_msg_ob)###
    print u'Connected'
    print u'New jid: '+unicode(jid.getNode())+'@'+unicode(domain)
    xmpp.features.register(cl, domain, {'username': node, 'password':password})
    au=cl.auth(jid.getNode(), password, jid.getResource())
    if not au:
      OB_MSG['reg']+=1
      if OB_MSG['reg']>10:
        reply(type,source,u'Превышен лимит ошибок.\nОшибка регистрации на '+gserv+u'для повторной попытки наберите объява_ак')
        OB_MSG['reg']=0
        return
      else:
        handler_reg_jid(type,source,lencon)
        return
    cl.sendInitPresence()
    reply(type,source,u'зайрегился как '+node+'@'+domain+u'\npass:'+password)
    print u'Autheticated'
    threading.Thread(None, Ob_On, 'at'+str(random.randrange(0, 999)), (cl,psw)).start()
    threading.Thread(None, hnd_run_ob, 'at'+str(random.randrange(0, 999)), (cl,domain,type,source,lencon)).start()
    ob_privacy_action(cl)
  except:
    pass
        
def hnd_run_ob(cl,domain,type,source,lencon):
  for x in range(0, int(lencon)):
    if not cl.isConnected():
      reply(type,source,u'Объява-бот завершил свою работу.Если это произошло раньше времени-возможно это являеться следствием ошибки.')
      break
    hd_obj_send(cl,domain,type,source,lencon)
  rm=str(len(OB_ROOM))
  if rm>10:
    print 'new registration'
    handler_reg_jid(type,source,lencon)
                
def hd_obj_send(cl,domain,type,source,parameters):
  if len(OB_ROOM)>1:
    spisok = ''
    if OB_SEND:
      for c in OB_SEND:
        spisok += c
    if spisok=='':
      reply(type,source,u'не добавлен текст объявы!')
      return
    chat = random.choice(OB_ROOM)
    OB_MSG['num']+=1
    n=str(OB_MSG['num'])
    if n.count('00'):
      reply(type,source,u'объяву отправлено в '+unicode(OB_MSG['num'])+u' конференций.')
    try:
      print unicode(chat)
    except:
      pass
    #time.sleep(25)
    threading.Thread(None, hd_ob_join, 'obyava_join'+str(random.randrange(0, 999)), (cl, chat)).start()
    time.sleep(2)
    if chat not in GROUPCHATS:
      for x in OB_SEND:
        omsg = xmpp.protocol.Message(chat, x, 'groupchat')
        try:
          cl.send(omsg)
        except:
          pass
    #else:
    #  try:
    #    omsg = xmpp.protocol.Message(chat, u'мне тут нельзя писать объяву,так что просто посижу)', 'groupchat')
    #    cl.send(omsg)
    #  except:
    #    pass
    time.sleep(4)
    ob_leave(cl,chat)
    try:
      if OB_ROOM:
        OB_ROOM.remove(chat)
    except ValueError:
      pass
    return
  else:
    reply(type,source,u'объяву выполнено!')
    try:
      xmpp.features.unregister(cl, domain)
    except:
      cl.disconnect()

                                                                 
def sortdis_ob(dis):
	disd,diss,disr=[],[],[]
	for x in dis:
		try:
			int(x[2])
			disd.append(x)
		except:
			diss.append(x)
	disd.sort(lambda x,y: int(x[2]) - int(y[2]))
	disd.reverse()
	diss.sort()
	for x in disd:
		disr.append(x)
	for x in diss:
		disr.append(x)
	return disr
	
disco=()

def omes_add(type, source, parameters):
  if parameters:
    if parameters == '':
      return
    OB_SEND[parameters]={}
    reply(type, source, parameters+u' добавленo')

def omes_show(type, source, parameters):
    if len(OB_SEND) == 0:
      reply(type, source, u'База пуста!')
      return
    spisok = ''
    for x in OB_SEND:
          spisok += x+'\n'
    reply(type, source, spisok)

def obyava_ban(type,source,parameters):
  try:
    file='dynamic/oban.txt'
    fp=open(file,'r')
    txt=eval(fp.read())
    fp.close()
  except:
    print 'no file dynamic/oban.txt'
    return
  if not parameters:
    if not txt:
      reply(type,source,u'нет запрещенных конференций!')
      return
    else:
      rep=''
      for x in txt:
        rep+=x+'\n'
      reply(type,source,rep)
      return
  if parameters.count(u'+'):
    s=parameters.split(u'+')[1]
    chat=s.strip()
    if not chat in txt:
      txt[chat]={}
      write_file(file,str(txt))
      reply(type,source,u'добавил запрет на '+chat)
      return
  if parameters.count(u'-'):
    s=parameters.split(u'-')[1]
    chat=s.strip()
    if chat in txt:
      del txt[chat]
      write_file(file,str(txt))
      reply(type,source,u'удалил запрет на '+chat)
      return
  if parameters.count(u'удалить'):
    write_file(file,'{}')
    reply(type,source,u'все запреты удалены!')

def ob_set_nick(type,source,parameters):
  OB_MSG['nick']=parameters[:100]

register_command_handler(ob_set_nick, 'объява_ник', ['мод','рассылка','спам'], 40, 'показывает объяву из базы.', 'объява_показать', ['объява_показать'])
register_command_handler(omes_show, 'объява_показать', ['мод','рассылка','спам'], 40, 'показывает объяву из базы.', 'объява_показать', ['объява_показать'])
register_command_handler(obyava_ban, 'объява_запрет', ['мод','рассылка','спам'], 40, 'запрет рассылки объявы в определенную конференцию.', 'объява_запрет <+|-|удалить> <чат>', ['объява_запрет + 123@conference.jabber.ru','объява_запрет удалить','объява_запрет'])
register_command_handler(omes_add, 'объява_адд', ['мод','спам','рассылка'], 40, 'добавить объяву', 'объява_адд текст', ['объява_адд привет жабберу от 40тмана'])
register_command_handler(handler_ob_start, 'объява_старт', ['мод','рассылка','спам'], 40, 'запускает рассылку сообщений в 500 лучших конф conference.jabber.ru. Чтоб довать мессагу юзай команду объява_адд', '.', ['.'])
register_command_handler(handler_reg_jid, 'объява_ак', ['мод','рассылка','спам'], 40, 'регистрирует новый аккаунт если авторегистрация была завершена с ошибкой', 'объява_ак', ['объява_ак'])
