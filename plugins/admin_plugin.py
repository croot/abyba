#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  admin_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import shutil, os
        

def popups_check(gch):
	DBPATH='dynamic/'+gch+'/config.cfg'
	if GCHCFGS[gch].has_key('popups'):
		if GCHCFGS[gch]['popups'] == 1:
			return 1
		else:
			return 0
	else:
		GCHCFGS[gch]['popups']=1
		write_file(DBPATH,str(GCHCFGS[gch]))
		return 1

ROM_DEL = {}

def handler_admin_check(type, source, parameters):
        reply(type, source, 'ok')
        d=os.listdir('dynamic')
        n=0
        rep=''
        SP=[]
        jid=get_true_jid(source[1]+'/'+source[2])
        for x in d:
                if x.count('.')>1:
                        for a in x:
                                if ord(a) in range(65, 90) or ord(a) in range(128, 159):
                                        SP.append('dynamic/'+x)
                                        n+=1
                                        rep+=str(n)+') '+x+u'(Верхний регистр)\n'
        for c in GROUPCHATS.keys():
                if len(GROUPCHATS[c])==0:
                        del GROUPCHATS[c]
                        if os.path.exists('dynamic/'+c):
                                SP.append('dynamic/'+c)
                                n+=1
                                rep+=str(n)+') '+c+u'(Бот не смог зайти в конференцию)\n'
        if rep:
                reply(type, source, rep+u'\nВы хотите удалить файлы конфигурации этих комнат?(Да!)')
        else:
                reply(type, source, u'all it\'s good!')
        ROM_DEL[jid]=SP
        time.sleep(35)
        if jid in ROM_DEL:
                del ROM_DEL[jid]

def h_message_delete(raw, type, source, parameters):
        jid=get_true_jid(source[1]+'/'+source[2])
        if jid in ROM_DEL:
                if parameters==u'Да!':
                        reply(type, source, u'ok')
                        for x in ROM_DEL[jid]:
                                try:
                                        shutil.rmtree(x)
                                except:
                                        pass
                        reply(type, source, 'done!')

register_message_handler(h_message_delete)
				
def handler_admin_join(type, source, data):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if data:
                if not isinstance(data, unicode):
                        reply(type, source, u'Адрес чата должен быть в Unicode!')
                        return
                parameters=data.lower()
		passw=''
		args = parameters.split()
		if not args[0].count('@') or not args[0].count('.')>=1:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
		if len(args)>1:
			groupchat = args[0]
			passw = string.split(args[1], 'pass=', 1)
			if not passw[0]:
				reason = ' '.join(args[2:])
			else:
				reason = ' '.join(args[1:])
		else:
			groupchat = parameters
			reason = ''
		try:
                        os.path.exists(groupchat)
                except:
                        reply(type, source, u'Ошибка при создании конфигурации комнаты!')
                        return
		get_gch_cfg(groupchat)
		for process in STAGE1_INIT:
			with smph:
				INFO['thr'] += 1
				threading.Thread(None,process,'atjoin_init'+str(INFO['thr']),(groupchat,)).start()
		DBPATH='dynamic/'+groupchat+'/config.cfg'
		write_file(DBPATH, str(GCHCFGS[groupchat]))
		if passw:
			join_groupchat_and_get_reason(type,source,groupchat, DEFAULT_NICK)
		else:
			join_groupchat_and_get_reason(type,source,groupchat, DEFAULT_NICK, passw)
		if popups_check(groupchat):
                        pass
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')

GET_JOIN_REAS=[]

def join_groupchat_and_get_reason(type=None, source=None, groupchat=None, nick=DEFAULT_NICK, passw=None):
	if not groupchat in GROUPCHATS:
		GROUPCHATS[groupchat] = {}
	global GET_JOIN_REAS
	if check_file(groupchat,'macros.txt'):
		pass
	else:
		print 'IO error when creating macros.txt for ',groupchat
	chat=groupchat
	add_gch(groupchat, nick, passw)
	prs=xmpp.protocol.Presence(groupchat+'/'+nick)
	try:
                prs.setStatus(GCHCFGS[groupchat]['status']['status'])
                prs.setShow(GCHCFGS[groupchat]['status']['show'])
        except:
                pass
        pres=prs.setTag('x',namespace=xmpp.NS_MUC)
	pres.addChild('history',{'maxchars':'0'})
	if passw:
		pres.setTagData('password', passw)
	if not groupchat in GET_JOIN_REAS:
                GET_JOIN_REAS.append(groupchat)
	JCON.SendAndCallForResponse(prs, join_get_reason,{'chat':chat,'type':type,'source':source})

