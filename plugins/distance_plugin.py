#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  distance_between_cities.py


import re,urllib

def handler_distance_between_cities(type, source, parameters):
	try:
		if parameters=='':
			reply(type,source,u'смотри хелп к команде')
			return
		parameters=parameters.strip().lower() 
		parameters=parameters.split(' ')
		if len(parameters)<2 or len(parameters)>2:
			reply(type,source,u'смотри хелп к команде')
			return
		parameters1=parameters[0].encode('utf8')
		parameters2=parameters[1].encode('utf8')
		url = 'http://www.ruscargoservice.ru/distance/'
		values = {'from_city_d' : parameters1, 'to_city_d' : parameters2}
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		try:
                        rep=''
                        z=re.findall('<b>(.*)Км</b>',the_page)
                        for x in z:
                                rep+=x
                                break
                        if rep=='' or rep.isspace():
                                reply(type, source, u'Dont know! Try more!')
                                return
                        reply(type, source, rep+u'Км')
                except:
                        pass
	except:
		reply(type,source,u'кажется что-то сломалось')

register_command_handler(handler_distance_between_cities, 'расстояние', ['фан','инфо','все'], 11, 'Показывает расстояние между городами', 'расстояние <город1> <город2>', ['расстояние Оренбург Москва'])

