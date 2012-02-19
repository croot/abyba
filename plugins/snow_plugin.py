#===istalismanplugin===
# -*- coding: utf-8 -*-

SNOW = {}

SNOW_USER = {}

SNOW_SYS = {'nick':{},'reani':{},'warm':{},'die':u'Ваша температура слишком упала,вы в отключке!'}

SNOW_LAST = 0

SNOW_DB = 'dynamic/snow.txt'

def snow_id(jid):
    global SNOW
    if not jid in SNOW or not SNOW[jid]['bat']:
        return 1
    list=SNOW[jid]['bat'].keys()
    while 1:
        id=random.randrange(1, 17)
        if not id in list:
            break
    return id

def handler_snow_start(type, source, parameters):
    global SNOW
    global SNOW_SYS
    jid = get_true_jid(source[1]+'/'+source[2])
    if type=='public':
        reply(type, source, u'Напиши мне эту команду в привате, ок?')
        return
    try:
        if jid.split('@')[0] in SNOW_SYS['nick']:
            if SNOW_SYS['nick'][jid.split('@')[0]]!=jid:
                reply(type, source, u'Юзер с таким логином уже есть!Попробуйте другой JabberID!')
                return
        if not jid in SNOW_USER:
            snow_exp(jid)
    except:
        pass
    if jid in SNOW_SYS['reani']:
        if time.time() - SNOW_SYS['reani'][jid]<120:
            reply(type, source, u'Ты ещё в реанимации, не дёргайся!')
            return
        else:
            del SNOW_SYS['reani'][jid]
    if jid in SNOW.keys():
        if not SNOW[jid]['bat']:
            reply(type, source, u'Ладно, иди грей задницу!')
            del SNOW[jid]
            return
        else:
            reply(type, source, u'Попытка сбежать не удалась! В твоем списке еще есть недобитые ( набери ?? )')
            return
    s=source[1]+'/'+source[2]
    if not source[1] in GROUPCHATS:
        s=source[1]
    SNOW[jid]={'dodge':0,'last':0,'bat':{},'temp':37,'source':s,'activ':time.time(),'invite':0}
    reply(type, source, u'Привет, '+jid.split('@')[0]+u'! Твоя задача - закидать всех снежками!!! Для этого дерзай команды(англ.):\na - чтобы зафигачить снежкой/найти противника,list - вывести все команды')

def get_snow_jid(jid, src):
    if not jid in SNOW or not SNOW[jid]['bat']:
        return 0
    for x in SNOW[jid]['bat']:
        if SNOW[jid]['bat'][x]['jid']==src:
            return x

def snow_exc(jid):
    SP=[]
    if not jid in SNOW or not SNOW[jid]['bat']:
        return SP
    for x in SNOW[jid]['bat']:
        SP.append(SNOW[jid]['bat'][x]['jid'])
    return SP
        
