#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  order_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

order_stats = {}
order_obscene_words = [u'бляд', u' блят', u' бля ', u' блять ', u' плять ', u' хуй', u' ибал', u' ебал', u'нахуй', u' хуй', u' хуи', u'хуител', u' хуя', u'хуя', u' хую', u' хуе', u' ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог']


def order_check_obscene_words(body):
	body=body.lower()
	body=u' '+body+u' '
	for x in order_obscene_words:
		if body.count(x):
			return True
	return False

def order_check_time_flood(gch, jid, nick):
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and time.time()-lastmsg<=2.2:
		order_stats[gch][jid]['msg']+=1
		if order_stats[gch][jid]['msg']>3:
			order_stats[gch][jid]['devoice']['time']=time.time()
			order_stats[gch][jid]['devoice']['cnd']=1
			order_stats[gch][jid]['msg']=0
			order_kick(gch, nick, u'слишком быстро отправляешь')
			return True
		return False

def order_check_len_flood(mlen, body, gch, jid, nick):
	if len(body)>mlen:
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'флуд')
		return True
	return False

def order_check_obscene(body, gch, jid, nick):
	if order_check_obscene_words(body):
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'нецензурно')
		return True
	return False

def order_check_caps(body, gch, jid, nick):
	ccnt=0
	nicks = GROUPCHATS[gch].keys()
	for x in nicks:
		if body.count(x):
			body=body.replace(x,'')
	for x in [x for x in body.replace(' ', '')]:
		if x.isupper():
			ccnt+=1
	if ccnt>=len(body)/2 and ccnt>9:
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'слишком много капса')
		return True
	return False

def order_check_like(body, gch, jid, nick):
	lcnt=0
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and order_stats[gch][jid]['msgbody']:
		if time.time()-lastmsg>60:
			order_stats[gch][jid]['msgbody']=body.split()
		else:
			for x in order_stats[gch][jid]['msgbody']:
				for y in body.split():
					if x==y:
						lcnt+=1
			if lcnt:
				lensrcmsgbody=len(body.split())
				lenoldmsgbody=len(order_stats[gch][jid]['msgbody'])
				avg=(lensrcmsgbody+lenoldmsgbody/2)/2
				if lcnt>avg:
					order_stats[gch][jid]['msg']+=1
					if order_stats[gch][jid]['msg']>=2:
						order_stats[gch][jid]['devoice']['time']=time.time()
						order_stats[gch][jid]['devoice']['cnd']=1
						order_stats[gch][jid]['msg']=0
						order_kick(gch, nick, u'мессаги слишком похожи')
						return True
			order_stats[gch][jid]['msgbody']=body.split()
	else:
		order_stats[gch][jid]['msgbody']=body.split()
	return False

####################################################################################################

