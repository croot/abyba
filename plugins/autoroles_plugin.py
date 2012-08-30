#===istalismanplugin===
# -*- coding: utf-8 -*-


AUTO_MUC = {}

AUTO_MUC_FILE = 'dynamic/auto.txt'

check_file(file='auto.txt')


def auto_moderator(type, source, p):
    global AUTO_MUC_FILE
    global AUTO_MUC

    if not source[1] in GROUPCHATS:
        return
    
    try: db = eval(read_file(AUTO_MUC_FILE))
    except:
        reply(type,source,u'Ошибка в файле \"dynamic/auto.txt\"!')
        return
    
    if p:
        t = p.lower()
        
        if t.count(u'дел')>0 and t.count('-')>0:
            numb = p.split('-')
            if len(numb[1].strip())>3 or len(numb[1].strip())==0:
                return
            if not source[1] in db.keys():
                reply(type, source, u'Пустой список!')
                return
            try:
                list = db[source[1]][2].keys()
                if len(list)<int(numb[1].strip()):
                    relpy(type, source, u'Неверный ввод!')
                    return
                who = list[int(numb[1].strip())]
                del db[source[1]][2][db[source[1]][2].keys()[int(numb[1].strip())]]
                write_file(AUTO_MUC_FILE, str(db))
                reply(type,source, who+u' удалeн!')
                AUTO_MUC = db.copy()
                return
            except:
                reply(type, source, u'Произошла ошибка!')
                return

            
        if not source[1] in db.keys():
            db[source[1]] = {}

        if not 2 in db[source[1]].keys():
            db[source[1]][2] = {}

        if not p in db[source[1]][2].keys():
            db[source[1]][2][p] = {}
            write_file(AUTO_MUC_FILE, str(db))
            auto_set_roles(source[1], p, 'moderator', 'amoderator')
            reply(type, source, u'Пользователь \"'+p+u'\" добавлен!')
            AUTO_MUC = db.copy()
            return
        else:
            del db[source[1]][2][p]
            write_file(AUTO_MUC_FILE, str(db))
            reply(type,source,u'Автомодер с \"'+p+u'\" снят!')
            auto_set_roles(source[1], p,'participant',u'command '+source[2])
            AUTO_MUC = db.copy()
            return
            
    else:
        try:
            list = [str(db[source[1]][2].keys().index(x))+') '+x for x in db[source[1]][2].keys()]
            if not list:
                reply(type, source, u'Список пуст!')
                return
            reply(type, source, '\n'.join(list))
        except:
            reply(type, source, u'Список пуст!')
            return

        
def auto_kick(type, source, p):
    global AUTO_MUC_FILE
    global AUTO_MUC

    if not source[1] in GROUPCHATS or p==get_bot_nick(source[1]):
        return
    
    db, rep = eval(read_file(AUTO_MUC_FILE)), ''

    if p:
        t = p.lower()
        s = p.split()

        if t.count(u'дел') and t.count('-'):
            numb = t.split('-')
            if len(numb[1].strip())>3 or len(numb[1].strip())==0:
                return
            if not source[1] in db.keys():
                reply(type, source, u'Пустой список!')
                return
            try:
                list = db[source[1]][1].keys()
                if len(list)<int(numb[1].strip()):
                    relpy(type, source, u'Неверный ввод!')
                    return
                who = list[int(numb[1].strip())]
                del db[source[1]][1][db[source[1]][1].keys()[int(numb[1].strip())]]
                write_file(AUTO_MUC_FILE, str(db))
                reply(type,source, who+u' удалeн!')
                AUTO_MUC = db.copy()
                return
            except Exception, err:
                reply(type, source, u'Произошла ошибка!')

            
        if not source[1] in db.keys():
            db[source[1]] = {}

        if not 1 in db[source[1]].keys():
            db[source[1]][1]={}
            
        if t.count(' ') and t.count('.count') and t.count('*')>0:
            dd = p.split('*')
            db[source[1]][1] = '*'+dd[1].strip()
            write_file(AUTO_MUC_FILE, str(db))
            reply(type, source, u'В акик добавлены все ники содержащие \"'+dd[1].strip()+'\"!')
            AUTO_MUC = db.copy()
            return
        
        if not p in db[source[1]][1].keys():
            db[source[1]][1][p] = {}
            write_file(AUTO_MUC_FILE ,str(db))
            reply(type, source, p+u' добавлено!')
            AUTO_MUC = db.copy()
            if p in GROUPCHATS[source[1]]:
                auto_set_roles(source[1], p,'none',u'Autokick!')
        else:
            del db[source[1]][1][p]
            write_file(AUTO_MUC_FILE, str(db))
            reply(type,source, p+u' удален!')
            AUTO_MUC = db.copy()
    else:
        try:
            list = [str(db[source[1]][1].keys().index(x))+') '+x for x in db[source[1]][1].keys()]
            if not list:
                reply(type, source, u'Список пуст!')
                return
            reply(type, source, '\n'.join(list))
        except:
            reply(type, source, u'Список пуст!')
            return
        

