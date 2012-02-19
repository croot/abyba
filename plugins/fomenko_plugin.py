#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
# Modifications Copyright © 2010 Evgеn

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_TVru_fomenko(type, source, parameters):
	import urllib2
	import re
	import time

	req = urllib2.Request('http://www.fomenko.ru/foma/lenta/text.html')
	r = urllib2.urlopen(req)
	radky=r.readlines()
	if len(radky)>=16:
		radky = radky[15].decode('windows-1251')
		if radky.count('<b>')>=1:
			radky = radky.split('<b>')
			radky = radky[1]
			reply(type,source, radky)
			return
	reply(type,source, u'Что-то не то, передайте админу бота!')

register_command_handler(handler_TVru_fomenko, 'фоменко', ['фан','все'], 10, 'Показать прикол Фоменко "фоменко"', 'фоменко', ['фоменко'])
