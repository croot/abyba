#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  presence_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.


check_pending=[]

def handler_presence_ra_change(prs):
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid = get_true_jid(groupchat+'/'+nick)
	item = findPresenceItem(prs)
	if jid in GLOBACCESS:
		return
	else:
		if groupchat in ACCBYCONFFILE and jid in ACCBYCONFFILE[groupchat]:
			pass
		else:
			if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat]:
				if jid != None and item != None:
					role = item['role']
					aff = item['affiliation']
					if role in ROLES:
						accr = ROLES[role]
						if role=='moderator' or user_level(jid,groupchat)>=15:
							GROUPCHATS[groupchat][nick]['ismoder'] = 1
						else:
							GROUPCHATS[groupchat][nick]['ismoder'] = 0
					else:
						accr = 0
					if aff in AFFILIATIONS:
						acca = AFFILIATIONS[aff]
					else:
						acca = 0
					access = accr+acca
					change_access_temp(groupchat, jid, access)

def handler_presence_nickcommand(prs):
	groupchat = prs.getFrom().getStripped()
	if groupchat in GROUPCHATS:
		code = prs.getStatusCode()
		if code == '303':
			nick = prs.getNick()
		else:
			nick = prs.getFrom().getResource()
		nicksource=nick.split()[0].strip().lower()
		if nicksource in COMMANDS.keys():
			order_kick(groupchat, nick, get_bot_nick(groupchat)+u' :your nickname is invalid here')
			
def iqkeepalive_and_s2scheck():
	for gch in GROUPCHATS.keys():
		iq=xmpp.Iq()
		iq = xmpp.Iq('get')
		id = 'p'+str(random.randrange(1, 1000))
		globals()['check_pending'].append(id)
		iq.setID(id)
		iq.addChild('ping', {}, [], 'urn:xmpp:ping')
		iq.setTo(gch+'/'+get_gch_info(gch, 'nick'))
		JCON.SendAndCallForResponse(iq, iqkeepalive_and_s2scheck_answ,{})
	try:
                threading.Timer(300, iqkeepalive_and_s2scheck).start()
        except:
                return

def iqkeepalive_and_s2scheck_answ(coze, res):
	id = res.getID()
	if id in globals()['check_pending']:
		globals()['check_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		gch,error=res.getFrom().getStripped(),res.getErrorCode()
		if error in ['405',None]:
			pass
		else:
			try:
                                threading.Timer(60, join_groupchat,(gch,get_gch_info(gch, 'nick') if get_gch_info(gch, 'nick') else DEFAULT_NICK, get_gch_info(gch, 'passw'))).start()
                        except:
                                return

def iqkeepalive_ping():
        if not 'JID' in globals(): return
        any, t = None, time.time()
        iq=xmpp.Iq()
	iq = xmpp.Iq('get')
	id = 'p'+str(random.randrange(1, 1000))
	#globals()['check_pending'].append(id)
	iq.setID(id)
	iq.addChild('ping', {}, [], 'urn:xmpp:ping')
	iq.setTo(JID+'/'+RESOURCE)
	try:
                JCON.SendAndCallForResponse(iq, iqkeepalive_ping_answ,{'t':t,'any':any})
        except:
                print 'Check iqkeepalive failed(1)! \nRESTART!\n'
                os.execl(sys.executable, sys.executable, sys.argv[0])
	try:
                threading.Timer(300, iqkeepalive_ping).start()
        except:
                return

def iqkeepalive_ping_answ(coze, res, t, any):
        if res.getType()=='error':
                print 'Check iqkeepalive failed(2)! \nRESTART!\n'
                os.execl(sys.executable, sys.executable, sys.argv[0])
        else:
                if time.time()-t>180:
                        print 'Check iqkeepalive failed(3)! \nRESTART!\n'
                        os.execl(sys.executable, sys.executable, sys.argv[0])
                else:
                        z=time.time()-t
                        print z

register_stage2_init(iqkeepalive_ping)


register_presence_handler(handler_presence_ra_change)
register_presence_handler(handler_presence_nickcommand)

register_stage2_init(iqkeepalive_and_s2scheck)
