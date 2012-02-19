#===istalismanplugin===
# -*- coding: utf-8 -*-

#plugin from http://jabbrik.ru

AMSGCONF = {}

def handler_amsg(type, source, parameters):
      ADMINFILE = 'static/amsg.txt'
      fp = open(ADMINFILE, 'r')
      txt = eval(fp.read())
      if checkbl(get_true_jid(source[1]+'/'+source[2]).lower()):
            reply(type, source, u'Вы заблокированы по причине: '+checkbl(get_true_jid(source[1]+'/'+source[2]).lower()) )
            return
      if len(txt)>=1:
        if parameters:
          if len(parameters)>150:
            reply(type, source, u'а не много ли ты написал?')
            return
      
          if not AMSGCONF.has_key(get_true_jid(source[1]+'/'+source[2])):
                AMSGCONF[get_true_jid(source[1]+'/'+source[2])] = {'timesend':time.time(), 'count':1}
          else:
                if time.time() - AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] <= 300:
                      reply(type, source, u'Лимит отправки сообщений для админа. Подождите 5 минут')
                      return
                else:
                      AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] = time.time()
                      AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['count'] += 1

          for x in txt:
            msg(x, u'Сообщение для подписчиков от '+source[1]+'/'+source[2]+u' (jid: '+get_true_jid(source[1]+'/'+source[2])+u')\nТекст сообщения: '+parameters)
          reply(type, source, u'Ваше сообщение отправленно.')
        else:
          reply(type, source, u'мессагу написать не забыл?')
      else:
        if not AMSGCONF.has_key(get_true_jid(source[1]+'/'+source[2])):
            AMSGCONF[get_true_jid(source[1]+'/'+source[2])] = {'timesend':time.time(), 'count':1}
        else:
            if time.time() - AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] <= 300:
                  reply(type, source, u'Лимит отправки сообщений для админа. Подождите 5 минут')
                  return
            else:
                  AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['timesend'] = time.time()
                  AMSGCONF[get_true_jid(source[1]+'/'+source[2])]['count'] += 1

        if parameters:
          if len(parameters)>150:
            reply(type, source, u'а не много ли ты написал?')
            return

          for z in ADMINS:
            msg(z, u'Сообщение для администраторов бота (нет подписчиков.) от '+source[1]+'/'+source[2]+u' (jid: '+get_true_jid(source[1]+'/'+source[2])+u')\nТекст сообщения: '+parameters)
          reply(type, source, u'Ваше сообщение отправленно!!')
        else:
          reply(type, source, u'мессагу написать не забыл?')
      
  
        

def amsg_subscribe(type, source, parameters):
    ADMINFILE = 'static/amsg.txt'
    fp = open(ADMINFILE, 'r')
    txt = eval(fp.read())
    if parameters:
      if parameters in txt:
        reply(type, source, u'такой JID в базе уже есть')
        return
      else:
        txt.append(parameters)
        write_file(ADMINFILE,str(txt))
        fp.close()
        reply(type, source, u'JID '+parameters+u' подписан на уведомления')
    else:
      parameters = get_true_jid(source[1]+'/'+source[2])
      fp = open(ADMINFILE, 'r')
      txt = eval(fp.read())
      fp.close()
      if parameters in txt:
        reply(type, source, u'Вы в базе уже есть')
        return
      else:
        txt.append(get_true_jid(source[1]+'/'+source[2]))
        write_file(ADMINFILE,str(txt))
        
        reply(type, source, u'добавил Вас в список подписчиков')
      
def amsg_unsubscribe(type, source, parameters):
      ADMINFILE = 'static/amsg.txt'
      if parameters:
            fp = open(ADMINFILE, 'r')
            txt = eval(fp.read())
            fp.close()
            if parameters in txt:
                  txt.remove(parameters)
            else:
                  reply(type, source, u'ты видишь такой jid в списке подписчиков? я - нет!')
                  return
            write_file(ADMINFILE,str(txt))

            reply(type, source, u'JID '+parameters+u' отписан от уведомлений')
      else:
            parameters = get_true_jid(source[1]+'/'+source[2])
            fp = open(ADMINFILE, 'r')
            txt = eval(fp.read())
            fp.close()
            if parameters in txt:
                  txt.remove(get_true_jid(source[1]+'/'+source[2]))
            else:
                  reply(type, source, u'ты видишь такой себя в списке подписчиков? я - нет!')
                  return
            write_file(ADMINFILE,str(txt))
            reply(type, source, u'удалил Вас из списка подписчиков')
      
def amsg_show(type, source, parameters):
    ADMINFILE = 'static/amsg.txt'
    fp = open(ADMINFILE, 'r')
    txt = eval(fp.read())
    fp.close()
    if len(txt) == 0:
      reply(type, source, u'База подписчиков пуста! Пожайлуста, заполните базу')
      return
    p =1
    spisok = ''
    for usr in txt:
          spisok += str(p)+'. '+usr+'\n'
          p +=1
    reply(type, source, u'Подписчики уведомлений (всего '+str(len(txt))+u'):\n'+spisok)
          
