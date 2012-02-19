#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  weather_plugin.py

#  Автор: 40tman

import urllib
import urllib2
import re

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')


def weather_get(type, source, parameters):
        if not parameters:
                reply(type, source, u'Город?')
                return
        n='3'
        if parameters.count(' '):
                for x in parameters:
                        if x.isdigit():
                                n='10'
                                parameters=parameters.split()[0]
                                break
        try:
                url = u'http://wap.weather.mail.ru/search.xhtml'
                values = {'name' : parameters.encode('utf8') }
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                the_page = response.read()
                #the_page.decode('utf8')
        except:
                handler_weather_pogoda(type, source, parameters)
                return
        if the_page.count('/index.xhtml?city='):
                the_page=the_page.replace('<!-- START: maintable -->','').replace('<!-- END: maintable -->','')
                try:
                        m = re.findall('<td><div>(.*)</a></div>',the_page)
                        rep=''
                        for x in m[0]:
                                if x.isdigit:
                                        rep+=x
                        kod=rep
                except:
                        handler_weather_pogoda(type, source, parameters)
                        return
        else:
                handler_weather_pogoda(type, source, parameters)
                return

        try:
                r = urllib.urlopen('http://wap.weather.mail.ru/forecast'+n+'.xhtml?city=%KOD%'.replace('%KOD%', kod))
                dom = r.read()
        except:
                handler_weather_pogoda(type, source, parameters)
                return

        RES = ''
        ret = ''
        mtiile={}
        dom=dom.replace('&#032;','').replace('&deg;','')
        dom=decode_w(dom)
        dom=dom.replace('\n\n','').replace('изменить','').replace('\n\n\n','')
        dom=dom[65:]
        dom=dom[:-185]
        try:
                reply(type, source, dom)
        except:
                reply(type, source, u'Неизвестная ошибка!')

