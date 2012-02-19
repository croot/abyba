#===istalismanplugin===
# -*- coding: utf-8 -*-

try:
        MK = 'dynamic/macros.txt'
        fp0 = file(MK, 'r')
        MX = eval(read_file(MK))
        fp0.close()
except:
        pass

TIME_ABORT=[]

LAST_FRA={}
SMALL_FRA=[u'ась?',u'а по-подробней?',u'и что ты хочешь сказать?',u'это что,все?']
BOLTUN={}
BOLTUN_QIP={}


def boltun_check_fra(fra):
        if not BOLTUN_QIP:
                return
        for x in BOLTUN_QIP:
                s=x.split('==')
                if s[0].count(fra)>0:
                        a1 = len(fra)
                        a2 = len(s[0])
                        if a1==a2:
                                return 1
                        if a1==(a2)+1:
                                return 1
                        if a1==(a2)-1:
                                return 1
        return 0
        
def boltun_qip(raw, type, source, parameters):
        if type=='private':
                return
        if not LAST_FRA.has_key(get_true_jid(source[1]+'/'+source[2])):
                LAST_FRA[get_true_jid(source[1]+'/'+source[2])]={'time':time.time(),'fra':''}
        else:
                if time.time() - LAST_FRA[get_true_jid(source[1]+'/'+source[2])]['time']<2.5:
                        return
                else:
                        LAST_FRA[get_true_jid(source[1]+'/'+source[2])]['time']=time.time()
        p=parameters.split()[0]
        if len(parameters)==1:
                rep=random.choice(SMALL_FRA)
                reply(type,source,rep)
                return
        ANSW=[]
        FRA=[]
        if not parameters.count(' '):
                FRA.append(parameters)
        if parameters.count(' '):
                pk=parameters.split()
                pk.sort()
                n=0
                for x in pk:
                        n+=1
                        if n==1:
                                if boltun_check_fra(x)==1:
                                        FRA.append(x)
                        if n==2:
                                if not FRA:
                                        if boltun_check_fra(x)==1:
                                                FRA.append(x)
                        if n==3:
                                if not FRA:
                                        if boltun_check_fra(x)==1:
                                                FRA.append(x)
        j=parameters.split()
        n=parameters.count(' ')
        for c in FRA:
                if len(c)>1:
                        c=c.lower()
                        if c.count('?') | c.count('!') | c.count('.') | c.count(','):
                                c=c.replace('?','').replace('!','').replace('.','').replace(',','')
                        for x in BOLTUN_QIP:
                                s=x.split('==')
                                if s[0].count(c)>0:
                                        a1=len(s[0])
                                        a2=len(c)
                                        if a1==a2:
                                                ANSW.append(s[1])
                                        if a1==(a2)+1:
                                                ANSW.append(s[1])
                                        if a1==(a2)-1:
                                                ANSW.append(s[1])
        b1=''
        n=random.randrange(2, 15)
        if ANSW:
                b1=random.choice(ANSW)
                if b1 not in LAST_FRA[get_true_jid(source[1]+'/'+source[2])]['fra']:
                        LAST_FRA[get_true_jid(source[1]+'/'+source[2])]['fra']=b1
                else:
                        return
        else:
                return
        time.sleep(n)
        reply(type,source,b1)
        LAST_FRA[get_true_jid(source[1]+'/'+source[2])]['time']=time.time()
        ANSW=['']
        FRA=['']


def fraza_time(fraza):
        if fraza in TIME_ABORT:
                return 1
        return 0

def fraza_append(fraza):
        TIME_ABORT.append(fraza)
        time.sleep(25)
        TIME_ABORT.remove(fraza)