def handler_snow_throw(type, source, parameters):
    global SNOW
    global SNOW_SYS
    jid = get_true_jid(source[1]+'/'+source[2])
    if not jid in SNOW:
        reply(type, source, u'Ты ничего не забыл? Например, написать <!снежки> ?')
        return
    fr, you, who, kill, tjid = 0, 0, None, '', ''
    a=SNOW[jid]
    if parameters:
        if parameters.isdigit():
            parameters=int(parameters)
            if parameters in SNOW[jid]['bat']:
                tjid = a['bat'][parameters]['jid']
                if not tjid in SNOW.keys():
                    reply(type, source, u'Ваш отморозок либо заснул, либо замерз в сугробе!\n***\na - подыскать другого')
                    del SNOW[jid]['bat'][parameters]
                    return
            else:
                time.sleep(1)
                reply(type, source, u'Нет такого в твоем списке!')
                return
            if time.time() - a['bat'][parameters]['time']<5:
                time.sleep(1)
                reply(type, source, u'Следующий ход через 5 секунд!')
                return
            a['bat'][parameters]['time']=time.time()
            who, fr, you = tjid.split('@')[0], snow_temp(tjid), snow_temp(jid)
            you = you-1
            SNOW[jid]['temp']-=you
            if SNOW[tjid]['dodge']:
                SNOW[tjid]['dodge']=0
                reply(type, source, who+u' увернулся от снежки! Ты обмерз на '+str(you)+u' градусов')
                return
            SNOW[tjid]['temp']-=fr
            if SNOW[tjid]['temp']>0 and SNOW[jid]['temp']>0:
                reply(type, source, u'Ты зарядил снежок в '+who+u'!\nТы обмерз на '+str(you)+u' градусов; '+who+u' - на '+str(fr)+u'\n***\na '+str(get_snow_jid(jid,tjid))+u' - чтобы продолжить; a - запустить снежок еше в кого-то')
                time.sleep(0.1)
                msg(SNOW[tjid]['source'],u'В вас запустил снежкой '+jid.split('@')[0]+u'!\nТы обмерз на '+str(fr)+u' градусов; \n***\na '+str(get_snow_jid(tjid,jid))+u' - чтобы ответить;')
                return
            else:
                if SNOW[tjid]['temp']<=0 and SNOW[jid]['temp']<=0:
                    msg(SNOW[tjid]['source'], u'Дубак сразил '+jid.split('@')[0]+u', и тебя тоже!У вас ничья!')
                    reply(type, source, u'Дубак сразил '+who+u', и тебя тоже! У вас ничья!')
                    del SNOW[jid]
                    del SNOW[tjid]
                    return
                if SNOW[tjid]['temp']<=0:
                    snow_exp(jid)
                    reply(type, source, who+u' сражен наповал! держи +1 рейтинга!')
                    msg(SNOW[tjid]['source'],u'В вас зафигачил снежкой '+jid.split('@')[0]+u'!\n'+SNOW_SYS['die'])
                    SNOW_SYS['reani'][tjid]=time.time()
                    try:
                        del SNOW[tjid]
                        del SNOW[jid][parameters]
                    except:
                        pass
                    return
                if SNOW[jid]['temp']<=0:
                    SNOW_SYS['reani'][jid]=time.time()
                    msg(SNOW[tjid]['source'],jid.split('@')[0]+u' с трудом поднял синюю руку для очередного броска, но тут же был сражен дубаком наповал!')
                    reply(type, source, SNOW_SYS['die'])
                    del SNOW[jid]
                    return
        else:
            if parameters.count('@') and parameters.count('.'):
                if not parameters.lower() in SNOW_USER:
                    if not SNOW[jid]['invite']:
                        SNOW[jid]['invite']=1
                    else:
                        reply(type, source, u'Вы исчерпали лимит инвайтов!')
                        return
                    msg(parameters, u'В вас зафигачил снежкой '+jid.split('@')[0]+u'!\nЧтобы ответить негодяю выйди не поле боя <!снежки>')
                    reply(type, source, u'Инвайт отправлен!')
                    return
                else:
                    reply(type, source, u'Такой юзер уже был в игре!')
                    return
            if parameters.lower() in [u'медведь']:
                try:
                    n=0
                    for x in SNOW.keys():
                        if x==jid:
                            continue
                        n+=1
                        msg(SNOW[x]['source'],u'Мимо пробежал '+jid.split('@')[0]+u', а вслед за ним медведь..')
                        if n>11:
                            break
                except:
                    pass
                ot=[u'руку',u'ногу',u'голову']
                reply(type, source, u'Медведь догнал вас и откусил '+random.choice(ot)+u'!\nПока!')
                return
    else:
        if SNOW[jid]['bat']:
            if len(SNOW[jid]['bat'])>10:
                reply(type, source, u'У вас в списке уже больше 10 отморозков!')
                return
        if len(SNOW)==1:
            reply(type, source, u'Никого нет!\nМожете пока покидать снежок в медведя:\n<a медведь>')
            return
        list = [x for x in SNOW.keys() if x!=jid and x not in snow_exc(jid)]
        if not list:
            reply(type, source, u'Свободного отморозка нет!\nМожете пока покидать снежок в медведя:\n <a медведь>')
            return
        th=random.choice(list)
        id=snow_id(jid)
        id2=snow_id(th)
        tjid=th
        SNOW[jid]['bat'][id]={'jid':th, 'time':time.time()}
        SNOW[th]['bat'][id2]={'jid':jid, 'time':time.time()-5}
        who, fr, you = th.split('@')[0], snow_temp(th), snow_temp(jid)
        you = you-1
        SNOW[jid]['temp']-=you
        if SNOW[tjid]['dodge']:
            SNOW[tjid]['dodge']=0
            reply(type, source, who+u' увернулся от снежки! Ты обмерз на '+str(you)+u' градусов')
            return
        SNOW[th]['temp']-=fr
        if SNOW[tjid]['temp']>0 and SNOW[jid]['temp']>0:
            reply(type, source, u'Ты зарядил снежок в '+who+u'!\nТы обмерз на '+str(you)+u' градусов; '+who+u' - на '+str(fr)+u'\n***\na '+str(get_snow_jid(jid,tjid))+u' - чтобы продолжить; a - запустить снежок еше в кого-то')
            time.sleep(0.1)
            msg(SNOW[tjid]['source'],u'В вас запустил снежкой '+jid.split('@')[0]+u'!\nТы обмерз на '+str(fr)+u' градусов; \n***\na '+str(get_snow_jid(tjid,jid))+u' - чтобы ответить;')
            return
        else:
            if SNOW[tjid]['temp']<=0 and SNOW[jid]['temp']<=0:
                msg(SNOW[tjid]['source'], u'Дубак сразил '+jid.split('@')[0]+u', и тебя тоже!У вас ничья!')
                reply(type, source, u'Дубак сразил '+who+u', и тебя тоже! У вас ничья!')
                del SNOW[jid]
                del SNOW[tjid]
                return
            if SNOW[th]['temp']<=0:
                snow_exp(jid)
                msg(SNOW[th]['source'],u'В вас запустил снежкой '+jid.split('@')[0]+u'!\n'+SNOW_SYS['die'])
                del SNOW[th]
                reply(type, source, who+u' сражен наповал! держи +1 рейтинга!')
                for x in SNOW[jid]['bat']:
                    if 'jid' in SNOW[jid]['bat'][x] and SNOW[jid]['bat'][x]['jid']==th:
                        del SNOW[jid]['bat'][x]
                return
            if SNOW[jid]['temp']<=0:
                SNOW_SYS['reani'][jid]=time.time()
                reply(type, source, SNOW_SYS['die'])
                msg(SNOW[tjid]['source'],jid.split('@')[0]+u' с трудом поднял синюю руку для очередного броска, но тут же был сражен дубаком наповал!')
                del SNOW[jid]
                return
        
