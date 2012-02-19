#===istalismanplugin===
# -*- coding: utf-8 -*-


def set_chatroom_acc(type, source, change, user, new, option, reason=''):
	iq = xmpp.Iq('set')
	iq.setTo(source[1])
	iq.setID('set'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {option: user, change: new })
	kick.setTagData('reason', get_bot_nick(source[1])+': '+reason)
	iq.addChild(node=query)
	JCON.SendAndCallForResponse(iq, order_my_result, {'type': type, 'source': source})

def order_my_result(coze, res, type, source):
        if res:
                if xmpp.isResultNode(res):
                        reply(type, source, u'Сделано!')
                else:
                        reply(type, source, u'Выполнение невозможно!')

	
def kick_my(type, source, parameters):
        if source[1] not in GROUPCHATS.keys():
                return
	if parameters:
                set_chatroom_acc(type, source, 'role', parameters, 'none', 'nick', 'command '+source[2])
	else:
		reply(type, source, u'кого?')
		
		
def ban_my(type, source, parameters):
        if source[1] not in GROUPCHATS.keys():
                return
	if parameters:
                if parameters.count(' '):
                        parameters=parameters.split()[0]
                nicks=GROUPCHATS[source[1]]
                if parameters in nicks:
                        set_chatroom_acc(type, source, 'affiliation', parameters, 'outcast', 'nick', 'command '+source[2])
                else:
                        set_chatroom_acc(type, source, 'affiliation', parameters, 'outcast', 'jid', 'command '+source[2])
	else:
		reply(type, source, u'кого?')	
		
		
def visitor_my(type, source, parameters):	
	if parameters:
		set_chatroom_acc(type, source, 'role', parameters, 'visitor', 'nick', 'command'+source[2])
	else:
		reply(type, source, u'кого?')
		
def unban_my(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
        if parameters:
                if not parameters.count('@') and not parameters.coun('.'):
                        reply(type, source, u'Ник не найден, если вы пытаетесь разбанить по нику-введите вместо него jid пользователя!')
                set_chatroom_acc(type, source, 'affiliation', parameters, 'none', 'jid', 'command '+source[2])
	else:
		reply(type, source, u'кого?')			
		
def participant_my(type, source, parameters):	
	if parameters:
		set_chatroom_acc(type, source, 'role', parameters, 'participant', 'nick', 'command '+source[2])
	else:
		reply(type, source, u'кого?')

def handler_who_join(type,source,parameters):
        #Idea WitcherGeralt
        if parameters:
                hnd_who_join_day(type,source,parameters)
                return
        if source[1] in GROUPCHATS:
                acc=int(user_level(source[1]+'/'+source[2], source[1]))
                l=''
                n=0
                for x in GROUPCHATS[source[1]]:
                        if GROUPCHATS[source[1]][x]['ishere']==0:
                                if len(l)<940:
                                        if acc>16:
                                                n+=1
                                                l+=unicode(n)+'. '+x[:20]+' : ['+GROUPCHATS[source[1]][x]['jid'].split('/')[0][:25]+']\n'
                                        else:
                                                n+=1
                                                l+=unicode(n)+'. '+x[:20]+'\n'
                if l=='':
                        reply(type,source,u'все вроде здесь)больше никого не видел')
                        return
                if type=='public':
                        reply(type,source,u'look at private!')
                reply('private',source,u'Я здесь видел '+unicode(n)+u' юзеров:\n'+l[:1000]+u'\nхтобыл + выведет время выхода и статистику за сегодня!')

PRSN={}		
def hnd_who_join_day(type,source,parameters):
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        rep=''
        n=0
        if source[1] not in GROUPCHATS:
                return
        nicks=GROUPCHATS[source[1]]
        for x in PRSN:
                if x.count('=='):
                        s=x.split('==')
                        if s[1]==str(day):
                                if PRSN[x]['gch']==source[1]:
                                        if s[0] in nicks:
                                                if GROUPCHATS[source[1]][s[0]]['ishere']!=1:
                                                        rep+=s[0]+' '+PRSN[x]['time']+'\n'
                                                        n+=1
        if rep=='':
                reply(type,source,u'пока все здесь')
                return
        r=u'| ник | время |\n'
        reply(type,source,u'За период с '+PRSN[str(day)]+u' я здесь видел '+unicode(n)+u' юзеров:\n'+r+rep)

def hnd_more_nicks(groupchat,nick,par,par2):
        if len(nick)>19:
                return
        if nick.isspace() or nick=='':
                return
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        i=str(day)+'.'+str(month)+'.'+str(year)+'\n['+str(hour)+':'+str(minute)+':'+str(second)+']'
        t='['+str(hour)+':'+str(minute)+':'+str(second)+']'
        r=nick+'=='+str(day)
        if not str(day) in PRSN:
                PRSN[str(day)]=i
        PRSN[r]={'gch':groupchat,'time':t}
                                
                
                
def handler_where_i(type,source,parameters):
        l=''
        n=0
        try:
                for x in GROUPCHATS:
                        if x not in NOACCESS:
                                n+=1
                                l+=unicode(n)+'. '+x+' :['+unicode(get_num_online(x))+']\n'
                for s in NOACCESS:
                        n+=1
                        l+=unicode(n)+'. '+s+' no access\n'
        except:
                pass
        reply(type,source,u'Я сижу в '+unicode(n)+u' комнатах:\n'+l)

def get_num_online(groupchat):
        try:
                n=0
                for x in GROUPCHATS[groupchat]:
                        if GROUPCHATS[groupchat][x]['ishere']==1:
                                n+=1
                return n
        except:
                pass
        return 0

def handler_searsh_conf(type,source,parameters):
        if parameters=='' or parameters.isspace():
                reply(type,source,u'напиши кого искать')
                return
        jid = parameters
	confs = ''
	t = 0
	
	for i in range(0, len(GROUPCHATS.keys())):
		for j in range(0, len(GROUPCHATS[GROUPCHATS.keys()[i]].keys())):
			truejid = get_true_jid(GROUPCHATS.keys()[i]+'/'+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j])
			truejid = truejid.lower()
			nick = GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]
			jid = jid.lower()
			nick = nick.lower()
			try:
                                if (truejid.count(jid)>0) | (nick.count(jid)>0):
                                        if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ishere']==1:
                                                t += 1
                                                if t<12 and len(confs)<600:
                                                        confs += str(t)+'. '+ GROUPCHATS.keys()[i] + ' ('+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]+') '+truejid+'\n'
                        except:
                                pass
	if confs == '':
		aa = u'No found =('
	else:
		aa = u'I seen :\n № [room][nick][jid]\n'+ confs
	reply(type, source, aa[:900])