def boltun_work(raw, type, source, parameters):
        base = BOLTUN
        if not base:
                return
        real_jid=get_true_jid(source[1]+'/'+source[2])
        if real_jid == CHAT_TO_JID['jid']:
                return
        xxc = parameters.split()
        body = parameters.lower()
        if source[1] in base['OFF']:
                return
        if parameters.count(' '):
                save = ' '.join(xxc[1:])
        else:
                save =''
        rnumb = random.randrange(1, 100)
        rtime = random.randrange(1, 9)
        if (body.count(' ') > 0):
                dss = xxc[1].lower()
        else:
                dss =''
        hgfw = int(user_level(source[1]+'/'+source[2], source[1]))
        if hgfw == -100 or hgfw == '-100':
                return
        if dss:
                if dss in COMMANDS or dss in MX:
                        return
        dff = xxc[0].lower()
        if dff in COMMANDS or dff in MX:
                return
        if xxc[0] in COMMANDS:
                return
        if source[2] == '':
                return
        if body in COMMANDS:
                return
        botnick = get_bot_nick(source[1])
        if source[2] == botnick:
                return
        if unicode(rnumb) == '5':
                boltun_qip(raw, type, source, parameters)
                return
        if base.has_key('FRAZA_BOT'):
                FRAZA_BOT = base['FRAZA_BOT']
        else:
                FRAZA_BOT = {}
        if base.has_key('FRAZA_USER'):
                FRAZA_USER = base['FRAZA_USER']
        else:
                FRAZA_USER = {}

        if base.has_key('FRAZA_ALL'):
                FRAZA_ALL = base['FRAZA_ALL']
        else:
                FRAZA_ALL = {}
        if base.has_key('FRAZA_ADMIN'):
                FRAZA_ADMIN = base['FRAZA_ADMIN']
        else:
                FRAZA_ADMIN = {}

        if source[1] in GROUPCHATS:
                nicks = GROUPCHATS[source[1]]
        else:
                nicks =''
        msgfor = 'all'
        if hgfw >16:
                msgfor = 'all2'
        if parameters.count(' ') > 0:
                if xxc[0].count(botnick)>0:
                        msgfor = 'bot'
                else:
                        for nick in nicks:
                                if parameters.split(' ')[0].count(nick) > 0:
                                        msgfor = 'user'
        if type=='private':
                return
                msgfor='bot'
        if msgfor == 'bot':
                for fr in FRAZA_BOT:
                        if (body.count(fr) > 0):
                                res = random.choice( FRAZA_BOT[fr] )
                                if fraza_time(res)==0:
                                        reply(type,source,res)
                                        fraza_append(res)
                                        return
                                else:
                                        return
        if msgfor == 'bot':
                for fr in FRAZA_BOT:
                        if (body.count(fr) == 0):
                                boltun_qip(raw, type, source, parameters)
                                return
                        else:
                                return
                                        
        elif msgfor == 'user':
                for fr in FRAZA_USER:
                        if (body.count(fr) > 0):
                                time.sleep(rtime)
                                res = random.choice( FRAZA_USER[fr] )
                                reply(type, source, res)
                                return
        elif msgfor == 'all':
                if type == 'private':
                        return
                for fr in FRAZA_ALL:
                        if hgfw < 19:
                                if (body.count(fr) > 0):
                                        res = random.choice( FRAZA_ALL[fr] )
                                        if fraza_time(res)==0:
                                                time.sleep(rtime)
                                                reply(type,source,res)
                                                fraza_append(res)
                                                return
                                        else:
                                                return

        elif msgfor == 'all2':
                if type == 'private':
                        return
                for fr in FRAZA_ADMIN:
                        if (body.count(fr) > 0):
                                time.sleep(rtime)
                                res = random.choice( FRAZA_ADMIN[fr] )
                                reply(type, source, res)

def boltun_sav(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters:
                if not parameters.count('='):
                        reply(type,source,u'неправильный ввод!')
                        return
                das = parameters.split('=')
                dfg = das[1].split(';')
                base['FRAZA_BOT'][das[0]] = (dfg)
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])
                return
        else:
                g=''
                for x in base['FRAZA_BOT']:
                        j=''
                        for s in base['FRAZA_BOT'][x]:
                                j+=s+';'
                        g+= x+'='+j
                if g=='':
                        reply(type,source,u'none')
                        return
                reply(type,source,g)

def boltun_frb_dell(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters in base['FRAZA_BOT']:
                del base['FRAZA_BOT'][parameters]
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])

def boltun_save_frall(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW)) 
        if parameters:
                if not parameters.count('='):
                        reply(type,source,u'неправильный ввод!')
                        return
                das = parameters.split('=')
                dfg = das[1].split(';')
                base['FRAZA_ALL'][das[0]] = (dfg)
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])
                return
        else:
                g=''
                for x in base['FRAZA_ALL']:
                        j=''
                        for s in base['FRAZA_ALL'][x]:
                                j+=s+';'
                        g+= x+'='+j
                if g=='':
                        reply(type,source,u'none')
                        return
                reply(type,source,g)

def boltun_fra_dell(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters in base['FRAZA_ALL']:
                del base['FRAZA_ALL'][parameters]
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])

def boltun_sav_frad(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters:
                if not parameters.count('='):
                        reply(type,source,u'неправильный ввод!')
                        return
                das = parameters.split('=')
                dfg = das[1].split(';')
                base['FRAZA_ADMIN'][das[0]] = (dfg)
                write_file(TREW,str(base))
                fp.close()
                reply(type, source,'Ok')
                boltun_init(source[1])
                return
        else:
                g=''
                for x in base['FRAZA_ADMIN']:
                        j=''
                        for s in base['FRAZA_ADMIN'][x]:
                                j+=s+'; '
                        g+= x+'='+j
                if g=='':
                        reply(type,source,u'none')
                        return
                reply(type, source,g)
                        

def boltun_frad_dell(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters in base['FRAZA_ADMIN']:
                del base['FRAZA_ADMIN'][parameters]
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])