def auto_visitor(type, source, p):
    global AUTO_MUC_FILE
    global AUTO_MUC

    if not source[1] in GROUPCHATS: return
    
    db = eval(read_file(AUTO_MUC_FILE))

    if p:
        t = p.lower()
        
        if t.count(u'дел')>0 and t.count('-')>0:
            numb = p.split('-')
            if len(numb[1].strip())>3 or len(numb[1].strip())==0:
                return
            if not source[1] in db.keys():
                reply(type, source, u'Пустой список!')
                return
            try:
                list = db[source[1]][3].keys()
                if len(list)<int(numb[1].strip()):
                    relpy(type, source, u'Неверный ввод!')
                    return
                who = list[numb[1].strip()]
                del db[source[1]][3][db[source[1]][3].keys()[int(numb[1].strip())]]
                write_file(AUTO_MUC_FILE, str(db))
                reply(type,source, who+u' удалeн!')
                AUTO_MUC = db.copy()
                return
            except:
                reply(type, source, u'Произошла ошибка!')
                return
            
        if not source[1] in db.keys():
            db[source[1]] = {}

        if not 3 in db[source[1]].keys():
            db[source[1]][3] = {}
        
        if not p in db[source[1]][3].keys():
            db[source[1]][3][p] = {}
            write_file(AUTO_MUC_FILE ,str(db))
            reply(type, source, p+u' добавлено!')
            AUTO_MUC = db.copy()
            if p in GROUPCHATS[source[1]]:
                auto_set_roles(source[1],parameters,'none',u'Autokick!')
        else:
            del db[source[1]][3][p]
            write_file(AUTO_MUC_FILE, str(db))
            reply(type,source, p+u' удален!')
            AUTO_MUC = db.copy()
    else:
        try:
            list = [str(db[source[1]][3].keys().index(x))+') '+x for x in db[source[1]][3].keys()]
            if not list:
                reply(type, source, u'Список пуст!')
                return
            reply(type, source, '\n'.join(list))
        except:
            reply(type, source, u'Список пуст!')
            return
        
                    
def autoroles_join_rm(gch,nick,afl,role):
    global AUTO_MUC
    if not gch in GROUPCHATS or len(nick)>25: return

    jid = get_true_jid(gch+'/'+nick)

    if not gch in AUTO_MUC.keys(): return

    if nick == get_bot_nick(gch): return

    if 1 in AUTO_MUC[gch]:
        for x in AUTO_MUC[gch][1].keys():
            if x[:1] == '*' and nick.count(unicode(x))>0:
                auto_set_roles(gch, nick, 'none', u'Autokick!')
                
    if 2 in AUTO_MUC[gch].keys():
        if jid in AUTO_MUC[gch][2].keys() or nick in AUTO_MUC[gch][2].keys():
            auto_set_roles(gch, nick,'moderator','Amoderator')

    if 1 in AUTO_MUC[gch].keys():
        if jid in AUTO_MUC[gch][1].keys() or nick in AUTO_MUC[gch][1].keys():
            auto_set_roles(gch, nick, 'none', u'Autokick!')

    if 3 in AUTO_MUC[gch].keys():
        if jid in AUTO_MUC[gch][3].keys() or nick in AUTO_MUC[gch][3].keys():
            auto_set_roles(gch, nick,'visitor','Read only!')
    
        
     
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
    global AUTO_MUC
    global AUTO_MUC_FILE
    
    if not AUTO_MUC:
        try:
            db = eval(read_file(AUTO_MUC_FILE))
            AUTO_MUC = db.copy()
        except: write_file()
        

register_stage1_init(auto_rol_init)
register_join_handler(autoroles_join_rm)
register_command_handler(auto_moderator, 'амодератор', ['все'], 20, 'Добавляет ник юзера в автомодераторы.Без параметров показывает список.Чтобы удалить жид пользуемся ключом \"дел - номер\", после минуса вписываем номер в списке,например: амодератор дел -1', 'амодератор <ник>', ['амодератор Вася'])
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


