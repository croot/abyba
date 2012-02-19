#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  commoff_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

poke_nicks={}

def handler_poke(type, source, parameters):
	if type=='private':
		reply(type,source,u':-P')
		return
	groupchat = source[1]
	if parameters:
		if parameters==u'last10':
			cnt=0
			rep=''
			nicks = set()
			for x in [poke_nicks[source[1]] for x in poke_nicks]:
				nicks = nicks | set(x)
			for x in nicks:
				cnt=cnt+1
				rep += str(cnt)+u') '+x+u'\n'
			reply('private',source,rep[:-1])
			return
		if not poke_nicks.has_key(source[1]):
			poke_nicks[source[1]]=source[1]
			poke_nicks[source[1]]=[]
		if len(poke_nicks[source[1]])==10:
			poke_nicks[source[1]]=[]
		else:
			poke_nicks[source[1]].append(source[2])
		if not parameters == get_bot_nick(source[1]):
			if parameters in GROUPCHATS[source[1]]:
				pokes=[]
				pokes.extend(poke_work(source[1]))
				pokes.extend(eval(read_file('static/delirium.txt'))['poke'])
				rep = random.choice(pokes)
				msg(source[1],u'/me '+rep % parameters)
			else:
				reply(type, source, u'а он тут? :-O')
		else:
			reply(type, source, u'шибко умный, да? ]:->')	
	else:
		reply(type, source, u'мазохист? :D')
		
