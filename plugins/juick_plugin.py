#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  juick_plugin.py
#  exclusively for juick.com ;)

#  Initial Copyright © Als <als-als@ya.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# msg types: 0-post, 1-replies

juick_reply={'uids': {}}

def handler_juick(type, source, parameters):
	if parameters:
		if re.match('^#[0-9]+(\+|/[0-9]+(-[0-9]+)?)?$',parameters): # thanks dimichxp!!!
			ray=parameters[1:]
			handler_juick_ray(type, source, ray, 0)
		elif parameters.startswith('@'):
			try:
				someid=parameters[1:]
				int(parameters)
				handler_juick_ray(type, source, someid, 1)
			except:
				someid=parameters[1:]
				handler_juick_convert(type, source, someid)
		else:
			reply(type, source, u'ошибочный синтаксис. прочти помощь по команде')
	else:
		iq = xmpp.Iq('get')
		id = 'j'+str(random.randrange(1, 1000))
		iq.setID(id)
		query=iq.addChild('query', {}, [], 'http://juick.com/query#messages')
		iq.setTo('juick@juick.com')
		JCON.SendAndCallForResponse(iq, handler_juick_answ,{'type': type, 'source': source, 'ray': u'last?show=all', 'selcmnts': '10', 'allcmnts': '10'})

def handler_juick_ray(type, source, ray, uname):
	jr = xmpp.Iq('get')
	id = 'jr'+str(random.randrange(1, 1000))
	jr.setID(id)
	jr.setTo('juick@juick.com')
	allcmnts, selcmnts='', ''

	if uname:
		query=jr.addChild('query', {}, [], 'http://juick.com/query#messages')
		query.setAttr('uid',ray)
		allcmnts, selcmnts='10', '10'
		ray=uname
		JCON.SendAndCallForResponse(jr, handler_juick_answ,{'type': type, 'source': source, 'ray': ray, 'selcmnts': selcmnts, 'allcmnts': allcmnts})
	else:
		if ray.endswith('+'):
			ray=ray[:-1]
			if type=='public':
				selcmnts='1-30'
			else:
				selcmnts='1-100'
			handler_juick_ray_cmnts(type, source, ray, jr, selcmnts)
		elif ray.count('/'):
			temp=ray.split('/')
			ray,selcmnts=temp[0],temp[1]
			temp=selcmnts.split('-')
			if len(temp)==2:
				if len(xrange(int(temp[0]),int(temp[1])))==0:
					reply(type, source, u'ошибочный синтаксис. прочти помощь по команде')
					return
			handler_juick_ray_cmnts(type, source, ray, jr, selcmnts)
		else:
			query=jr.addChild('query', {}, [], 'http://juick.com/query#messages')
			query.setAttr('mid',ray)
			allcmnts, selcmnts='1', '1'
			JCON.SendAndCallForResponse(jr, handler_juick_answ,{'type': type, 'source': source, 'ray': ray, 'selcmnts': selcmnts, 'allcmnts': allcmnts})

def handler_juick_ray_cmnts(type, source, ray, jr, selcmnts):
	query=jr.addChild('query', {}, [], 'http://juick.com/query#messages')
	query.setAttr('rid','*')
	query.setAttr('mid',ray)

	jcn = xmpp.Iq('get')
	id = 'jcn'+str(random.randrange(1, 1000))
	jcn.setID(id)
	query=jcn.addChild('query', {}, [], 'http://juick.com/query#messages')
	query.setAttr('mid',ray)
	jcn.setTo('juick@juick.com')
	JCON.SendAndCallForResponse(jcn, juick_check_comments_num_answ,{'type': type, 'source': source, 'ray': ray, 'jr': jr, 'selcmnts': selcmnts})

def juick_check_comments_num_answ(coze, res, type, source, ray, jr, selcmnts):
	if res:
		if res.getType()=='error':
			if res.getErrorCode()=='404':
				reply(type, source, u'нет такого луча')
			elif res.getErrorCode()=='403':
				reply(type, source, u'нет доступа')
			else:
				reply(type, source, u'неизвестная ошибка')
		elif res.getType()=='result':
			jmsgs = res.getChildren()[0].getChildren()
			if jmsgs:
				allcmnts=jmsgs[0].getAttr('replies')
				JCON.SendAndCallForResponse(jr, handler_juick_answ,{'type': type, 'source': source, 'ray': ray, 'selcmnts': selcmnts, 'allcmnts': allcmnts})
			else:
				reply(type, source, u'в луче нет ответов')
	else:
		reply(type, source, u'таймаут')

