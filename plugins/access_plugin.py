#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  access_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.


def handler_access_login(type, source, parameters):
	if type == 'public':
		reply(type, source, u'эту команду нужно было выполнять в привате!')
	jid = get_true_jid(source)
	if parameters.strip() == ADMIN_PASSWORD:
		GLOBACCESS[jid]=100
		reply('private', source, u'пароль принят, глобальный полный доступ выдан')
	else:
		reply('private', source, u'неверный пароль')

def handler_access_logout(type, source, parameters):
	jid = get_true_jid(source)
	del GLOBACCESS[jid]
	reply(type, source, u'доступ снят')

def handler_access_view_access(type, source, parameters):
	accdesc={'-100':u'(полный игнор)','-1':u'(заблокирован)','0':u'(никто)','1':u'(пасхалка :) )','10':u'(юзер)','11':u'(мембер)','15':u'(модер)','16':u'(модер)','20':u'(админ)','30':u'(овнер)','40':u'(джойнер)','100':u'(админ бота)'}
	if not parameters:
		level=str(user_level(source[1]+'/'+source[2], source[1]))
		if level in accdesc.keys():
			levdesc=accdesc[level]
		else:
			levdesc=''
		reply(type, source, level+u' '+levdesc)
	else:
                reply(type, source, u'Информация по доступам временно недоступна!')
		#if not source[1] in GROUPCHATS:
		#	reply(type, source, u'это возможно только в конференции')
		#	return
		#nicks = GROUPCHATS[source[1]].keys()
		#if parameters.strip() in nicks:
		#	level=str(user_level(source[1]+'/'+parameters.strip(),source[1]))
		#	if level in accdesc.keys():
		#		levdesc=accdesc[level]
		#	else:
		#		levdesc=''
		#	reply(type, source, level+' '+levdesc)
		#else:
		#	reply(type, source, u'а он тут? :-O')

