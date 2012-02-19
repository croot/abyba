#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  info_plugin.py

#  Initial Copyright © 2007 Als <Als@exploru.net>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

ver_ch=[]

ALL_BOTS=[]

BAN_VER={}

BAN_VER_LAST=0

import threading

def handler_banos(groupchat, nick, aff, role):
        if time.time() - INFO['start'] < 70:	
		return
        if len(nick)>20:
                return
        botnick = get_bot_nick(groupchat)
        if not groupchat in GROUPCHATS:
                return
        if nick == botnick:
                return
        global BAN_VER_LAST
        if not BAN_VER_LAST:
                BAN_VER_LAST=time.time()
        else:
                if time.time()-BAN_VER_LAST<1.1:
                        return
                else:
                        BAN_VER_LAST=time.time()
        if check_file(groupchat,'banver.txt'):
                jid=groupchat+'/'+nick
                iq = xmpp.Iq('get')
                id='vers'+str(random.randrange(1000, 9999))
                globals()['ver_ch'].append(id)
                iq.setID(id)
                iq.addChild('query', {}, [], 'jabber:iq:version');
                jid=groupchat+'/'+nick
                iq.setTo(jid)
                JCON.SendAndCallForResponse(iq, handler_verch_get, {'groupchat': groupchat, 'nick': nick})
                return

def handler_verch_get(coze, res, groupchat, nick):
        mjid = groupchat+'/'+nick
	id=res.getID()
	jid=get_true_jid(groupchat+'/'+nick)
	if id in globals()['ver_ch']:
		globals()['ver_ch'].remove(id)
	else:
		print 'someone is doing wrong...(info_plugin)'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			name = '[no name]'
			version = '[no ver]'
			os = '[no os]'
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'name':
					name = p.getData()
				elif p.getName() == 'version':
					version = p.getData()
				elif p.getName() == 'os':
					os = p.getData()
			if name:
                                if (name == u'Neutron') | (name == u'Юта') | (name == u'PoeBot') | (name == u'GluxiBot') | (name == u'freqbot') | (name == u'Endless Bot [Talisman based "*Less" multicore]') | (name == u'FreQ') | (name == u'ταλιςμαη') | (name == u'Pako bot') | (name == u'Erl-Bot') | (name == u'Isida-Bot'):
                                        change_access_perm_glob(mjid, -10)
                                        if not mjid in ALL_BOTS:
                                                ALL_BOTS.append(mjid)
                                if (name.count(u'ταλιςμαη')>0) | (name.count(u'fatal-bot')>0) | (name.count(u'Black')>0) | (name.count(u'Tali')>0) | (name.count(u'Endless')>0) | (name.count(u'jame')>0) | (name.count(u'Glu')>0):
                                        change_access_perm_glob(mjid, -10)
                                        if not mjid in ALL_BOTS:
                                                ALL_BOTS.append(mjid)
                                if (name.count(u'ταλιςμαη')>0) | (name.count(u'Tali')>0) | (name.count(u'Black')>0) | (name.count(u'Лютик')>0) | (name.count(u'Talizmanko')>0):
                                        try:
                                                if AUTO_PUBLIC_COMOFF=='0':
                                                        return
                                                if not groupchat in BOT_CMD:
                                                        BOT_CMD[groupchat]=[]
                                                        BOT_CMD[groupchat].append(jid)
                                                        prs=xmpp.protocol.Presence(groupchat+'/'+get_bot_nick(groupchat))
                                                        prs.setStatus(u'в вашей комнате уже есть талисман,поэтому мои команды доступны только в привате!')
                                                        prs.setShow('dnd')
                                                        JCON.send(prs)
                                                else:
                                                        BOT_CMD[groupchat].append(jid)
                                                        prs=xmpp.protocol.Presence(groupchat+'/'+get_bot_nick(groupchat))
                                                        prs.setStatus(u'в вашей комнате уже есть талисман,поэтому мои команды доступны только в привате!')
                                                        prs.setShow('dnd')
                                                        JCON.send(prs)
                                        except:
                                                pass
			if version:
                                if os:
                                        if version == u'2.0.x test' or version == u'2.0β':
                                                change_access_perm_glob(mjid, -100)
                                        gfr = version+' '+os
                                        tojid = groupchat+'/'+nick
                                        if not groupchat in BAN_VER:
                                                return
                                        if gfr in BAN_VER[groupchat]:
                                                govn=get_true_jid(groupchat+'/'+nick)
                                                try:
                                                        order_ban(groupchat,nick,u'your Client and OS in banlist')
                                                except:
                                                        pass

