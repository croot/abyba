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

def handler_commoff(type,source,parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	na=[u'доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'свал',u'рестарт',u'globacc',u'команды',u'sh',u'exec',u'commoff',u'common']
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,rep,commoff=u'',u'',u'',u'',0,0,0,0,u'',[]
	if not source[1] in COMMOFF:
		get_commoff(source[1])
	commoff=COMMOFF[source[1]]
	DBPATH='dynamic/'+source[1]+'/config.cfg'
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if not y in commoff:
						commoff.append(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'были отключены следующие команды:\n'+valcomm
		if alrcomm:
			rep+=u'\nследующие команды уже отключены:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nперечисленное ниже не является командами:\n'+notvalcomm
		if npcomm:
			rep+=u'\nследующие команды неотключаемы:\n'+npcomm
		if not GCHCFGS[source[1]].has_key('commoff'):
			GCHCFGS[source[1]]['commoff']='commoff'
			GCHCFGS[source[1]]['commoff']=[]
		GCHCFGS[source[1]]['commoff']=commoff
		write_file(DBPATH, str(GCHCFGS[source[1]]))
		get_commoff(source[1])
	else:
		for x in commoff:
			vcnt+=1
			valcomm+=str(vcnt)+u') '+x+u'\n'
		if valcomm:
			rep=u'в этой конференции отключены следующие команды:\n'+valcomm
		else:
			rep=u'в этой конференции включены все команды'


	reply(type,source,rep.strip())

def handler_common(type,source,parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	na=[u'доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'свал',u'рестарт',u'globacc',u'команды',u'sh',u'exec',u'commoff',u'common']
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,rep,commoff=u'',u'',u'',u'',0,0,0,0,u'',[]
	if not source[1] in COMMOFF:
		get_commoff(source[1])
	commoff=COMMOFF[source[1]]
	DBPATH='dynamic/'+source[1]+'/config.cfg'
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if y in commoff:
						commoff.remove(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'следующие команды были включены:\n'+valcomm
		if alrcomm:
			rep+=u'\nследующие команды не были включены, поскольку они не были отключены:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nперечисленное ниже не является командами:\n'+notvalcomm
		if npcomm:
			rep+=u'\nследующие команды неотключаемы:\n'+npcomm
		if not GCHCFGS[source[1]].has_key('commoff'):
			GCHCFGS[source[1]]['commoff']='commoff'
			GCHCFGS[source[1]]['commoff']=[]
		GCHCFGS[source[1]]['commoff']=commoff
		write_file(DBPATH, str(GCHCFGS[source[1]]))
		get_commoff(source[1])
	else:
		rep=u'ииии?'

	reply(type,source,rep.strip())

def get_commoff(gch):
	try:
		if GCHCFGS[gch].has_key('commoff'):
			commoff=GCHCFGS[gch]['commoff']
			COMMOFF[gch]=commoff
		else:
			COMMOFF[gch]=gch
			COMMOFF[gch]=[]
	except:
		pass


register_command_handler(handler_commoff, 'commoff', ['админ','мук','все'], 20, 'Отключает определённые команды для текущей конференции, без параметров показывает список уже отключенных команд.', 'commoff [команды]', ['commoff','commoff тык диско версия пинг'])
register_command_handler(handler_common, 'common', ['админ','мук','все'], 20, 'Включает определённые команды для текущей конференции.', 'common [команды]', ['common тык диско версия пинг'])

register_stage1_init(get_commoff)
