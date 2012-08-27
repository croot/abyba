#===istalismanplugin===
# -*- coding: utf-8 -*-

PR_TEST = {}
PRIVACY_ID = {}
PRIVACY_LIST = []
ROSTER_OLD = []
PRIVACY_FILTER = {}


def privacy_xml(typ='get', nod=None, name=None):
    iq = xmpp.Iq(typ)# 1
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_PRIVACY)
    if nod and name:
        l=xmpp.Node(nod, {'name': name})# 2,3
        query.addChild(node=l)
    if nod and not name:
        l=xmpp.Node(nod)# 2
        query.addChild(node=l)
    iq.addChild(node=query)
    return iq

def privacy_collect_jids():
    list = [u'conference.jabber.ru',u'conference.qip.ru',u'conference.talkonaut.com']
    
    try:
        R = JCON.getRoster()
        list.extend(R.getItems())
    except: pass
    
    ACC=[x for x in GLOBACCESS.keys() if GLOBACCESS[x]>30]
    if ACC: list.extend(ACC)

    return list


def set_privacy():
    global PRIVACY_LIST
    global ROSTER_OLD
    time.sleep(30)

    print 'Send privacy configuration quest\n'

    list = privacy_collect_jids()
    ROSTER_OLD.extend(list)
    
    time.sleep(2.5)

    id = random.randrange(100, 99999)
    
    iq = privacy_xml()
    JCON.SendAndCallForResponse(iq, get_prv_node, {'id':id})
    
    tim = time.time()
    while not id in PR_TEST.keys() and time.time() - tim<5:
        time.sleep(1)
        pass
    if id in PR_TEST.keys():
        if 'lists' in PR_TEST[id]:
            PRIVACY_LIST.extend(PR_TEST[id]['lists'])
    n = 0
    if list:
        for x in list:
            iq = xmpp.Iq('set')
            id = str(random.randrange(10, 999))
            iq.setID(id)
            query = xmpp.Node('query')
            query.setNamespace(xmpp.NS_PRIVACY)
            pri=query.addChild('list', {'name':'bot'})
            pri.addChild('item', {'action':'deny', 'order':str(1), 'type':'group', 'value':'ignore'})
            k = pri.addChild('item', {'action':'allow', 'order':str(2), 'type':'jid', 'value':'none'})
            iq.addChild(node=query)
            JCON.send(iq)


