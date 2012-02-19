#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman

AUTO_ROL={}


def auto_moderator(type, source, parameters):
    userjid = get_true_jid(source[1]+'/'+parameters)
    try:
        AUTO = 'dynamic/auto.txt'
        base = eval(read_file(AUTO))
    except:
        reply(type,source,u'check file dynamic/auto.txt')
        return
    if parameters:
        t = parameters.lower()
        if t.count(u'дел')>0 and t.count('-')>0:
            numb=parameters.split('-')
            v=0
            for x in base['AMODER']:
                if x.count(source[1]):
                    full = x.split(source[1])
                    v+=1
                    if unicode(v)==numb[1]:
                        base['AMODER'].remove(x)
                        write_file(AUTO,str(base))
                        reply(type,source,full[1]+u' убран')
                        arol_load()
                        return
        if source[1] in GROUPCHATS:
            if parameters in GROUPCHATS[source[1]]:
                if not source[1]+userjid in base['AMODER']:
                    base['AMODER'].append(source[1]+userjid)
                    write_file(AUTO,str(base))
                    auto_set_roles(source[1],parameters,'moderator','amoderator')
                    reply(type,source,u'пользователь '+parameters+u' добавлен!')
                    arol_load()
                else:
                    base['AMODER'].remove(source[1]+userjid)
                    write_file(AUTO,str(base))
                    reply(type,source,u'амодератор '+parameters+u' снят!')
                    arol_load()
            if parameters not in GROUPCHATS[source[1]]:
                reply(type,source,u'а он тут?')
    else:
        d=''
        n=0
        for x in base['AMODER']:
            if x.count(source[1]):
                k= x.split(source[1])
                n+=1
                d+=unicode(n)+') '+k[1]+'\n'
        if d=='':
            reply(type,source,u'список пуст!')
            return
        reply(type,source,d)

def auto_kick(type,source,parameters):
    AUTO = 'dynamic/auto.txt'
    base = eval(read_file(AUTO))
    if parameters:
        t = parameters.lower()
        s = parameters.split()
        if t.count(u'дел')>0 and t.count('-')>0:
            numb = t.split('-')
            if len(numb[1])>3 or len(numb[1])==0:
                return
            allkick=''
            j =0
            for x in base['AKICK']:
                if x.count(source[1]):
                    g = x.split(source[1])
                    j+=1
                    if unicode(j)==numb[1]:
                        base['AKICK'].remove(x)
                        write_file(AUTO,str(base))
                        reply(type,source,g[1]+u' удалeн!')
                        arol_load()
                        return
            for m in base['COUNT']:
                if base['COUNT'][m]['chat']==source[1]:
                    j+=1
                    if unicode(j)==numb[1]:
                        del base['COUNT'][m]
                        write_file(AUTO,str(base))
                        reply(type,source,m+u' удален')
                        arol_load()
                        return
                    else:
                        reply(type,source,u'нет такого!')
                        return
                else:
                    return
        if t.count(' ')>0 and t.count('.count')>0:
            if t.count('*')>0:
                d = parameters.split('*')
                base['COUNT'][d[1]]={'chat':source[1],'time':time.time()}
                write_file(AUTO,str(base))
                reply(type,source,u'в акик добавлены все ники содержащие '+d[1])
                arol_load()
                return
        if source[1] in GROUPCHATS:
            if len(parameters)>3:
                if t.count(u'дел')>0 and t.count(u'-')>0:
                    return
                if not source[1]+parameters in base['AKICK']:
                    base['AKICK'].append(source[1]+parameters)
                    write_file(AUTO,str(base))
                    reply(type,source,parameters+u' добавлено!')
                    arol_load()
                    if parameters in GROUPCHATS[source[1]]:
                        auto_set_roles(source[1],parameters,'none',u'ты в акик листе!')
                else:
                    base['AKICK'].remove(source[1]+parameters)
                    write_file(AUTO,str(base))
                    reply(type,source, parameters+u' удален!')
                    arol_load()
    else:
        allkick=''
        j =0
        for x in base['AKICK']:
            if x.count(source[1]):
                g = x.split(source[1])
                j+=1
                allkick+=unicode(j)+') '+g[1]+';\n'
        for m in base['COUNT']:
            if base['COUNT'][m]['chat']==source[1]:
                j+=1
                allkick+=unicode(j)+') *'+m+';\n'
        if allkick=='':
            reply(type,source,u'список пуст!')
            return
        reply(type,source,'\n'+allkick)
        return