def handler_access_set_access(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	splitdata = string.split(parameters)
	if len(splitdata) > 1:
		try:
			int(splitdata[1].strip())
		except:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
		if int(splitdata[1].strip())>100 or int(splitdata[1].strip())<-100:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
	nicks=GROUPCHATS[source[1]]
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	us=splitdata[0].strip()
	if not splitdata[0].strip() in nicks and us.count('@'):
                tjidto=splitdata[0].strip()
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	tjidsource=get_true_jid(source)
	groupchat=source[1]
	jidacc=user_level(source, groupchat)
	toacc=user_level(tjidto, groupchat)

	if len(splitdata) > 1:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				if int(splitdata[1]) > int(jidacc):
					reply(type, source, u'недостаточно прав')
					return
			elif int(toacc) > int(jidacc):
				reply(type, source, u'недостаточно прав')
				return
			elif int(splitdata[1]) >= int(jidacc):
				reply(type, source, u'недостаточно прав')
				return
	else:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				pass
			elif int(toacc) > int(jidacc):
				reply(type, source, u'недостаточно прав')
				return

	if len(splitdata) == 1:
		change_access_perm(source[1], tjidto)
		if splitdata[0].strip()==source[2]:
			reply(type, source, u'постоянный доступ снят. тебе необходимо перезайти в конференцию')
		else:
			reply(type, source, u'постоянный доступ снят. %s, перезайди в конференцию' % splitdata[0].strip())
	elif len(splitdata) == 2:
		change_access_temp(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'доступ выдан до выхода из конференции')
	elif len(splitdata) == 3:
		change_access_perm(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'выдан постоянный доступ')

def handler_access_set_access_glob(type, source, parameters):
	#if not source[1] in GROUPCHATS:
	#	reply(type, source, u'это возможно только в конференции')
	#	return
	if parameters:
		splitdata = parameters.strip().split()
		if len(splitdata)<1 or len(splitdata)>2:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
		nicks=''
		if source[1] in GROUPCHATS:
                        nicks=GROUPCHATS[source[1]].keys()
		tjidto=get_true_jid(source[1]+'/'+splitdata[0])
		if not splitdata[0].strip() in nicks:
                        if splitdata[0].count('@'):
                                tjidto=splitdata[0]
                        else:
                                reply(type,source,u'ник либо содержит пробелы,либо юзера нет в чате!')
                                return
		if len(splitdata)==2:
			change_access_perm_glob(tjidto, int(splitdata[1]))
			reply(type, source, u'дал')
		else:
			change_access_perm_glob(tjidto)
			reply(type, source, u'снял')

def get_access_levels():
	global GLOBACCESS
	global ACCBYCONFFILE
	GLOBACCESS = eval(read_file(GLOBACCESS_FILE))
	for jid in ADMINS:
		GLOBACCESS[jid] = 100
		write_file(GLOBACCESS_FILE, str(GLOBACCESS))
	ACCBYCONFFILE = eval(read_file(ACCBYCONF_FILE))

register_command_handler(handler_access_login, 'логин', ['доступ','админ','все'], 0, 'Авторизоваться как админиcтратор бота. Использовать только в привате!', 'логин <пароль>', ['логин мой_пароль'])
register_command_handler(handler_access_login, 'логаут', ['доступ','админ','все'], 0, 'Снять авторизацию.', 'логаут', ['логаут'])
register_command_handler(handler_access_view_access, 'доступ', ['доступ','админ','все'], 0, 'Показывает уровень доступа определённого ника.\n-100 - абсолютное игнорирование, все сообщения от пользователя с таким доступом будут пропускатся на уровне ядра бота\n-1 - не сможет сделать ничего\n0 - очень ограниченное кол-во команд и макросов, автоматически присваивается гостям (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается пользователям (participant)\n11 - расширенный набор команд и макросов, автоматически присваивается участникам (member)\n15 (16) - набор команд и макросов для модераторов, автоматически присваивается модераторам (moderator)\n20 - набор команд и макросов для администраторов, автоматически присваивается администраторам конференции (admin)\n30 - набор команд и макросов для владельца, автоматически присваиватся владельцам конференции (owner)\n40 - не реализовано сейчсас толком, позволяет пользователю с этим доступом заводить и выводить бота из конференций + все возможности доступа 30\n100 - администратор бота, может всё.', 'доступ [ник]', ['доступ', 'доступ guy'])
register_command_handler(handler_access_set_access, 'дать_доступ', ['доступ','админ','все'], 15, 'Устанавливает или снимает (если ник писать без уровня, после снятия доступа нужно обязательно перезайти в конференцию) уровень доступа для определённого ника на определённый уровень. Поддерживаются только ники без пробела. Если указываеться третий параметр, то изменение происходит навсегда, иначе установленный уровень будет действовать до выхода бота или пользователя из конференции.\n-100 - абсолютное игнорирование, все сообщения от пользователя с таким доступом будут пропускатся на уровне ядра бота\n-1 - не сможет сделать ничего\n0 - очень ограниченное кол-во команд и макросов, автоматически присваивается гостям (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается пользователям (participant)\n11 - расширенный набор команд и макросов, автоматически присваивается участникам (member)\n15 (16) - набор команд и макросов для модераторов, автоматически присваивается модераторам (moderator)\n20 - набор команд и макросов для администраторов, автоматически присваивается администраторам конференции (admin)\n30 - набор команд и макросов для владельца, автоматически присваиватся владельцам конференции (owner)\n40 - не реализовано сейчсас толком, позволяет пользователю с этим доступом заводить и выводить бота из конференций + все возможности доступа 30\n100 - администратор бота, может всё.', 'дать_доступ <ник> [уровень] [навсегда]', ['дать_доступ guy 100', 'дать_доступ guy 100 что-нибудь'])
register_command_handler(handler_access_set_access_glob, 'глобдоступ', ['доступ','суперадмин','все'], 100, 'Устанавливает или снимает (если ник писать без уровня) уровень доступа для определённого ника на определённый уровень ГЛОБАЛЬНО. Поддерживаются только ники без пробела.', 'глобдоступ <ник|jid> [уровень]', ['глобдоступ guy 100','глобдоступ guy'])

register_stage0_init(get_access_levels)
