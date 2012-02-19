#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  sg_plugin.py

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

def handler_SG_get(type, source, parameters):
		groupchat = source[1]
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		if parameters!='':
			iq.setTo(parameters.strip())
		else:
			iq.setTo(CONNECT_SERVER)
			parameters=CONNECT_SERVER
		JCON.SendAndCallForResponse(iq,first_handler_SG,{'parameters':parameters,'type':type,'source':source})

def first_handler_SG(coze,res,parameters,type,source):
    try:
        qu=res.getQueryChildren()
	if res.getType()=='error':
		reply(type,source,u'не судьба :(')
		pass
	elif res.getType()=='result':
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		iq.setQueryPayload(qu)
		iq.setTo(parameters)
		JCON.SendAndCallForResponse(iq,second_handler_SG,{'parameters':parameters,'type':type,'source':source})
	else:
		reply(type,source,u'не дождался :(')
    except:
        reply(type,source,u'ошибочный ответ сервера')

def second_handler_SG(coze,stats,parameters,type,source):
	try:
            pay=stats.getQueryPayload()
            if stats.getType()=='result':
                result=u'Инфа о ' + parameters + ':\n'
                for stat in pay:
                    result=result+stat.getAttrs()['name']+': '+stat.getAttrs()['value'] + ' '+stat.getAttrs()['units'] + '\n'
			
		reply(type,source,result.strip())
	except:
            pass
		
		
register_command_handler(handler_SG_get, 'инфа', ['инфо','все'], 10, 'Возвращает статистику о сервере юзая XEP-0039.', 'инфа <сервер>', ['инфа jabber.aq'])
