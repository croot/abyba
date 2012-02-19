#===istalismanplugin===
# -*- coding: utf-8 -*-

PRFILT={}

def prsfilt_set(type, source, parameters):
    try:
        jid=get_true_jid(source[1]+'/'+source[2])
        if not jid or jid.count('@conference'):
            reply(type, source, u'нет возможности получить ваш JabberID')
            return
        if not parameters or parameters.isspace():
            reply(type, source, u'так не пойдет')
            return
        n=1
        if parameters.count(' '):
            s=parameters.split()
            if s[1].isdigit() and int(s[1])<10:
                n=int(s[1])
                parameters=s[0]
        if parameters==source[2]:
            reply(type, source, u'это ваш ник!')
            return
        if len(PRFILT)>9:
            reply(type, source, u'сработал лимит команды т.к. более 9-ти человек используют ее')
            return
        if len(parameters)<3:
            reply(type, source, u'искомый ник должен содержать не менее трех символов!')
            return
        if GROUPCHATS:
            for x in GROUPCHATS.keys():
                for c in GROUPCHATS[x]:
                    if c.count(parameters) or c==parameters:
                        if GROUPCHATS[x][c]['ishere']:
                            reply(type, source, u'пользователь с ником '+parameters+u' сейчас в '+x)
                            return
        PRFILT[jid]={'nick':parameters, 'result':0, 'n':n, 'off':[]}
        reply(type, source, u'дам знать как только увижу '+parameters)
    except Exception, err:
        pass

def prsjoin(groupchat, nick, a, b):
    global PRFILT
    jid=get_true_jid(groupchat+'/'+nick)
    if jid in PRFILT.keys():
        if PRFILT[jid]['off']:
            rep=''
            for m in PRFILT[jid]['off']:
                rep+=m+'\n'
            msg(groupchat+'/'+nick, rep)
            if PRFILT[jid]['result']==PRFILT[jid]['n']:
                del PRFILT[jid]
            return
    if PRFILT:
        for x in PRFILT.keys():
            if 'nick' in PRFILT[x].keys():
                if nick.count(PRFILT[x]['nick']) or nick == PRFILT[x]['nick']:
                    PRFILT[x]['result']+=1
                    rep_finded(groupchat,nick,x)
                    break

def rep_finded(chat, nick, jid):
    t=0
    tim=''
    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
    tim=str(hour)+':'+str(minute)+':'+str(second)
    if GROUPCHATS:
        for x in GROUPCHATS.keys():
            for c in GROUPCHATS[x]:
                if GROUPCHATS[x][c]['jid'].split('/')[0]==jid and GROUPCHATS[x][c]['ishere']:
                    print 'result'
                    msg(x+'/'+c, u'пользователь с ником '+nick+u' только что зашел в '+chat)
                    t=1
                    if PRFILT[jid]['result']==PRFILT[jid]['n']:
                        del PRFILT[jid]
                    break
    if not t:
        if not PRFILT[jid]['result']>PRFILT[jid]['n']:
            PRFILT[jid]['off'].append(u'видел пользователя ['+tim+']'+nick+u' в '+chat)
    
register_join_handler(prsjoin)
register_command_handler(prsfilt_set, 'стрелка', ['все'], 0, 'даст вам знать как только увидит определенный ник в конференциях где сидит бот, есть доп параметер- кол-во. результатов, по умолчанию 1', 'стрелка <ник> <кол-во>', ['стрелка вася'])