def decode_w(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')


# Coded by: Avinar  (avinar@xmpp.ru)


import string


def handler_weather_pogoda(type, source, parameters):
	if parameters == '':
		reply(type ,source, u'И что ты от меня хочешь?')
		return
	else:
		import urllib
		from xml.dom import minidom
		## Вычисление города
		import urllib2
		import re
		import time
		parameters = parameters.lower().replace('\n','')
		wez_file = 'dynamic/weather.txt'
		fp = file(wez_file)
		lines = fp.readlines()
		kod = ''
		for line in lines:
			line = line.split(' ')
			if unicode(line[1],"utf-8").replace('\n','')==parameters:
				kod = line[0]
				break
		if kod:
			req = urllib2.Request(u'http://informer.gismeteo.ru/xml/'+kod+u'_1.xml')
			r = urllib2.urlopen(req)
			radky=r.read()
			radky=radky.split('<FORECAST')
			weather = u'Погода по г. '+parameters.capitalize()+u':'
			for keq in radky:
#			for i in range(1,5,1):
				if not keq.count('TEMPERATURE'):
					continue
				pars = string.split(keq, '"')
				day = pars[1]
				mounth = pars[3]
				hour = pars[7]
				week = pars[13]
				cloud = pars[15]
				precipitation = pars[17]
				presmax = pars[23]
				presmin = pars[25]
				tempmax = pars[27]
				tempmin = pars[29]
				windmin = pars[31]
				windmax = pars[33]
				winddir = pars[35]
				rewmax = pars[37]
				rewmin = pars[39]
				
				if hour == '00':
					hour=u'Ночь'
				elif hour == '01':
					hour=u'Ночь'
				elif hour == '02':
					hour=u'Ночь'
				elif hour == '03':
					hour=u'Ночь'		
				elif hour == '04':
					hour=u'Ночь'
				elif hour == '05':
					hour=u'Ночь'
				elif hour == '06':
					hour=u'Утро'
				elif hour == '07':
					hour=u'Утро'		
				elif hour == '08':
					hour=u'Утро'
				elif hour == '09':
					hour=u'Утро'
				elif hour == '10':
					hour=u'Утро'
				elif hour == '11':
					hour=u'Утро'		
				elif hour == '12':
					hour=u'День'
				if hour == '13':
					hour=u'День'
				elif hour == '14':
					hour=u'День'
				elif hour == '15':
					hour=u'День'
				elif hour == '16':
					hour=u'День'		
				elif hour == '17':
					hour=u'День'
				elif hour == '18':
					hour=u'Вечер'
				elif hour == '19':
					hour=u'Вечер'
				elif hour == '20':
					hour=u'Вечер'		
				elif hour == '21':
					hour=u'Вечер'
				elif hour == '22':
					hour=u'Вечер'
				elif hour == '23':
					hour=u'Вечер'
				elif hour == '24':
					hour=u'Ночь'		
						
				
				if mounth == '01':
					mounth=u'Января'
				elif mounth == '02':
					mounth=u'Февраля'
				elif mounth == '03':
					mounth=u'Марта'
				elif mounth == '04':
					mounth=u'Апреля'
				elif mounth == '05':
					mounth=u'Мая'
				elif mounth == '06':
					mounth=u'Июня'
				elif mounth == '07':
					mounth=u'Июля'
				elif mounth == '08':
					mounth=u'Августа'
				elif mounth == '09':
					mounth=u'Сентября'
				elif mounth == '10':
					mounth=u'Октября'
				elif mounth == '11':
					mounth=u'Ноября'
				elif mounth == '12':
					mounth=u'Декабря'
			
    
				if week == '1':				# тут я так и не понял особо, видимо идет отсчет по английским стандартам с воскресения
					week=u'Воскресенье'				
				elif week == '2':
					week=u'Понедельник'
				elif week == '3':
					week=u'Вторник'
				elif week == '4':
					week=u'Среда'
				elif week == '5':
					week=u'Четверг'
				elif week == '6':
					week=u'Пятница'
				elif week == '7':
					week=u'Суббота'
				elif week == '8':
					week=u'Восьмесение О_о'
					
				if winddir == '0':
					winddir=u'северный'
				elif winddir == '1':
					winddir=u'северо-восточный'
				elif winddir == '2':
					winddir=u'восточный'
				elif winddir == '3':
					winddir=u'юго-восточный'
				elif winddir == '4':
					winddir=u'южный'
				elif winddir == '5':
					winddir=u'юго-западный'
				elif winddir == '6':
					winddir=u'западный'
				elif winddir == '7':
					winddir=u'северо-западный'
			
				if cloud == '0':
					cloud=u'ясно'
				elif cloud == '1':
					cloud=u'малооблачно'
				elif cloud == '2':
					cloud=u'облачно'
				elif cloud == '3':
					cloud=u'пасмурно'
				
				if precipitation == '4':
					precipitation=u'дождь'
				elif precipitation == '5':
					precipitation=u'ливень'
				elif precipitation == '6':
					precipitation=u'снег'
				elif precipitation == '7':
					precipitation=u'снег'
				elif precipitation == '8':
					precipitation=u'гроза'
				elif precipitation == '9':
					precipitation=u'нет данных'
				elif precipitation == '10':
					precipitation=u'без осадков'
				
				weather = weather + '\n'+hour+ u' (' +day+ ' ' +mounth+ ', '+week+u'):\n  температура воздуха от '+tempmin+ u' до '+tempmax+u';\n  '+cloud+u', '+precipitation+u';\n  атмосферное давление '+presmin+u'-'+presmax+u'мм.рт.ст.;\n  ветер '+winddir+ u', '+windmin+'-'+windmax+u'м/с;\n  влажность воздуха '+rewmin+'-'+rewmax+u'%;'
		
		
			if type=='private':
				reply(type ,source, weather+u'\nПогода предоставлена gismeteo')
				return
			else:
				reply(type,source,u'Ушла в приват')
				reply('private', source, weather+u'\nПогода предоставлена gismeteo')
				return
		else:
			reply(type ,source, u'Город "'+parameters.capitalize()+u'" не найден. Может неправильно написали?')
		return

register_command_handler(weather_get, 'погода', ['все', 'инфо'], 0, 'Погода с сайта wap.mail.ru', 'Погода <город>', ['погода Новосибирск'])
