#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  horo_plugin.py

#  Автор: 40tman

import urllib
import urllib2
import re

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')



def horo_get(type, source, parameters):
        if not parameters:
                reply(type, source, u'Знак?')
                return
        ZNAKI={u'овен':'1',u'телец':'2',u'близнецы':'3',u'рак':'4',u'лев':'5',u'дева':'6',u'весы':'7',u'скорпион':'8',u'стрелец':'9',u'козерог':'10',u'водолей':'11',u'рыбы':'12'}
        if not parameters.lower() in ZNAKI.keys():
                return
        zod=ZNAKI[parameters.lower()]
        try:
                url = u'http://wap.horo.mail.ru/prediction.html?sign=%s&time=1' % (zod)
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                page = response.read()
                od = re.search('<div class="p">',page)
		b1 = page[od.end():]
		dom = b1[:re.search('</div>',b1).start()]
        except:
                reply(type, source, u'Не возможно установить соединение, попробуйте позже.')
                return

        RES = ''
        ret = ''
        dom=dom.replace('&#032;','').replace('&deg;','')
        try: dom=decode_w(dom)
        except: dom=decode(dom)
        dom=dom.replace('\n\n','\n').replace('&ndash;','-').replace('изменить','').replace('\n\n','').replace(chr(10),'')
        wh=(u'Гороскоп '+parameters[:1].upper()+parameters[1:]+u',Сегодня.\n').encode('utf8')
        try: reply(type, source, wh+dom)
        except: reply(type, source, u'Неизвестная ошибка!')


register_command_handler(horo_get, 'гороскоп', ['все', 'инфо'], 0, 'Гороскоп с сайта wap.mail.ru', 'Гороскоп <знак>', ['Гороскоп Лев'])
