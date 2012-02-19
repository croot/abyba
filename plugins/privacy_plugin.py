#===istalismanplugin===
# -*- coding: utf-8 -*-

PR_TEST = {}

PRIVACY_FILE = 'dynamic/privacy.txt'

PRIVACY_LIST = []

ROSTER_OLD = []

PRIVACY_FILTER = {}


PRV_MORE="""<iq type="set" id="some_id" >
    <query xmlns="jabber:iq:privacy">
      <list name="ignore" >
        <item action="allow" order="1" type="jid" value="conference.talkonaut.com" />
        <item action="allow" order="2" type="jid" value="conference.jabber.ru" />
        <item action="allow" order="3" type="jid" value="talkonaut.com" />
        <item action="allow" order="4" type="jid" value="mrim.xmpp.ws" />
        <item action="allow" order="5" type="jid" value="conference.qip.ru" />
        <item action="allow" order="6" type="jid" value="jabber.ru" />
        <item action="allow" order="7" type="jid" value="qip.ru" />
        <item action="allow" order="8" type="jid" value="jabberon.ru" />
        <item action="allow" order="9" type="jid" value="xmpps.ru" />
        <item action="allow" order="10" type="jid" value="jabber.perm.ru" />
        <item action="allow" order="11" type="jid" value="worldskynet.net" />
        <item action="allow" order="12" type="jid" value="icq.proc.ru" />
        <item action="allow" order="13" type="jid" value="xmpp.ru" />
        <item action="deny" order="14" type="subscription" value="none" />
      </list>
    </query>
  </iq>"""###Пример списка


def set_privacy():
    global PRIVACY_LIST
    global PRIVACY_FILE
    global ROSTER_OLD
    time.sleep(30)
    try:
        R=JCON.getRoster()
        ROSTER_OLD.extend(R.getItems())
        ACC=[x for x in GLOBACCESS.keys() if GLOBACCESS[x]>39]
        if ACC:
            ROSTER_OLD.extend(ACC)
    except:
        pass
    if PR_TEST:
        PR_TEST.clear()
    time.sleep(2)
    iq = xmpp.Iq('get')
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_PRIVACY)
    iq.addChild(node=query)
    JCON.SendAndCallForResponse(iq, get_prv_node)
    tim = time.time()
    while not PR_TEST and time.time() - tim<5:
        time.sleep(1)
        pass
    if PR_TEST:
        if 'lists' in PR_TEST.keys():
            PRIVACY_LIST.extend(PR_TEST['lists'])
    sp=''
    if not os.path.exists(PRIVACY_FILE):
        fp=file(PRIVACY_FILE,'w')
        fp.write('{}')
        fp.close()
        return
    txt=eval(read_file(PRIVACY_FILE))
    if txt:
        for x in txt:
            if x in PRIVACY_LIST:
                iq = xmpp.Iq('set')
                id = str(random.randrange(10, 999))
                iq.setID(id)
                query = xmpp.Node('query')
                query.setNamespace(xmpp.NS_PRIVACY)
                l=xmpp.Node('active', {'name': x})
                query.addChild(node=l)
                iq.addChild(node=query)
                JCON.send(iq)
                print 'Active Privacy List',unicode(x)
                break