def handler_poke_add(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
	if not parameters.count('%s'):
		reply(type, source, u'не вижу %s')
		return
	res=poke_work(source[1],1,parameters)
	if res:
		reply(type, source, u'добавлено')
	else:
		reply(type, source, u'больше нельзя')
		
def handler_poke_del(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
	if parameters=='*':
		parameters='0'
	else:
		try:
			int(parameters)
		except:
			reply(type,source,u'синтакс инвалид')
	res=poke_work(source[1],2,parameters)
	if res:
		reply(type, source, u'удалено')
	else:
		reply(type, source, u'такой нет')
		
def handler_poke_list(type, source, parameters):
	rep,res=u'',poke_work(source[1],3)
	if res:
		res=sorted(res.items(),lambda x,y: int(x[0]) - int(y[0]))
		for num,phrase in res:
			rep+=num+u') '+phrase+u'\n'
		reply(type,source,rep.strip())
	else:
		reply(type,source,u'нет пользовательских фраз')
		
def handler_test(type, source, parameters):
	reply(type,source,u'пассед')
	
def handler_clean_conf(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		for x in range(0, 21):
			msg(source[1], '')
			time.sleep(1.3)
		reply('private',source,u'очищено!')
		
def handler_afools_control(type, source, parameters):
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'синтакс инвалид')
		if int(parameters)>1:
			reply(type,source,u'синтакс инвалид')
		if parameters=="1":
			GCHCFGS[source[1]]['afools']=1
			reply(type,source,u'шуточки включены')
		else:
			GCHCFGS[source[1]]['afools']=0
			reply(type,source,u'шуточки отключены')			
	else:
		if GCHCFGS[source[1]]['afools']==1:
			reply(type,source,u'здесь шуточки включены')
		else:
			reply(type,source,u'здесь шуточки отключены')
	
			
def get_afools_state(gch):
	if not 'afools' in GCHCFGS[gch]:
		GCHCFGS[gch]['afools']=1
		
def poke_work(gch,action=None,phrase=None):
	DBPATH='dynamic/'+gch+'/delirium.txt'
	if check_file(gch,'delirium.txt'):
		pokedb = eval(read_file(DBPATH))
		if action==1:
			for x in range(1, 21):
				if str(x) in pokedb.keys():
					continue
				else:
					pokedb[str(x)]=phrase
					write_file(DBPATH, str(pokedb))
					return True
			return False
		elif action==2:
			if phrase=='0':
				pokedb.clear()
				write_file(DBPATH, str(pokedb))
				return True
			else:
				try:
					del pokedb[phrase]
					write_file(DBPATH, str(pokedb))
					return True
				except:
					return False
		elif action==3:
			return pokedb
		else:
			return pokedb.values()
	else:
		return None
		
def remix_string(parameters):
	remixed=[]
	for word in parameters.split():
		tmp=[]
		if len(word)<=1:
			remixed.append(word)
			continue
		elif len(word)==2:
			tmp=list(word)
			random.shuffle(tmp)
			remixed.append(u''.join(tmp))
		elif len(word)==3:
			tmp1=list(word[1:])
			tmp2=list(word[:-1])
			tmp=random.choice([tmp1,tmp2])
			if tmp==tmp1:
				random.shuffle(tmp)
				remixed.append(word[0]+u''.join(tmp))
			else:
				random.shuffle(tmp)
				remixed.append(u''.join(tmp)+word[-1])					
		elif len(word)>=4:
			tmp=list(word[1:-1])
			random.shuffle(tmp)
			remixed.append(word[0]+u''.join(tmp)+word[-1])
	return u' '.join(remixed)
	
register_command_handler(handler_poke, 'тык', ['фан','все','тык'], 10, 'Тыкает юзера. Заставляет его обратить внимание на вас/на чат.\nlast10 вместо ника покажет список ников, которые тыкали последними.', 'тык <ник>|<параметр>', ['тык qwerty','тык + пришиб %s','тык - 2','тык *'])
register_command_handler(handler_poke_add, 'тык+', ['фан','все','тык'], 20, 'Добавить пользовательскую фразу. Переменная %s во фразе обозначает место для вставки ника (обязательный параметр). Фраза должна быть написана от третьего лица, т.к. будет использоваться в виде "/me ваша фраза". max кол-во пользовательских фраз - 20.', 'тык+ <фраза>', ['тык+ побил %s'])
register_command_handler(handler_poke_del, 'тык-', ['фан','все','тык'], 20, 'Удалить пользовательскую фразу. Пишем номер удаляемой фразы и она удаляется навсегда. Пронумерованный список выдаёт команда "тык*". Удалить все фразы можно с помощью символа "*" вместо номера фразы.', 'тык- <номер>', ['тык- 5','тык- *'])
register_command_handler(handler_poke_list, 'тык*', ['фан','все','тык'], 20, 'Показывает пронумерованный список всех пользовательских фраз.', 'тык*', ['тык*'])
register_command_handler(handler_test, 'тест', ['фан','инфо','все'], 0, 'Тупо отвечает пассед.', 'тест', ['тест'])
register_command_handler(handler_test, 'test', ['фан','инфо','все'], 0, 'Тупо отвечает пассед.', 'test', ['test'])
register_command_handler(handler_clean_conf, 'чисть', ['фан','мук','все'], 0, 'Очищает конференцию (считает до 20).', 'фконфу', ['фконфу'])
register_command_handler(handler_afools_control, 'afools', ['фан','мук','все'], 30, 'Включает и выключает шуточки бота, которыми он порою подменяет (саму команду он всегда исполняет!) стандартный ответ команды.', 'afools <1|0>', ['afools 1','afools 0'])


register_stage1_init(get_afools_state)

POKE_ALL={}

def handler_pokeall(type, source, parameters):
    try:
        if not source[1] in GROUPCHATS.keys():
            reply(type, source, u'only to chatrooms!')
            return
        if type=='private':
            return
        if source[1] in POKE_ALL.keys():
            if 't' in POKE_ALL[source[1]]:
                if time.time() - POKE_ALL[source[1]]['t']<60:
                    reply(type, source, u'хорош тыкать уже')
                    return
                else:
                    POKE_ALL[source[1]]['t']=time.time()
        else:
            POKE_ALL[source[1]]={'t':time.time()}
        SP=[]
        for x in GROUPCHATS[source[1]]:
            if GROUPCHATS[source[1]][x]['ishere']:
                SP.append(x)
        if not len(SP)>2:
            reply(type, source, u'мы тут в двоем походу!')
            return
        txt=read_file('static/delirium.txt')
        if not txt:
            reply(type, source, u'no joke in static/delirium.txt')
            return
        while SP:
            s=random.choice(SP)
            SP.remove(s)
            pokes=[]
            pokes.extend(eval(read_file('static/delirium.txt'))['poke'])
            z=random.choice(pokes)
            if s!=get_bot_nick(source[1]):
                msg(source[1], '/me '+z % s)
                time.sleep(1.5)
    except:
        raise
        reply(type, source, u'у когото из списка неприкосновенность,поэтому тыкать не буду!')

register_command_handler(handler_pokeall, 'тык_всех', ['все'], 10, 'Тыкает всех', 'тык_всех', ['тык_всех'])



