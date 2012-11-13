#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman

DEV_BACKUP_ROOMF = 'dynamic/backup_roomf.txt'

BACKUP_MUC = {}

db_file(DEV_BACKUP_ROOMF, dict)


def making_backup_muc_quest(muc, afl):
        iq = xmpp.Iq('get')
	id='item'+str(random.randrange(1000, 9999))
	iq.setTo(muc)
	iq.setID(id)
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'affiliation':afl})
	iq.addChild(node=query)
	JCON.SendAndCallForResponse(iq, backup_muc_res, {'muc': muc, 'afl': afl})
        #################
        

def backup_muc_res(coze, res, muc, afl):
        if res:
                if res.getType() == 'result':
                        props = res.getChildren()[0].getChildren()
                        props = [x for x in props if x!=None]
                        list = [x.getAttrs()['jid'] for x in props]
                        if not list: return
                        db=eval(read_file(DEV_BACKUP_ROOMF))
                        if not muc in db.keys():
                                db[muc]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                        db[muc][afl].extend([x for x in list if not x in db[muc][afl]])
                        write_file(DEV_BACKUP_ROOMF, str(db))


def self_join_for_owner(prs):
        fromjid = prs.getFrom()
        ptype = prs.getType()
	g = fromjid.getStripped()
	n = fromjid.getResource()
	a = prs.getAffiliation()
	if ptype not in ['available',None]: return
        if a==u'owner' and n==get_bot_nick(g):
                iq = xmpp.Iq('get')
                id = 'item'+str(random.randrange(1000, 9999))
                iq.setTo(g)
                iq.setID(id)
                query = xmpp.Node('query')
                query.setNamespace('http://jabber.org/protocol/muc#admin')
                ban = query.addChild('item', {'affiliation':'owner'})
                iq.addChild(node=query)
                JCON.SendAndCallForResponse(iq, backup_muc_answ, {'something': 1, 'g': g})
        else:
                if time.time()-INFO['start']<60: return
                if g in GROUPCHATS and get_bot_nick(g) in GROUPCHATS[g] and GROUPCHATS[g][get_bot_nick(g)]['ismoder']:
                        if g in BACKUP_MUC.keys() and time.time()-BACKUP_MUC[g]<(86400*3):
                                return
                        else:
                                db=eval(read_file(DEV_BACKUP_ROOMF))
                                if not g in BACKUP_MUC.keys() and not g in db.keys():
                                        db[g]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                                        write_file(DEV_BACKUP_ROOMF, str(db))
                                else:
                                        try: db[g]['last']=time.time()
                                        except: db[g]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                                        write_file(DEV_BACKUP_ROOMF, str(db))
                                BACKUP_MUC[g]=time.time()
                                for x in ['owner','admin','member','outcast']:
                                        making_backup_muc_quest(g, x)
                                iq = xmpp.Iq('get')
                                id = 'info'+str(random.randrange(1, 9999))
                                iq.setID(id)
                                query=iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#info')
                                iq.setTo(g)
                                JCON.SendAndCallForResponse(iq, back_up_info_res, {'sm': 1, 'g': g})
                                        
def back_up_info_res(coze, res, sm, g):
        if res:
                if res.getType()=='result':
                        db=eval(read_file(DEV_BACKUP_ROOMF))
                        list = res.getQueryChildren()
                        if not list: return
                        for x in list:
                                if x.getNamespace()=='jabber:x:data':
                                        desc = x.getChildren()[1]
                                        desc = desc.getTagData('value')
                                        try:
                                                db[g]['info'] = desc
                                                write_file(DEV_BACKUP_ROOMF, str(db))
                                        except: pass