def snow_load():
    global SNOW_DB
    global SNOW_USER
    global SNOW_SYS
    if not os.path.exists(SNOW_DB):
        file=open(SNOW_DB, 'w')
        file.write('{}')
        file.close()
    data=eval(read_file(SNOW_DB))
    SNOW_USER=data
    for x in SNOW_USER.keys():
        if x.count('@') and not x.split('@')[0] in SNOW_SYS['nick'].keys():
            SNOW_SYS['nick'][x.split('@')[0]]=x

def snow_temp(jid):
    n=9
    if jid in SNOW_USER:
        if 'exp' in SNOW_USER[jid]:
            if SNOW_USER[jid]['exp']>10:
                n-=2
            if SNOW_USER[jid]['exp']>200:
                n-=2
            if SNOW_USER[jid]['exp']>500:
                n-=2
            if SNOW_USER[jid]['exp']>1000:
                n-=2
    return n

def snow_get(jid):
    rep=[u'халат']
    if jid in SNOW_USER:
        if 'exp' in SNOW_USER[jid]:
            if SNOW_USER[jid]['exp']>10:
                rep.append(u'валенки')
            if SNOW_USER[jid]['exp']>200:
                rep.append(u'шапка-ушанка')
            if SNOW_USER[jid]['exp']>500:
                rep.append(u'штаны с начесом')
            if SNOW_USER[jid]['exp']>1000:
                rep.append(u'фуфайка')
    return rep

