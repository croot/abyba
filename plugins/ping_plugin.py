#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  ping_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

ping_pending=[]
def handler_ping(type, source, parameters):
        param=''
	nick=parameters
	groupchat=source[1]
	iq = xmpp.Iq('get')
	id = 'p'+str(random.randrange(1, 1000))
	globals()['ping_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				if GROUPCHATS[groupchat][nick]['ishere']==0:
					reply(type, source, u'а он тут? :-O')
					return
				param=nick
				jid=groupchat+'/'+nick
				iq.setTo(jid)
		else:
                        iq.setTo(parameters.strip())
                        param = parameters.strip()
	else:
		jid=groupchat+'/'+source[2]
		iq.setTo(jid)
		param=''
	t0 = time.time()
	JCON.SendAndCallForResponse(iq, handler_ping_answ,{'t0': t0, 'mtype': type, 'source': source, 'param': param})

def handler_ping_answ(coze, res, t0, mtype, source, param):
        ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
        id = res.getID()
        rep=''
	if id in globals()['ping_pending']:
		globals()['ping_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
			t = time.time()
			rep = u'понг от '
			if param:
				rep += param
			else:
				rep += u'тебя'
			rep+=u' '+str(round(t-t0, 3))+u' секунд'
		else:
                        if res.getType() == 'error' and res.getErrorCode() in ERROR:
                                reply(mtype, source, u'Ответ от '+param+': '+res.getErrorCode()+' '+ERROR[res.getErrorCode()])
                                return
                        else:
                                reply(mtype, source, u'Ответ от '+param+u': не пингуется')
                                return
	reply(mtype, source, rep)

BPING={}

def hnd_user_bot_ping(type, source, parameters):
        hnd_bot_ping(type+'spec',source)
        
def hnd_bot_ping(type,source):
        n=random.randrange(0, 5)
        if type in ['public','private'] and n in range(0, 4):
                return
        time.sleep(0.1)
        who=get_true_jid(source[1]+'/'+source[2])
        tim=time.time()
        jid=GENERAL_CONFIG('JID')
        iq = xmpp.Iq('get')
	id = 'p'+str(random.randrange(1, 1000))
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	iq.setTo(jid)
	try:
                JCON.SendAndCallForResponse(iq, hnd_botp_a,{'tim': tim,'type':type,'source':source,'who':who})
        except:
                pass

def hnd_botp_a(coze,res,tim,type,source,who):
        try:
                if res:
                        if type in ['privatespec','publicspec']:
                                t='private'
                                if type[:2]=='pu':
                                        t='public'
                                reply(t, source, u'Пинг бота '+str(round(time.time()-tim, 3))+u' секунд')
                                return
                        t=round(time.time() - tim, 0)
                        print str(t)
                        if t>5:
                                if not who in BPING:
                                        reply(type,source,u'что-то я подвис')
                                        BPING[who]={'t':time.time()}
                                        return
                                else:
                                        if time.time()-BPING[who]['t']<1000:
                                                return
                                        else:
                                                reply(type,source,u'что-то я подвис')
                                                BPING[who]['t']=time.time()
        except:
                pass

def hnd_rm_control(prs):
        try:
                if not RM_CONT:
                        return
                else:
                        for x in RM_CONT:
                                if time.time()-RM_CONT[x]['t']<60:
                                        return
                                else:
                                        nick=RM_CONT[x]['nick']
                                        join_groupchat(x,nick)
        except:
                pass

register_presence_handler(hnd_rm_control)
register_command_handler(hnd_user_bot_ping, 'ботпинг', ['инфо','мук','все'], 20, 'Проверка скорости реакции бота.', 'ботпинг', ['ботпинг'])	
register_command_handler(handler_ping, 'пинг', ['инфо','мук','все'], 0, 'Пингует тебя или определённый ник или сервер.', 'пинг [ник]', ['пинг guy','пинг jabber.aq'])	
register_command_handler(handler_ping, '.', ['инфо','мук','все'], 0, 'Пингует тебя или определённый ник или сервер.', '. [ник]', ['. guy','. jabber.aq'])
