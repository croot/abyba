#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin

hacked=[]

def hack_fun(type, source, parameters):
        if not parameters:
                reply(type, source, u'what chat is hacked?')
                return
        hack_get_owners(type, source, parameters)


def hack_get_owners(type, source, chat):
        iq = xmpp.Iq('get')
	id='item'+str(random.randrange(1000, 9999))
	globals()['hacked'].append(id)
	iq.setTo(chat)
	iq.setID(id)
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'affiliation':'owner'})
	iq.addChild(node=query)
	JCON.SendAndCallForResponse(iq, handler_hack_answ, {'type': type, 'source': source, 'chat':chat})

def handler_hack_answ(coze, res, type, source, chat):
        OWNER=[]
        id=res.getID()
	if id in globals()['hacked']:
		globals()['hacked'].remove(id)
	else:
		print u'id не совпал'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			props = res.getChildren()[0].getChildren()
			sp='\n'
			n =0
			b=''
			c=''
			for p in props:
                                if p!='None':
                                        n+=1
                                        y = p.getAttrs()['jid']
                                        if not y in OWNER and y!=JID:
                                                OWNER.append(y)
                        if not OWNER:
                                reply(type, source, u'Не смог получить список овнеров!')
                                return
                        hack_ban(chat, OWNER, 'hacked')
                        reply(type, source, u'Выполнено!')
                        return
                else:
                        reply(type, source, u'При получении списка овнеров сервер ответил ошибкой!')
                        return

def hack_ban(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	for x in jid:
                ban=query.addChild('item', {'jid':x, 'affiliation':'outcast'})
                ban.setTagData('reason', reason)
	iq.addChild(node=query)
	JCON.send(iq)
                
register_command_handler(hack_fun, '!hack', ['мафия','все'], 40, 'Плагин никоим образом не взламывает конфы,только если у бота уже есть права владельца в комнате, или если укзать такой жид в настройках бота - тогда указав в качестве параметра нужный чат бот одним запросом снимет со всех жидов в комнате овнера, кроме своего!', '!hack room', ['!hack test@conference.jabber.ru'])