def backup_muc_answ(coze, res, something, g):
        props = str()
        if res:
                if res.getType() == 'result':
                        props = res.getChildren()[0].getChildren()
                        props = [x for x in props if x!=None]
                if len(props)==1:
                        msg(g, u'Запущена программа восcтановления комнаты...\nПоиск резервной базы...')
                        time.sleep(2)
                else: return
                inf, enab = '', 1
                try: db=eval(read_file(DEV_BACKUP_ROOMF))
                except: db = {}
                if not g in db.keys():
                        enab = 0
                        msg(g, u'База не найдена! owner, admin, member, outcast листы не будут восставнолены!')
                        inf = 'BACKUP_BUSTER_ROOM'
                else:
                        inf = db[g]['info']
                        
                msg(g, u'Делаю комнату постоянной!')
                iq = xmpp.Iq('set')
                iq.setTo(g)
                query = xmpp.Node('query')
                query.setNamespace('http://jabber.org/protocol/muc#owner')
                x = xmpp.Node('x',{'type':'submit'})
                x.setNamespace(xmpp.NS_DATA)
                inv=x.addChild('field', {'var':"FORM_TYPE"})
                inv.setTagData('value', xmpp.NS_MUC_ROOMCONFIG)
                cap=x.addChild('field', {'var':"muc#roomconfig_persistentroom"})
                cap.setTagData('value', "1")
                field = x.addChild('field', {'var':"muc#roomconfig_roomdesc"})
                field.setTagData('value', inf)
                query.addChild(node=x)
                iq.addChild(node=query)
                JCON.send(iq)
                clc = 0
                if enab:
                        if 'owner' in db[g]:
                                for x in db[g]['owner']:
                                        clc+=1
                                        moderate_a(g, 'jid', x, 'affiliation', 'owner')
                        if 'admin' in db[g]:
                                for x in db[g]['admin']:
                                        if x == JID:
                                                continue
                                        clc+=1
                                        moderate_a(g, 'jid', x, 'affiliation', 'admin')
                        if 'member' in db[g]:
                                for x in db[g]['member']:
                                        if x == JID:
                                                continue
                                        clc+=1
                                        moderate_a(g, 'jid', x, 'affiliations', 'memeber')
                        if 'outcast' in db[g]:
                                for x in db[g]['outcast']:
                                        if x == JID:
                                                continue
                                        clc+=1
                                        moderate_a(g, 'jid', x, 'affiliation', 'outcast')
                        if 'subject' in db[g] and len(db[g]['subject'])>2:
                                send_subject(g, db[g]['subject'])

                if clc:
                        msg(g, u'Восстановлено JID Affiliations '+str(clc))

def moderate_a(groupchat, jid_nick, par1, afl_role, par2, reason=None):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {jid_nick : par1, afl_role : par2})
	ban.setTagData('reason', get_bot_nick(groupchat))
	iq.addChild(node=query)
	JCON.send(iq)


register_presence_handler(self_join_for_owner)


def msg_subject(r, t, s, p):
        if not s[2] and s[1] in GROUPCHATS:
                subject = ''
                db = eval(read_file(DEV_BACKUP_ROOMF))
                if not s[1] in db.keys():
                        db[s[1]]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                try:
                        if r.getTag('subject'):
                                ch = r.getChildren()
                                for x in ch:
                                        if x.getName() =='subject':
                                                subject = x.getData()
                                db[s[1]]['subject'] = subject
                except: return
                write_file(DEV_BACKUP_ROOMF, str(db))

def backup_muc_subject(g, n, sub):
        if not g in GROUPCHATS: return
        db = eval(read_file(DEV_BACKUP_ROOMF))
        if not g in db.keys():
                db[g]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
        if sub != db[g]['subject']:
                db[g]['subject']=sub
                write_file(DEV_BACKUP_ROOMF, str(db))

if "register_subject_handler" in globals().keys():
        register_subject_handler(backup_muc_subject)

register_message_handler(msg_subject)



def send_subject(muc, body):
        STANZA="""<message type="groupchat" to="%s" >
    <subject>%s</subject>
  </message>""" % (muc, body)
        node = xmpp.simplexml.XML2Node(unicode(STANZA).encode('utf8'))
        JCON.send(node)


def muc_backup_init(*something):
        global BACKUP_MUC
        global DEV_BACKUP_ROOMF
        if not BACKUP_MUC:
                db=eval(read_file(DEV_BACKUP_ROOMF))
                for x in db.keys():
                        if 'time' in db[x]:
                                BACKUP_MUC[x]=db[x]['time']

register_stage0_init(muc_backup_init)
                
def get_room_backup_status(t, s, p):
        if not p and s[1] in GROUPCHATS:
                p=s[1]
        else:
                reply(t, s, u'?')
                return
        rep, p = '', p.lower()
        db = eval(read_file(DEV_BACKUP_ROOMF))
        if not p in db.keys():
                reply(t, s, u'Бэкап комнаты отсутствует')
                return
        rep+=u'Бэкап комнаты создан '+timeElapsed(time.time()-db[p]['last'])+u' назад.\n'
        rep+=u'Топик '+db[p]['subject'][:20]+'... '+str(len(db[p]['subject']))+u' символов.\n'
        rep+=u'Информация о комнате '+db[p]['info']+'\n'
        rep+=u'Овнеры '+str(len(db[p]['owner']))+'\n'
        rep+=u'Админы '+str(len(db[p]['admin']))+'\n'
        rep+=u'Мемберы '+str(len(db[p]['member']))+'\n'
        rep+=u'Изгои '+str(len(db[p]['outcast']))+'\n'
        reply(t, s, rep)
        

register_command_handler(get_room_backup_status, 'backup_status', ['все'], 10, 'Выводит информацию по резервному копированию команты.', 'backup_status', ['backup_status'])        