def auto_visitor(type,source,parameters):
    AUTO = 'dynamic/auto.txt'
    base = eval(read_file(AUTO))
    if parameters and source[1] in GROUPCHATS:
        t = parameters.lower()
        if source[1]+parameters in base['AVISITOR']:
                base.remove(source[1]+parameters)
                write_file(AUTO,str(base))
                reply(type,source,parameters+u' удален!')
                arol_load()
                return
        else:
                base['AVISITOR'].append(source[1]+parameters)
                write_file(AUTO,str(base))
                reply(type,source,parameters+u' добавлено!')
                arol_load()
                if parameters in GROUPCHATS[source[1]]:
                        auto_set_roles(source[1],parameters,'visitor',u'read only')
    else:
        d=''
        n=0
        for x in base['AVISITOR']:
            if x.count(source[1]):
                k= x.split(source[1])
                n+=1
                d+=unicode(n)+') '+k[1]+'\n'
        if d.isspace():
            reply(type,source,u'список пуст!')
            return
        reply(type,source,d)
                    
def autoroles_join_rm(groupchat,nick,afl,role):
    if groupchat not in GROUPCHATS:
        return
    if len(nick)>25:
        return
    jid = get_true_jid(groupchat+'/'+nick)
    base=AUTO_ROL
    if 'COUNT' in base:
        for x in base['COUNT']:
            if groupchat == unicode(base['COUNT'][x]['chat']) and nick.count(unicode(x))>0:
                auto_set_roles(groupchat,nick,'none',u'ты в акик листе')
    if groupchat+jid in base['AMODER']:
        auto_set_roles(groupchat,nick,'moderator','amoderator')
        return
    if groupchat+nick in base['AKICK'] or groupchat+jid in base['AKICK']:
        auto_set_roles(groupchat,nick,'none',u'ты в акик листе')
        return
    if groupchat+nick in base['AVISITOR'] or groupchat+jid in base['AVISITOR']:
        auto_set_roles(groupchat,nick,'visitor','read only')
        return
        
     
