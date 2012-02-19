#===istalismanplugin===
# -*- coding: utf-8 -*-


JOINSF={}

def leave_nick_stat(groupchat,nick,code,reason):
        if len(nick)>19:
                return
        if groupchat in GROUPCHATS:
                if not groupchat+nick in JOINSF:
                        JOINSF[groupchat+nick] = {'joins':time.time()}
                else:
                        JOINSF[groupchat+nick]['joins'] = time.time()


def show_joins(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if not parameters:
                reply(type,source,u'кого?')
                return
        else:
                if source[1]+parameters in JOINSF and GROUPCHATS[source[1]][parameters]['ishere']==0:
                        seen=int(time.time() - JOINSF[source[1]+parameters]['joins'])
                        mem = timeElapsed(seen)
                        reply(type,source,u'пользователя '+parameters+u' видел '+mem+u' назад')
                        return
                else:
                        if parameters in GROUPCHATS[source[1]]:
                                if GROUPCHATS[source[1]][parameters]['ishere']==1:
                                        reply(type,source,u'он все еще здесь!')
                                        return
                        else:
                                reply(type,source,u'небыло тут таких!')
                
        

register_leave_handler(leave_nick_stat)
register_command_handler(show_joins, 'seen', ['все'], 0, 'показывает время последнего визита пользователя', 'seen <nick>', ['seen abyba'])

