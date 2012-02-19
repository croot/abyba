#===istalismanplugin===
# -*- coding: utf-8 -*-

# by 40tman
import os, xmpp, time, sys, time, pdb, urllib, threading, types, random

LAST_REG_JID={}

JID_REG_TIME={}

def generate_reg(_len = None, sg = None):
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

  
def hnd_gonew_jid(type,source,parameters):
  l = parameters.lower()
  s= parameters.split()
  jid=get_true_jid(source[1]+'/'+source[2])
  if jid in JID_REG_TIME and int(user_level(source[1]+'/'+source[2],source[1]))<40:
    if time.time() - JID_REG_TIME[jid]['time']<60:
      reply(type,source,u'Вы исчерпали лимит команды. Подождите 60 секунд!')
      return
    else:
      JID_REG_TIME[jid]['time']=time.time()
  if not jid in JID_REG_TIME:
    JID_REG_TIME[jid]={'time':time.time()}
  if not parameters:
    reply(type,source,u'и?')
    return
  if len(parameters)>50:
    reply(type,source,u'букав много!')
    return
  if not l.count(u'@')>0:
    reply(type,source,u'жид должен быть вида login@server..')
    return
  if not l.count(u'.')>0:
    reply(type,source,u'неверно введено имя сервера')
    return
  aka=l.split('@')
  dom=aka[1].split()[0]
  LAST_REG_JID[source[1]+'/'+source[2]]={}
  pas = generate_reg(random.Random().randint(5,10))
  if l.count(' ')>0:
    pas = s[1]
  if type=='public':
    reply(type, source,u'Смотри в привате!')
  reply('private',source,u'Регистрируем новый JID:\nлогин: '+aka[0]+u'\nсервер: '+dom+u'\nпароль: '+pas)
  name, domain, password, newBotJid, mainRes = aka[0], dom, pas, 0,'QIP'
  print u'Regjid:START'
  node = name
  jid = xmpp.JID(node=node, domain=domain, resource=mainRes)
  cl = xmpp.Client(jid.getDomain(), debug=[])
  con = cl.connect()
  if not con:
    reply(type,source,u'немогу подключиться к '+dom)
    return
  cl.RegisterHandler('message', hnd_newreg_Hnd)
  try:
    #iq=xmpp.Iq('get',xmpp.NS_REGISTER,to=domain)
    #resp=cl.SendAndWaitForResponse(iq)
    #if xmpp.isResultNode(resp):
    #  print unicode(resp)
    #  reply(type, source, resp.getTagData('instructions'))
    #  return
    info, au = {'username': node, 'password':password}, 0
    iq=xmpp.Iq('set',xmpp.NS_REGISTER,to=domain)
    for i in info.keys(): iq.setTag('query').setTagData(i,info[i])
    resp=cl.SendAndWaitForResponse(iq)
    if xmpp.isResultNode(resp):
      au=1
    else:
      code=resp.getErrorCode()
      dict={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
      if code in dict.keys():
        reply(type, source, u'Ошибка при регистрации:\n'+code+' - '+dict[code])
        return
    #xmpp.features.register(cl, domain, {'username': node, 'password':password})
    print u'Regjid:Registered'
  except:
    reply(type,source,u'немогу зарегиться '+unicode(JCON.lastErr)+', '+unicode(JCON.lastErrCode))
  try:
    au=cl.auth(jid.getNode(), password, jid.getResource())
    if not au:
      reply(type,source,u'Ошибка при регистрации!')
      return
  except UnicodeEncodeError:
    reply(type,source,u'русский пока не поддерживаеться плагином!')
    return
  cl.sendInitPresence()
  reply(type,source,u'зайрегился как '+node+'@'+domain+u'\n password: '+password)
  #threading.Thread(None, hnd_regs_timer, 'reg_new_jid_timer'+str(random.randrange(0, 999)), (type, source)).start()
  tim=time.time()
  while time.time()-tim<3:
    cl.Process(1)
  print 'Regjid:unavibile'
  try:
    cl.disconnect()
  except:
    return

#def hnd_regs_timer(cl):
#  time.sleep(10)
#  try:
#    cl.disconnect()
#  except:
#    return
  
    
def hnd_newreg_Hnd(cl,mess):
  print 'Regjid:new message!'
  try:
    body=mess.getBody()
    if LAST_REG_JID:
      for x in LAST_REG_JID:
        msg(x,body[:450])
        del LAST_REG_JID[x]
  except (RuntimeError,IOError,AttributeError):
    pass
        
    
  
register_command_handler(hnd_gonew_jid, 'регжид', ['все'], 10, 'регистрирует жид,если указать только жид,пароль сгенерирует сам бот( 5-10 символов)', 'регжид <name@server> <password>', ['регжид 40tman@jabber.perm.ru 12345','регжид 40tman@jabber.perm.ru'])
