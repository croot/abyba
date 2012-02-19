#===istalismanplugin===
# -*- coding: utf-8 -*-

def hnd_change_config(type,source,parameters):
    if not parameters:
        reply(type,source,u'?')
        return
    if not parameters.count(' '):
        reply(type,source,u'что-то тут не так!')
        return
    s=parameters.split()
    if not s[0].count('@'):
        reply(type,source,u'неверный jid '+s[0])
        return
    serv=s[0].split('@')[1]
    login=s[0].split('@')[0]
    jid = xmpp.JID(node=login, domain=serv, resource='both')
    cl = xmpp.Client(jid.getDomain(), debug=[])
    con = cl.connect()
    if not con:
        reply(type,source,u'не могу подключиться к'+unicode(serv))
        return
    au=cl.auth(jid.getNode(), s[1], jid.getResource())
    if not au:
        reply(type,source,u'Jid не прошел авторизацию!')
        return
    try:
        cl.disconnect()
    except:
        pass
    f='config.list'
    fp=open(f)
    #print unicode(fp.read())
    MAS=''
    for x in fp.readlines():
        if x.count('CONNECT_SERVER'):
            x=u'CONNECT_SERVER = '+serv+'\n'
            MAS+=x
        elif x.count('JID'):
            x=u'JID = '+s[0]+'\n'
            MAS+=x
        elif x.count('PASSWORD') and x.count(PASSWORD):
            x='PASSWORD = '+s[1]+'\n'
            MAS+=x
        else:
            MAS+=x+'\n'
    tx=file(f,'w')
    tx.write(MAS)
    tx.close()
    reply(type,source,u'config change!')
    print 'RESTARTING'
    os.execl(sys.executable, sys.executable, sys.argv[0])

register_command_handler(hnd_change_config, 'ботконфиг', ['все'], 100, 'Меняет конфиг бота.', 'ботконфиг <логин@сервер> <пароль>', ['ботконфиг 111@talkonaut.com 12345'])        