def auto_set_roles(groupchat, nick, rol, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':rol})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def auto_rol_init(groupchat):
    if not AUTO_ROL:
        try:
            AUTO = 'dynamic/auto.txt'
            base = eval(read_file(AUTO))
            for x in base:
                AUTO_ROL[x]=base[x]
        except:
            print 'error in dynamic/auto.txt'

def arol_load():
    if AUTO_ROL:
        for k in AUTO_ROL.keys():
            del AUTO_ROL[k]
    try:
        if check_file(file='auto.txt'):
            AUTO = 'dynamic/auto.txt'
            base = eval(read_file(AUTO))
            w=0
            if not 'COUNT' in base:
                base['COUNT']={}
                w=1
            if not 'AMODER' in base:
                base['AMODER']=[]
                w=1
            if not 'AVISITOR' in base:
                base['AVISITOR']=[]
                w=1
            if not 'AKICK' in base:
                base['AKICK']=[]
                w=1
            if w:
                write_file(AUTO, str(base))
                base = eval(read_file(AUTO))
            for x in base:
                AUTO_ROL[x]=base[x]
    except: print 'error in dynamic/auto.txt'

register_stage1_init(auto_rol_init)

register_join_handler(autoroles_join_rm)
register_command_handler(auto_moderator, 'амодератор', ['все'], 20, 'Добавляет ник юзера в автомодераторы.Без параметров показывает список.Чтобы удалить жид пользуемся ключом <дел -> после минуса вписываем номер в списке,например: амодератор дел -1', 'амодератор <ник>', ['амодератор Вася'])
register_command_handler(auto_kick, 'акик', ['все'], 20, 'Добавляет ник либо jid в автокик,без параметров покажет акик лист,дополнительные ключи команды:  .count *В - будет кикать все ники содержащие <В>; дел -1 - удалит из списка елемент с номером <1>', 'акик <ник>', ['акик Вася','акик .count *В'])
register_command_handler(auto_visitor, 'авизитор', ['все'], 20, 'Добавляет/удаляет ник либо jid в список пользователей без права голоса.Без параметров показывает список.', 'авизитор <ник>', ['авизитор Вася'])

ping_pd=[]
CK_US={}
VOI_CE={}
	
def handler_ch_ping(groupchat,nick,afl,role):
    if not groupchat in CK_US:
        return
    if time.time() - INFO['start'] < 60:
        return
    if groupchat+nick in VOI_CE:
        if time.time() - VOI_CE[groupchat+nick]['time']<3:
            return
        else:
            VOI_CE[groupchat+nick]['time']=time.time()
    if not groupchat+nick in VOI_CE:
        VOI_CE[groupchat+nick]={'time':time.time()}
    base=AUTO_ROL
    jid=groupchat+'/'+nick
    rjid=get_true_jid(groupchat+'/'+nick)
    if rjid in ADMINS:
        return
    if AUTO_ROL:
        if 'AMODER' in AUTO_ROL and 'AVISITOR' in AUTO_ROL:
            if (groupchat+rjid in base['AMODER']) | (groupchat+rjid in base['AVISITOR']) | (groupchat+nick in base['AVISITOR']):
                return
    auto_set_roles(groupchat, nick, 'visitor', 'ping')
    iq = xmpp.Iq('get')
    id = 'p'+str(random.randrange(1, 1000))
    globals()['ping_pd'].append(id)
    iq.setID(id)
    iq.addChild('query', {}, [], 'jabber:iq:version');
    iq.setTo(jid)
    JCON.SendAndCallForResponse(iq, handler_chus_answ,{'groupchat': groupchat, 'nick': nick})

def handler_chus_answ(coze, res, groupchat, nick):
    id = res.getID()
    if id in globals()['ping_pd']:
        globals()['ping_pd'].remove(id)
    else:
	    print 'someone is doing wrong(check_userping)...'
	    return
    if res:
	    if res.getType() == 'result':
                auto_set_roles(groupchat, nick, 'participant', 'ok')
		return
	    else:
		return

def check_user_or_bot(groupchat):
        try:
                file='dynamic/check_us_or_bot.txt'
                fp=open(file,'r')
                txt=eval(fp.read())
                fp.close()
        except:
                print 'no file dynamic/check_us_or_bot.txt'
                return
        for x in txt:
                if not x in CK_US:
                        CK_US[x]={}

def hndd_wrus_ping(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if not parameters:
                return
        try:
                file='dynamic/check_us_or_bot.txt'
                fp=open(file,'r')
                txt=eval(fp.read())
                fp.close()
        except:
                return
        if parameters =='1':
                reply(type,source,'ok')
                if not source[1] in CK_US:
                        CK_US[source[1]]={}
                if not source[1] in txt:
                        txt[source[1]]={}
                        write_file(file,str(txt))
                        return
        if parameters=='0':
                reply(type,source,'ok')
                if source[1] in CK_US:
                        del CK_US[source[1]]
                if source[1] in txt:
                        del txt[source[1]]
                        write_file(file,str(txt))
                        return

        
register_join_handler(handler_ch_ping)                
register_stage1_init(check_user_or_bot)
register_command_handler(hndd_wrus_ping, 'юзер_пинг', ['мод', 'антивайп', 'антиспам', 'админ'], 20, 'Пингует вошедшего юзера,если нет ответа-лишает без голоса-т.к. скорее всего это бот', 'юзер_пинг <0|1>', ['юзер_пинг 1'])