def amsg_clear(type, source, parameters):
    ADMINFILE = 'static/amsg.txt'
    write_file(ADMINFILE,str('[]'))
    reply(type, source, u'очистил список подписчиков')

def amsg_blacklist(type, source, parameters):
      ADMINFILE = 'static/blacklist.txt'
      if not parameters:
            reply(type, source, u'не правильные параметры, прочитайте помощь по команде')
            return
      params = parameters.split(' ', 1)
      if len(params) == 2:

            if params[0] == 'add':
                  fp = open(ADMINFILE, 'r')
                  txt = eval(fp.read())
                  fp.close()
                  a = params[1].split('|', 1)
                  if txt.has_key(a[0].lower()):
                        reply(type, source, u'Данный JID уже есть в черном листе')
                        return
                  else:
                        if len(a) == 1:
                              txt[a[0].lower()] = u'Locked'
                        elif len(a) == 2:
                              txt[a[0].lower()] = a[1]
                              
                        write_file(ADMINFILE, str(txt))
                        reply(type, source, u'JID добавлен в черный лист')

            elif params[0] == 'del':
                  fp = open(ADMINFILE, 'r')
                  txt = eval(fp.read())
                  fp.close()
                  if txt.has_key(params[1].lower() ):
                        del txt[params[1].lower()]
                        write_file(ADMINFILE, str(txt))
                        reply(type, source, u'Удалил JID из черного листа')
                  else:
                        reply(type, source, u'JID отсутствует в черном листе')
            else:
                  reply(type, source, u'Неизвестная команда')
                  return
      elif len(params) == 1:
            if params[0] == 'show':
                  fp = open(ADMINFILE, 'r')
                  txt = eval(fp.read())
                  fp.close()
                  p = 1
                  spisok = ''
                  if len(txt.keys()) == 0:
                        reply(type, source, u'В черном листе пусто')
                        return
                  for usr in txt.keys():
                        spisok += str(p)+'. '+usr+' ('+txt[usr]+')\n'
                        p +=1
                  reply(type, source, u'Список игнор листа (всего '+str(len(txt.keys()))+u'):\n'+spisok)
      else:
            reply(type, source, u'Неизвестная команда')
            return

def checkbl(jid):
      jid = jid.lower()
      ADMINFILE = 'static/blacklist.txt'
      fp = open(ADMINFILE, 'r')
      txt = eval(fp.read())
      fp.close()

      if txt.has_key(jid):
            return txt[jid]
      else:
            return 0
      

register_command_handler(handler_amsg, 'amsg', ['все','amsg'], 0,'Отправляет сообщение всем администраторам бота на jid, указывать от кого сообщение- не надо, бот сам показывает конфу и ник отправителя\nplugin version 1.0 , by ferym','amsg', ['amsg Привет, есть некая проблемка, зайди ко мне'])
register_command_handler(handler_amsg, 'мессага_админу', ['amsg','все'], 0,'Отправляет сообщение всем администраторам бота на jid, указывать от кого сообщение- не надо, бот сам показывает конфу и ник отправителя\nplugin version 1.0 , by ferym','мессага_админу', ['мессага_админу Привет, есть некая проблемка, зайди ко мне'])
register_command_handler(amsg_subscribe, 'amsg_subscribe', ['amsg','все','суперадмин'], 100, 'подписка на уведомления плагина amsg. список джидов которым будут приходить сообщения. Без параметра добавляет ваш джид', 'amsg_subscribe <jid>', ['amsg_subscribe vasya@jabber.ru'])
register_command_handler(amsg_unsubscribe, 'amsg_unsubscribe', ['amsg','все','суперадмин'], 100, 'отпиписать jid от уведомлений плагина amsg. Без параметра удаляет ваш джид', 'amsg_unsubscribe <jid>', ['amsg_unsubscribe vasya@jabber.ru'])
register_command_handler(amsg_show, 'amsg_show', ['amsg','все','суперадмин'], 100, 'Просмотр подписчиков на уведомления', 'amsg_show', ['amsg_show'])
register_command_handler(amsg_clear, 'amsg_clear', ['amsg','все','суперадмин'], 100, 'Очищение списка подписчиков', 'amsg_clear', ['amsg_clear'])
register_command_handler(amsg_blacklist, 'amsg_blacklist', ['amsg','все','суперадмин'], 100, 'заблокировать пользователей (команда amsg будет недоступна)', 'amsg_blacklist <add|del|show>', ['amsg_blacklist add vasya@jabber.ru','amsg_blacklist add vasya@jabber.ru|причина','amsg_blacklist del vasya@jabber.ru','amsg_blacklist show'])