def handler_ban_everywhere(type, source, jid):
        if not GROUPCHATS:
                reply(type, source, u'Список конференций пуст!')
                return
	if not jid:
                reply(type, source, u'и?')
                return
	for gch in GROUPCHATS.keys():
                try:
                        iq = xmpp.Iq('set')
                        iq.setTo(gch)
                        iq.setID('ban'+str(random.randrange(1000, 9999)))
                        query = xmpp.Node('query')
                        query.setNamespace('http://jabber.org/protocol/muc#admin')
                        query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
                        iq.addChild(node=query)
                        JCON.send(iq)
                except:
                        pass
	reply(type, source, u'сделано!')

def handler_unban_everywhere(type, source, jid):
	if not GROUPCHATS:
                reply(type, source, u'Список конференций пуст!')
                return
        if not jid:
                reply(type, source, u'и?')
                return
	for gch in GROUPCHATS.keys():
                try:
                        iq = xmpp.Iq('set')
                        iq.setTo(gch)
                        iq.setID('unban'+str(random.randrange(1000, 9999)))
                        query = xmpp.Node('query')
                        query.setNamespace('http://jabber.org/protocol/muc#admin')
                        query.addChild('item', {'jid':jid, 'affiliation':'none'})
                        iq.addChild(node=query)
                        JCON.send(iq)
                except:
                        pass
        reply(type, source, u'Убрано!')

