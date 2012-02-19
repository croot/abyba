#===istalismanplugin===
# -*- coding: utf-8 -*-

# author ferym@jabbim.org.ru
# web sites - http://jabbrik.ru , http://veganet.org
# plugin version 1.5-testing

import os

def handler_note_add(type, source, parameters):
    if check_file('notepad','notepad.txt'):
      files = 'dynamic/notepad/notepad.txt'
      fp = open(files, 'r')
      note = eval(fp.read())
      fp.close()
      if parameters:
        if note.has_key(get_true_jid(source[1]+'/'+source[2])):
            if os.path.isfile('dynamic/notepad/limit.cfg'):
              lf = 'dynamic/notepad/limit.cfg'
              lr = open(lf, 'r')
              limit = eval(lr.read())
              lr.close()
              if len(note[get_true_jid(source[1]+'/'+source[2])])>=limit:
                if limit==0:
                  reply(type, source, u'Запись в блокнот временна отключена администратором бота')
                  return
                reply(type, source, u'Максимальное число хранимых записей - '+str(limit))
              else:
                dates = time.strftime('%H:%M:%S %d.%m.%y\n')
                note[get_true_jid(source[1]+'/'+source[2])].append(dates+parameters)
                write_file(files, str(note))
                reply(type, source, u'Записал')
            else:
              lf = 'dynamic/notepad/limit.cfg'
              write_file(lf, str(25))
              lr = open(lf, 'r')
              limit = eval(lr.read())
              lr.close()
              if len(note[get_true_jid(source[1]+'/'+source[2])])>=limit:
                if limit==0:
                  reply(type, source, u'Запись в блокнот временна отключена администратором бота')
                  return
                reply(type, source, u'Максимальное число хранимых записей - '+str(limit))
              else:
                dates = time.strftime('%H:%M:%S %d.%m.%y\n')
                note[get_true_jid(source[1]+'/'+source[2])].append(dates+parameters)
                write_file(files, str(note))
                reply(type, source, u'Записал')
        else:
          if os.path.isfile('dynamic/notepad/limit.cfg'):
            lf = 'dynamic/notepad/limit.cfg'
            lr = open(lf, 'r')
            limit = eval(lr.read())
            lr.close()
            note[get_true_jid(source[1]+'/'+source[2])] = []
            dates = time.strftime('%H:%M:%S %d.%m.%y\n')
            if limit==0:
              reply(type, source, u'Запись в блокнот временна отключена администратором бота')
              return
            note[get_true_jid(source[1]+'/'+source[2])].append(dates+parameters)
            write_file(files, str(note))
            reply(type, source, u'Записал')
          else:
            lf = 'dynamic/notepad/limit.cfg'
            write_file(lf, str(25))
            note[get_true_jid(source[1]+'/'+source[2])] = []
            dates = time.strftime('%H:%M:%S %d.%m.%y\n')
            note[get_true_jid(source[1]+'/'+source[2])].append(dates+parameters)
            write_file(files, str(note))
            reply(type, source, u'Записал')
      else:
        reply(type, source, u'Что записать то?')
    else:
      reply(type, source, u'Ошибка в базе notepad!\nСрочно сообщите админу бота')
      
def handler_note_del(type, source, parameters):
  if check_file('notepad','notepad.txt'):
    files = 'dynamic/notepad/notepad.txt'
    fp = open(files, 'r')
    note = eval(fp.read())
    fp.close()
    if not parameters:
      reply(type, source, u'Не нахожу твоих записей')
      return
    if note.has_key(get_true_jid(source[1]+'/'+source[2])):
      try:
        parameters = int(parameters) - int(1)
        del note[get_true_jid(source[1]+'/'+source[2])][parameters]
        write_file(files, str(note))
        reply(type, source, u'Удалил')
      except:
        reply(type, source, u'Не получилось')
    else:
      reply(type, source, u'Не нахожу твоих записей')
  else:
    reply(type, source, u'База notepad не создана. Сообщите админу бота')
    
