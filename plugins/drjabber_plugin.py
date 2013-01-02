#===istalismanplugin===
# -*- coding: utf-8 -*-

DR_JABBER = {'captcha':{'jabber.ru':None,'qip.ru':None,'xmpp.ru':None},'open':{},'close':{}}
DR_JABBER_FILE = 'dynamic/drjabber.txt'

db_file(DR_JABBER_FILE, dict)

WHITE_SERV = ['jabber.ru','xmpp.ru','qip.ru','talkonaut.com']

def grab_drjab():
        serv = []
        list = ['http://jabberworld.info/RAW:'+u'_Список_Jabber-серверов'.encode('utf8'),'http://jabberworld.info/'+u'Список_работающих_публичных_серверов_Jabber'.encode('utf8')]
        for x in list:
                try:
                        req = urllib2.Request('http://jabberworld.info/RAW:'+u'_Список_Jabber-серверов'.encode('utf8'))
                        req.add_header = ('User-agent', 'Mozilla/5.0')
                        res = urllib2.urlopen(req).read()
                except: pass
                if list.index(x) == 0:
                        serv.extend(re.findall('<p>(.*)\n', res))
                else:
                        serv.extend(re.findall('<td style=\"text-align: left;\">(.*)\n',res))
        return [x for x in serv if x not in WHITE_SERV]

def drjab_sendq(x):
        iq = xmpp.Iq('get')
	iq.setTo(x)
	id = str(random.randrange(1000, 9999))
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:register')
	JCON.SendAndCallForResponse(iq, drjab_resxml, {})

fm = None

def drjab_resxml(cl, res):
        global fm
        fm = res
        if res:
                if res.getType() == 'result':
                        ch = res.getChildren()
                        if ch:
                                ch = ch[0]
                                if not ch.getTag('data'): DR_JABBER['open'][res.getFrom().__str__()] = None
                                else: DR_JABBER['captcha'][res.getFrom().__str__()] = None
                else: DR_JABBER['close'][res.getFrom().__str__()] = None

DRJ_FUNC = {}

def hnd_drjabber(t, s, p):
        global DR_JABBER_FILE
        global DR_JABBER
        txt = eval(read_file(DR_JABBER_FILE))
        if p.lower() in DR_JABBER.keys():
                try: reply(t, s, ', '.join(txt[p.lower()].keys()))
                except: pass
                return
        if len(p.split())>1 and p.split()[0].lower() == u'serv':
                c = p.split()[1].lower()
                if txt:
                        if c in txt['captcha']:
                                reply(t, s, u'Сервер '+c+u' на капче!')
                                return
                        if c in txt['open']:
                                reply(t, s, u'Сервер '+c+u' с открытой регой!')
                                return
                        if c in txt['close']:
                                reply(t, s, u'Сервер '+c+u' закрытый(50/50 т.к. в силу ряда причин статус может быть неверный(нет коннекта s2s и т.д.), поэтому такие серверы баняться)!')
                                return
                        drjab_sendq(c)
                        time.sleep(3)
                        list = [x for x in DR_JABBER.keys() if c in DR_JABBER[x].keys()]
                        reply(t, s, u'Сервер не найден в списке, проверка показала:\n сервер '+c+' '+(list[0] if list else u' не ответил вовремя на запрос'))
                        return
                
        if not s[1] in GROUPCHATS: return

        if s[1] in DRJ_FUNC.keys():
                if time.time()-DRJ_FUNC[s[1]]<1200:
                        reply(t, s, u'Лимит команды 20 минут!')
                        return
                
        DRJ_FUNC[s[1]] = time.time()

        list, w = grab_drjab(), 0

        if not list:
                reply(t, s, u'Граббер сломался или сайт лежит!')
                return
        reply(t, s, u'В списке найдено '+str(len(list))+u' серверов.')
        if p.lower()==u'update' or time.time()-os.path.getmtime(DR_JABBER_FILE)>86400*3 or not eval(read_file(DR_JABBER_FILE)):
                w = 1
                reply(t, s, u'Проверка займет '+str((len(list)/2)/60)+u' минут, скорость 120 серв./мин.')
                for x in list:
                        drjab_sendq(x)
                        time.sleep(0.5)
        else:
                DR_JABBER = txt.copy()

        rep = u'Серверов защищенных CAPTCHA FORM: '+str(len(DR_JABBER['captcha']))
        rep += u',\n серверов с открытой регистрацией (outcast): '+str(len(DR_JABBER['open']))
        rep += u',\n серверов ответивших ошибкой (uknown status => outcast): '+str(len(DR_JABBER['close']))
        time.sleep(10)
        reply(t, s, rep)
        UNBAN = DR_JABBER['captcha']
        UNBAN.update(DR_JABBER['close'])
        drj_afl(s[1], 'none', UNBAN.keys())
        time.sleep(3)
        drj_afl(s[1], 'outcast', DR_JABBER['open'].keys())
        if w: write_file(DR_JABBER_FILE, str(DR_JABBER))
        for x in DR_JABBER.keys():
                DR_JABBER[x].clear()

def drj_afl(groupchat, afl, list):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	for x in list:
                query.addChild('item', {'jid':x, 'affiliation':afl})
                if sys.getsizeof(query)>60000: break
	iq.addChild(node=query)
	JCON.send(iq)



register_command_handler(hnd_drjabber, 'dr.jabber', ['админ','все'], 20, 'Команда оптимизирует защиту вашей конференции от спам ботом, баня серверы с открытой регистрацией, в то же время удаляя из бана безопасные серверы.\nСписок обновляеться из сайта http://jabberworld.info с помощью ключа команды update или автоматически', 'dr.jabber', ['dr.jabber','dr.jabber serv jabbrik.ru','dr.jabber update'])
