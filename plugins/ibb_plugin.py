#===istalismanplugin===
# -*- coding: utf-8 -*-

import base64

def si_gf_request(frm,fjid,sid,name,size,site):
	iq = xmpp.Protocol(name = 'iq', to = fjid,
		typ = 'set')
	ID = 'si%s' % (time.time())
	iq.setID(ID)
	si = iq.setTag('si')
	si.setNamespace(xmpp.NS_SI)
	si.setAttr('profile', xmpp.NS_FILE)
	si.setAttr('id', sid)
	file_tag = si.setTag('file')
	file_tag.setNamespace(xmpp.NS_FILE)
	file_tag.setAttr('name', name)
	file_tag.setAttr('size', size)
	desc = file_tag.setTag('desc')
	desc.setData(u'Файл "%s".' % (site))
	file_tag.setTag('range')
	feature = si.setTag('feature')
	feature.setNamespace(xmpp.NS_FEATURE)
	_feature = xmpp.DataForm(typ='form')
	feature.addChild(node=_feature)
	field = _feature.setField('stream-method')
	field.setAttr('type', 'list-single')
	field.addOption(xmpp.NS_IBB)
	field.addOption('jabber:iq:oob')
	return iq


def handler_get_file(type, source, parameters):
	groupchat=source[1]
	nick = source[2]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'Эта команда может быть использована только в конференции!')
		return
	
	if parameters:
		url = parameters.strip()
		
		if GROUPCHATS[groupchat].has_key(nick):
			to = GROUPCHATS[groupchat][nick]['jid']
		
		if not to:
			reply(type, source, u'Внутреняя ошибка, невозможно выполнить операцию!')
			return
		
		sid = 'file'+str(random.randrange(10000000, 99999999))
		site = parameters

		if parameters==u'log':
                        if not PUBLIC_LOG_DIR:
                                reply(type, source, u'Логи не включены!')
                                return
                        parameters=os.path.join(PUBLIC_LOG_DIR,source[1],str(time.localtime()[0]),str(time.localtime()[1]),str(time.localtime()[2])+'.html')
		

		if not os.path.exists(parameters):
                        reply(type, source, u'Файла несуществует!')
                        return

                dlsize = os.path.getsize(parameters)

                path = parameters
                name = parameters

		
		try:
			fp = open(path,'rb')
		except:
			reply(type, source, u'Невозможно получить этот файл!')
			return
		
		frm = JID+'/'+RESOURCE
		
		sireq = si_gf_request(frm,to,sid,name,dlsize,site)
		
		JCON.SendAndCallForResponse(sireq, handler_get_file_answ, args={'type':type,'source':source,'sid':sid,'to':to,'fp':fp})
	else:
		reply(type, source, u'Неверный синтаксис!')

		
def handler_get_file_answ(coze,resp,type,source,sid,to,fp):
	try:
		rtype = resp.getType()
		nick = source[2]
		groupchat = source[1]
		
		if rtype == 'result':
                        reply(type, source, u'Передача файла начата!')
                        syn=xmpp.Protocol('iq',to,'set',payload=[xmpp.Node(xmpp.NS_IBB+' open',{'sid':sid,'block-size':'3000','stanza':'message'})])
                        JCON.send(syn)
                        n=1
                        z=3000
                        k=0
                        f=0
                        while 1:
                                data=fp.read(3000)
                                if data=='':
                                        break
                                datanode=xmpp.Node(xmpp.NS_IBB+' data',{'sid':sid,'seq':str(k)},base64.encodestring(data))
                                JCON.send(xmpp.Protocol('message',to,payload=[datanode]))
                                k+=1
                        JCON.send(xmpp.Protocol('iq',to,'set',payload=[xmpp.Node(xmpp.NS_IBB+' close',{'sid':sid})]))
                        reply(type, source, u'Файл передан!')
                        fp.close()
		else:
			fp.close()
			reply(type, source, u'Неудачная передача!')
	except Exception:
                reply(type, source, u'Неизвестная ошибка!')

    
register_command_handler(handler_get_file, 'get_file', ['все'], 100, 'Переда файлов бот--клиент через IBB.Доп.ключ команды - log, передаст файл логов текущей конференции за этот день.', 'get_file file', ['get_file'])

