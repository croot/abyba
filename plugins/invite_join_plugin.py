#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman
#Для захода бота по инвайту в комнате должно быть не меньше 3-х человек.

inv_id=[]
PROTECT_INV=[]

def invite_join(msg):
    mas, fromjid, body = msg.getChildren(), msg.getFrom(), ''
    try:
        cp=msg.getBody()
        body=cp.split()[0]
    except: return
    if INVITE_JOIN!='1': return
    if not fromjid in PROTECT_INV:
        PROTECT_INV.append(fromjid)
        for x in mas:
            try:
                gch=fromjid
                file='dynamic/inviteblock.txt'
                txt=eval(read_file(file))
                if gch in txt:
                    print 'room in balacklist'
                    return
                if gch not in GROUPCHATS:
                    iq = xmpp.Iq('get')
                    id='dis'+str(random.randrange(1, 9999))
                    globals()['inv_id'].append(id)
                    iq.setID(id)
                    query=iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
                    iq.setTo(gch)
                    JCON.SendAndCallForResponse(iq, inv_join_answ, {'gch': gch, 'body': body})
            except: pass

def inv_join_answ(coze,res,gch,body):
    id = res.getID()
    if not id in globals()['inv_id']:
        return
    if res:
        if res.getType()=='result':
            try:
                props=res.getQueryChildren()
                d=''
                n=0
                for x in props:
                    i=x.getAttrs()['jid']
                    n+=1
                print n
                if n>2:
                    print 'ok'
                    gch=str(gch)
                    get_gch_cfg(gch)
                    #MACROS.load(gch)
                    join_groupchat(gch)
                    if popups_check(gch):
                        print 'joined'
                    #handler_admin_join('public', [gch,body,body], gch)
            except:
                pass

def hnd_ivite_block(type,source,parameters):
    if not parameters:
        try:
            txt=eval(read_file('dynamic/inviteblock.txt'))
            rep=''
            for x in txt:
                rep+=x+'\n'
            if rep=='':
                reply(type,source,u'запрещенных комнат нет')
                return
            reply(type,source,rep)
        except:
            pass
    if len(parameters)<3:
        return
    try:
        txt=eval(read_file('dynamic/inviteblock.txt'))
        if not parameters.lower() in txt:
            txt[parameters.lower()]={}
            write_file('dynamic/inviteblock.txt',str(txt))
            reply(type,source,u'добавил в черный лист '+parameters)
            return
        del txt[parameters.lower()]
        write_file('dynamic/inviteblock.txt',str(txt))
        reply(type,source,u'удалил')
    except:
        pass
                        
register_invite_handler(invite_join)
register_command_handler(hnd_ivite_block, 'антиджойн', ['все','мод','суперадмин'], 40, 'Добавляет/удаляет запрет на вход бота в определенную комнату по инвайту.Без параметров показывает список.', 'антиджойн <комната>', ['антиджойн уг@conference.jabber.ru'])


