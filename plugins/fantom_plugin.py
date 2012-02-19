#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman
import os, xmpp, time, sys, time, pdb, urllib, threading, types, random


FANTOM={'user':{},'nick':[], 'serv':[], 'w':0}


def fantom_hnd_join(cl,groupchat):
  nick = random.choice(FANTOM['nick'])
  prs = xmpp.protocol.Presence(groupchat+'/'+nick)
  prs.setTag('x', namespace=xmpp.NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
  try:
    cl.send(prs)
  except:
    pass

	
def generate_fantom(_len = None, sg = None):
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

		      
def handler_fantom_start(type,source,parameters):
  if not parameters:
    return
  if parameters.count(' '):
    return
  if not parameters.count('@') and not parameters.count('.'):
    reply(type, source, u'введите адрес конференции!')
    return
  if not FANTOM['serv']:
    reply(type, source, u'список серверов из файла dynamic/spamserv.txt не был загружен!')
    return
  reply(type,source,u'ok')
  FANTOM['w']=1
  for x in range(0, 20):
    threading.Thread(None, handler_fantom_auth, 'fantom_auth'+str(random.randrange(0, 999)), (type,source,parameters)).start()
    time.sleep(20)
    

def fantom_proc(cl,psw):
  while cl.isConnected() and FANTOM['w']:
    try:
      cl.Process(1)
    except:
      pass
           
def handler_fantom_auth(type,source,conf):
  print 'ok'
  try:
    new=1
    name = generate_fantom(random.Random().randint(6,11))
    gserv = random.choice(FANTOM['serv'])
    domain=gserv
    password=generate_fantom(random.Random().randint(6,11))
    mainRes=generate_fantom(random.Random().randint(4,5))
    if FANTOM['user']:
      new=0
      N=[]
      for x in FANTOM['user']:
        N.append(x)
      rd=random.choice(N)
      pr=rd.split(':')
      s=pr[0].split('@')
      domain=s[1]
      name=s[0]
      password=pr[1]
    print u'START'
    node = unicode(name)
    jid = xmpp.protocol.JID(node=node, domain=domain, resource=mainRes)
    print u'bot jid: '+unicode(jid)
    cl = xmpp.Client(jid.getDomain(), debug=[])
    con = cl.connect()
    if not con:
      if FANTOM['user']:
        if name+'@'+domain+':'+password in FANTOM['user']:
          del FANTOM['user'][name+'@'+domain+':'+password]
      threading.Thread(None, handler_fantom_auth, 'fantom_auth'+str(random.randrange(0, 999)), (type,source,conf)).start()
      return
    cl.RegisterHandler('presence',fantom_prs)
    print u'Connected'
    if new:
      try:
        xmpp.features.register(cl, domain, {'username': node, 'password':password})
      except AttributeError:
        pass
      print u'Registered'
    au=cl.auth(jid.getNode(), password, jid.getResource())
    if not au:
      if FANTOM['user']:
        if name+'@'+domain+':'+password in FANTOM['user']:
          del FANTOM['user'][name+'@'+domain+':'+password]
      print 'Auth error'
      threading.Thread(None, handler_fantom_auth, 'fantom_auth'+str(random.randrange(0, 999)), (type,source,conf)).start()
      return
    print u'Autheticated'
    if new:
      try:
        txt=eval(read_file('dynamic/user.txt'))
        txt[name+'@'+domain+':'+password]={}
        write_file('dynamic/user.txt', str(txt))
        FANTOM['user'][name+'@'+domain+':'+password]={}
      except:
        pass
    cl.sendInitPresence()
    psw=''
    threading.Thread(None, fantom_proc, 'fantom_process'+str(random.randrange(0, 999)), (cl,psw)).start()
    fantom_hnd_join(cl, conf)
  except:
    raise
    print 'error in fantom_auth'
    pass

def fantom_prs(cl,mess):
  try:
    fromjid = mess.getFrom()
    groupchat = fromjid.getStripped()
    nick = fromjid.getResource()
    ptype = mess.getType()
    if ptype == 'error':
      print 'get error presence'
      ecode = mess.getErrorCode()
      if ecode==u'409':
        fantom_hnd_join(cl,groupchat)
        

  except:
    pass

def handler_fantom_stop(type,source,parameters):
  if FANTOM['w']:
    FANTOM['w']=0
    reply(type,source,u'остановлено!')
  else:
    reply(type,source,u'не активно!')

def fantom_load():
  try:
    nick='dynamic/nick.txt'
    txt=eval(read_file(nick))
    for x in txt.keys():
      FANTOM['nick'].append(x)
    user='dynamic/user.txt'
    if not os.path.exists(user):
      fp=open(user, 'w')
      fp.write('{}')
      fp.close()
    txt=eval(read_file(user))
    for x in txt:
      FANTOM['user'][x]={}
    serv='dynamic/spamserv.txt'
    txt=eval(read_file(serv))
    for x in txt:
      FANTOM['serv'].append(x)
  except:
    print u'Error in fantom_plugin.py!!! you may check file dynamic/nick.txt, spamserv.txt to normal work'
        
register_stage0_init(fantom_load)
register_command_handler(handler_fantom_stop, 'фантом_стоп', ['отакэ','все'], 40, 'выключает обработчик фантомных ботов', 'фантом_стоп', ['фантом_стоп'])
register_command_handler(handler_fantom_start, 'фантом', ['отакэ','все'], 40, 'заводит 20 фантомных юзеров в конференцию, с интервалом 20с.Мук Фильтры если они есть должны быть выключены,а сервера разбанены.', 'фантом <конфа>', ['фантом cool@conference.jabber.ru'])
