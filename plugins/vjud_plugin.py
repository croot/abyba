#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman


SR_PS={u'полное_имя':u'fn',u'fn':u'fn',u'организация':u'orgname',u'orgname':u'orgname',u'mail':u'email',u'name':u'first',u'фамилия':u'last',u'city':u'locality',u'дата':u'bday',u'data':u'bday',u'nick':u'nick',u'ник':u'nick',u'мыло':u'email',u'мейл':u'email',u'имя':u'first',u'город':u'locality'}

VJUD={'t':0}

def jud_iq(type,source,parameters):
  if time.time()-VJUD['t']<60:
    reply(type,source,u'подождите минуту,на эту команду установлен лимит.')
    return
  else:
    VJUD['t']=time.time()
  k1=''
  k2=''
  p1=''
  p2=''
  if not parameters:
    reply(type,source,u'кого?')
    return
  if len(parameters)>150:
    reply(type,source,u'а не слишком много написал?')
    return
  if not parameters.count(' '):
    k1='nick'
    p1=parameters
  else:
    s=parameters.split()
    if parameters.count(' ')==1:
      k1=s[0]
      p1=s[1]
    else:
      if parameters.count(' ')==3:
        k1=s[0]
        p1=s[1]
        k2=s[2]
        p2=s[3]
  if not k1 in globals()['SR_PS']:
    reply(type,source,u'ключ <'+k1+u'> не найден.Доступны - nick, name, city, data')
    return
  if p1.isspace():
    reply(type,source,u'введите параметер поиска')
    return
  iq = xmpp.Iq('set')
  global JID
  try:
    iq.setTo('vjud.'+CONNECT_SERVER)
  except:
    iq.setTo('jud.jabber.ru')
  iq.setID('src'+str(random.randrange(1000, 9999)))
  query = xmpp.Node('query')
  query.setNamespace('jabber:iq:search')
  x = xmpp.Node('x',{'type':'submit'})
  x.setNamespace(xmpp.NS_DATA)
  inv=x.addChild('field', {'var':SR_PS[k1]})
  inv.setTagData('value', p1)
  if k2!='':
    if k2 in globals()['SR_PS']:
      cap=x.addChild('field', {'var':SR_PS[k2]})
      cap.setTagData('value', p2)
    else:
      reply(type,source,u'второй ключ <'+k2+u'> не найден,идет поиск по значению первого.')
  query.addChild(node=x)
  iq.addChild(node=query)
  JCON.SendAndCallForResponse(iq, jud_get, {'type': type, 'source': source})

def jud_get(coze, res, type, source):
        if res:
                if res.getType() == 'result':
                        try:
                                s=res.getChildren()[0].getChildren()
                                z=''
                                n=0
                                for x in s:
                                        o=''
                                        m=x.getChildren()
                                        for i in m:
                                                k=''
                                                f=i.getChildren()
                                                for d in f:
                                                        j=d.getCDATA()
                                                        if j!='':
                                                                k+=j+' '
                                                if len(k)>7:
                                                        n+=1
                                                        o+='\n'+unicode(n)+' ) '+k
                                if o=='':
                                        reply(type,source,'no found')
                                        return
                                reply(type,source,u'Результаты поиска в vjud.'+CONNECT_SERVER+':\n'+o)
                        except:
                                pass
                if res.getType() == 'error':
                        reply(type,source,u'сервер '+CONNECT_SERVER+u' не поддерживает поиск')

        
register_command_handler(jud_iq, 'vjud', ['все','мод','инфо'], 0, 'Поиск пользователя по анкетным данным в jud.jabber.ru Доступен поиск по следующим ключам: nick|ник, name|имя, фамилия, city|город, мейл|мыло|mail, data|дата, fn|полное_имя, orgname|организация.Без ключа будет искать по-нику.Поиск по-совпадению-дописываем *', 'vjud <ключ> <текст>', ['vjud 40t*','vjud 40tman','vjud mail 40tman@mail.ru','vjud name Andrej city Kiev'])
register_command_handler(jud_iq, '!контакт', ['все','мод','инфо'], 0, 'Поиск пользователя по анкетным данным в jud.jabber.ru Доступен поиск по следующим ключам: nick|ник, name|имя, фамилия, city|город, мейл|мыло|mail, data|дата, fn|полное_имя, orgname|организация.Без ключа будет искать по-нику.Поиск по-совпадению-дописываем *', '!контакт <ключ> <текст>', ['!контакт 40t*','!контакт 40tman','!контакт мейл 40tman@mail.ru','!контакт имя Андрей город Киев'])

