#===istalismanplugin===
# -*- coding: utf-8 -*-

INVITE_S = {}

INVITE_LIM = {}

invite_pending=[]


def handler_invite_start(type, source, parameters):
	truejid, nick, reason = '', '', ''
	global INVITE_S
	global INVITE_LIM
	if not parameters or parameters.isspace():
		reply(type,source,u'ииии?')
		return
	if not source[1] in GROUPCHATS:
                reply(type, source, u'Работает только в чате!')
                return
	LIST={u'овнеров':u'owner',u'админов':u'admin',u'мемберов':u'member',u'всех':u'None'}
	if parameters.lower() in LIST:
                if not source[1] in INVITE_LIM:
                        INVITE_LIM[source[1]] = {'time':time.time()}
                else:
                        if time.time() - INVITE_LIM[source[1]]['time'] < 360:
                                reply(type,source,u'Лимит команды - 5 минут!!!')
                                return
                        else:
                                INVITE_LIM[source[1]]['time'] = time.time()
                if not source[1] in INVITE_S:
                        invite_get_list(type, source)
                        tim = time.time()
                        while not source[1] in INVITE_S and time.time() - tim <5:
                                time.sleep(2)
                                pass
                        if not source[1] in INVITE_S:
                                reply(type, source, u'Не смог получить список!')
                                return
                        if not INVITE_S[source[1]]:
                                reply(type, source, u'Не смог получить список!')
                                return
                time.sleep(3)
                n=0
                if parameters.lower()==u'всех':
                        for x in INVITE_S[source[1]]:
                                for c in INVITE_S[source[1]][x]:
                                        n+=1
                                        invite_send(source[1], c, source[2])
                else:
                        if LIST[parameters.lower] in INVITE_S[source[1]]:
                                for x in INVITE_S[source[1]][LIST[parameters.lower]]:
                                        n+=1
                                        invite_send(source[1], x, source[2])
                reply(type, source, u'Призвал '+str(n)+u' юзеров!')
                return
	else:
                if not parameters.count('@'):
                        nicks = GROUPCHATS[source[1]].keys()
                        nick = parameters.split()[0]
                        if not nick in nicks:
                                reply(type,source,u'юзер не наден, попробуйте ввести jid')
                                return
                        else:
                                truejid=get_true_jid(source[1]+'/'+nick)
                                reason=' '.join(parameters.split()[1:])
                else:
                        truejid = parameters
                        reason = u'Вас приглашает '+source[2]
                invite_send(source[1], truejid, reason)
                reply(type, source, u'Призвал!')


def invite_send(chat, user, reason):
        msg=xmpp.Message(to=chat)
	id = 'inv'+str(random.randrange(1, 1000))
	globals()['invite_pending'].append(id)
	msg.setID(id)
	x=xmpp.Node('x')
	x.setNamespace('http://jabber.org/protocol/muc#user')
	inv=x.addChild('invite', {'to':user})
	if reason:
		inv.setTagData('reason', reason)
	else:
		inv.setTagData('reason', u'Вас здесь ждут.')
	msg.addChild(node=x)
	JCON.send(msg)


def invite_get_list(type, source):
        for aff in ['owner','admin','member']:
                iq = xmpp.Iq('get')
                id='item'+str(random.randrange(1000, 9999))
                iq.setTo(source[1])
                iq.setID(id)
                query = xmpp.Node('query')
                query.setNamespace('http://jabber.org/protocol/muc#admin')
                ban=query.addChild('item', {'affiliation':aff})
                iq.addChild(node=query)
                JCON.SendAndCallForResponse(iq, invite_list_answ, {'type': type,'source': source, 'aff': aff})

def invite_list_answ(coze, res, type, source, aff):
	id=res.getID()
	rep =''
	allinf=''
	n=0
	al=0
	if res:
		if res.getType() == 'result':
                        at=res.getFrom()
                        mas=res.getQueryChildren()
                        for x in mas:
                                try:
                                        jid=x.getAttrs()['jid']
                                        if jid.count('@'):
                                                if not source[1] in INVITE_S:
                                                        INVITE_S[source[1]]={}
                                                if not aff in INVITE_S[source[1]]:
                                                        INVITE_S[source[1]][aff]={}
                                                INVITE_S[source[1]][aff][jid]={}
                                except:
                                        pass
                                     
					
register_command_handler(handler_invite_start, 'призвать', ['мук','все'], 10, 'Может приглашать заданного пользователя в конференцию', 'призвать [ник/JID] [причина]', ['призвать админов','призвать guy','призвать guy@jabber.aq','призвать guy@jabber.aq есть дело'])