def handler_note_show(type, source, parameters):
      if check_file('notepad','notepad.txt'):
        files = 'dynamic/notepad/notepad.txt'
        fp = open(files, 'r')
        note = eval(fp.read())
        fp.close()
        if not parameters:
          if note.has_key(get_true_jid(source[1]+'/'+source[2])):
            rep = ''
            for a, b in enumerate(note[get_true_jid(source[1]+'/'+source[2])]):
              rep+=str(a+1)+') '+b+'\n'
            if str(note[get_true_jid(source[1]+'/'+source[2])]) == '[]':
              reply(type, source, u'Не нахожу твоих записей')
              return
            reply(type, source, '\n'+rep)
          else:
            reply(type, source, u'Не нахожу твоих записей')
            return
        params = parameters.split(' ', 1)
        if len(params) == 1:
              if params[0]==u'clear':
                if note.has_key(get_true_jid(source[1]+'/'+source[2])):
                  del note[get_true_jid(source[1]+'/'+source[2])]
                  write_file(files, str(note))
                  reply(type, source, u'Очистил список твоих записей')
                else:
                  reply(type, source, u'Не нахожу твоих записей')
              if params[0]==u'limit':
                if os.path.isfile('dynamic/notepad/limit.cfg'):
                  lf = 'dynamic/notepad/limit.cfg'
                  lr = open(lf, 'r')
                  lt = eval(lr.read())
                  lr.close()
                  if str(lt)=='0':
                    reply(type, source, u'Запись в блокнот временна отключена администратором бота')
                    return
                  reply(type, source, u'Установлен лимит записей - '+str(lt))
                else:
                  lf = 'dynamic/notepad/limit.cfg'
                  write_file(lf,str(25))
                  time.sleep(0.1)
                  lr = open(lf, 'r')
                  lt = eval(lr.read())
                  lr.close()
                  reply(type, source, u'Установлен лимит записей - '+str(lt))
        elif len(params) == 2:
            if params[0]==u'limit':
              if user_level(source[1]+'/'+source[2], source[1])==100:
                try:
                  if int(params[1])+int(1):
                    write_file('dynamic/notepad/limit.cfg',str(params[1]))
                    if params[1]==u'0':
                      reply(type, source, u'Запись в блокнот отключена')
                      return
                    reply(type, source, u'Установлен лимит записей - '+str(params[1]))
                except ValueError:
                  reply(type, source, u'Ты где такие цифры видел?')
              else:
                reply(type, source, u'Смена лимита доступна только админам бота')
            else:
              if note.has_key(get_true_jid(source[1]+'/'+source[2])):
                rep = ''
                for a, b in enumerate(note[get_true_jid(source[1]+'/'+source[2])]):
                  rep+=str(a+1)+') '+b+'\n'
                if str(note[get_true_jid(source[1]+'/'+source[2])]) == '[]':
                  reply(type, source, u'Не нахожу твоих записей')
                  return
                reply(type, source, '\n'+rep)
              else:
                reply(type, source, u'Не нахожу твоих записей')
                return
      else:
        reply(type, source, u'База notepad не создана. сообщите админу боту')
        
        
register_command_handler(handler_note_add, 'note+', ['mod','все','фан'], 10, 'Ваш личный блокнотик. Всё введенные вами записи привязываются к вашему JID, доступно в любой конференции где сидит бот.\n#добавляет запись в ваш личный блокнот', 'note+ <что-то>', ['note+ нужно посетить jabbrik.ru\nby ferym'])
register_command_handler(handler_note_del, 'note-', ['mod','все','фан'], 10, 'Ваш личный блокнотик. Всё введенные вами записи привязываются к вашему JID, доступно в любой конференции где сидит бот.\n#Удаляет запись из вашего личного блокнота', 'note- <номер записи>', ['note- 2\nby ferym'])
register_command_handler(handler_note_show, 'note', ['mod','все','фан'], 10, 'Ваш личный блокнотик. Всё введенные вами записи привязываются к вашему JID, доступно в любой конференции где сидит бот.\n#без параметра - Показывает все записи из вашего личного блокнота\nnote clear - очищает весь список ваших записей\nnote limit - просмотр установленного админом лимита на кол-во записей\nnote limit <число> - установка лимита записей, доступно админам бота', 'note\nnote <parameters> <parameters>', ['note\nnote clear\nnote limit\nnote limit 15\nby ferym'])