def start_privacy_list(type, source, parameters):
    global PR_TEST
    rep=''
    if not parameters:
        if PR_TEST:
            PR_TEST.clear()
        iq = xmpp.Iq('get')
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_PRIVACY)
        iq.addChild(node=query)
        JCON.SendAndCallForResponse(iq, get_prv_node)
        tim = time.time()
        while not PR_TEST and time.time() - tim<5:
            time.sleep(1)
            pass
        if not PR_TEST:
            reply(type, source, u'Список приватностей не настроен, либо произошла ошибка!')
            return
        z=PR_TEST
        if z:
            for x in z.keys():
                if x=='active':
                    rep+=u'Активный список "'+unicode(z[x])+'"\n'
                if x=='default':
                    rep+=u'Список по умолчанию "'+unicode(z[x])+'"\n'
                if x=='lists':
                    rep+=u'Всего списков найдено '+str(len(z[x]))+': \n'+('\n'.join(z[x]))
            reply(type, source, rep)
            return
    if parameters.lower()==u'auto':
        SP=[]
        CONF=[u'conference.jabber.ru',u'conference.qip.ru',u'conference.talkonaut.com']
        if ROSTER_OLD:
            SP.extend(ROSTER_OLD)
        if CONF:
            SP.extend(CONF)
        acc=[x for x in GLOBACCESS.keys() if GLOBACCESS[x]>39]
        if acc:
            SP.extend(acc)
        if GROUPCHATS:
            for x in GROUPCHATS:
                try:
                    if x.count('@'):
                        s=x.split('@')[1]
                        if s not in CONF:
                            SP.append(x)
                except:
                    pass
        iq = xmpp.Iq('set')
        id='privacy'+str(random.randrange(1000, 9999))
        iq.setID(id)
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_PRIVACY)
        pri=query.addChild('list', {'name':'ignore'})
        n=0
        for x in SP:
            n+=1
            pri.addChild('item', {'action':'allow', 'order':str(n), 'type':'jid', 'value':x})
        n+=1
        pri.addChild('item', {'action':'deny', 'order':str(n), 'type':'subscription', 'value':'none'})
        iq.addChild(node=query)
        JCON.send(iq)
        reply(type, source, u'Список "ignore" успешно сформирован! \nВсего пунктов '+str(n))
        if not 'ignore' in PRIVACY_LIST:
            PRIVACY_LIST.append('ignore')
        return
    if parameters.lower() not in [u'undefault',u'auto',u'active',u'0',u'remove',u'default'] and not parameters.count(' '):
        if PR_TEST:
            PR_TEST.clear()
        privacy_get(type, source, parameters.lower())
        tim = time.time()
        rep = ''
        while not PR_TEST and time.time() - tim<5:
            time.sleep(1)
            pass
        if not PR_TEST:
            reply(type, source, u'Списка '+parameters.lower()+u' не существует!')
            return
        for x in PR_TEST.keys():
            try:
                rep+= unicode(PR_TEST[x]['order'])+') '+unicode(PR_TEST[x]['action'])+' '+unicode(PR_TEST[x]['type'])+' '+unicode(PR_TEST[x]['value'])+'\n'
            except:
                raise
        reply(type, source, u'Лист '+parameters.lower()+' ('+str(len(PR_TEST))+') :\n'+rep)
        return
    if parameters.lower() in [u'undefault']:
        iq = xmpp.Iq('set')
        id = str(random.randrange(10, 999))
        iq.setID(id)
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_PRIVACY)
        l=xmpp.Node('default')
        query.addChild(node=l)
        iq.addChild(node=query)
        JCON.send(iq)
        reply(type, source, u'ok')
        return
    if parameters.lower() in [u'отключить',u'0']:
        iq = xmpp.Iq('set')
        id = str(random.randrange(10, 999))
        iq.setID(id)
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_PRIVACY)
        l=xmpp.Node('active')
        query.addChild(node=l)
        iq.addChild(node=query)
        JCON.send(iq)
        reply(type, source, u'Активные списки отключены!')
        fp=file(PRIVACY_FILE,'w')
        fp.write('{}')
        fp.close()
        return
    if parameters.count(' '):
        s=parameters.split()
        if s[0].lower()==u'active':
            iq = xmpp.Iq('set')
            id = str(random.randrange(10, 999))
            iq.setID(id)
            query = xmpp.Node('query')
            query.setNamespace(xmpp.NS_PRIVACY)
            l=xmpp.Node('active', {'name': s[1].lower()})
            query.addChild(node=l)
            iq.addChild(node=query)
            JCON.send(iq)
            reply(type, source, u'ok')
            try:
                txt=eval(read_file(PRIVACY_FILE))
                txt[s[1].lower()]={}
                write_file(PRIVACY_FILE, str(txt))
            except:
                pass
            return
        if s[0].lower()==u'remove':
            iq = xmpp.Iq('set')
            id = str(random.randrange(10, 999))
            iq.setID(id)
            query = xmpp.Node('query')
            query.setNamespace(xmpp.NS_PRIVACY)
            l=xmpp.Node('list', {'name': s[1].lower()})
            query.addChild(node=l)
            iq.addChild(node=query)
            JCON.send(iq)
            reply(type, source, u'удалил '+s[1])
            try:
                txt=eval(read_file(PRIVACY_FILE))
                if s[1].lower() in txt:
                    txt[s[1].lower()]={}
                    write_file(PRIVACY_FILE, str(txt))
            except:
                pass
            return
        if s[0].lower()==u'default':
            df=xmpp.features.setDefaultPrivacyList(JCON,s[1].lower())
            if df:
                reply(type, source, s[1]+u' установлен по умолчанию')
                return
            reply(type, source, u'Такого списка нет')
            return