def snow_warm(type, source, parameters):
    global SNOW_SYS
    global SNOW
    jid = get_true_jid(source[1]+'/'+source[2])
    if not jid in SNOW:
        reply(type, source, u'Что греешь то?Тебя нет на поле сражения!')
        return
    if SNOW[jid]['temp'] in [37]:
        reply(type, source, u'С температурой у тебя все ок, можешь продолжать бой!')
        return
    if jid in SNOW_SYS['warm']:
        if time.time()-SNOW_SYS['warm'][jid]<60:
            reply(type, source, u'Греться можно только раз в минутy!')
            return
    SNOW_SYS['warm'][jid]=time.time()
    t=random.randrange(5, 8)
    SNOW[jid]['temp']+=t
    reply(type, source, u'Вы согрелись на '+str(t)+u' градусов!Вперед в бой!\n***\n')
            

def snow_exp(jid, b=1):
    data=eval(read_file(SNOW_DB))
    if not jid in data.keys():
        data[jid]={'exp':1}
    else:
        data[jid]['exp']+=1
    write_file(SNOW_DB, str(data))
    snow_load()

def handler_snow_info(type, source, parameters):
    n=0
    next=0
    jid = get_true_jid(source[1]+'/'+source[2])
    if not parameters:
        if jid in SNOW_USER:
            n=SNOW_USER[jid]['exp']
            if n<10:
                next=10-n
            if n>=10 and n<200:
                next=200-n
            if n>=200 and n<500:
                next=500-n
            if n>=500 and n<1000:
                next=1000-n
        t=u'Ты не на поле боя'
        if jid in SNOW:
            t=u'Твоя температура: '+str(SNOW[jid]['temp'])+u'\nСейчас ты на поле боя!'
        reply(type, source, u'Твой опыт: '+str(n)+u'\nНа тебе '+','.join(snow_get(jid))+u'\n'+t+u'\nДо следующего предмета одежды осталось: '+str(next))
    else:
        if not parameters in SNOW_SYS['nick']:
            reply(type, source, u'Ник не найден!')
            return
        if SNOW_SYS['nick'][parameters] in SNOW_USER:
            jid=SNOW_SYS['nick'][parameters]
            n=SNOW_USER[jid]['exp']
            t=u'Нет на поле боя'
            if jid in SNOW:
                t=u'Температура '+str(SNOW[jid]['temp'])+u'\nСейчас на поле боя!'
            reply(type, source, u'Опыт: '+str(n)+u'\nНа нем '+','.join(snow_get(jid))+u'\n'+t)