def join_get_reason(coze, res, chat, type, source):
        if res:
                try:
                        fromjid=res.getFrom()
                        nick=fromjid.getResource()
                        if chat in GET_JOIN_REAS:
                                try:
                                        GET_JOIN_REAS.remove(chat)
                                except:
                                        globals()['GET_JOIN_REAS']=[]
                        else:
                                return
                        r=res.getType()
                        if r=='error':
                                c=res.getErrorCode()
                                reply(type,source,u'Бот не смог зайти в '+chat+u', код ошибки '+c)
                                if c=='409':
                                        join_groupchat(chat, nick+'_')
                                return
                        jid=res.getFrom()
                        to=res.getTo()
                        reply(type, source, u'зашел с ником '+get_bot_nick(chat))
                        return
                except:
                        pass
        
def handler_admin_leave(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	args = parameters.split()
	if len(args)>1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'недостаточно прав')
			return
		reason = ' '.join(args[1:]).strip()
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'меня там нет')
			return
		groupchat = args[0]
	elif len(args)==1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'недостаточно прав')
			return
		rm=parameters.lower()
		rm=rm.strip()
		if parameters.count(' '):
                        rm=args[0]
		if not GROUPCHATS.has_key(rm):
			reply(type, source, u'меня там нет')
                        return
		reason = ''
		groupchat = args[0]
	else:
		if not source[1] in GROUPCHATS:
			reply(type, source, u'это возможно только в конференции')
			return
		groupchat = source[1]
		reason = ''
	if popups_check(groupchat):
                reply(type,source,'ok')
		#if reason:
			#msg(groupchat, u'меня уводит '+source[2]+u' по причине:\n'+reason)
		#else:
			#msg(groupchat, u'меня уводит '+source[2])
	if reason:
		leave_groupchat(groupchat, u'меня уводит '+source[2]+u' по причине:\n'+reason)
	else:
		leave_groupchat(groupchat,u'меня уводит '+source[2])


def handler_admin_msg(type, source, parameters):
	if not parameters:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
		return
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	reply(type, source, u'сообщение ушло')
	
def handler_glob_msg_help(type, source, parameters):
	total = '0'
	totalblock='0'
	nick=u'Admin'
	if source[1] in GROUPCHATS:
                nick=source[2]
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
		for x in gch:
			if popups_check(x):
				msg(x, u'Новости от '+nick+u':\n'+parameters+u'\nНапоминаю, что как всегда все помощь можно получить написав "помощь".\nО всех глюках, ошибках, ляпях, а также предложения и конструктивную критику прошу направлять мне таким образом: пишем "передать botadmin и тут ваше сообщение", естественно без кавычек.\nСПАСИБО ЗА ВНИМАНИЕ!')
				totalblock = int(totalblock) + 1
			total = int(total) + 1
		reply(type, source, 'сообщение ушло в '+str(totalblock)+' конференций (из '+str(total)+')')
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
		
def handler_glob_msg(type, source, parameters):
	total = '0'
	totalblock='0'
	nick=u'Admin'
	if source[1] in GROUPCHATS:
                nick=source[2]
	if parameters:
		if GROUPCHATS:
			gch=GROUPCHATS.keys()
			for x in gch:
				if popups_check(x):
					msg(x, u'Новости от '+nick+':\n'+parameters)
					totalblock = int(totalblock) + 1
				total = int(total) + 1
			reply(type, source, 'сообщение ушло в '+str(totalblock)+' конференций (из '+str(total)+')')
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
	

def handler_admin_say(type, source, parameters):
	if parameters:
		args=parameters.split()[0]
		msg(source[1], parameters)
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')

def handler_admin_restart(type, source, parameters):
        nick=u'Admin'
        if source[1] in GROUPCHATS:
                nick=source[2]
        prs=xmpp.Presence(typ='unavailable')
	prs.setStatus(nick+u': рестарт')
	JCON.send(prs)
	time.sleep(1)
	JCON.disconnect()

def handler_admin_exit(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
	gch=[]
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня выключает '+source[2]+u' по причине:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня выключает '+source[2])
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': выключаюсь -> '+reason)
	else:
		prs.setStatus(source[2]+u': выключаюсь')
	JCON.send(prs)
	time.sleep(2)
	os.abort()
	
