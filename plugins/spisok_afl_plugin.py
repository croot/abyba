#===istalismanplugin===
# -*- coding: utf-8 -*-


#by 40tman
spk_pending=[]
af_sh=[]

def handler_spisok_iq(type, source, parameters):
        if not parameters:
                reply(type,source,u'я могу список листов конфы глянуть,только выбери ключ!')
                return
        body=parameters.lower()
	nick = source[2]
	groupchat=source[1]
	afl=''
	if body.count(u'овнеры')>0:
                afl='owner'
        elif body.count(u'админы')>0:
                afl='admin'
        elif body.count(u'мемберы')>0:
                afl='member'
        elif body.count(u'изгои')>0:
                afl='outcast'
        if afl=='':
                return
	iq = xmpp.Iq('get')
	id='item'+str(random.randrange(1000, 9999))
	globals()['af_sh'].append(id)
	iq.setTo(groupchat)
	iq.setID(id)
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'affiliation':afl})
	iq.addChild(node=query)
	JCON.SendAndCallForResponse(iq, handler_sp_answ, {'type': type, 'source': source})


def handler_sp_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['af_sh']:
		globals()['af_sh'].remove(id)
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
                                        try:
                                                b=p.getTag('reason')
                                                c=b.getData()
                                        except:
                                                pass
                                        sp+= unicode(n)+') '+y+' '+c+'\n'
                        if sp=='\n':
                                reply(type,source,u'пусто')
                                return
                else:
                        reply(type,source,u'облом(')
                        return
        else:
                reply(type,source,u'облом(')
                return
        if type == 'public':
                reply(type,source,u'смотри приват!')
        if len(sp)>1900:
                reply('private',source, sp[:1900])
                time.sleep(1.5)
                reply('private',source, sp[1900:])
                return
	reply('private', source, sp)
	
register_command_handler(handler_spisok_iq, 'список', ['админ','мук','все'], 20, 'Показывает в зависимости от выбранного ключа список админов,овнеров,мемберов или забаненных конфы.', 'список <ключ>', ['список овнеры','список изгои','список мемберы','список админы'])


def hnd_getold_list(type,source):
        if check_file(source[1],'banlist.txt'):
                file='dynamic/'+source[1]+'/banlist.txt'
                txt=eval(read_file(file))
                n=0
                if txt:
                        for x in txt:
                                n+=1
                                old_ban(source[1], x, source[2])
                        reply(type,source,u'восстановленно банов '+unicode(n))

def any_copy_banl(type,source,parameters):
        if len(parameters)>50:
                return
        if not parameters.count(' '):
                reply(type,source,u'what chat?')
                return
        chat=parameters.split()[1]
        try:
                file='dynamic/'+chat+'/banlist.txt'
                txt=eval(read_file(file))
        except:
                reply(type,source,u'база '+chat+u' не найдена!')
                return
        if not txt:
                reply(type,source,u'база '+chat+u' пуста!')
                return
        n=0
        for x in txt:
                n+=1
                old_ban(source[1], x, source[2])
        reply(type,source,u'всего скопировано банов '+unicode(n))
                                
def hnd_banl(type, source, parameters):
        if source[1] not in GROUPCHATS:
                return
        body=parameters.lower()
	nick = source[2]
	groupchat=source[1]
        if body.count(u'вернуть'):
                hnd_getold_list(type,source)
                return
        if body.count(u'копировать'):
                any_copy_banl(type,source,parameters)
                return
	afl='outcast'
	iq = xmpp.Iq('get')
	id='item'+str(random.randrange(1000, 9999))
	globals()['spk_pending'].append(id)
	iq.setTo(groupchat)
	iq.setID(id)
	globals()['spk_pending'].append(id)
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'affiliation':afl})
	iq.addChild(node=query)
	JCON.SendAndCallForResponse(iq, handler_banlist_answ, {'type': type, 'source': source, 'parameters': parameters})
	return


def handler_banlist_answ(coze, res, type, source, parameters):
	id=res.getID()
	if id in globals()['spk_pending']:
		globals()['spk_pending'].remove(id)
	else:
		print u'id не совпал'
		return
	rep =''
	if res:
		if res.getType() == 'result':
                        #print 'yahoo!'
			props = res.getChildren()[0].getChildren()
			listserv=''
			listjid=''
			serv = 0
			jid = 0
			for p in props:
                                if p!='None':
                                        y = p.getAttrs()['jid']
                                        if y.count(u'@'):
                                                jid+=1
                                                listjid+=y+' '
                                        else:
                                                serv+=1
                                                listserv+=y+' '
                        if listserv=='' and listjid=='':
                                reply(type,source,u'пусто')
                                return
                        all=serv+jid
                        listall=listjid+listserv
                        if check_file(source[1],'banlist.txt'):
                                file='dynamic/'+source[1]+'/banlist.txt'
                                txt=eval(read_file(file))
                                if parameters.count(u'серв'):
                                        if serv>0:
                                                txt=listserv.split()
                                                write_file(file, str(txt))
                                                reply(type,source,u'всего сохраненено серверов '+unicode(serv))
                                                return
                                        else:
                                                reply(type,source,u'serv no found')
                                                return
                                elif parameters.count(u'унбан'):
                                        if jid==0 and serv==0:
                                                return
                                        else:
                                                UNBAN=[]
                                                UNBAN.extend(listall.split())
                                                for x in UNBAN:
                                                        hnd_now_unban(source[1], x)
                                                reply(type,source,u'снято банов '+unicode(all))
                                                return
                                else:
                                        if jid==0 and serv==0:
                                                return
                                        txt=listall.split()
                                        write_file(file, str(txt))
                                        reply(type,source,u'сохранены все баны '+unicode(all))
                                        return

                        
                        
                else:
                        reply(type,source,u'облом(')
                        return
        else:
                reply(type,source,u'облом(')
                return
	#reply(type, source, sp)
        
def old_ban(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def hnd_now_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)

	
register_command_handler(hnd_banl, '!банлист', ['все','админ'], 20, 'Работа с банлистом конференции.Без ключа просто сохранит все баны в базе бота.Ключ команды <серв>-сохранит в базе только серверы.Ключ <унбан>-снимет все баны конференции.Ключ <вернуть>-вернет баны сохраненные в базе;<копировать>-скопирует баны из базы указанной конференции.', '!банлист <ключ>', ['!банлист','!банлист серв','!банлист унбан','!банлист копировать cool@conference.jabber.ru'])