####################################################
# UName<>UID,UID+UName<JID
# START
####################################################

def handler_juick_convert(type, source, someid):
	if someid in juick_reply['uids'].keys():
		handler_juick_ray(type, source, juick_reply['uids'][someid], someid)
	else:
		jconv = xmpp.Iq('get')
		id = 'jsub'+str(random.randrange(1, 1000))
		jconv.setID(id)
		jconv.setTo('juick@juick.com')
		jquery=jconv.addChild('query', {}, [], 'http://juick.com/query#users')
		juser=jquery.addChild('user', {}, [], 'http://juick.com/user')
		if someid.count('@') and someid.count('.'):
			juser.setAttr('jid',someid)
		else:
			juser.setAttr('uname',someid)
		JCON.SendAndCallForResponse(jconv, handler_juick_convert_answ,{'type': type, 'source': source, 'someid': someid})

def handler_juick_convert_answ(coze, res, type, source, someid):
	if res:
		if res.getType()=='error':
			if res.getErrorCode()=='404':
				reply(type, source, u'не найдено')
			elif res.getErrorCode()=='403':
				reply(type, source, u'нет доступа')
			else:
				reply(type, source, u'неизвестная ошибка')
		elif res.getType()=='result':
			juser = res.getChildren()[0].getChildren()
			if juser:
				juser = juser[0].getAttrs()
				uid = juser['uid']
				uname = juser['uname']
				juick_reply['uids'].update({uname: uid})
				handler_juick_ray(type, source, uid, uname)
			else:
				reply(type, source, u'кто это?')

####################################################
# UName<>UID,UID+UName<JID
# END
###################################################


##########################################################################################

def handler_juick_answ(coze, res, type, source, ray, selcmnts, allcmnts):
	if res:
		if res.getType()=='error':
			if res.getErrorCode()=='404':
				reply(type, source, u'не найдено')
			elif res.getErrorCode()=='403':
				reply(type, source, u'нет доступа')
			else:
				reply(type, source, u'неизвестная ошибка')
		elif res.getType()=='result':
			resid=res.getID()
			if not source[1] in juick_reply:
				juick_reply[source[1]]=source[1]
				juick_reply[source[1]]={}
			query_child=res.getQueryChildren()[0].getNamespace()
			jmsgs = res.getChildren()[0].getChildren()
			if jmsgs:
				if query_child=='http://juick.com/message':
					if not resid in juick_reply[source[1]]:
						juick_reply[source[1]][resid]={'msg': [], 'childs': []}
					handler_juick_msg_answ(resid, type, source, jmsgs, ray, selcmnts, allcmnts)
				elif query_child=='http://juick.com/user':
					del juick_reply[source[1]][resid]


def handler_juick_msg_answ(resid, type, source, jmsgs, ray, selcmnts, allcmnts):
	if selcmnts:
		selcmnts=selcmnts.split('-')
	for child in jmsgs:
		juick_reply[source[1]][resid]['childs'].append(child)
		if len(juick_reply[source[1]][resid]['childs'])==int(allcmnts):
			for jmsg in juick_reply[source[1]][resid]['childs']:
				msg=parse_juick_msg_stanza(jmsg, selcmnts, allcmnts, resid)
				if msg==False:
					break
				elif msg:
					juick_reply[source[1]][resid]['msg'].append(msg)
			if juick_reply[source[1]][resid]['msg']:
				rep=u'http://juick.com/%s' % ray
				msgs=u'\n'.join(juick_reply[source[1]][resid]['msg'])
				if msgs.count(u'нет ответов') or ray.count('last'):
					rep+=u'\n' + msgs
				else:
					rep+=u'#%s\n' % selcmnts[0] + msgs
				reply(type, source, unicode(rep))
				del juick_reply[source[1]][resid]
			else:
				reply(type, source, u'что это было?')
				del juick_reply[source[1]][resid]


