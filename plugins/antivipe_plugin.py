#===istalismanplugin===
# -*- coding: utf-8 -*-

# by 40tman

AUTO_PRO = []

AVSERVERS=['diary.ru','livejournal.com','vk.com','gajim.org','myjabber.ru','ya.ru','jabber.perm.ru','gmail.com','jabber.ru','xmpp.ru', 'jabbers.ru', 'xmpps.ru', 'qip.ru', 'talkonaut.com', 'jabbus.org','gtalk.com','jabbrik.ru','jabber.cz','jabberon.ru','jabberid.org','linuxoids.net','jabber.kiev.ua','jabber.ufanet.ru','jabber.corbina.ru']

RED_SERVERS=[u'kaluga.org',u'alpha-labs.net',u'jabber.zp.ua',u'burtonini.com',u'braxis.org',u'pop3.ru',u'bugfactory.org',u'jabber.fr',u'jabber.454.ru',u'jabber.chirt.ru',u'aqq.eu',u'newserv.intellectronika.ru',u'jabber.openchaos.org',u'jabber.altline.ru',u'dollchan.ru',u'volity.net']

	
def order_ban_v(groupchat, jid):
        if jid in AVSERVERS:
                return
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', u'Подозрение на вайп атаку!')
	iq.addChild(node=query)
	JCON.send(iq)
		


def protect_spam_serv(groupchat, nick, afl, role):
        global AUTO_PRO
        global AVSERVERS
        if groupchat in AUTO_PRO:
                jid = get_true_jid(groupchat+'/'+nick)
                serv = jid.split('@')[1]
                if serv in AVSERVERS:
                        return
                try:
                        order_ban_v(groupchat, serv)
                        msg(groupchat, u'/me добавил в баню '+serv)
                except:
                        pass
                
def antivipe_ban_serv(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        global AUTO_PRO
        if parameters:
                i = parameters.lower()
                if i.count(u'вайп')>0:
                        l=''
                        for x in RED_SERVERS:
                                l+=x+','
                                order_ban_v(source[1], x)
                        reply(type,source,u'следующие сервера занесены в бан-лист:\n'+l)
                        return
                if i.count(u'урожай')>0:
                        if not source[1] in AUTO_PRO:
                                AUTO_PRO.append(source[1])
                                reply(type,source,u'принимаем урожай!')
                                return
                        else:
                                AUTO_PRO.remove(source[1])
                                reply(type,source,u'прием урожая окончен')
                                return
                order_ban_v(source[1], parameters)
                reply(type,source,parameters+u' в бане')

register_command_handler(antivipe_ban_serv, 'бансерв', ['все','антивайп', 'админ'], 20, 'Банит сервер, ключ вайп-заносит основные сервера используемые вайп-ботами в бан-лист,\nурожай - банит все серверы регистрация которых выполняеться не через сайт.', 'бансерв <сервер>', ['бансерв jabber.zp.ua','бансерв ласт','бансерв урожай'])

