#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  macro_plugin.py

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

def prog_grabru(code):
	import urllib2
	import re
	import time

	kod=code.lower()
	kod=kod.strip()
	if kod == '' or not kod.isdecimal():
		program = u'И какой канал мне показывать? Номер канала можно узнать, дав команду боту "тв_лист"'
		return program
	req = urllib2.Request('http://tv.yandex.ru/?mode=print&channel='+kod)
	r = urllib2.urlopen(req)
	radky=r.readlines()
	program = ''
	for x in radky:
		if x.find('<div>') != -1:
			if re.search('<.*?>\d', x):
				program+='\n'+re.sub(r'<.*?>', '', x).replace('\n', '')
	if program == '':
		program = u'Нет программы на сегодня.'
	return program

def prog_grabru2(code):
	import urllib2
	import re
	import time

	kod=code.lower()
	kod=kod.strip()
	if kod == '' or not kod.isdecimal():
		program = u'И какой канал мне показывать? Номер канала можно узнать, дав команду боту "тв_лист"'
		return program
	req = urllib2.Request('http://tv.yandex.ru/?flag=&channel='+kod)
	r = urllib2.urlopen(req)
	radky=r.readlines()
	radky=''.join(radky)
	if radky.count('<b><a href="/?day=')>=1:
		radky = radky.replace('<b><a href="/?day=', 'EVGEN')
		radky = radky.replace('&amp;hour=16&amp', 'EVGEN')
		radky = radky.split('EVGEN')
		radky = radky[1]
		if radky.count('&'):
                        radky=radky.split('&')[0]
		req = urllib2.Request('http://tv.yandex.ru/?day='+radky+'&hour=4&period=24&mode=print&channel='+kod)
		r = urllib2.urlopen(req)
		radky=r.readlines()
		program = ''
		for x in radky:
			if x.find('<div>') != -1:
				if re.search('<.*?>\d', x):
					program+='\n'+re.sub(r'<.*?>', '', x).replace('\n', '')
		if program == '':
			program = u'Нет программы на сегодня.'
		return program
	program = u'Что-то сломалось'
	return program

def prog_listru():
	import urllib2
	import re
	import time

	req = urllib2.Request('http://tv.yandex.ru/')
	r = urllib2.urlopen(req)
	radky=r.readlines()
	program='\n'
	for x in radky:
		if x.find('<option value="') != -1:
			program+=re.sub('\xc2\xa0\xc2\xa0\xc2\xa0', '', re.sub('/s*', '', re.sub(r'</.*?>', '', x)).replace('">', '-').replace('<option value="', '').replace('\n', '').replace('\t', '').replace('\r', ''))+',  '
	return program

def handler_TVru_get(type, source, parameters):
	reply(type,source, prog_grabru(parameters))

def handler_TVru_get2(type, source, parameters):
	if type == 'public':
		reply(type,source,u'смотри приват!')
	reply('private',source, prog_grabru2(parameters))

def handler_TVru_list(type, source, parameters):
	if type == 'public':
		reply(type,source,u'смотри приват!')
	rep=''
	f=prog_listru().split(',')
	f.sort(tv_sort)
	for x in f:
                rep+=x+','
	reply('private',source, rep)

def tv_sort(a, b):
        a=a[:5]
        b=b[:5]
        a=a[-1:]
        b=b[-1:]
        if a>b:
                return 1
        if a<b:
                return -1
        return 0

def handler_TVru_search(type, source, parameters):
        if not parameters or parameters.isspace():
                return
        parameters=parameters.lower()
	if type == 'public':
		reply(type,source,u'смотри приват!')
	rep=''
	f=prog_listru().split(',')
	f.sort(tv_sort)
	for x in f:
                x=x.decode('utf-8','replace')
                x=x.lower()
                if x.count('-'):
                        c=x.split('-')[1]
                        if c.count(parameters):
                                rep+=x+'\n'
        if not rep or rep.isspace():
                reply('private', source, u'Ничего не найдено!')
                return
	reply('private',source, rep)

register_command_handler(handler_TVru_search, 'тв_найти', ['фан','все'], 11, 'Ищет код по названию канала или по совпадению', 'тв_найти канал', ['тв_найти Discovery'])	
register_command_handler(handler_TVru_get2, 'тв_полностью', ['фан','все'], 11, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист"', 'тв_полностью [номер канала]', ['тв_полностью 144'])
register_command_handler(handler_TVru_get, 'тв', ['фан','все'], 11, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист"', 'тв [номер канала]', ['тв 144'])
register_command_handler(handler_TVru_list, 'тв_лист', ['фан','все'], 11, 'Просмотреть номера каналов чтобы потом узнать телепрограму', 'тв_лист', ['тв_лист'])
