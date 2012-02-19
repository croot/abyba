#===istalismanplugin===
# -*- coding: utf-8 -*-

DR_GREEN = 'dynamic/drjabber_green.txt'
DR_RED = 'dynamic/drjabber_red.txt'
DR_GREEN_LIST = []
DR_RED_LIST = []


def drjabber_grab():
        req = urllib2.Request('http://jabberworld.info/'+u'Список_работающих_публичных_серверов_Jabber'.encode('utf8'))
        req.add_header = ('User-agent', 'Mozilla/5.0')
        res = urllib2.urlopen(req).read()
        serv = re.findall('<td align="left">(.*)\n',res)
        return serv
                        
def drjabber_start(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
        if parameters.lower()==u'update':
                if int(user_level(source[1]+'/'+source[2],source[1]))<40:
                        reply(type, source, u'Нужен доступ 40 для этого ключа, посколько активация может вызвать дополнительную нагрузку на бота!')
                        return
                try: drjabber_get()
                except: pass
                if DR_RED_LIST or DR_GREEN_LIST:
                        db=eval(read_file(DR_RED))
                        for x in DR_RED_LIST:
                                if not x in db.keys():
                                        db[x]={}
                        write_file(DR_RED, str(db))
                        db=eval(read_file(DR_GREEN))
                        for x in DR_GREEN_LIST:
                                if not x in db.keys():
                                        db[x]={}
                        write_file(DR_GREEN, str(db))
                return
        if get_bot_nick(source[1]) in GROUPCHATS[source[1]]:
                if not GROUPCHATS[source[1]][get_bot_nick(source[1])]['ismoder']:
                        reply(type, source, u'Я здесь не админ!')
                        return
        reply(type, source, u'Будут забанены все серверы на которых открыта регистрация,серверы с закрытой регистрацией или с использованием капчи будут разбанены! Последнее обновлениее базы '+timeElapsed(time.time()-os.path.getmtime(DR_RED)))
        db_r=eval(read_file(DR_RED))
        if not db_r:
                reply(type, source, u'По какойто причине список серверов не был загружен, обратитесь к администратору бота!')
                return
        for x in db_r.keys():
                if x in ['jabber.ru','xmpp.ru','qip.ru','talkonaut.com','jabberon.ru']:
                        continue
                if x.isspace():
                        continue
                drjabber_ban(source[1], x)
        db_g=eval(read_file(DR_GREEN))
        if db_g:
                for x in db_g.keys():
                        drjabber_unban(source[1], x)
        reply(type, source, u'Выполнено!\nЗабанено:'+str(len(db_r))+u'\nОткрыто безопасных:'+str(len(db_g)))


def generate_drjabber(_len = None, sg = None):
  if sg == None:
    sg = 'aoeuizxcvbnmsdfghjklqwrtyp1234567890'
  if _len == None:
    _len = random.Random().randint(1, 100)
  s = ''
  l = len(sg)
  while _len > 0:
    s += sg[random.Random().randint(0, l - 1)]
    _len -= 1
  return s


def drjabber_get():
        list=drjabber_grab()
        n=len(list)
        if list:
                for x in list:
                        if x.isspace():
                                continue
                        try:
                                if threading.activeCount()>12:
                                        time.sleep(15)
                                #else:
                                #        time.sleep(0.5)
                                threading.Thread(None, drjabber_reg, 'drjabber_reg'+str(random.randrange(1, 9999)), (n, x)).start()
                        except: pass
        for c in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
                msg(c, u'Cписок серверов dr.jabber автоматически обновлен!')

try:
        import dns.resolver
        DR_DNS=1
except:
        DR_DNS=0

def drjabber_reg(n, domain):
        port, serv, dnss = 5222, '', 0
        try:
                if DR_DNS:
                        record = "_xmpp-client._tcp.%s" % domain
                        for answer in dns.resolver.query(record, dns.rdatatype.SRV):
                                serv = answer.target.to_text()[:-1]
                                serv = serv.strip()
                                port = int(answer.port)
                                if serv!=domain:
                                        dnss=1
                                        if not port or not str(port).isdigit():
                                                port=5222
                                        print domain
                                        print '-->'
                                        print serv
                                        print port
        except: pass
        node, resource, password = generate_drjabber(random.Random().randint(5,10)), 'QIP', generate_drjabber(random.Random().randint(5,10))
        jid = xmpp.JID(node=node, domain=domain, resource=resource)
        cl = xmpp.Client(jid.getDomain(), debug=[])
        try:
                if dnss:
                        con = cl.connect(server=(serv, port),secure=0,use_srv=True)
                else:
                        con = cl.connect()
                if not con:
                        return
        except: return
        try:
                info = {'username': node, 'password':password}
                iq=xmpp.Iq('set',xmpp.NS_REGISTER,to=domain)
                for i in info.keys(): iq.setTag('query').setTagData(i,info[i])
                resp=cl.SendAndWaitForResponse(iq)
                if xmpp.isResultNode(resp):
                        DR_RED_LIST.append(domain)
                else:
                        code=resp.getErrorCode()
                        if code in ['403','405']:
                                DR_GREEN_LIST.append(domain)
                cl.disconnect()
        except: pass
                
def drjabber_ban(groupchat, jid):
        iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', u'dr.jabber')
	iq.addChild(node=query)
	JCON.send(iq)

def drjabber_unban(groupchat, jid):
        iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'none'})
	ban.setTagData('reason', u'dr.jabber')
	iq.addChild(node=query)
	JCON.send(iq)

def drjabber_init():
        global DR_GREEN
        global DR_RED
        global DR_RED_LIST
        global DR_GREEN_LIST
        new=0
        if not os.path.exists(DR_RED):
                new=1
                write_file(DR_RED, '{}')
        if not os.path.exists(DR_GREEN):
                new=1
                write_file(DR_GREEN, '{}')
#        if new or time.time()-os.path.getmtime(DR_RED)>691200:
#                time.sleep(60)

register_stage0_init(drjabber_init)
register_command_handler(drjabber_start, 'dr.jabber', ['админ','все'], 20, 'Команда оптимизирует защиту вашей конференции от спам ботом, баня серверы с открытой регистрацией и в то же время удаляя из бана безопасные серверы!Список обновляеться из сайта http://jabberworld.info с помощью ключа команды update', 'dr.jabber', ['dr.jabber'])
