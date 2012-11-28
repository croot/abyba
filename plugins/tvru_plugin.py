#===istalismanplugin===
# -*- coding: utf-8 -*-


#fix by 40tman
#


def prog_grabru(code, n='1', uk=0):
        import urllib2
	import re
	import time

	kod=code.lower()
	kod=kod.strip()
	if kod == '' or not kod.isdecimal():
		program = u'И какой канал мне показывать? Номер канала можно узнать, дав команду боту "тв_лист"'
		return program
	
	zone = '1'

	if uk: zone+='87'
	
	url = 'http://m.tv.yandex.ua/'+zone+'/channels/'+kod
	if n == '2': url = 'http://m.tv.yandex.ua/'+zone+'?channel='+kod+'&when='+n+'&day='+prog_listru()[0]
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
        r = urllib2.urlopen(req).read()
        r = re.findall('<th class="channel">(.*?)Выбор каналов', r, re.DOTALL | re.IGNORECASE)
        if not r:
                if not uk:
                        return prog_grabru(code, n, uk=1)
                else:
                        program = u'Нет программы на сегодня.'
        else:
                r = r[0]
                r = r.replace('</tr>','\n').replace('</a>',' ')
                r = re.compile(r'<[^<>]*>').sub('', r)
                program = r
	return program

def prog_grabru2(code):
    return prog_grabru(code, n='2')


def tv_finder_by_name(t, s, p, full=0):
        req = urllib2.Request('http://m.tv.yandex.ru/')
        req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')

        r = urllib2.urlopen(req).read().decode('utf8','ignore')

        day = re.findall('<input type="hidden" name="day" value="(.*?)"', r, re.DOTALL | re.IGNORECASE)
        if day: day = day[0]

        try: r = r.split('Все настроенные')[1]
        except: pass

        r = re.findall('<option value="(.*?)">(.*?)</option>', r, re.DOTALL | re.IGNORECASE)
        r = filter(lambda x : x[0].isdigit(), r)
        r = [x for x in r if not [c[0] for c in r].count(x[0])>1 and not x[0] in ['2']]

        rep = str()
        list = [x for x in r if x[1].strip().lower().count(p.lower())]
        if not list:
                reply(t, s, u'Канал по запросу < '+p+u' > не найден!')
                return
        x = list[0]
        reply(t, s, ('Найдено возможных совпадений по каналам: '+str(len(list))+' см. тв_лист\n' if len(list)>1 else '')+(prog_grabru(x[0]) if full==0 else prog_grabru(x[0],n='2')))


def prog_listru(nn=0,k=0):
        req = urllib2.Request('http://m.tv.yandex.ru/1'+('87' if k else ''))
        req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')

        r = urllib2.urlopen(req).read()#.decode('utf8','ignore')
        day = re.findall('<input type="hidden" name="day" value="(.*?)"', r, re.DOTALL | re.IGNORECASE)
        if day: day = day[0]

        try: r = r.split('Все настроенные')[1]
        except: pass

        r = re.findall('<option value="(.*?)">(.*?)</option>', r, re.DOTALL | re.IGNORECASE)

        program=''

        r = filter(lambda x : x[0].isdigit(), r)
        r = [x for x in r if not [c[0] for c in r].count(x[0])>1 and not x[0] in ['2']]
        r = sorted(r, key=lambda x: int(x[0]))

        rep=''
        n=0
        for x in r:
                s=', '
                if r.index(x)==(len(r)-1): s=''
                n+=1
                if n == 3:
                        n = 0
                        s = '\n'
                rep+=x[0]+' -'+x[1]+s

        program = ', '.join([x[0]+' -'+x[1] for x in r])
        return day, (rep if not nn else program)

def handler_TVru_get(type, source, parameters):
        if parameters and not parameters.isdigit():
                tv_finder_by_name(type, source, parameters)
        else:
                reply(type,source, prog_grabru(parameters))

def handler_TVru_get2(type, source, parameters):
        if type == 'public':
                type == 'private'
		reply(type,source,u'смотри приват!')
	if parameters and not parameters.isdigit():
                tv_finder_by_name(type, source, parameters, 1)
        else:
                reply('private',source, prog_grabru2(parameters))

def handler_TVru_list(type, source, parameters):
	if type == 'public':
		reply(type,source,u'смотри приват!')
	rep=''
	f=prog_listru()[1]
	reply('private',source, f)


def handler_TVru_search(type, source, parameters):
        if not parameters or parameters.isspace():
                return
        parameters=parameters.lower()
	if type == 'public':
		reply(type,source,u'смотри приват!')
	rep=''
	f=prog_listru(nn=1)[1].split(',')
	f2=prog_listru(nn=1,k=1)[1].split(',')
	f.extend([ x for x in f2 if not x in f])
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

register_command_handler(handler_TVru_search, 'тв_найти', ['фан','все'], 0, 'Ищет код по названию канала или по совпадению', 'тв_найти канал', ['тв_найти Discovery'])	
register_command_handler(handler_TVru_get2, 'тв_полностью', ['фан','все'], 11, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист"', 'тв_полностью [номер канала]', ['тв_полностью 144'])
register_command_handler(handler_TVru_get, 'тв', ['фан','все'], 0, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист"', 'тв [номер канала]', ['тв 144'])
register_command_handler(handler_TVru_list, 'тв_лист', ['фан','все'], 0, 'Просмотреть номера каналов чтобы потом узнать телепрограму', 'тв_лист', ['тв_лист'])
