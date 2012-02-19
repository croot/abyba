1#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman
#beta

ANTIBAN_SERV=[]

import urllib
try:
  import PIL
  from PIL import Image
except:
  print 'Exception in anonymouse_plugin,\nyou need PIL library from your python'


ANTIBAN={'pri':0,'url':'','on':0,'err':0,'thr':0,'msg':'','chat':'','ban':'','work':0,'all':[],'nick':'','lim':0,'jid':'','try':0}
GET_NI=[]
GEN_NI=[]

def antiban_timer(z, conf):
  return
  time.sleep(10)
  try:
    if not cl.isConnected() or not ANTIBAN['jid']:
      try:
        cl.disconnect()
      except:
        pass
    antiban_reg('','',conf)
  except:
    antiban_reg('','',conf)

def antiban_dchnd():
  return
    
def antiban_join_cl(cl,groupchat):
  threading.Thread(None, antiban_privacy_action, 'antiban_timer'+str(random.randrange(0, 999)), (cl,'',)).start()
  ANTIBAN['thr']=0
  if not ANNICK:
    nick=generate_antiban(random.Random().randint(6,11))
  else:
    nick = random.choice(ANNICK)
  ANTIBAN['nick']=nick
  #GEN_NI.append(groupchat+'/'+nick)
  prs=xmpp.protocol.Presence(groupchat+'/'+nick)
  pres=prs.setTag('x',namespace=xmpp.NS_MUC)
  pres.addChild('history',{'maxchars':'0'})
  #CAPS = 'http://qip.ru/caps'
  #NODE_ = u'<presence to="%TO_ROOM%/%NICK%"><priority>%PRIORETET%</priority><x xmlns="http://jabber.org/protocol/muc" /><c xmlns="http://jabber.org/protocol/caps" node="%CAPS%" ver="9036" /><show>%SHOW%</show><x xmlns="http://qip.ru/x-status" id="20"><title></title></x><status>%TEXT%</status></presence>'.replace('%TO_ROOM%', groupchat).replace('%NICK%', nick).replace('%PRIORETET%', u'1').replace('%CAPS%', CAPS).replace('%TEXT%', u'').replace('%SHOW%', u'')
  #prs=xmpp.simplexml.XML2Node(unicode(NODE_).encode('utf8'))
  try:
    cl.send(prs)
  except:
    pass
  time.sleep(2)
  #threading.Timer(2, antiban_all, 'antiban_all'+str(random.randrange(0, 999)), (groupchat,nick)).start()
  ANTIBAN['on']=1

def antiban_all(x, y):
  print 'all users'
  if str(len(ANTIBAN['all']))>1:
    rep=u'Список юзеров:\n'
    ms=''
    for x in ANTIBAN['all']:
      if x!='QIP':
        ms+=x+'\n'
    if ms=='' or ms==ANTIBAN['nick']+'\n':
      return
    JCON.send(xmpp.Message(ANTIBAN['msg'],rep+ms,'chat'))
    ANTIBAN['thr']=1
    ANTIBAN['all']=[]

def antiban_leave(cl,groupchat,status=''):
  prs=xmpp.Presence(groupchat, 'unavailable')
  try:
    cl.send(prs)
  except:
    pass
	
def generate_antiban(_len = None, sg = None):
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
  

		      
def hand_anon_start(type,source,parameters):
  global ANTIBAN
  global ANTIBAN_SERV
  body= parameters.split()
  if parameters:
    if parameters.isdigit():
      if parameters=='0':
        antiban_stop(type,source,parameters)
        return
    if parameters.count(u'ник'):
      if ANTIBAN['work']==1:
        s=parameters.split()
        prs=xmpp.protocol.Presence(ANTIBAN['chat']+'/'+s[1])
        try:
          cl.send(prs)
        except:
          pass
        return
    if not parameters.count('@'):
      reply(type,source,u'читай помощь по команде!')
      return
    i=1
    if not ANTIBAN_SERV:
      reply(type,source,u'список серверов не найден')
      return
    if ANTIBAN['work']:
      reply(type,source,u'команда на данный момент активна,чтобы остановить дайте команду антибан 0')
      return
    ANTIBAN['work']=1
    ANTIBAN['all']=[]
    ANTIBAN['lim']=0
    ANTIBAN['try']=1
    reply(type,source,u'ok')
    ms=source[1]
    if type=='private':
      ms=source[1]+'/'+source[2]
    ANTIBAN['msg']=source[1]
    ANTIBAN['chat']=parameters.lower()
    #threading.Thread(None, handler_timer_otake, 'antiban_timer'+str(random.randrange(0, 999)), (type,source,parameters)).start()
    threading.Thread(None, antiban_reg, 'antiban_start'+str(random.randrange(0, 999)), (type,source,parameters.lower())).start()
    