P_APP = []

SPAME_PRIVACY = []

def privacy_timer():
    time.sleep(1200)

def privacy_msg(raw, type, source, parameters):
    global PRIVACY_FILTER
    global SPAME_PRIVACY
    global ROSTER_OLD
    
    lim=3
    
    if time.time() - INFO['start'] < 15:  return
    if parameters.isspace(): return
    if type=='public': return
    
    jid=get_true_jid(source[1]+'/'+source[2])
    
    if not jid: return
    
    if jid in ROSTER_OLD:
        lim=6
    if parameters in [u'[no text]']:
        lim=10
        
    try:
        if jid==JID or jid in GROUPCHATS: return
        if source[1] in GROUPCHATS:
            if source[2]==get_bot_nick(source[1]):
                return
            if not source[2] or source[2].isspace():
                return
            jid=source[1]+'/'+source[2]
        if not jid in PRIVACY_FILTER:
            PRIVACY_FILTER[jid]={'time':time.time(), 'n':0}
            return
        else:
            if time.time() - PRIVACY_FILTER[jid]['time']<1.2 or len(parameters)>500:
                PRIVACY_FILTER[jid]['n']+=1
                if PRIVACY_FILTER[jid]['n']<lim:
                    return
            else:
                PRIVACY_FILTER[jid]['time']=time.time()
                PRIVACY_FILTER[jid]['n']=0
                return
        if not jid in SPAME_PRIVACY:
            SPAME_PRIVACY.append(jid)
        #threading.Thread(None,hnd_unreg,'hnd_unreg'+str(INFO['thr'])).start()
        try:
            iq = xmpp.Iq('set')
            id='privacy'+str(random.randrange(1000, 9999))
            iq.setID(id)
            query = xmpp.Node('query')
            query.setNamespace(xmpp.NS_PRIVACY)
            pri=query.addChild('list', {'name':'autoprotect'})
            n=0
            for x in SPAME_PRIVACY:
                n+=1
                pri.addChild('item', {'action':'deny', 'order':str(n), 'type':'jid', 'value':x})
            n+=1
            pri.addChild('item', {'action':'allow', 'order':str(n), 'type':'jid', 'value':'none'})
            iq.addChild(node=query)
            JCON.send(iq)
            start_privacy_list('privacy',['','',''],u'active autoprotect')
        except: pass
        print 'Bot inclusion privacy list for auto protect!'
        #threading.Thread(None,hnd_w_reg,'hnd_w_reg'+str(INFO['thr'])).start()
        if len(SPAME_PRIVACY)>2: return
        admin=[x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]
        if admin:
            for x in admin:
                msg(x, u'Подозрение на спам от '+jid+u',\nвременно включен список приватностей!')
        if GROUPCHATS:
            for chat in GROUPCHATS.keys():
                for nick in GROUPCHATS[chat].keys():
                    if get_true_jid(chat+'/'+nick) in admin and GROUPCHATS[chat][nick]['ishere']:
                        msg(chat,nick+u', Подозрение на спам от '+jid+u',\nвременно включен список приватностей!')
    except:
        pass

def hnd_unreg():
    JCON.UnregisterHandler('message',messageHnd)

def hnd_w_reg():
    JCON.RegisterHandler('message', messageHnd)

def get_prv_node(coze, res):
    if xmpp.isResultNode(res):
        try:
            for list in res.getQueryPayload():
                if list.getName()=='list':
                    if not 'lists' in PR_TEST:
                        PR_TEST['lists']=[]
                    PR_TEST['lists'].append(list.getAttr('name'))
                else:
                    PR_TEST[list.getName()]=list.getAttr('name')
        except:
            print 'for get privacy lists error'
    