def banver_subscribe(type, source, parameters):
        BANVER = 'dynamic/'+source[1]+'/banver.txt'
        juk = eval(read_file(BANVER))
        if parameters:
                if parameters in juk:
                        reply(type, source, u'такая версия в бан-листе уже есть')
                        return
                else:
                        juk[parameters] = {}
                        write_file(BANVER,str(juk))
                        reply(type, source, u'версия '+parameters+u' добавлена в банлист')
                        banver_load(source[1])

def banver_show(type, source, parameters):
    BANVER = 'dynamic/'+source[1]+'/banver.txt'
    juk = eval(read_file(BANVER))
    if len(juk) == 0:
      reply(type, source, u'Список пуст!')
      return
    p =1
    spisok = ''
    for usr in juk:
          spisok += str(p)+'. '+usr+'\n'
          p +=1
    reply(type, source, u'(всего '+str(len(juk))+u'):\n'+spisok)

def banver_unsubscribe(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
        BANVER = 'dynamic/'+source[1]+'/banver.txt'
        if parameters:
                juk = eval(read_file(BANVER))
                if parameters in juk:
                        del juk[parameters]
                        write_file(BANVER,str(juk))
                        banver_load(source[1])
                else:
                        reply(type, source, u'не найдено!')
                        return
                reply(type, source, u'версия '+parameters+u' удалена')

def bot_cmd_remove(groupchat, nick, reason, code):
        try:
                if groupchat in BOT_CMD:
                        jid=get_true_jid(groupchat+'/'+nick)
                        if jid in BOT_CMD[groupchat]:
                                BOT_CMD[groupchat].remove(jid)
        except:
                pass
        
register_join_handler(handler_banos)
register_leave_handler(bot_cmd_remove)
register_command_handler(banver_subscribe, 'banver+', ['админ','мод'], 20, 'добавить версию и ось в банлист', 'banver+ <version><os>', ['banver+ 9032 Windows XP'])
register_command_handler(banver_show, 'banver_show', ['админ','мод'], 20, 'просмотр списка банлиста по версии клиента', 'banver_show', ['banver_show'])
register_command_handler(banver_unsubscribe, 'banver-', ['админ','мод'], 20, 'удалить версию из банлиста', 'banver- <version>', ['banver- 9032 Windows XP'])



def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		nick = parameters.strip()
		if not nick in nicks:
			reply(type,source,u'ты уверен, что <'+nick+u'> был тут?')
			return
		else:
			jidsource=groupchat+'/'+nick
			if get_true_jid(jidsource) == 'None':
				reply(type, source, u'я ж не модер')
				return
			truejid=get_true_jid(jidsource)
			if type == 'public':
				reply(type, source, u'ушёл')
		reply('private', source, u'реальный жид <'+nick+u'> --> '+truejid)
		
		
def handler_total_in_muc(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		inmuc=[]
		for x in GROUPCHATS[groupchat].keys():
			if GROUPCHATS[groupchat][x]['ishere']==1:
				inmuc.append(x)
		reply(type, source, u'я здесь вижу '+str(len(inmuc))+u' юзеров\n'+u', '.join(inmuc))
	else:
		reply(type, source, u'аблом какой-то...')

def all_usr_inf():
        n=0
        for x in GROUPCHATS:
                for s in GROUPCHATS[x]:
                        if GROUPCHATS[x][s]['ishere']==1 and s!=get_bot_nick(x):
                                n+=1
        return n

		
		
def handler_bot_uptime(type, source, parameters):
	if INFO['start']:
                ib=str(len(ALL_BOTS))
		uptime=int(time.time() - INFO['start'])
		rep,mem = u' - в сети уже '+timeElapsed(uptime),''
		try:
                        rep += u'\n - обслуживаю '+unicode(all_usr_inf())+u' юзеров'
                        rep += u'\n - ботов '+unicode(ib)
                except:
                        pass
		rep += u'\n - всего получено %s сообщений,\n - обработано %s презенсов \n - %s iq-запросов \n - выполнено %s команд\n'%(str(INFO['msg']),str(INFO['prs']),str(INFO['iq']),str(INFO['cmd']))
		try:
                        rep+= u'\n - входящий траффик '+str(INFO['itr']//1024)+' KB.'
                        rep+= u'\n - исходящий '+str(xmpp.dispatcher.z//1024)+' KB.'
                except: pass
                if os.name=='posix':
			try:
				pr = os.popen('ps -o rss -p %s' % os.getpid())
				pr.readline()
				mem = pr.readline().strip()
				pr.close()
			except:
				pass
			if mem: rep += u'\n - мной съедено %s кб памяти, ' % mem
		(user, system,qqq,www,eee,) = os.times()
		rep += u'\n - потрачено %.2f секунд процессора, \n - %.2f секунд системного времени \n - %.2f секунд общесистемного времени\n' % (user, system, user + system)
		rep += u'\n - я породил всего %s потоков, \n - в данный момент активно %s потоков' % (INFO['thr'], threading.activeCount())
	else:
		rep = u'аблом...'
	reply(type, source, rep)

def banver_load(groupchat):
        try:
                global BANVER
                BANVER = 'dynamic/'+groupchat+'/banver.txt'
                txt = eval(read_file(BANVER))
                if not groupchat in BAN_VER:
                        BAN_VER[roupchat]=[]
                for x in txt:
                        BAN_VER[roupchat].append(x)
        except:
                pass
        
def get_thr_list():
	thr_list = []
	enu_list = threading.enumerate()
	for thread in enu_list:
		thr_name = thread.getName()
		splthr = thr_name.split('.')
		
		if len(splthr) == 1:
			thr_list.append(u'%d) "%s".' % (enu_list.index(thread)+1,thr_name))
		elif len(splthr) == 5:
			thr_list.append(u'%d) "%s" из "%s" в %s:%s:%s.' % (enu_list.index(thread)+1,splthr[0],splthr[1],splthr[2],splthr[3],splthr[4]))
				
	return (len(enu_list),thr_list)

def handler_thr_show(type, source, parameters):
	thr_list_get = get_thr_list()
	count = thr_list_get[0]
	thr_list = thr_list_get[1]	
	rep = u'Список активных потоков (всего: %d):\n\n%s' % (count,'\n'.join(thr_list))
	reply(type, source, rep)


register_stage1_init(banver_load)
register_command_handler(handler_thr_show, 'потоки', ['инфо','админ','все'], 20, 'Показывает активные потоки бота', 'потоки', ['потоки'])
register_command_handler(handler_getrealjid, 'тружид', ['инфо','админ','мук','все'], 20, 'Показывает реальный жид указанного ника. Работает только если бот модер ессно', 'тружид <ник>', ['тружид guy'])
register_command_handler(handler_total_in_muc, 'инмук', ['инфо','мук','все'], 10, 'Показывает количество юзеров находящихся в конференции.', 'инмук', ['инмук'])
register_command_handler(handler_bot_uptime, 'ботап', ['инфо','админ','все'], 10, 'Показывает сколько времени бот работает без падений.', 'ботап', ['ботап'])
