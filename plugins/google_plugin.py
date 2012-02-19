#===istalismanplugin===
# -*- coding: utf-8 -*-

#Ported from fatal-bot

import sijs

def rmv_tgs_esc(text):
	rep_src_frst = ['&quot;','&amp;','&lt;','&gt;','&trade;','&nbsp;','&cent;','&pound;','&curren;','&yen;','&brvbar;','&sect;','&copy;','&laquo;','&not;','&reg;','&deg;','&plusmn;','&sup2;','&sup3;','&micro;','&para;','&middot;','&sup1;','&raquo;','&frac14;','&frac12;','&times;','&divide;']
	rep_src_sec = ['&#34;','&#38;','&#60;','&#62;','&#153;','&#160;','&#162;','&#163;','&#164;','&#165;','&#166;','&#167;','&#169;','&#171;','&#172;','&#174;','&#176;','&#177;','&#178;','&#179;','&#181;','&#182;','&#183;','&#185;','&#187;','&#188;','&#189;','&#215;','&#247;']
	rep_dest = ['"','&','<','>','™',' ','¢','£','¤','¥','¦','§','©','«','¬','®','°','±','²','³','µ','¶','·','¹','»','¼','½','×','÷']
	
	nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&#39;', "'").replace('   ',' ')
	
	for ri in rep_dest:
		noescape = noescape.replace(rep_src_frst[rep_dest.index(ri)].decode('utf-8'),ri.decode('utf-8')).replace(rep_src_sec[rep_dest.index(ri)].decode('utf-8'),ri.decode('utf-8'))
	
	return noescape

def google_search(query,shw):
	try:
		res = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % urllib2.quote(query.encode('utf-8')))
		res_dict = sijs.load(res)
	except urllib2.HTTPError, e:
		return str(e)

	if res_dict['responseStatus'] == 200 and res_dict['responseData']:
		total = res_dict['responseData']['cursor']['estimatedResultCount']
		results = res_dict['responseData']['results']
		rep = u'Результаты поиска (всего: %s; показано: %d):\n\n' % (total, shw)

		for rsi in results[:shw]:
			if rsi['titleNoFormatting'][-1] != '!' or rsi['titleNoFormatting'][-1] != '.' or rsi['titleNoFormatting'][-1] != '?':
				rsi['titleNoFormatting'] += '.'
			
			if rsi['content'][-1] != '!' or rsi['content'][-1] != '.' or rsi['content'][-1] != '?':
				rsi['content'] += '.'
			
			rep += u'%d) %s\nОписание: %s\nСсылка: %s\n' % (results.index(rsi)+1,rsi['titleNoFormatting'],rsi['content'],rsi['unescapedUrl'])
			
			if rsi['cacheUrl']:
				rep += u'В кэше: %s\n\n' % (rsi['cacheUrl'])
			else:
				rep += u'\n'
	
		return rmv_tgs_esc(rep)
	else:
		return u'Неизвестная ошибка!'

def handler_google_search(type, source, parameters):
	if parameters:
		results = ''
		
		spltdp = parameters.split()
		
		if len(spltdp) >= 1:
			if spltdp[0] == '+':
				try:
                                        results = google_search(parameters,4)
                                except:
                                        pass
			else:
				try:
                                        results = google_search(parameters,2)
                                except:
                                        pass
		if results:
			reply('private', source, results)
		else:
			reply(type, source, u'Ничего не найдено!')
	else:
		reply(type, source, u'Неверный синтаксис!')


register_command_handler(handler_google_search, 'гугль', ['инфо','все'], 0, 'Поиск в Google.Если дописать + перед запросом-покажет 4 результата.', 'гугль <запрос>', ['гугль что-то'])