def antiban_proc():
  while ANTIBAN['work']:
    try:
      cl.Process(1)
    except:
      pass

def rr_ff():
  try:
    hhhz=eval(read_file('dynamic/nick.txt'))
    for x in hhhz:
      ANNICK.append(x)
  except:
    pass


    
cl=None
ANNICK=[]
rr_ff()

def antiban_reg(type,source,conf):
  if not ANTIBAN['try']:
    return
  if not ANTIBAN['work']:
    print '+1'
    ANTIBAN['work']=1
  print 'ok, try register on new server!'
  gserv=''
  try:
    threading.Thread(None, antiban_timer, 'antiban_timer'+str(random.randrange(0, 999)), ('',conf,)).start()
    bvc = generate_antiban(random.Random().randint(7,9))
    try:
      file='dynamic/anonymouse.txt'
      txt=eval(read_file(file))
    except:
      txt={}
    gserv = random.choice(ANTIBAN_SERV)
    name, domain, password, newBotJid, mainRes = bvc, gserv, generate_antiban(random.Random().randint(6,11)), 0,'talkonaut'
    print u'START'
    node = unicode(name)
    lastnick = name
    jid = xmpp.protocol.JID(node=node, domain=domain, resource=mainRes)
    print u'bot jid: '+unicode(jid)
    psw = u''
    global cl
    cl = xmpp.Client(jid.getDomain(), debug=[])
    reply(type, source, u'Попытка подключиться к '+unicode(domain))
    con = cl.connect()
    if not con:
      try:
        if groupchat in txt:
          txt[groupchat].append(domain)
          write_file('dynamic/anonymouse.txt',str(txt))
        else:
          txt[groupchat]=[]
          write_file('dynamic/anonymouse.txt',str(txt))
          txt[groupchat].append(domain)
          write_file('dynamic/anonymouse.txt',str(txt))
      except:
        pass
      try:
        cl.disconnect()
      except:
        pass
      threading.Thread(None, antiban_reg, 'antiban_start'+str(random.randrange(0, 999)), (type,source,conf)).start()
      return
    cl.RegisterHandler('presence',antiban_presence_)
    cl.RegisterHandler('message',antiban_msg_)
    cl.RegisterHandler('iq',antiban_iq_)
    cl.RegisterDisconnectHandler(antiban_dchnd)
    print u'Connected'
    print u'New jid: '+unicode(jid.getNode())+'@'+unicode(domain)
    ANTIBAN['jid']=jid.getNode()+'@'+domain
    try:
      xmpp.features.register(cl, domain, {'username': node, 'password':password})
    except AttributeError:
      pass
    print u'Registered'
    au=cl.auth(jid.getNode(), password, jid.getResource())
    reply(type, source, u'Аутентификация')
    if not au:
      try:
        cl.disconnect()
      except:
        pass
      antiban_reg(type,source,conf)
      return
    print u'Autheticated'
    cl.sendInitPresence()
    try:
      node=xmpp.simplexml.XML2Node(VC_BOT)
      cl.send(node)
    except:
      pass
    ANTIBAN['lim']+=1
    if ANTIBAN['lim']>39:
      reply(type,source,u'исчерпано количество попыток регистрации.')
      return
    threading.Thread(None, antiban_join_cl, 'antiban_join'+str(random.randrange(0, 999)), (cl,conf)).start()
    while ANTIBAN['work']:
      cl.Process(1)
  except:
    pass

def antiban_iq_(cl, iq):
  try:
    antiban_iq_try(cl, iq)
  except:
    pass


