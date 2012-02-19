#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  stanza_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>



def handler_stanza(type, source, parameters):
	if parameters:
		node=xmpp.simplexml.XML2Node(unicode(parameters).encode('utf8'))
#		JCON.SendAndCallForResponse(node, handler_stanza_answ,{'type': type, 'source': source})
		JCON.send(node)
		return
	rep = u'ты что посылать собралсо?'
	reply(type, source, rep)


register_command_handler(handler_stanza, '!stanza', ['суперадмин','все','мук'], 100, 'отправка станзы', '!stanza <payload>', ['!stanza aaabbb'])



