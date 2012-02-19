#===istalismanplugin===
# -*- coding: utf-8 -*-


def roster_sub(type,source,parameters):
        if parameters:
                if not parameters.count('@') or not parameters.count('.'):
                        reply(type,source,u'читай помощь по команде!')
                        return
                ROSTER = JCON.getRoster()
                ROSTER.Subscribe(parameters)
                reply(type,source,u'ok!')

def roster_unsub(type,source,parameters):
        if parameters:
                if  not parameters.count('@') or not parameters.count('.'):
                        reply(type,source,u'читай помощь по команде!')
                        return
                ROSTER = JCON.getRoster()
                ROSTER.Unsubscribe(parameters)
                ROSTER.delItem(parameters)
                reply(type,source,u'ok!')

def roster_all(type,source,parameters):
        ROSTER = JCON.getRoster()
        s=''
        rep = ROSTER.getItems()
        for x in rep:
                s+=x+' : '+unicode(ROSTER.getShow(x))+'\n'
        k=u'All '+str(len(rep))+':\n'
        reply(type,source, k+s)
        
def roster_clean(type, source, parameters):
        R=JCON.getRoster()
        Z=R.getItems()
        us=0
        J=[u'ya.ru',u'jabber.ru',u'xmpp.ru',u'talkonaut.com',u'icq.transport.talkonaut.com',u'jabberon.ru',u'jabber.perm.ru']
        for x in Z:
                if x.count('@'):
                        usr=x.split('@')[1]
                        if not usr in J:
                                us+=1
                                R.Unsubscribe(x)
                                R.delItem(x)
        reply(type, source, u'Remove '+str(us)+u' spam object')

register_command_handler(roster_all, 'roster_all', ['суперадмин','мод'], 100, 'Контакты бота в ростере.', 'roster_all', ['roster_all'])		
register_command_handler(roster_sub, 'roster_add', ['суперадмин','мод'], 100, 'Позволяет добавить контакт в ростер бота.', 'roster_add <jid>', ['roster_add guy@jabber.aq'])
register_command_handler(roster_unsub, 'roster_del', ['суперадмин','мод'], 100, 'Позволяет удалить контакт и подписку из ростера бота.', 'roster_del <jid>', ['рroster_del guy@jabber.aq'])
register_command_handler(roster_clean, 'roster_clean', ['суперадмин','мод'], 100, 'Позволяет удалить spam подписку из ростера бота.', 'roster_clean', ['roster_clean'])