def boltun_save_fruser(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters:
                if not parameters.count('='):
                        reply(type,source,u'неправильный ввод!')
                        return
                das = parameters.split('=')
                dfg = das[1].split(';')
                base['FRAZA_USER'][das[0]] = (dfg)
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])
                return
        else:
                g=''
                for x in base['FRAZA_USER']:
                        j=''
                        for s in base['FRAZA_USER'][x]:
                                j+=s+'; '
                        g+= x+'='+j
                if g=='':
                        reply(type,source,'none')
                        return
                reply(type,source,g)

def boltun_frus_dell(type, source, parameters):
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters in base['FRAZA_USER']:
                del base['FRAZA_USER'][parameters]
                write_file(TREW,str(base))
                reply(type, source,'Ok')
                boltun_init(source[1])


def boltun_config(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        TREW = 'dynamic/boltun.txt'
        fp = file(TREW, 'r')
        base = eval(read_file(TREW))
        if parameters:
                l = parameters.lower()
                if l.count('work')>0:
                        if source[1] in base['OFF']:
                                base['OFF'].remove(source[1])
                                write_file(TREW,str(base))
                                try:
                                        BOLTUN['OFF'].remove(source[1])
                                except:
                                        pass
                                reply(type,source,u'болталка здесь включена!')
                                return
                        else:
                                base['OFF'].append(source[1])
                                write_file(TREW,str(base))
                                try:
                                        BOLTUN['OFF'].append(source[1])
                                except:
                                        pass
                                reply(type,source,u'болталка здесь отключена!')
                                return
        else:
                kkk=''
                if BOLTUN['OFF']:
                        t =''
                        for x in BOLTUN['OFF']:
                                t+= x+','
                        if t!='':
                                kkk +=u'болталка отключена в следующих конфах: \n'+t
                if kkk=='':
                        kkk=u'болтун включен.Смотри ключи команды.'
                reply(type,source,kkk)

def boltun_load(groupchat):
        if not BOLTUN:
                try:
                        MK = 'dynamic/otveti.txt'
                        fp0 = open(MK, 'r')
                        iii = fp0.read()
                        iii=iii.decode('cp1251')
                        fp0.close()
                        for i in iii.splitlines():
                                BOLTUN_QIP[i]={}
                        TREW ='dynamic/boltun.txt'
                        fp = open(TREW,'r')
                        text = eval(fp.read())
                        fp.close()
                        for x in text:
                                BOLTUN[x]=text[x]
                except:
                        for x in ADMINS:
                                msg(x,u'ошибка в boltun_plugin, проверьте файлы dynamic/otveti.txt dynamic/boltun.txt')

def boltun_init(groupchat):
        try:
                for k in BOLTUN:
                        del BOLTUN[k]
        except RuntimeError:
                pass
        try:
                MK = 'dynamic/otveti.txt'
                fp0 = open(MK, 'r')
                iii = fp0.read()
                iii=iii.decode('cp1251')
                fp0.close()
                for i in iii.splitlines():
                        BOLTUN_QIP[i]={}
                TREW ='dynamic/boltun.txt'
                fp = open(TREW,'r')
                text = eval(fp.read())
                fp.close()
                for x in text:
                        BOLTUN[x]=text[x]
        except:
                for x in ADMINS:
                        msg(x,u'ошибка в boltun_plugin, проверьте файлы dynamic/otveti.txt & dynamic/boltun.txt')

CHAT_TO_JID={'chat':'','jid':''}

def chat_to_jid_start(type,source,parameters):
        if type=='private':
                reply(type,source,u'команда может быть использована только в общем окне чата!')
                return
        if not source[1] in GROUPCHATS:
                return
        if CHAT_TO_JID['chat']:
                if parameters!='0':
                        reply(type,source,u'some user used this command now, you must wait!')
                        return
        if parameters=='0':
                if source[1]==CHAT_TO_JID['chat']:
                        CHAT_TO_JID['chat']=''
                        JCON.send(xmpp.Message(CHAT_TO_JID['jid'],u'диалог с конференцией завершен!','chat'))
                        CHAT_TO_JID['jid']=''
                        reply(type, source, u'close!')
                        return
                else:
                        reply(type,source,u'no active to this room')
                        return
        if not parameters:
                reply(type,source,u'enter some jid!')
                return
        l=parameters.lower()
        if l.count('@conference.'):
                reply(type,source,u'this work only to jid')
                return
        if not parameters.count('@'):
                reply(type,source,u'write some jid!')
                return
        if len(parameters)<6 or len(parameters)>50:
                reply(type,source,u'this jid is invalid!')
                return
        if parameters.lower() in ADMINS:
                reply(type,source,u'cannot use this jid!')
                return
        ak=parameters.lower()
        ROSTER = JCON.getRoster()
        ROSTER.Subscribe(ak)
        reply(type,source,u'ok!')
        CHAT_TO_JID['chat']=source[1]
        CHAT_TO_JID['jid']=ak
        JCON.send(xmpp.Message(ak,u'С вами открыт диалог от конференции '+source[1],'chat'))

def chat_to_jid_msg(raw, type, source, parameters):
    if type=='private':
        if source[1] not in GROUPCHATS:
            if get_true_jid(source[1]+'/'+source[2]) == CHAT_TO_JID['jid']:
                if parameters=='' or parameters.isspace():
                    return
                if parameters.count(' '):
                    m=parameters.split()[0]
                    if m.lower() in COMMANDS:
                        return
                JCON.send(xmpp.Message(CHAT_TO_JID['chat'],u'Сообщение от '+CHAT_TO_JID['jid']+u'\n'+parameters[:500],'groupchat'))
    else:
        if source[1] == CHAT_TO_JID['chat']:
            if parameters=='' or parameters.isspace():
                return
            if source[2] == get_bot_nick(source[1]):
                return
            if parameters.count(' '):
                m=parameters.split()[0]
                if m.lower() in COMMANDS:
                    return
            JCON.send(xmpp.Message(CHAT_TO_JID['jid'],source[2]+':\n'+parameters[:500],'chat'))

register_message_handler(chat_to_jid_msg)
register_stage1_init(boltun_load)
register_command_handler(chat_to_jid_start, '!окно', ['все'], 20, 'открывает чат с определенным jid-ом прямо с конференции.Для закрытыя чата юзаем ключ команды 0', '!окно <jid>', ['!окно user@talkonaut.com','!окно 0'])
register_command_handler(boltun_config, 'болтун', ['болтун'], 40, 'Bключает/отключает болталку в определенной конфе', 'болтун', ['болтун'])
register_command_handler(boltun_save_fruser, 'фрюзер', ['болтун'], 40, 'Без параметров покажет все ключевые слова.Добавляет ключевое слово в базу фразаюзер(бот реагирует если мессага адресована комуто в чате).', 'фрюзер <ключ слово>=<ответ1>,<ответ2>,..', ['фрюзер привет=а со мной поздороваться?,и тебе привет!,ога'])
register_command_handler(boltun_frus_dell, 'фрюзер_дел', ['болтун'], 40, 'Удаляет из базы болтуна через ключевое слово варианты ответа на это слово', 'фрюзер_дел <ключ слово>', ['фрюзер_дел привет'])
register_command_handler(boltun_sav_frad, 'фрадмин', ['болтун'], 40, 'Без параметров показывает все ключевые слова.Добавляет в базу фразаадмин ключевое слово и варианты ответа(бот реагирует если мессага написана админом в общак и адресована всем)', 'фрадмин <ключ слово>=<ответ1>,<ответ2>,..', ['фрадмин привет=здравствуй ночальнег!,насяльника привет!,ога'])
register_command_handler(boltun_frad_dell, 'фрадмин_дел', ['болтун'], 40, 'Удаляет из базы болтуна через ключевое слово все занесенные варианты ответа на это слово', 'фрадмин_дел <ключевое слово>', ['фрадмин_дел привет'])
register_command_handler(boltun_save_frall, 'фралл', ['болтун'], 40, 'Бот реагирует если мессага адресована всем при условии что доступ написавшего менее 20,для админов есть отдельная база см.фрадмин', 'фралл <ключ слово>=<ответ1>,<ответ2>,..', ['фралл привет=здравствуй,привет,ога'])
register_command_handler(boltun_fra_dell, 'фралл_дел', ['болтун'], 40, 'Удаляет из базы болтуна через ключевое слово все занесенные варианты ответа на это слово', 'фралл_дел <ключевое слово>', ['фралл_дел привет'])
register_command_handler(boltun_sav, 'фрбот', ['болтун'], 40, 'Добавляет в базу болтуна ключевое слово на которое реагирует бот и возможные вариации ответа при обращении к боту в чате', 'фрбот <ключ слово>=<ответ1>,<ответ2>,..', ['фрбот привет=здравствуй,привет,ога'])
register_command_handler(boltun_frb_dell, 'фрбот_делл', ['болтун'], 40, 'Удаляет из базы болтуна через ключевое слово все занесенные варианты ответа на это слово', 'фрбот_дел <ключевое слово>', ['фрбот_дел привет'])
register_message_handler(boltun_work)