def start_privacy_list(type, source, parameters):
    global PR_TEST

    keys, rep, id = [u'undefault',u'auto',u'active',u'0',u'remove',u'default'], '', random.randrange(100, 99999)
    
    if not parameters:
        iq = privacy_xml()
        
        JCON.SendAndCallForResponse(iq, get_prv_node, {'id':id})

        tim = time.time()
        while not id in PR_TEST.keys() and time.time() - tim<5:
            time.sleep(1)
            pass
        if not id in PR_TEST.keys():
            reply(type, source, u'Список приватностей не настроен, либо произошла ошибка!')
            return
        z = PR_TEST[id]
        if z:
            for x in z.keys():
                if x=='active':
                    rep+=u'Активный список "'+unicode(z[x])+'"\n'
                if x=='default':
                    rep+=u'Список по умолчанию "'+unicode(z[x])+'"\n'
                if x=='lists':
                    rep+=u'Всего списков найдено '+str(len(z[x]))+': \n'+('\n'.join(z[x]))
            reply(type, source, rep)
            del PR_TEST[id]
            return
        
    if parameters.lower()==u'auto':
        SP = []
        CONF = [u'conference.jabber.ru',u'conference.qip.ru',u'conference.talkonaut.com']

        if ROSTER_OLD: SP.extend(ROSTER_OLD)
        if CONF: SP.extend(CONF)
        acc = [x for x in GLOBACCESS.keys() if GLOBACCESS[x]>39]
        if acc: SP.extend(acc)
        if GROUPCHATS: SP.extend(GROUPCHATS.keys())
        
        iq = xmpp.Iq('set')
        id = str(random.randrange(1000, 9999))
        iq.setID(id)
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_PRIVACY)
        pri=query.addChild('list', {'name':'ignore'})
        n=0
        for x in SP:
            n+=1
            pri.addChild('item', {'action':'allow', 'order':str(n), 'type':'jid', 'value':x})
        k = pri.addChild('item', {'action':'deny', 'order':str(n+1), 'type':'subscription', 'value':'none'})
        k.setTag('message')
        k.setTag('presence-in')
        iq.addChild(node=query)
        JCON.send(iq)
        
        reply(type, source, u'Список "ignore" успешно сформирован! \nВсего пунктов '+str(n))
        
        if not 'ignore' in PRIVACY_LIST:
            PRIVACY_LIST.append('ignore')
            return
        
    if not parameters.lower() in keys and not parameters.count(' '):
        privacy_get(type, source, parameters.lower())

        PRIVACY_ID[id] = 'get'

        tim = time.time()
        rep = ''
        while not id in PR_TEST.keys() and time.time() - tim<5:
            time.sleep(1)
            pass
        if not id in PR_TEST.keys():
            reply(type, source, u'Списка '+parameters.lower()+u' не существует!')
            return
        action = ''
        for x in PR_TEST[id].keys():
            try:
                if PR_TEST[id][x]['action']=='allow':
                    action=u'разрешить'
                if PR_TEST[id][x]['action']=='deny':
                    action=u'запретить'
            except: pass
            try: rep+= unicode(PR_TEST[id][x]['order'])+u') Если '+unicode(PR_TEST[id][x]['type'])+' '+unicode(PR_TEST[id][x]['value'])+u' тогда '+action+' '+PR_TEST[id][x]['tags']+'\n'
            except: pass
        reply(type, source, u'Лист '+parameters.lower()+' ('+str(len(PR_TEST[id]))+') :\n'+rep)
        del PR_TEST[id]
        return
    
    if parameters.lower() in [u'undefault']:
        iq = privacy_xml('set','default')
        JCON.send(iq)
        
        reply(type, source, u'Список по умолчанию отключен!')
        return
    
    if parameters.lower() in [u'off',u'0']:

        iq = privacy_xml('set', 'active')
        JCON.send(iq)
        
        reply(type, source, u'Активные списки отключены!')
        return
    
    if parameters.count(' '):
        s = parameters.split()
        ss = s[0].lower()

        if ss == u'active':
            iq = privacy_xml('set','active',s[1].lower())
            JCON.send(iq)
            
            reply(type, source, u'Список активирован!')
            return
        
        if ss == u'remove':
            iq = privacy_xml('set', 'list', s[1].lower())
            JCON.send(iq)
            
            reply(type, source, u'Удалил '+s[1])
            return
        
        if s[0].lower()==u'default':
            df=xmpp.features.setDefaultPrivacyList(JCON,s[1].lower())
            if df:
                reply(type, source, s[1]+u' установлен по умолчанию')
                return
            reply(type, source, u'Такого списка нет')
            return


PR_LIMIT = 0

SPAME_PRIVACY = []

def privacy_timer():
    time.sleep(1200)

def privacy_msg(raw, type, source, parameters):
    global PR_LIMIT
    global PRIVACY_FILTER
    global SPAME_PRIVACY
    global ROSTER_OLD
    
    lim = 3
    
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
            if time.time() - PRIVACY_FILTER[jid]['time']<1.2 or len(parameters)>500 or (len(parameters)>150 and not parameters.count(' ')):
                PRIVACY_FILTER[jid]['n']+=1
                if PRIVACY_FILTER[jid]['n']<lim:
                    return
            else:
                PRIVACY_FILTER[jid]['time']=time.time()
                PRIVACY_FILTER[jid]['n']=0
                return
        if not jid in SPAME_PRIVACY:
            SPAME_PRIVACY.append(jid)
        else: return
            #####JCON.send(xmpp.protocol.Presence(to=jid, typ='unsubscribe'))
        
        try:
            if not source[1] in GROUPCHATS:
                iq=xmpp.Iq('set',xmpp.NS_ROSTER)
                query=iq.getTag('query')
                attrs={'jid':jid}
                attrs['name']=jid
                item=query.setTag('item',attrs)
                item.addChild(node=xmpp.Node('group',payload=['ignore']))
                JCON.send(iq)
                ########
            if source[1] in GROUPCHATS:
                iq = xmpp.Iq('set')
                id = str(random.randrange(1000, 9999))
                iq.setID(id)
                query = xmpp.Node('query')
                query.setNamespace(xmpp.NS_PRIVACY)
                pri=query.addChild('list', {'name':'bot'})
                n=1
                j = pri.addChild('item', {'action':'deny', 'order':str(n), 'type':'group', 'value':'ignore'})
                for x in SPAME_PRIVACY:
                    n+=1
                    pri.addChild('item', {'action':'deny', 'order':str(n), 'type':'jid', 'value':x})
                k = pri.addChild('item', {'action':'allow', 'order':str(n+1), 'type':'jid', 'value':'none'})
                iq.addChild(node=query)
                JCON.send(iq)
            if time.time()-PR_LIMIT<60:
                iq = privacy_xml('set','active','bot')
                JCON.send(iq)
                #iq = privacy_xml('set','default','bot')
                #JCON.send(iq)
                PR_LIMIT=time.time()
        except: pass
        print 'Bot inclusion privacy list for auto protect!'
        
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

