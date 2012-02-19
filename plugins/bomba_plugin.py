#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman
COLOR = [u'красный',u'зеленый',u'черный',u'синий',u'белый',u'желтый',u'серый',u'оранжевый',u'фиолетовый']
PROVOD =[]
FLL={}
FLL2={}
BOMB_FRA=[u' неудачный сапер!',u' оя-яй-яй!падарвался баец!',u' покойся с миром!',u' теперь в космосе!!!']

def bomb_send(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
        if not parameters:
                reply(type, source, u'Кому?')
                return
        if type=='private':
                reply(type,source,u'разрешено только в общем чате!')
                return
        if not parameters in GROUPCHATS[source[1]]:
                reply(type,source,u'а он тут?')
                return
        if parameters in FLL2:
                return
        if not parameters:
                parameters=source[2]
        tim = random.randrange(20,45)
        e = u', вам вручена бомба, на ней '
        rd = random.randrange(15,27)
        hh = random.choice(COLOR)
        d =''
        for x in COLOR:
                if len(d)<rd:
                        d +=x+' '
                        #print d
                        PROVOD.append(x)
                        if not parameters in FLL:
                                FLL[parameters]={'w':1}
                        else:
                                FLL[parameters]['w']+=1
        s = random.choice(PROVOD)
        #print s,'prav'
        FLL2[parameters]={'answ':s}
        l = unicode(FLL[parameters]['w'])
        msg(source[1],u'/me '+parameters+e+l+u' провода: '+d+u' выберите цвет провода который нужно перерезать, на таймере '+unicode(tim)+u' sek.')
        PROVOD.remove(s)
        del FLL[parameters]
        print 'ok'
        bomb_start(source[1],parameters,tim)

def kick_bomb(groupchat, nick, reason=''):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)
	time.sleep(0.1)
	jid=get_true_jid(groupchat+'/'+nick)
	try:
                if groupchat in order_stats and jid in order_stats[groupchat]:
                        order_stats[groupchat][jid]['kicks']=0
        except:
                pass

def bomb_start(groupchat,nick,tim):
        time.sleep(tim)
        if nick in FLL2 and nick in GROUPCHATS[groupchat]:
                kick_bomb(groupchat,nick,u'птыдыщь!')
                rep=random.choice(BOMB_FRA)
                msg(groupchat, u'/me '+nick+rep)
                del FLL2[nick]
                
def bomb_msg(raw,type,source,parameters):
        if source[1] not in GROUPCHATS:
                return
        if source[2] in FLL2:
                ad = parameters.lower()
                if ad in FLL2[source[2]]['answ']:
                        msg(source[1],u'/me '+source[2]+u', бомба обезврежена!')
                        del FLL2[source[2]]
                        return
                else:
                        kick_bomb(source[1],source[2],u'птыдыщь!')
                        rep=random.choice(BOMB_FRA)
                        msg(source[1],u'/me '+source[2]+rep)
                        del FLL2[source[2]]

def bomb_leave(groupchat,nick,pr,prr):
        if nick in FLL2:
                msg(groupchat,u'бомба не обезврежена,'+nick+u' сосцал')
                del FLL2[nick]
                
register_leave_handler(bomb_leave)                    
register_message_handler(bomb_msg)
register_command_handler(bomb_send, 'бомба', ['мук','все'], 15, 'Вручает учасникам бомбу),если перерезать не той провод будет кик, время 15 секунд', 'бомба <nick>', ['бомба abyba'])