def parse_juick_msg_stanza(stanza, selcmnts, allcmnts, resid):
	attrs=stanza.getAttrs()
	pjmsg={}
	for attr in ['rid','uname','mid','replies','photo','ts']:
		pjmsg.update({attr: juick_check_attr(attrs, attr)})
		if pjmsg['rid']:
			if len(selcmnts)==2:
				if int(pjmsg['rid']) in xrange(int(selcmnts[0]),int(selcmnts[1])+1):
					pass
				elif int(pjmsg['rid'])<int(selcmnts[0]):
					return
				elif int(pjmsg['rid'])>int(selcmnts[1]):
					return False
			else:
				if not pjmsg['rid']==selcmnts[0]: return
	jmbody=stanza.getTagData('body')
	jtags=stanza.getTags('tag')
	tags=u', '.join([u'*'+x.getData() for x in jtags]) or None
	pjmsg.update({'tags': tags, 'body': jmbody})
	if pjmsg['rid'] is None:
		return format_juick_msg(0,pjmsg)
	else:
		return format_juick_msg(1,pjmsg)

def juick_check_attr(stdt, attr):
	if attr in stdt:
		return stdt[attr]
	else:
		return None

def format_juick_msg(mode, pjmsg):
	if mode:
		return u'@%(uname)s @ '% pjmsg +convert_juick_timestamp(pjmsg['ts'])+u' GMT\n%(body)s\n#%(mid)s/%(rid)s\n' % pjmsg
	else:
		rep=u'@%(uname)s @ '% pjmsg +convert_juick_timestamp(pjmsg['ts'])+u' GMT -'
		if pjmsg['photo']:
			rep+=u' PhotoRay!' % pjmsg
		if pjmsg['replies']:
			case=get_repl_case(pjmsg['replies'])
			rep+=u' %s ответ%s' % (pjmsg['replies'], case)
		else:
			rep+=u' нет ответов'
		if pjmsg['tags']:
			rep+=u'\n%(tags)s: %(body)s\n#%(mid)s\n' % pjmsg
		else:
			rep+=u'\n%(body)s\n#%(mid)s\n' % pjmsg
		return rep

def get_repl_case(num):
	num=int(num)
	if num in xrange(5,21): return u'ов'
	elif str(num).endswith('1'): return u''
	elif num in xrange(2,5): return u'а'
	else: return u'ов'

def convert_juick_timestamp(tm):
	jtm=time.strptime(tm, '%Y-%m-%d %H:%M:%S')
	if time.strftime('%Y-%m-%d',time.localtime())==time.strftime('%Y-%m-%d',jtm):
		tm=time.strftime('%H:%M:%S',jtm)
	else:
		if time.strftime('%Y',time.localtime())==time.strftime('%Y',jtm):
			tm=time.strftime('%d %b %H:%M:%S',jtm)
		else:
			tm=time.strftime('%Y %b %d  %H:%M:%S',jtm)
	return tm

##########################################################################################

def handler_juick_friend(type, source, parameters):
	try:
		int(parameters)
	except:
		reply(type, source, u'ошибочный синтаксис. прочти помощь по команде')
		return
	iq = xmpp.Iq('get')
	id = 'j'+str(random.randrange(1, 1000))
	iq.setID(id)
	query=iq.addChild('query', {}, [], 'http://juick.com/query#users')
	query.setAttr('friends',parameters)
	iq.setTo('juick@juick.com')
	JCON.SendAndCallForResponse(iq, handler_juick_answ,{'type': type, 'source': source, 'parameters': parameters})


register_command_handler(handler_juick, 'juick', ['инфо','мук','все','эксклюзив','juick'], 10, 'Работа с Juick.\nМожно посмотреть на десять последних сообщений, написав команду без параметров.\nПросмотр постов и комметариев аналогичен синтаксису бота Juick. Также есть возможность просмотреть диапазон комментариев (#1/1-10).\n', 'jlast [UID]', ['juick','juick #1','juick #1+','juick #1/1','juick #1/1-10','juick @ugnich'])
