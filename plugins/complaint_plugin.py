#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  complaint_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_complaint(type, source, parameters):
	if type == 'public':
		reply(type, source, u'это команда работает только у меня в привате!')
	elif type == 'private':
		groupchat=source[1]
		if GROUPCHATS.has_key(groupchat):
			nicks = GROUPCHATS[groupchat].keys()
			args = parameters.split(' ')
			nick = args[0].strip()
			body = ' '.join(args[1:])
			if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['ishere']==1:		
				jidsource=groupchat+'/'+nick
				if user_level(jidsource,groupchat)>=15:
					reply(type,source,u'если попробуешь ещё хоть раз пожаловатся на модера - пойдёшь в баню ]:->')
					return			
				if len(nick)>20 or len(body)>100:
					reply(type, source, u'а не много ли ты написал?')
					return
				for x in nicks:
					jid=groupchat+'/'+x
					if user_level(jid,groupchat)>=15 and GROUPCHATS[groupchat][x]['status'] in ['online','away','chat']:
						msg(jid, u'юзер <'+source[2]+u'>\nжалуется на <'+nick+u'>\nпо причине <'+body+u'>\n\nВы можете забанить (банан '+nick+u' `ризон`) или кикнуть (кик '+nick+u' `ризон`) этого юзера прямо сейчас из моего привата')
				reply(type, source, u'жалоба на <'+nick+u'> ушла всем модераторам данной конференции. если вашу жалобу сочтут спамом, то вас забанят!')
			else:
				reply(type,source,u'ты уверен, что <'+nick+u'> сейчас тут?')
				
register_command_handler(handler_complaint, 'жалоба',  ['мук','все'], 10, 'Пожаловаться на определённый ник по определённой причине. Работает только у меня в привате!', 'жалоба <ник> <причина>', ['жалоба Nick7 спам'])
