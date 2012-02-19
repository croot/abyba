#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  idle_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

idle_pending=[]
def handler_idle(type, source, parameters):
	idle_iq = xmpp.Iq('get')
	id='idle'+str(random.randrange(1000, 9999))
	globals()['idle_pending'].append(id)
	idle_iq.setID(id)
	idle_iq.addChild('query', {}, [], 'jabber:iq:last');
	if parameters:
		param = parameters.strip()
		idle_iq.setTo(param)
	else:
		param=CONNECT_SERVER
		idle_iq.setTo(param)
	JCON.SendAndCallForResponse(idle_iq, handler_idle_answ, {'type': type, 'source': source, 'param': param})
	
		
def handler_idle_answ(coze, res, type, source, param):
	id=res.getID()
	if id in globals()['idle_pending']:
		globals()['idle_pending'].remove(id)
	else:
		print 'ooops!'
		return
	rep =''
	if res:
		if res.getType()=='error':
			reply(type,source,u'там или нету жабер сервера или он упал или он запрещает смотреть эту инфу')
			return
		elif res.getType() == 'result':
			sec = ''
			props = res.getPayload()
			if not props:
				reply(type,source,u'там или упал жабер сервер или его вообще нету')
				return 
			for p in props:
				sec=p.getAttrs()['seconds']
				if not sec == '0':
					rep = param+u' работает уже '+timeElapsed(int(sec))
	else:
		rep = u'глюк'
	reply(type, source, rep)

def handler_userinfo_idle(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		if not parameters:
			reply(type,source,u'ииии?')
			return
		nick = parameters.strip()
		if nick==source[2]:
			reply(type,source,u'и что я должен сказать? ;)')
			return
		if GROUPCHATS[source[1]].has_key(nick) and GROUPCHATS[source[1]][nick]['ishere']==1:
			groupchat = source[1]
			idletime = int(time.time() - GROUPCHATS[groupchat][nick]['idle'])
			reply(type, source, nick+u' заснул '+timeElapsed(idletime)+u' назад')
		else:
			reply(type,source,u'а он тут? :-O')

def handler_amoder_admin(groupchat,nick,afl,role):
        jid=get_true_jid(groupchat+'/'+nick)
        if jid in ADMINS and role!='moderator':
                reason=''
                iq = xmpp.Iq('set')
                iq.setTo(groupchat)
                iq.setID('kick'+str(random.randrange(1000, 9999)))
                query = xmpp.Node('query')
                query.setNamespace('http://jabber.org/protocol/muc#admin')
                kick=query.addChild('item', {'nick':nick, 'role':'moderator'})
                kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
                iq.addChild(node=query)
                JCON.send(iq)

register_join_handler(handler_amoder_admin)
register_command_handler(handler_idle, 'аптайм', ['инфо','мук','все'], 10, 'Показывает аптайм определённого сервера.', 'аптайм <сервер>', ['аптайм jabber.aq'])
register_command_handler(handler_userinfo_idle, 'жив', ['инфо','мук','все'], 10, 'Показывает сколько времени неактивен юзер.', 'жив <ник>', ['жив guy'])
