#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin

DH_FIL='dynamic/dischack.txt'

DH_DIC={'time':0,'chat':{}}

dischc=[]

def discohack_start(type, source, parameters):
        if not parameters or parameters.isspace():
                if not DH_DIC['chat']:
                        reply(type, source, u'Проверяемых конф нет!')
                        return
                rep=u'Всего '+str(len(DH_DIC['chat']))+u':\n'
                for x in DH_DIC['chat']:
                        rep+=x+'\n'
                rep+=u'Время последнего запроса '+timeElapsed(time.time()-DH_DIC['time'])
                reply(type, source, rep)
                return
        if not parameters.count('@conference') or parameters.count('.')<2:
                reply(type, source, u'Адрес конференции не корректен!')
                return
        jid=get_true_jid(source[1]+'/'+source[2])
        if not os.path.exists(DH_FIL):
                f=open(DH_FIL,'w')
                f.write('{}')
                f.close()
        txt=eval(read_file(DH_FIL))
        if not parameters.lower() in txt:
                txt[parameters.lower()]={}
                txt[parameters.lower()]={'jid':jid}
                write_file(DH_FIL, str(txt))
                DH_DIC['chat'][parameters.lower()]={}
                reply(type, source, u'Добавил!')
                discohack_quest(parameters.lower())
                if len(txt)==1:
                        dischc_timer()
                return
        else:
                del txt[parameters.lower()]
                write_file(DH_FIL, str(txt))
                if parameters.lower() in DH_DIC['chat']:
                        del DH_DIC['chat'][parameters.lower()]
                reply(type, source, u'Убрал!')

def discohack_quest(chat):
        DH_DIC['time']=time.time()
        type, source = None, None
        iq = xmpp.Iq('get')
        id='dis'+str(random.randrange(1, 9999))
        globals()['dischc'].append(id)
	iq.setID(id)
	query=iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
	iq.setTo(chat)
	JCON.SendAndCallForResponse(iq, handler_dischc_ext, {'type': type, 'source': source, 'chat':chat})
	
def handler_dischc_ext(coze, res, type, source, chat):
        id=res.getID()
        #chat=''
        if id in globals()['dischc']:
		globals()['dischc'].remove(id)
	else:
                return
        if res:
                if res.getType() == 'error':
                        #chat=res.getFrom()
                        ecode = res.getErrorCode()
                        if ecode==u'404':
                                print 'True'
                                prs=xmpp.protocol.Presence(chat+'/Cool'+str(time.time()))
                                JCON.send(prs)
                                time.sleep(5)
                                iq = xmpp.Iq('set')
                                iq.setTo(chat)
                                query = xmpp.Node('query')
                                query.setNamespace('http://jabber.org/protocol/muc#owner')
                                x = xmpp.Node('x',{'type':'submit'})
                                x.setNamespace(xmpp.NS_DATA)
                                inv=x.addChild('field', {'var':"FORM_TYPE"})
                                inv.setTagData('value', xmpp.NS_MUC_ROOMCONFIG)
                                cap=x.addChild('field', {'var':"muc#roomconfig_persistentroom"})
                                cap.setTagData('value', "1")
                                query.addChild(node=x)
                                iq.addChild(node=query)
                                JCON.send(iq)
                                try:
                                        txt=eval(read_file(DH_FIL))
                                        if chat in txt:
                                                msg(txt[chat]['jid'], chat+u' теперь ваша!!!')
                                                iq = xmpp.Iq('set')
                                                iq.setTo(chat)
                                                iq.setID('owner'+str(random.randrange(1000, 9999)))
                                                query = xmpp.Node('query')
                                                query.setNamespace('http://jabber.org/protocol/muc#admin')
                                                ban=query.addChild('item', {'jid':txt[chat]['jid'], 'affiliation':'owner'})
                                                ban.setTagData('reason', get_bot_nick(chat))
                                                iq.addChild(node=query)
                                                JCON.send(iq)
                                                del txt[chat]
                                                if chat in DH_DIC['chat']:
                                                        del DH_DIC['chat'][chat]
                                                write_file(DH_FILE, str(txt))
                                except:
                                        pass
                                
#def dischc_prs(prs):
#        if DH_DIC['chat']:
#                if not DH_DIC['time'] or time.time() - DH_DIC['time']>1800:
#                        DH_DIC['time']=time.time()
#                        for x in DH_DIC['chat'].keys():
#                                discohack_quest(x)

def dischc_timer():
        while True and DH_DIC['chat']:
                for x in DH_DIC['chat'].keys():
                        discohack_quest(x)
                time.sleep(1800)
        

def dischc_load():
        if not os.path.exists(DH_FIL):
                return
        txt=eval(read_file(DH_FIL))
        if txt:
                for x in txt:
                        DH_DIC['chat'][x]={}
                dischc_timer()
        
        
                
register_command_handler(discohack_start, '!discohack', ['все'], 40, 'Дискаверит указанную конфу с интервалом ~30 мин. Если конфа по каким либо причинам удалена, заходит и делает ее постоянной, отправив при это уведомление вам на жид!', '!discohack room', ['!discohack test@conference.jabber.ru'])
#register_presence_handler(dischc_prs)
register_stage0_init(dischc_load)

