#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  disco_plugin.py

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

disco_pending=[]

def handler_disco(type, source, parameters):
	if parameters:
		parst=parameters.split(' ', 2)
		stop,srch,tojid='','',parst[0]
		if not tojid.count('.') and not tojid.count('@'):
                        tojid=tojid+u'@conference.jabber.ru'
		if len(parst)==1:
			if type == 'public': stop=10
			else: stop=50
			srch=None
		elif len(parst)>1:
			try:
				stop=int(parst[1])
				try:
					srch=parst[2]
				except:
					srch=None
			except:
				srch=parst[1]
				if type == 'public': stop=10
				else: stop=50
			if type == 'public':
				if stop>50: stop='50'
			else:
				if stop>250: stop='250'
		iq = xmpp.Iq('get')
		id='dis'+str(random.randrange(1, 9999))
		globals()['disco_pending'].append(id)
		iq.setID(id)
		query=iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
		if len(tojid.split('#'))==2:
			query.setAttr('node',tojid.split('#')[1])
			iq.setTo(tojid.split('#')[0])
		else:
			iq.setTo(tojid)
		JCON.SendAndCallForResponse(iq, handler_disco_ext, {'type': type, 'source': source, 'stop': stop, 'srch': srch, 'tojid': tojid})
	else:
		reply(type,source,u'ииии?')
		return

def handler_disco_ext(coze, res, type, source, stop, srch, tojid):
	disco=[]
	rep,trig='',0
	id=res.getID()
	if id in globals()['disco_pending']:
		globals()['disco_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		reply(type, source, u'вглюкнуло...')
		return
	if res:
		if res.getType() == 'result':
			props=res.getQueryChildren()
			if not isinstance(props, list):
				reply(type, source, u'пустое диско')
				return
			for x in props:
				att=x.getAttrs()
				if att.has_key('name'):
					try:
						if tojid.count('@'):
							raise TypeError
						st=re.search('^(.*) \((.*)\)$', att['name']).groups()
						disco.append([st[0],att['jid'],st[1]])
						trig=1
					except:
						if not trig:
							temp=[]
							if att.has_key('name'):
								temp.append(att['name'])
							if att.has_key('jid') and not tojid.count('@'):
								temp.append(att['jid'])
							if att.has_key('node'):
								temp.append(att['node'])
							disco.append(temp)
				else:
					disco.append([att['jid']])
			if disco:
				handler_disco_answ(type,source,stop,disco,srch)
			else:
				reply(type, source, u'пустое диско')
			return
		else:
                        ecode = res.getErrorCode()
			rep = u'не могу'
			if ecode==u'403':
                                rep=u'Запрещено в настройках конфы/сервера (403)'
                        elif ecode==u'404':
                                rep=u'Конференции, сервера либо сервиса с таким адресом не существует (404)'
	else:
		rep = u'аблом...'
	reply(type, source, rep)


def handler_disco_answ(type,source,stop,disco,srch):
        try:
                handler_sisco_try(type,source,stop,disco,srch)
        except:
                pass

def handler_sisco_try(type,source,stop,disco,srch):
	total=0
	if total==stop:
		reply(type, source, u'всего '+str(len(disco))+u' пунктов')
		return
	rep,dis,disco = u'надискаверил:\n',[],sortdis(disco)
	for item in disco:
		if len(item)==3:
			total+=1
			if srch:
				if srch.endswith('@'):
					if item[1].startswith(srch):
						dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']: '+str(item[2]))
						break
					else:
						continue
				else:
					if not item[0].count(srch) and not item[1].count(srch):
						continue
			try:
                                dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']: '+str(item[2]))
                        except:
                                pass
			if len(dis)==stop:
				break
		elif len(item)==2:
			total+=1
			if srch:
				if not item[0].count(srch) and not item[1].count(srch):
					continue
			try:
                                dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']')
                        except:
                                pass
			if len(dis)==stop:
				break
		else:
			total+=1
			if srch:
				if not item[0].count(srch):
					continue
			try:
                                dis.append(str(total)+u') '+item[0])
                        except:
                                pass
			if len(dis)==stop:
				break
	if dis:
		if len(disco)!=len(dis):
			try:
                                dis.append(u'всего '+str(len(disco))+u' пунктов')
                        except:
                                pass
	else:
		rep=u'пустое диско'
	reply(type, source, rep+u'\n'.join(dis))

def sortdis(dis):
	disd,diss,disr=[],[],[]
	for x in dis:
		try:
			int(x[2])
			disd.append(x)
		except:
			diss.append(x)
	disd.sort(lambda x,y: int(x[2]) - int(y[2]))
	disd.reverse()
	diss.sort()
	for x in disd:
		disr.append(x)
	for x in diss:
		disr.append(x)
	return disr

disco=[]

register_command_handler(handler_disco, 'диско', ['мук','инфо','все'], 10, 'Показывает результаты обзора сервисов для указанного JID.\nТакже можно запросить обзор по узлу (node). Формат запроса jid#node.\nВторой или третий (если также даётся ограничитель кол-ва) параметр - поиск. Ищет заданное слово в JID и описании элемента диско. Если поисковым словом задать имя конференции до названия сервера (например qwerty@), то покажет место этой конференции в общем рейтинге.\nВ общий чат может дать max 50 результатов, без указания кол-ва - 10.\n В приват может дать max 250, без указания кол-ва 50.', 'диско <сервер> <кол-во результатов> <поисковая строка>', ['диско jabber.aq','диско conference.jabber.aq 5','диско conference.jabber.aq qwerty','диско conference.jabber.aq 5 qwerty','диско conference.jabber.aq qwerty@', 'диско jabber.aq#services'])