def antiban_iq_try(cl, iq):
	fromjid = iq.getFrom()
	try:
          print unicode(iq)
        except:
          pass
	if not iq.getType() == 'error':
		if iq.getTags('query', {}, xmpp.NS_VERSION):
			if os.name=='nt':
                          osname=os.popen("ver")
			  osver=osname.read().strip().decode('cp866')+'\n'
			  osname.close()
			else:
                          osname=os.popen("uname -sr", 'r')
			  osver=osname.read().strip()+'\n'
			  osname.close()
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setTagData('name', u'talkonaut')
			query.setTagData('version', u's60-3rd')
			query.setTagData('os', u'Nokia N9')
			try:
                          cl.send(result)
                        except:
                          pass
		elif iq.getTags('time', {}, 'urn:xmpp:time'):
			tzo=(lambda tup: tup[0]+"%02d:"%tup[1]+"%02d"%tup[2])((lambda t: tuple(['+' if t<0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
			utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
			result = iq.buildReply('result')
			reply=result.addChild('time', {}, [], 'urn:xmpp:time')
			reply.setTagData('tzo', tzo)
			reply.setTagData('utc', utc)
			try:
                          cl.send(result)
                        except:
                          pass
		elif iq.getTags('query', {}, xmpp.NS_DISCO_INFO):
			items=[]
			ids=[]
			ids.append({'category':'client','type':'qip','name':'infium'})
			features=[xmpp.NS_DISCO_INFO,xmpp.NS_DISCO_ITEMS,xmpp.NS_MUC,'urn:xmpp:time','urn:xmpp:ping',xmpp.NS_VERSION,xmpp.NS_PRIVACY,xmpp.NS_ROSTER,xmpp.NS_VCARD,xmpp.NS_DATA,xmpp.NS_LAST,xmpp.NS_COMMANDS,'msglog','fullunicode',xmpp.NS_TIME]
			info={'ids':ids,'features':features}
			b=xmpp.browser.Browser()
			b.PlugIn(cl)
			b.setDiscoHandler({'items':items,'info':info})
		elif iq.getTags('query', {}, xmpp.NS_LAST):
			last=time.time()-LAST['t']
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setAttr('seconds',int(last))
			query.setData(LAST['c'])
			try:
                          cl.send(result)
                        except:
                          pass
		elif iq.getTags('query', {}, xmpp.NS_TIME):
			timedisp=time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.localtime())
			timetz=time.strftime("%Z", time.localtime())
			timeutc=time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
			result = xmpp.Iq('result')
			result.setTo(fromjid)
			result.setID(iq.getID())
			query = result.addChild('query', {}, [], 'jabber:iq:time')
			query.setTagData('utc', timeutc)
			query.setTagData('display', timedisp)
			try:
                          cl.send(result)
                        except:
                          pass
		elif iq.getTags('ping', {}, 'urn:xmpp:ping'):
			result = xmpp.Iq('result')
			result.setTo(iq.getFrom())
			result.setID(iq.getID())
			try:
                          cl.send(result)
                        except:
                          pass

def antiban_presence_(cl, mess):
  try:
    scode=1
    try:
      scode = mess.getStatusCode()
    except:
      pass
    fromjid = mess.getFrom()
    groupchat = fromjid.getStripped()
    nick = fromjid.getResource()
    ptype = mess.getType()
    if mess.getRole()=='visitor' and mess.getTo()==ANTIBAN['jid']+'/QIP':
      JCON.send(xmpp.Message(ANTIBAN['msg'],u'*вы теперь визитор*','chat'))
    if ANTIBAN['thr']==0:
      ANTIBAN['all'].append(nick)
    if nick == ANTIBAN['nick']:
      antiban_all(groupchat,nick)
    if nick and ANTIBAN['thr']==1:
      if ptype == 'available' or ptype == None:
        if nick==ANTIBAN['nick']:
          return
        JCON.send(xmpp.Message(ANTIBAN['msg'],nick+u' подключился*','chat'))
      if ptype == 'unavailable':
        JCON.send(xmpp.Message(ANTIBAN['msg'],nick+u' покинул чат*','chat'))
    if ptype=='error':
      ecode = prs.getErrorCode()
      if ecode == '409':
        antiban_join_cl(cl,groupchat)
        return
      if ecode == '403' or ecode == '404':
        try:
          file='dynamic/anonymouse.txt'
          txt=eval(read_file(file))
          s=ANTIBAN['jid']
          serv=s.split('@')[1]
          if groupchat in txt:
            txt[groupchat].append(serv)
            write_file(file, str(txt))
          else:
            txt[groupchat]=[]
            write_file(file, str(txt))
            txt[groupchat].append(serv)
            write_file(file, str(txt))
        except:
          pass
      if ecode == '407':
        JCON.send(xmpp.Message(ANTIBAN['msg'],u'*в эту конференцию могуть входить только члены*',u'chat'))
        ANTIBAN['on']=0
        return
      ANTIBAN['on']=0
      antiban_reg('','',groupchat)
      return
    if scode=='301':
      print 'BAN'
      JCON.send(xmpp.Message(ANTIBAN['msg'],u'*вас забанили*',u'chat'))
      ANTIBAN['on']=0
      try:
        xmpp.features.unregister(cl, ANTIBAN['jid'].split('@')[1])
        cl.disconnect()
      except:
        pass
      ANTIBAN['work']=0
      antiban_reg('','',groupchat)
    if scode=='307':
      time.sleep(2)
      ANTIBAN['on']=0
      JCON.send(xmpp.Message(ANTIBAN['msg'],u'*вас выкинули из комнаты*',u'chat'))
      antiban_join_cl(cl,groupchat)
    if scode=='404' or scode =='403':
      ANTIBAN['work']=0
      ANTIBAN['on']=0
      antiban_reg('','',groupchat)
    if scode=='322':
      ANTIBAN['work']=0
      JCON.send(xmpp.Message(ANTIBAN['msg'],u'*конференция доступна только для мемберов*',u'chat'))
  except:
    pass


def antiban_msg_(cl,msg):
  txt=msg.getBody()
  fromjid=msg.getFrom()
  try:
    print unicode(fromjid),unicode(txt)
  except:
    pass
  if fromjid.getStripped()!=ANTIBAN['chat'] and fromjid.getStripped()!=ANTIBAN['jid']:
    print 'ANTISPAM ON!'
    return
  if ANTIBAN['on']==1:
    if txt.count(u'установил(') or txt.count(u'subject'):
      return
    JCON.send(xmpp.Message(ANTIBAN['msg'],unicode(fromjid)+',\n'+txt[:600],'chat'))
  if len(txt)>1:
    if txt.count(u'радуга'):
      print u'IQ Control'
      try:
        cl.send(xmpp.Message(fromjid,u'7','chat'))
      except:
        pass
      return
    elif txt.count(u'толица'):
      print u'IQ Control'
      try:
        cl.send(xmpp.Message(fromjid,u'москва','chat'))
      except:
        pass
      return
    elif txt.count(u'2') and txt.count('+'):
      print u'IQ Control'
      try:
        cl.send(xmpp.Message(fromjid,u'4','chat'))
      except:
        pass
      return
    elif txt.count(u'1024') and txt.count(u'йте'):
      print u'IQ Control'
      try:
        cl.send(xmpp.Message(fromjid,u'1024','chat'))
      except:
        pass
    elif txt.count(u'cap') and txt.count(u'http'):
      print u'CAPTCHA'
      par=txt.split()
      for x in par:
        if x.count(u'http'):
          ANTIBAN['url']=x
          antiban_cap_detect(x)
      try:
        JCON.send(xmpp.Message(ANTIBAN['msg'],txt,'chat'))
      except:
        pass
      return


def antiban_stop(type,source,parameters):
  global ANTIBAN
  ANTIBAN['msg']=''
  ANTIBAN['try']=0
  if ANTIBAN['work']:
    ANTIBAN['work']=0
    reply(type,source,u'ушел в оффлайн!')
  else:
    reply(type,source,u'не активно')

def antiban_load():
  if not ANTIBAN_SERV:
    try:
      sss='dynamic/spamserv.txt'
      tt=open(sss,'r')
      nxn=eval(tt.read())
      tt.close()
      for x in nxn:
        ANTIBAN_SERV.append(x)
    except:
      print u'error in atiban_plugin.py, check file dynamic/spamserv.txt'
    antiban_open_list()

def antiban_open_list():
  try:
    fl='dynamic/anonymouse.txt'
    if os.path.exists(file):
      fp=open(fl, 'r')
      txt=eval(fp.read())
      fp.close()
    else:
      if os.access(fl, os.F_OK):
        fp = file(fl, 'w')
      else:
        fp = open(fl, 'w')
      fp=open(file, 'w')
      fp.write('{}')
      fp.close()
  except:
    write_file('dynamic/anonymouse.txt','{}')
    
      


def antiban_msg(type,source,parameters):
  try:
    cl.send(xmpp.Message(ANTIBAN['chat'],parameters,'groupchat'))
  except:
    pass

VC_BOT="""<iq type="set" id="qip_58">
<vCard xmlns="vcard-temp">
<FN />
<N>
<GIVEN />
<MIDDLE />
<FAMILY />
</N>
<NICKNAME>anonymouse</NICKNAME>
<BDAY>1899-12-30</BDAY>
<ADR>
<HOME />
<STREET />
<EXTADR />
<EXTADD />
<LOCALITY />
<REGION />
<PCODE />
<CTRY />
<COUNTRY />
</ADR>
<ADR>
<WORK />
<STREET />
<EXTADR />
<EXTADD />
<LOCALITY />
<REGION />
<PCODE />
<CTRY />
<COUNTRY />
</ADR>
<ORG>
<ORGNAME />
<ORGUNIT />
</ORG>
<TITLE />
<ROLE />
<URL />
<DESC />
<PHOTO />
</vCard>
</iq>
"""

PRBJ={}
PRVC={}

def antiban_privacy_action(cl,f):
    type,source=0,0
    od=str(random.randrange(1, 999))
    iq = xmpp.Iq('set')
    id='privacy'+str(random.randrange(1000, 9999))
    iq.setID(id)
    query = xmpp.Node('query')
    query.setNamespace('jabber:iq:privacy')
    pri=query.addChild('list', {'name':"1"})
    z=ANTIBAN['chat']
    zc=z.split('@')[1]
    vara=pri.addChild('item', {'action':"allow", 'order':'1', 'type':"jid", 'value':'conference.jabber.ru'})
    var2=pri.addChild('item', {'action':"allow", 'order':'2', 'type':"jid", 'value':'conference.talkonaut.com'})
    var3=pri.addChild('item', {'action':"allow", 'order':'3', 'type':"jid", 'value':'conference.qip.ru'})
    var4=pri.addChild('item', {'action':"deny", 'order':'4', 'type':"subscription", 'value':'none'})
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

ZK_=[]

TAB={'26':'7','37':'5','36':'0','40':'8','32':'2','35':'4','39':'6','27':'1','31':'3','39':'9'}


def imd_try(img):
    try:
      img=Image.open(img)
    except:
      return ''
    global ZK_
    w,h=img.size
    print w,h
    for c in range(0, w):
        for x in range(0, h):
            if x==49:
                ZK_.append('\n')
            ZK_.append(str(img.getpixel((c,x))))
    w=file('im.txt','w')
    w.write(str("".join(ZK_).replace('0',' ')))
    w.close()
    fp=open('im.txt','r')
    txt=fp.read().split('\n')
    fp.close()
    n=0
    px=0
    ress=''
    marker=[]
    for x in txt:
        if not x.isspace():
            if not px:
                marker.append(x.count('1'))
                #print x.count('1')#1
                n+=1
            px+=x.count('1')
        else:
            if px!=0:
                #print px
                if str(px) in TAB.keys():
                    num=TAB[str(px)]
                    if TAB[str(px)]=='9':
                        nn=n-1
                        try:
                            if marker[nn]==6:
                                num='6'
                        except:
                            pass
                    ress+=num
                px=0
    ZK_=[]
    return ress

    
def antiban_cap_detect(url):
  try:
    global ANTIBAN
    z=str(random.randrange(1001, 999999))
    urllib.urlretrieve(url+'/image', 'img/'+z+'.png')
    time.sleep(0.1)
    p=imd_try('img/'+z+'.png')
    if p=='':
      msg(ANTIBAN['msg'],u'капча не распознана')
      return
    p=p[:6]
    msg(ANTIBAN['msg'],p)
    data = urllib.urlencode({"key": p.decode('utf8','replace')})
    page = urllib.urlopen(ANTIBAN['url'], data)
    #os.remove('img/'+z+'.png')
    #ANTIBAN['url']=''
    #s = page.read()
    #img = Image.open('img/'+z+'.png')
    #img.show()
  #except Exception, err:
  #  msg(ANTIBAN['msg'], err)
  #print 'error in captcha url quest'
  except:
    pass

def antiban_cap(raw, type, source, parameters):
  if type=='private' and parameters.isdigit():
    if ANTIBAN['url']:
      data = urllib.urlencode({"key": parameters})
      page = urllib.urlopen(ANTIBAN['url'], data)
      s = page.read()
      try:
        print unicode(s)
      except:
        pass
      
register_message_handler(antiban_cap)#hand_antiban_start
register_command_handler(antiban_msg, '!а', ['все'], 40, 'см. помощь антибан.Кидает при активации антибана сообщение в чат', '!а <текст>', ['!а соскучились?'])
register_stage0_init(antiban_load)
register_command_handler(hand_anon_start, 'антибан', ['все'], 40, 'Если вас забанили, вы можете зайти в чат через бота, где бот будет выступать в роле траспорта.Писать в чат через !а в начале.', 'антибан <чат>', ['антибан cool@conference.talkonaut.com'])