def snow_msg(raw, type, source, parameters):
    global SNOW_LAST
    global SNOW
    if not SNOW_LAST:
        SNOW_LAST=time.time()
    else:
        if time.time() - SNOW_LAST>60 and SNOW:
            SNOW_LAST=time.time()
            for x in SNOW.keys():
                if time.time()-SNOW[x]['activ']>1200:
                    msg(SNOW[x]['source'],u'Вы удалены с поля боя по неактивности!')
                    del SNOW[x]
    jid = get_true_jid(source[1]+'/'+source[2])
    if jid in SNOW.keys():
        if parameters.count(' '):
            s=parameters.split()
            if s[0].lower() in ['say']:
                if len(parameters)>500:
                    reply(type, source, u'А не много ты написал?')
                    return
                if not s[1] in SNOW_SYS['nick']:
                    reply(type, source, u'Нет такого ника!')
                    return
                if not SNOW_SYS['nick'][s[1]] in SNOW:
                    reply(type, source, u'Юзера сейчас нет в игре!')
                    return
                body = ' '.join(s[2:])
                if not body or body.isspace():
                    reply(type, source, u'А текст?')
                    return
                msg(SNOW[SNOW_SYS['nick'][s[1]]]['source'],u'Вам сообщение от '+jid.split('@')[0]+u':\n'+body)
                reply(type, source, u'Отправлено!')
                return
        if parameters.lower()=='r':
            n=random.randrange(1, 11)
            if n%2==0:
                SNOW[jid]['dodge']=1
                reply(type, source, u'ok')
                return
            else:
                reply(type, source, u'Попытка увернуться не удалась!')
                return
        if parameters.lower()=='list':
            reply(type, source, u'br - согреться;\nr - попытаться увернуться;\ni / i <nick> - выведет ваш рейтинг и состояние, либо рейтинг юзера <nick>;\na / a <jid> - поиск противника, инвайт в игру;\nsay <nick> - написать личное сообщение;\n??-список ваших противников;\ntop - топ 10-ка кидал;\n!snowballs - выход.')
            return
        if parameters=='??':
            rep=u''
            if SNOW[jid]['bat']:
                for x in SNOW[jid]['bat']:
                    rep+=str(x)+' '+SNOW[jid]['bat'][x]['jid'].split('@')[0]+'\n'
            if not rep or rep.isspace():
                reply(type, source, u'В списке никого нет!')
                return
            reply(type, source, rep)

def snow_game_top(type, source, parameters):
        nick, l, DB = '', '', []
	try:
                txt=eval(read_file(SNOW_DB))
        except:
                reply(type, source, u'ошибка чтения БД')
                return
        DB=[]
        if txt:
                for x in txt:
                        if 'exp' in txt[x]:
                                l=txt[x]['exp']
                                nick=x
                                try:
                                        if nick.count('@'):
                                                nick=nick.split('@')[0]
                                except:
                                        pass
                                DB.append(unicode(nick)+u'=='+str(l))
        DB.sort(snow_topsort)
        DB.reverse()
        list=''
        n=0
        for c in DB:
                n+=1
                if n>10:
                        break
                f1=c.split('==')[0]
                f2=c.split('==')[1]
                list+=str(n)+u') '+f1+' '+f2+'\n'
        if list=='' or list.isspace():
            reply(type, source, u'статистики нет')
            return
        reply(type, source, list)

def snow_topsort(a, b):
        a1=snow_get_digit(a)
        b1=snow_get_digit(b)
        if a1>b1:
                return 1
        if a1<b1:
                return -1
        return 1

def snow_get_digit(n):
        if n.count('=='):
                n=n.split('==')[1]
        rep=''
        for x in n:
                if x.isdigit():
                        rep+=x
        if len(rep)==1:
                rep='0000'+rep
        elif len(rep)==2:
                rep='000'+rep
        elif len(rep)==3:
                rep='00'+rep
        elif len(rep)==4:
                rep='0'+rep
        return rep


register_stage0_init(snow_load)
register_message_handler(snow_msg)
register_command_handler(snow_game_top, 'top', ['snowballs'], 0, 'test command', 'top', ['top'])		
register_command_handler(snow_warm, 'br', ['snowballs'], 0, 'test command', 'br', ['br'])		
register_command_handler(handler_snow_info, 'i', ['snowballs'], 0, 'test command', 'i', ['i'])		
register_command_handler(handler_snow_throw, 'a', ['snowballs'], 0, 'Команда чтобы запустить в когото снежкой', 'a', ['a'])		
register_command_handler(handler_snow_start, '!снежки', ['все'], 0, 'Игра в снежки', '!снежки', ['!снежки'])
register_command_handler(handler_snow_start, '!snowballs', ['все'], 0, 'Игра в снежки', '!snowballs', ['!snowballs'])