def order_kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_visitor(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_ban(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)

def order_check_idle():
	for gch in GROUPCHATS.keys():
		if 'filt' in GCHCFGS[gch] and GCHCFGS[gch]['filt']['idle']['cond']==1:
			timee=GCHCFGS[gch]['filt']['idle']['time']
			now=time.time()
			for nick in GROUPCHATS[gch].keys():
				if GROUPCHATS[gch][nick]['ishere']==1:
					if user_level(gch+'/'+nick,gch)<15:
						idle=now-GROUPCHATS[gch][nick]['idle']
						if idle > timee:
							order_kick(gch, nick, u'молчание более '+timeElapsed(idle))
	threading.Timer(120,order_check_idle).start()

####################################################################################################

def handler_order_message(raw=None, type=None, source=None, body=None):
	nick=source[2]
	groupchat=source[1]
	if groupchat in GROUPCHATS.keys() and user_level(source,groupchat)<15:
		if get_bot_nick(groupchat)!=nick:
			jid=get_true_jid(groupchat+'/'+nick)
			if groupchat in order_stats and jid in order_stats[groupchat]:
				if GCHCFGS[groupchat]['filt']['time']==1:
					if order_check_time_flood(groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['len']==1:
					if order_check_len_flood(900, body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['obscene']==1:
					if order_check_obscene(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['caps']==1:
					if order_check_caps(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['like']==1:
					if order_check_like(body, groupchat, jid, nick):	return
				order_stats[groupchat][jid]['msgtime']=time.time()

def handler_order_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<15:
		now = time.time()
		if not groupchat in order_stats.keys():
			order_stats[groupchat] = {}
		if jid in order_stats[groupchat].keys():
			if order_stats[groupchat][jid]['devoice']['cnd']==1:
				if now-order_stats[groupchat][jid]['devoice']['time']>300:
					order_stats[groupchat][jid]['devoice']['cnd']=0
				else:
					order_visitor(groupchat, nick, u'право голоса снято за предыдущие нарушения')

			if GCHCFGS[groupchat]['filt']['kicks']['cond']==1:
				kcnt=GCHCFGS[groupchat]['filt']['kicks']['cnt']
				if order_stats[groupchat][jid]['kicks']>kcnt:
					order_ban(groupchat, nick, u'слишком много киков')
					return

			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
					if order_stats[groupchat][jid]['prs']['fly']>4:
						order_stats[groupchat][jid]['prs']['fly']=0
						fmode=GCHCFGS[groupchat]['filt']['fly']['mode']
						ftime=GCHCFGS[groupchat]['filt']['fly']['time']
						if fmode=='ban':
							order_ban(groupchat, nick, u'хватит летать')
							time.sleep(ftime)
							order_unban(groupchat, jid)
						else:
							order_kick(groupchat, nick, u'хватит летать')
							return
				else:
					order_stats[groupchat][jid]['prs']['fly']=0

			if GCHCFGS[groupchat]['filt']['obscene']==1:
				if order_check_obscene(nick, groupchat, jid, nick):	return

			if GCHCFGS[groupchat]['filt']['len']==1:
				if order_check_len_flood(20, nick, groupchat, jid, nick):	return

		elif nick in GROUPCHATS[groupchat]:
			order_stats[groupchat][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}

	elif groupchat in order_stats and jid in order_stats[groupchat]:
		del order_stats[groupchat][jid]
	else:
		pass

LAST_CAPS_BAN={}

def handler_order_presence(prs):
	ptype = prs.getType()
	if ptype=='unavailable' or ptype=='error':
		return
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	if nick==get_bot_nick(groupchat):
                return
	stmsg = prs.getStatus()
	jid=get_true_jid(groupchat+'/'+nick)
	item=findPresenceItem(prs)

	if groupchat in order_stats and jid in order_stats[groupchat]:
		if item['affiliation'] in ['admin','owner']:
			del order_stats[groupchat][jid]
			return
	else:
		if (item['affiliation']=='none') | (item['affiliation']=='member'):
			try:
                                order_stats[groupchat][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}
                        except KeyError:
                                pass
        try:
                if GCHCFGS[groupchat]['filt']['bot']['cond']:
                        cap=prs.getTagAttr('c','node')
                        srv=jid.split('@')[1]
                        bmode=GCHCFGS[groupchat]['filt']['bot']['mode']
                        md=''
                        if cap==None and srv not in [u'jabber.ru',u'xmpp.ru',u'talkonaut.com']:
                                if bmode=='ban':
                                        md=u'забанен'
                                        order_ban(groupchat,nick,u'Фильтр юзеров по наличию капса в клиенте.(чтобы выключить filt bot 0)')
                                else:
                                        md=u'выкинут'
                                        order_kick(groupchat,nick,u'Фильтр юзеров по наличию капса в клиенте.(чтобы выключить filt bot 0)')
                                if groupchat not in LAST_CAPS_BAN:
                                        LAST_CAPS_BAN[groupchat]={}
                                        if groupchat in GROUPCHATS and get_bot_nick(groupchat) in GROUPCHATS[groupchat]:
                                                if GROUPCHATS[groupchat][get_bot_nick(groupchat)]['ismoder']:
                                                        msg(groupchat, u'/me Упс! Юзер '+unicode(nick[:20])+u' был '+md+u' , посколько в его презенесе не найден капс с версией клиента, что характерно для ботов! \nНапоминаю что отключить фильтр ботов можно так: filt bot 0')
        except:
                pass

	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			now = time.time()
			if now-GROUPCHATS[groupchat][nick]['joined']>1:
				if item['role']=='participant':
					order_stats[groupchat][jid]['devoice']['cnd']=0
				lastprs=order_stats[groupchat][jid]['prstime']['status']
				order_stats[groupchat][jid]['prstime']['status']=now

				if GCHCFGS[groupchat]['filt']['presence']==1:
					if now-lastprs>300:
						order_stats[groupchat][jid]['prs']['status']=0
					else:
						order_stats[groupchat][jid]['prs']['status']+=1
						if order_stats[groupchat][jid]['prs']['status']>5:
							order_stats[groupchat][jid]['prs']['status']=0
							order_kick(groupchat, nick, u'презенс-флуд')
							return

				if GCHCFGS[groupchat]['filt']['obscene']==1:
					if order_check_obscene(nick, groupchat, jid, nick):	return

				if GCHCFGS[groupchat]['filt']['prsstlen']==1 and stmsg:
					if order_check_len_flood(200, nick, groupchat, jid, nick):	return

def handler_order_leave(groupchat, nick, reason, code):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<15:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			if GCHCFGS[groupchat]['filt']['presence']==1:
				if reason=='Replaced by new connection':
					return
				if code:
					if code=='307': # kick
						order_stats[groupchat][jid]['kicks']+=1
						return
					elif code=='301': # ban
						del order_stats[groupchat][jid]
						return
					elif code=='407': # members-only
						return
			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				now = time.time()
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
				else:
					order_stats[groupchat][jid]['prs']['fly']=0

######################################################################################################################

def handler_order_filt(type, source, parameters):
	if parameters:
		parameters=parameters.split()
		if len(parameters)<2:
			reply(type,source,u'синтакс инвалид')
			return
		if GCHCFGS[source[1]].has_key('filt'):
			if parameters[0]=='time':
				if parameters[1]=='0':
					reply(type,source,u'временная фильтрация сообщений отключена')
					GCHCFGS[source[1]]['filt']['time']=0
				elif parameters[1]=='1':
					reply(type,source,u'временная фильтрация сообщений включена')
					GCHCFGS[source[1]]['filt']['time']=1
				else:
					reply(type,source,u'синтакс инвалид')
			
			elif parameters[0]=='bot':
                                if parameters[1]=='mode':
                                        if parameters[2] in ['kick','ban']:
                                                if parameters[2] == 'ban':
                                                        reply(type,source,u'клиенты без капса будем банить')
							GCHCFGS[source[1]]['filt']['bot']['mode']='ban'
						else:
							reply(type,source,u'клиенты без капса будем кикать')
							GCHCFGS[source[1]]['filt']['bot']['mode']='kick'
					else:
						reply(type,source,u'синтакс инвалид')
				if parameters[1]=='0':
					reply(type,source,u'фильтрация ботов отключена')
					GCHCFGS[source[1]]['filt']['bot']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация ботов включена')
					GCHCFGS[source[1]]['filt']['bot']['cond']=1
				else:
					pass

			elif parameters[0]=='presence':
				if parameters[1]=='0':
					reply(type,source,u'временная фильтрация презенсов отключена')
					GCHCFGS[source[1]]['filt']['presence']=0
				elif parameters[1]=='1':
					reply(type,source,u'временная фильтрация презенсов включена')
					GCHCFGS[source[1]]['filt']['presence']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='len':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных сообщений отключена')
					GCHCFGS[source[1]]['filt']['len']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных сообщений включена')
					GCHCFGS[source[1]]['filt']['len']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='like':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений отключена')
					GCHCFGS[source[1]]['filt']['like']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений включена')
					GCHCFGS[source[1]]['filt']['like']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='caps':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация капса отключена')
					GCHCFGS[source[1]]['filt']['caps']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация капса включена')
					GCHCFGS[source[1]]['filt']['caps']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='prsstlen':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных статусных сообщений отключена')
					GCHCFGS[source[1]]['filt']['prsstlen']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных статусных сообщений включена')
					GCHCFGS[source[1]]['filt']['prsstlen']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='obscene':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация мата отключена')
					GCHCFGS[source[1]]['filt']['obscene']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация мата включена')
					GCHCFGS[source[1]]['filt']['obscene']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='fly':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					if int(parameters[2]) in xrange(0,121):
						reply(type,source,u'разморозка установлена на '+parameters[2]+u' секунд')
						GCHCFGS[source[1]]['filt']['fly']['time']=int(parameters[2])
					else:
						reply(type,source,u'не более двух минут (120 секунд)')
				elif parameters[1]=='mode':
					if parameters[2] in ['kick','ban']:
						if parameters[2] == 'ban':
							reply(type,source,u'за полёты будем банить')
							GCHCFGS[source[1]]['filt']['fly']['mode']='ban'
						else:
							reply(type,source,u'за полёты будем кикать')
							GCHCFGS[source[1]]['filt']['fly']['mode']='kick'
					else:
						reply(type,source,u'синтакс инвалид')
				elif parameters[1]=='0':
					reply(type,source,u'фильтр полётов отключен')
					GCHCFGS[source[1]]['filt']['fly']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр полётов включен')
					GCHCFGS[source[1]]['filt']['fly']['cond']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='kicks':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					if int(parameters[2]) in xrange(2,10):
						reply(type,source,u'автобан после '+parameters[2]+u' киков')
						GCHCFGS[source[1]]['filt']['kicks']['cnt']=int(parameters[2])
					else:
						reply(type,source,u'от 2 до 10 киков')
				elif parameters[1]=='0':
					reply(type,source,u'фильтр автобана после нескольких киков отключен')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр автобана после нескольких киков включен')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='idle':
				if parameters[1]=='time':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					reply(type,source,u'кик за молчание после '+parameters[2]+u' секунд ('+timeElapsed(int(parameters[2]))+u')')
					GCHCFGS[source[1]]['filt']['idle']['time']=int(parameters[2])
				elif parameters[1]=='0':
					reply(type,source,u'фильтр кика за молчание отключен')
					GCHCFGS[source[1]]['filt']['idle']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр кика за молчание включен')
					GCHCFGS[source[1]]['filt']['idle']['cond']=1
			else:
				reply(type,source,u'синтакс инвалид')
				return
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
		else:
			reply(type,source,u'случилось что-то странное, ткните админа бота')
	else:
		rep,foff,fon=u'',[],[]
		time=GCHCFGS[source[1]]['filt']['time']
		prs=GCHCFGS[source[1]]['filt']['presence']
		flen=GCHCFGS[source[1]]['filt']['len']
		like=GCHCFGS[source[1]]['filt']['like']
		bot=GCHCFGS[source[1]]['filt']['bot']['cond']
		caps=GCHCFGS[source[1]]['filt']['caps']
		prsstlen=GCHCFGS[source[1]]['filt']['prsstlen']
		obscene=GCHCFGS[source[1]]['filt']['obscene']
		fly=GCHCFGS[source[1]]['filt']['fly']['cond']
		flytime=str(GCHCFGS[source[1]]['filt']['fly']['time'])
		flymode=GCHCFGS[source[1]]['filt']['fly']['mode']
		kicks=GCHCFGS[source[1]]['filt']['kicks']['cond']
		kickscnt=str(GCHCFGS[source[1]]['filt']['kicks']['cnt'])
		idle=GCHCFGS[source[1]]['filt']['idle']['cond']
		idletime=GCHCFGS[source[1]]['filt']['idle']['time']
		if time:
			fon.append(u'временная фильтрация сообщений')
		else:
			foff.append(u'временная фильтрация сообщений')
		if prs:
			fon.append(u'временная фильтрация презенсов')
		else:
			foff.append(u'временная фильтрация презенсов')
		if flen:
			fon.append(u'фильтрация длинных сообщений')
		else:
			foff.append(u'фильтрация длинных сообщений')
		if like:
			fon.append(u'фильтрация подозрительно одинаковых сообщений')
		else:
			foff.append(u'фильтрация подозрительно одинаковых сообщений')
		if caps:
			fon.append(u'фильтрация капса')
		else:
			foff.append(u'фильтрация капса')
		if prsstlen:
			fon.append(u'фильтрация длинных статусных сообщений')
		else:
			foff.append(u'фильтрация длинных статусных сообщений')
		if obscene:
			fon.append(u'фильтрация мата')
		else:
			foff.append(u'фильтрация мата')
		if fly:
			fon.append(u'фильтр полётов (режим '+flymode+u', таймер '+flytime+u' секунд)')
		else:
			foff.append(u'фильтр полётов')
		if kicks:
			fon.append(u'автобан после '+kickscnt+u' киков')
		else:
			foff.append(u'автобан после нескольких киков')
		if idle:
			fon.append(u'кик за молчание через '+str(idletime)+u' секунд ('+timeElapsed(idletime)+u')')
		else:
			foff.append(u'кик за молчание')
		if bot:
                        fon.append(u'фильтрация ботов (режим '+GCHCFGS[source[1]]['filt']['bot']['mode']+u')')
                else:
                        foff.append(u'фильтрация ботов')
		fon=u', '.join(fon)
		foff=u', '.join(foff)
		if fon:
			rep+=u'ВКЛЮЧЕНЫ\n'+fon+u'\n\n'
		if foff:
			rep+=u'ВЫКЛЮЧЕНЫ\n'+foff
		reply(type,source,rep.strip())


def get_order_cfg(gch):
	if not 'filt' in GCHCFGS[gch]:
		GCHCFGS[gch]['filt']={}
	for x in ['time','presence','len','like','caps','prsstlen','obscene','kicks','fly','excess','idle','bot']:
		if x == 'excess':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'mode': 'kick'}
			continue
		if x == 'kicks':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'cnt': 2}
			continue
		if x == 'fly':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'mode': 'ban', 'time': 60}
			continue
		if x == 'idle':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'time': 3600}
			continue
		if x == 'bot':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'mode' : 'kick'}
			continue
		if not x in GCHCFGS[gch]['filt']:
			GCHCFGS[gch]['filt'][x]=1

register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'filt', ['админ','мук','все'], 20, 'Включает или отключает определённые фильтры для конференции.\ntime - временной фильтр\nlen - количественный фильтр\npresence - фильтр презенсов\nlike - фильтр одинаковых сообщений\ncaps - фильтр капса (ЗАГЛАВНЫХ букв)\nprsstlen - фильтр длинных статусных сообщений\nobscene - фильтр матов\nfly - фильтр полётов (частых входов/выходов в конмату), \nbot- спасает от примитивных спам-ботов,в списке три сервера на которых действие не распостряняеться(jabber.ru,xmppp.ru,talkonaut.com),имеет два режима ban и kick(filt bot mode ban),\nkicks - автобан после N киков, параметр cnt - количество киков от 1 до 10\nidle - кик за молчание в общем чате после N секунд, параметр time - кол-во секунд для срабатывания', 'filt [фильтр] [режим] [состояние]', ['filt smile 1', 'filt len 0','filt fly mode ban'])

register_stage1_init(get_order_cfg)
register_stage2_init(order_check_idle)