#def hnd_unreg():
    #JCON.UnregisterHandler('message',messageHnd)
#def hnd_w_reg():
    #JCON.RegisterHandler('message', messageHnd)

def get_prv_node(coze, res, id):
    global PR_TEST
    
    if xmpp.isResultNode(res):
        PR_TEST[id]={}
        try:
            for list in res.getQueryPayload():
                if list.getName()=='list':
                    if not 'lists' in PR_TEST[id]:
                        PR_TEST[id]['lists']=[]
                    PR_TEST[id]['lists'].append(list.getAttr('name'))
                else:
                    PR_TEST[id][list.getName()]=list.getAttr('name')
        except:
            print 'In get privacy lists error'
    

def privacy_get(type, source, sp):
    iq = privacy_xml('get','list',sp.lower())
    JCON.SendAndCallForResponse(iq, privacy_get_result, {'type': type, 'source': source})
	
def privacy_get_result(coze, res, type, source):
    DICT = {}
    global PR_TEST
    global PRIVACY_ID
    if res and xmpp.isResultNode(res):
        z = res.getQueryChildren()
        for x in z:
            c = x.getChildren()
            num = 0
            tags = ''
            for n in c:
                tags = ''
                try:
                    if n.getTag('message'): tags+=u'*сообщения; '
                    if n.getTag('presence-in'): tags+=u'*входящие презенсы; '
                    if n.getTag('presence-out'): tags+=u'*исходящие презенсы; '
                    if n.getTag('iq'): tags+=u'*iq-запросы; '
                except: pass
                num+=1
                try: DICT[num]={'value':n.getAttr('value'),'type':n.getAttr('type'),'order':n.getAttr('order'),'action':n.getAttr('action'),'tags':tags}
                except: pass
    for x in PRIVACY_ID.keys():
        if PRIVACY_ID[x]=='get' and not x in PR_TEST.keys():
            PR_TEST[x]=DICT.copy()
            del PRIVACY_ID[x]


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
                if not s[3] in ['jid','subscription','group']:
                    reply(type, source, s[3]+u' может быть только jid, group или subscription')
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
    reply(type, source, u'Изменения сохранены!')

    
register_command_handler(start_privacy_list, 'privacy', ['суперадмин','все'], 100, 'Работа со списком приватностей бота. Команда без параметров выведет список листов и их состояние.\nКлючи: auto - сформирует автоматический список ignore, active <list>, remove <list>, default <list>, undefault <list>\nПросто название листа в качестве параметра покажет вам его содержимое.\nЧтобы отключить все активные списки используется параметер 0.', 'privacy <key> <name_list>', ['privacy','privacy active ignore','privacy ignore','privacy remove ignore','privacy default ignore','privacy 0'])
register_message_handler(privacy_msg)
register_stage0_init(set_privacy)
register_command_handler(handler_privacy_edit, 'privacy_edit', ['суперадмин','все'], 100, 'Редактирует уже созданный список приватности на боте, в часности удаляет, изменяет или добавляет условие в лист по номеру. Для удаления определенного пункта из листа указываеться название листа и номер пункта. Для редактирования указваеться название листа, номер пункта в листе, если указать несуществующий номер он будет создан, третьим идет allow или deny (запретить или разрешить), четвертым идет jid, subscription или group, ну и на последок сам jid!Если условие должно работать на все жиды - тогда просто none', 'privacy_edit <name list> <order> <action> <type> <value>', ['privacy_edit ignore 1','privacy_edit ignore 33 allow jid jabber.ru'])