def handler_botnick(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if len(parameters)>21:
                reply(type, source, u'А не большой ник будет?')
                return
        if parameters:
                file = 'dynamic/'+source[1]+'/bot.list'
                fp = open(file, 'r')
                txt = eval(fp.read())
                if source[1] in txt:
                        txt[source[1]]['nick']=parameters.strip()
                        write_file(file, str(txt))
                        join_groupchat(source[1],parameters)
                        try:
                                global GET_BOT_NICK
                                GET_BOT_NICK[source[1]]=parameters
                        except:
                                pass

def owner_my(type, source, parameters):
        jid=''
        if source[1] in GROUPCHATS:
                if parameters:
                        if parameters.count('@') and parameters.count('.'):
                                jid = parameters
                        else:
                                jid=get_true_jid(source[1] + '/' + parameters)
                set_chatroom_acc(type, source, 'affiliation', jid, 'owner', 'jid', 'command '+source[2])
	


def member_my(type,source,parameters):
        jid=''
        if source[1] in GROUPCHATS:
                if parameters:
                        if parameters.count('@') and parameters.count('.'):
                                jid = parameters
                        else:
                                jid=get_true_jid(source[1] + '/' + parameters)
                set_chatroom_acc(type, source, 'affiliation', jid, 'member', 'jid', 'command '+source[2])
	

def handler_acshow_glob(type,source,parameters):
        file='dynamic/globaccess.cfg'
        fp=open(file, 'r')
        txt=eval(fp.read())
        fp.close()
        f=''
        j=''
        for x in txt:
                if txt[x]==100:
                        f+=x+'\n'
                if unicode(txt[x])=='-100':
                        j+=x+'\n'
        if j=='':
                j=u'not found\n'
        if f=='':
                f=u'not found\n'
        file_c='dynamic/accbyconf.cfg'
        fpc=open(file_c, 'r')
        xxx=eval(fpc.read())
        fpc.close()
        m=''
        for z in xxx:
                for c in xxx[z]:
                        m+=z+' : '+c+'='+str(xxx[z][c])+'\n'
        if m=='':
                m=u'not found'
        if type=='public':
                reply(type,source,u'seen to privat!')
        reply('private',source,u'админы бота:\n'+f+u'полный игнор:\n'+j+u'доступы конференций:\n'+m)

register_leave_handler(hnd_more_nicks)
register_command_handler(owner_my, 'овнер', ['админ','все'], 30, 'Дает овнера определенному нику или JID-у', 'овнер <nick>', ['овнер Guy'])
register_command_handler(handler_acshow_glob, 'доступы', ['инфо','мук','все'], 40, 'доступы', 'доступы', ['доступы'])
register_command_handler(handler_ban_everywhere, 'fullban', ['админ','все'], 100, 'Бан пользователя во всех конференциях где сидит бот', 'fullban jid', ['fullban vasya_pupkin@jabber.ru'])
register_command_handler(handler_unban_everywhere, 'fullunban', ['админ','все'], 100, 'Достает jid из бана во всех комнатах где сидит бот', 'fullunban jid', ['fullunban vasya_pupkin@jabber.ru'])
register_command_handler(handler_where_i, 'хдея', ['все'], 20, 'показывает конфы в которых сидит бот', 'хдея', ['хдея'])
register_command_handler(handler_searsh_conf, '!хде', ['все'], 20, 'поиск по всем комнатам где сидит бот,ищет по совпадению в jid-e или нике', 'хде <ник>', ['хде вася'])
register_command_handler(kick_my, 'кик', ['админ','все'], 15, 'кикает посетителя из конфы', 'кик <nick>', ['кик Guy'])
register_command_handler(handler_who_join, 'хтобыл', ['все'], 0, 'хтобыл', 'хтобыл', ['хтобыл'])
register_command_handler(ban_my, 'бан', ['админ','все'], 20, 'банит посетителя в данной конфе', 'бан <nick>', ['бан Guy'])
register_command_handler(visitor_my, 'девойс', ['админ','все'], 15, 'лишает посетителя голоса', 'девоис <nick>', ['девоис Guy'])
register_command_handler(unban_my, 'избани', ['админ','все'], 20, 'удаляет жид из бан листа', 'избани <nick>/<JID>', ['избани Guy'])
register_command_handler(participant_my, 'войс', ['админ','все'], 15, 'даёт посетителю право голоса', 'воис <nick>', ['воис Guy'])		
register_command_handler(handler_botnick, 'ботник', ['админ','все'], 20, 'меняет ник бота', 'ботник <nick>', ['ботник Guy'])		
register_command_handler(member_my, 'мембер', ['админ','все'], 20, 'делает юзера постоянным участником по jid-y или нику', 'мембер <nick>', ['мембер Guy'])			