def privacy_get(type, source, sp):
    iq = xmpp.Iq('get')
    id = str(random.randrange(10, 999))
    iq.setID(id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_PRIVACY)
    l=xmpp.Node('list',{'name':sp})
    query.addChild(node=l)
    iq.addChild(node=query)
    JCON.SendAndCallForResponse(iq, privacy_get_result, {'type': type, 'source': source})
	
def privacy_get_result(coze, res, type, source):
    num=0
    if res:
        if xmpp.isResultNode(res):
            z=res.getQueryChildren()
            for x in z:
                c=x.getChildren()
                num=0
                for n in c:
                    num+=1
                    try:
                        PR_TEST[num]={'value':n.getAttr('value'),'type':n.getAttr('type'),'order':n.getAttr('order'),'action':n.getAttr('action')}
                    except:
                        pass

def handler_privacy_edit(type, source, parameters):
    usr_num=0
    remove=0
    if parameters:
        if parameters.count(' '):
            s=parameters.split()
            if parameters.count(' ')==1:
                if s[1].isdigit():
                    remove=int(s[1])
            else:
                if not s[1].isdigit():
                    reply(type, source, s[1]+u' не является числом!')
                    return
                if not s[2] in ['allow','deny']:
                    reply(type, source, s[2]+u' может быть только allow или deny')
                    return
                if not s[3] in ['jid','subscription']:
                    reply(type, source, s[3]+u' может быть только jid или subscription')
                    return
                usr_num=int(s[1])
    iq = xmpp.Iq('set')
    id='privacy'+str(random.randrange(1000, 9999))
    iq.setID(id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_PRIVACY)
    pri=query.addChild('list', {'name':s[0].lower()})
    if PR_TEST:
        PR_TEST.clear()
    privacy_get('','',s[0].lower())
    tim=time.time()
    while not PR_TEST and time.time()-tim<5:
        time.sleep(1)
        pass
    if not PR_TEST:
        reply(type, source, u'Списка '+s[0].lower()+u' не существует, будет создан новый список!')
    if usr_num!=0:
        pri.addChild('item', {'action':s[2], 'order':s[1], 'type':s[3], 'value':s[4]})
    if PR_TEST:
        for x in PR_TEST.keys():
            try:
                if usr_num:
                    if usr_num==int(PR_TEST[x]['order']):
                        continue
                if remove:
                    if remove==int(PR_TEST[x]['order']):
                        continue
                pri.addChild('item', {'action':PR_TEST[x]['action'], 'order':PR_TEST[x]['order'], 'type':PR_TEST[x]['type'], 'value':PR_TEST[x]['value']})
            except:
                pass
    iq.addChild(node=query)
    JCON.send(iq)
    reply(type, source, u'ok')

    
register_command_handler(start_privacy_list, 'privacy', ['суперадмин','все'], 100, 'Работа со списком приватностей бота. Команда без параметров выведет список листов и их состояние.\nКлючи: auto - сформирует автоматический список ignore, active <list>, remove <list>, default <list>, undefault <list>\nПросто название листа в качестве параметра покажет вам его содержимое.\nЧтобы отключить все активные списки используется параметер 0.', 'privacy <key> <name_list>', ['privacy','privacy active ignore','privacy ignore','privacy remove ignore','privacy default ignore','privacy 0'])
register_message_handler(privacy_msg)
register_stage0_init(set_privacy)
register_command_handler(handler_privacy_edit, 'privacy_edit', ['суперадмин','все'], 100, 'Редактирует уже созданный список приватности на боте, в часности удаляет, изменяет или добавляет условие в лист по номеру. Для удаления определенного пункта из листа указываеться название листа и номер пункта. Для редактирования указваеться название листа, номер пункта в листе, если указать несуществующий номер он будет создан, третьим идет allow или deny (запретить или разрешить), четвертым идет jid или subscription, ну и на последок сам jid!Если условие должно работать на все жиды - тогда просто none', 'privacy_edit <name list> <order> <action> <type> <value>', ['privacy_edit ignore 1','privacy_edit ignore 33 allow jid jabber.ru'])
#register_command_handler(privacy_get, '!f', ['суперадмин','все'], 100, '', '!f', ['!f'])