def handler_popups_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'ошибочный запрос. прочитай помощь по использованию команды')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['popups']=1
			reply(type,source,u'глобальные оповещения включены')
		else:
			GCHCFGS[source[1]]['popups']=0
			reply(type,source,u'глобальные оповещения выключены')
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['popups']
		if ison==1:
			reply(type,source,u'здесь глобальные оповещения включены')
		else:
			reply(type,source,u'здесь глобальные оповещения выключены')
	
	
def handler_changebotstatus(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
	if parameters:
		args,show,status=parameters.split(' ',1),'',''
		if args[0] in ['away','xa','dnd','chat']:
			show=args[0]
		else:
			show=None
			status=parameters
		if not status:
			try:
				status=args[1]
			except:
				status=None
		try:
                        file='dynamic/'+source[1]+'/config.cfg'
                        fp=open(file,'r')
                        txt=eval(fp.read())
                        txt['status']={'status':status,'show':show}
                        write_file(file, str(txt))
                except:
                        pass
                change_bot_status(source[1],status,show,0)
		GCHCFGS[source[1]]['status']={'status': status, 'show': show}
		
	else:
		stmsg=GROUPCHATS[source[1]][get_bot_nick(source[1])]['stmsg']
		status=GROUPCHATS[source[1]][get_bot_nick(source[1])]['status']
		if stmsg:
			reply(type,source, u'я сейчас '+status+u' ('+stmsg+u')')
		else:
			reply(type,source, u'я сейчас '+status)
			
def get_autoaway_state(gch):
        return None
		
def set_default_gch_status(gch):
	try:
                if isinstance(GCHCFGS[gch].get('status'), str):
                        GCHCFGS[gch]['status']={'status': u'I am online', 'show': u'chat'}
                elif not isinstance(GCHCFGS[gch].get('status'), dict):
                        GCHCFGS[gch]['status']={'status': u'I am online', 'show': u'chat'}
        except:
                pass

def hnd_down_room(type,source,parameters):
        try:
                req = urllib2.Request(parameters.encode('utf-8'))
                req.add_header = ('User-agent', 'Mozilla/5.0')
                r = urllib2.urlopen(req)
                t = r.readlines()
                for x in t:
                        try:
                                x=x.decode('utf-8','replace')
                        except:
                                x=unicode(x)
                        if x.count(' '):
                                chat=x.split()[0]
                                nick=x.split()[1]
                                handler_admin_join(type, source, chat)
                                try:
                                        handler_botnick(type,[chat+'/'+source[2],chat,source[2]],nick)
                                except:
                                        pass
        except:
                reply(type,source,u'ошибка')

CMD_REPL={u' ':u' ',u'q':u'й',u'w':u'ц',u'e':u'у',u'r':u'к',u't':u'е',u'y':u'н',u'u':u'г',u'i':u'ш',u'o':u'щ',u'p':u'з',u'[':u'х',u']':u'ъ',u'a':u'ф',u's':u'ы',u'd':u'в',u'f':u'а',u'g':u'п',u'h':u'р',u'j':u'о',u'k':u'л',u'l':u'д',u';':u'ж',u'\'':u'э',u'z':u'я',u'x':u'ч',u'c':u'с',u'v':u'м',u'b':u'и',u'n':u'т',u'm':u'ь',u',':u'б',u'.':u'ю'}


def data_cmd_replace(data):
        global CMD_REPL
        rep=''
        for x in data:
                if x in CMD_REPL.keys():
                        rep+=CMD_REPL[x]
                else:
                        rep+=x
        return rep
                        
def cmd_repl(raw, type, source, parameters):
        try:
                if not parameters:
                        return
                if len(parameters)>50:
                        return
                parameters = parameters.lower()
                if parameters in COMMANDS.keys():
                        return
                if parameters.count(' '):
                        cmd=parameters.split()[0]
                        if cmd in COMMANDS.keys():
                                return
                if source[1] in GROUPCHATS:
                        if source[2]==get_bot_nick(source[1]):
                                return
                if source[2] and source[2]!=None:
                        cmd=data_cmd_replace(source[2])
                        if source[2].count(' '):
                                cmd=source[2].split()[0]
                                cmd=data_cmd_replace(cmd)
                        if cmd in COMMANDS.keys():
                                return
                rep=''
                c=''
                rep=data_cmd_replace(parameters)
                if not rep or rep.isspace():
                        return
                command=rep
                if rep.count(' '):
                        s=rep.split()
                        command=s[0]
                        c=' '.join(s[1:])
                if command in COMMANDS:
                        if source[1] in COMMOFF and command in COMMOFF[source[1]]:
                                return
                        else:
                                reply(type, source, u'Команду распознано как:\n'+rep)
                                call_command_handlers(command, type, source, unicode(c), command)
                                INFO['cmd'] += 1
                                LAST['t'] = time.time()
                                LAST['c'] = command

        except:
                pass

def join_check_own(groupchat, nick, a, b):
        if a==u'owner' and nick==get_bot_nick(groupchat):
                #for x in ADMINS:
                #        msg(x, u'Внимание,зашел как овнер в '+groupchat+u',навсякий делаю ее постоянной!')
                iq = xmpp.Iq('set')
                iq.setTo(groupchat)
                query = xmpp.Node('query')
                query.setNamespace('http://jabber.org/protocol/muc#owner')
                x = xmpp.Node('x',{'type':'submit'})
                x.setNamespace(xmpp.NS_DATA)
                inv=x.addChild('field', {'var':"FORM_TYPE"})
                inv.setTagData('value', xmpp.NS_MUC_ROOMCONFIG)
                cap=x.addChild('field', {'var':"muc#roomconfig_persistentroom"})
                cap.setTagData('value', "1")
                query.addChild(node=x)
                iq.addChild(node=query)
                JCON.send(iq)

register_join_handler(join_check_own)
register_message_handler(cmd_repl)
register_command_handler(handler_admin_check, '!проверка', ['суперадмин','мук','все'], 100, 'Проверка конференций', '!проверка', ['!проверка'])
register_command_handler(hnd_down_room, '!восстановить', ['суперадмин','мук','все'], 100, 'Использует url текстового файла для захода в конфы.Пример файла\n12345@conference.jabber.ru Талисман\nanyroom@conference.jabber.ru Талисман', '!восстановить <url>', ['!восстановить http://talisman.wen.ru/room.txt'])
register_command_handler(handler_admin_join, 'зайти', ['суперадмин','мук','все'], 40, 'Зайти в определённую конференцию. Если она запаролена то пишите пароль сразу после её названия.', 'зайти <конференция> [pass=пароль] [причина]', ['зайти z@conference.jabber.aq', 'зайти z@conference.jabber.aq test', 'зайти z@conference.jabber.aq pass=1234 test'])
register_command_handler(handler_admin_leave, 'свал', ['админ','мук','все'], 20, 'Заставляет выйти из текущей или определённой конференции.', 'свал <конференция> [причина]', ['свал z@conference.jabber.aq спать', 'свал спать','свал'])
register_command_handler(handler_admin_msg, 'мессага', ['админ','мук','все'], 40, 'Отправляет сообщение от имени бота на определённый JID.', 'мессага <jid> <сообщение>', ['мессага guy@jabber.aq здорово чувак!'])
register_command_handler(handler_admin_say, 'сказать', ['админ','мук','все'], 20, 'Говорить через бота в конференции.', 'сказать <сообщение>', ['сказать салют пиплы'])
register_command_handler(handler_admin_restart, 'рестарт', ['суперадмин','все'], 100, 'Перезапускает бота.', 'рестарт [причина]', ['рестарт','рестарт ы!'])
register_command_handler(handler_admin_exit, 'пшёл', ['суперадмин','все'], 100, 'Остановка и полный выход бота.', 'пшёл [причина]', ['пшёл','пшёл глюки'])
register_command_handler(handler_glob_msg, 'globmsg', ['суперадмин','мук','все'], 100, 'Разослать сообщение (новостное) по всем конференциям, в которых сидит бот.', 'globmsg [сообщение]', ['globmsg всем привет!'])
register_command_handler(handler_glob_msg_help, 'hglobmsg', ['суперадмин','мук','все'], 100, 'Разослать сообщение (новостное) по всем конфам, в которых сидит бот. Сообщение будет содержать в себе предустановленный заголовок с короткой справкой об испольовании бота.', 'hglobmsg [сообщение]', ['hglobmsg всем привет!'])
register_command_handler(handler_changebotstatus, 'ботстатус', ['админ','мук','все'], 20, 'Меняет статус бота на указанный из списка:\naway - отсутствую,\nxa - давно отсутствую,\ndnd - не беспокоить,\nchat - хочу чатиться,\nа также статусное сообщение (если оно даётся).', 'stch [статус] [сообщение]', ['stch away','stch away я сдох'])

register_stage1_init(get_autoaway_state)
register_stage1_init(set_default_gch_status)
