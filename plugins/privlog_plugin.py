#===istalismanplugin===
# -*- coding: utf-8 -*-

import shutil

PRIVLOG_SEARCH={}




def handler_privlog_q(type, source, parameters):
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        global PRIVLOG_SEARCH
        if not PRIVATE_LOG_DIR:
                reply(type, source, u'В настройках бота не указана папка логов!')
                return
        if not parameters or parameters.isspace():
                reply(type, source, u'и?')
                return
        if parameters==u'чистить':
                J=[u'ya.ru',u'jabber.ru',u'xmpp.ru',u'talkonaut.com',u'icq.transport.talkonaut.com',u'jabberon.ru',u'jabber.perm.ru']
                                        
                try:
                        rd=0
                        SD=[]
                        for user in os.listdir(PRIVATE_LOG_DIR):
                                if user.count('@'):
                                        srv=user.split('@')[1]
                                        if not srv in J:
                                                shutil.rmtree(PRIVATE_LOG_DIR+'/'+user)
                                                rd+=1
                        reply(type, source, u'Было удалено '+str(rd)+u' подозрительных папок')
                        return
                except:
                        return
        if parameters==u'топ':
                LI={}
                ST=[]
                rep=''
                for m in os.listdir(PRIVATE_LOG_DIR):
                        kk=PRIVATE_LOG_DIR+'/'+m+'/'+str(year)+'/'+str(month)+'/'+str(day)+'.html'
                        if os.path.exists(kk):
                                sz=os.path.getsize(PRIVATE_LOG_DIR+'/'+m+'/'+str(year)+'/'+str(month)+'/'+str(day)+'.html')
                                sz=sz//1024
                                LI[sz]=m
                                ST.append(sz)
                ST.sort()
                ST.reverse()
                n=0
                for x in ST:
                        n+=1
                        rep+=str(n)+') '+LI[x]+' '+str(x)+u'kb.\n'
                        if n==10:
                                break
                reply(type, source, rep)
                return
        if parameters.lower()==u'сегодня':
                rep=''
                for m in os.listdir(PRIVATE_LOG_DIR):
                        kk=PRIVATE_LOG_DIR+'/'+m+'/'+str(year)+'/'+str(month)+'/'+str(day)+'.html'
                        if os.path.exists(kk):
                                rep+=m+'\n'
                reply(type, source, rep)
                return
        file=''
        q=parameters
        day_search=0
        size=0
        my_dir=''
        rep=''
        result=0
        n=0
        jid=get_true_jid(source[1]+'/'+source[2])
        reply(type, source, u'Поиск начат!')
        if parameters.count(' ')>1:
                s=parameters.split()
                if s[0].isdigit() and s[1].isdigit():
                        month=s[0]
                        day=s[1]
                        day_search=1
                        q=' '.join(s[2:])
        if day_search:
                result=0
                read=os.listdir(PRIVATE_LOG_DIR)
                for x in read:
                        my_dir=(PRIVATE_LOG_DIR+'/'+x+'/'+str(year)+'/'+str(month)+'/'+str(day)+'.html')
                        if os.path.exists(my_dir) and x!=jid:
                                print 'exists'
                                size+=os.path.getsize(my_dir)
                                file=open(my_dir, 'r')
                                text=file.read()
                                file.close()
                                if text.count(q.encode('utf-8','replace')):
                                        print 'Count!'
                                        rep+=(str(day)+'.'+str(month)+'.'+str(year)+'\n')
                                        lines=text.split('\n')
                                        for l in lines:
                                                n+=1
                                                if l.count(q.encode('utf-8','replace')):
                                                        l=decode_log(l)
                                                        if not l.isspace():
                                                                result+=1
                                                                if len(l)>160:
                                                                        l=l[:160]+' ...'
                                                                rep+=str(result)+') '+l+('\n'.encode('utf-8','replace'))
                                                                if not jid in PRIVLOG_SEARCH:
                                                                        PRIVLOG_SEARCH[jid]={}
                                                                PRIVLOG_SEARCH[jid][result]={'file':my_dir,'str':n}
        

                if rep.isspace() or rep=='':
                        reply(type, source, u'Нет результатов')
                        return
                sizeinfo=u'Проверено'+str(size//1024)+u' кб; Результатов '+str(result)+'\n'
                if len(rep)>3000:
                        reply(type, source, sizeinfo+rep[:3000].decode('utf-8','replace'))
                        rep=rep[3000:]
                        sizeinfo=''
                reply(type, source, sizeinfo+rep.decode('utf-8','replace'))
                return
        else:
                read=os.listdir(PRIVATE_LOG_DIR)
                result=0
                day_m=0
                if parameters.count('day-'):
                        strp=parameters.split('day-')[1].strip()
                        if strp.isdigit():
                                alld=year+month+day
                                day_m=alld-int(strp)
                                q=parameters.split('day-')[0].strip()
                for x in read:
                        try:
                                list_year=os.listdir(PRIVATE_LOG_DIR+'/'+x+'/'+str(year))
                                if os.path.exists(PRIVATE_LOG_DIR+'/'+x+'/'+str(year)):
                                        for xa in list_year:
                                                list_day=os.listdir(PRIVATE_LOG_DIR+'/'+x+'/'+str(year)+'/'+str(xa))
                                                for xb in list_day:
                                                        try:
                                                                if day_m:
                                                                        if (year+xa+xb)>day_m:
                                                                                continue
                                                                n=0
                                                                file=PRIVATE_LOG_DIR+'/'+x+'/'+str(year)+'/'+xa+'/'+xb
                                                                if os.path.exists(file):
                                                                        size+=os.path.getsize(file)
                                                                        fp=open(file, 'r')
                                                                        text=fp.read()
                                                                        fp.close()
                                                                        if text.count(q.encode('utf-8','replace')):
                                                                                rep+=(xb+'.'+xa+'.'+str(year)+' - '+x+'\n')
                                                                                lines=text.splitlines()
                                                                                for l in lines:
                                                                                        n+=1
                                                                                        if l.count(q.encode('utf-8','replace')):
                                                                                                l=decode_log(l)
                                                                                                l=l.decode('utf-8','replace')
                                                                                                if not l.isspace():
                                                                                                        if len(l)>160:
                                                                                                                l=l[:160]+' ...'
                                                                                                        result+=1
                                                                                                        rep+=str(result)+') '+l+'\n'
                                                                                                        if not jid in PRIVLOG_SEARCH:
                                                                                                                PRIVLOG_SEARCH[jid]={}
                                                                                                        PRIVLOG_SEARCH[jid][result]={'file':file,'str':n}
                                                        except:
                                                                pass
                        except:
                                pass

                                                
                if rep.isspace() or rep=='':
                        reply(type, source, u'Нет результатов')
                        return
                sizeinfo=u'Проверено '+str(size//1024)+u' кб;Результатов '+str(result)+'\n'
                if len(rep)>3000:
                        reply(type, source, sizeinfo+rep[:3000])
                        rep=rep[3000:]
                        sizeinfo=''
                reply(type, source, sizeinfo+rep)

def handler_privlog_more(type, source, parameters):
        global PRIVLOG_SEARCH
        jid=get_true_jid(source[1]+'/'+source[2])
        if not parameters or not parameters.isdigit():
                return
        if not jid in PRIVLOG_SEARCH:
                return
        if not int(parameters) in PRIVLOG_SEARCH[jid]:
                return
        parameters=int(parameters)
        rep=''
        n=0
        if 'file' in PRIVLOG_SEARCH[jid][parameters].keys() and 'str' in PRIVLOG_SEARCH[jid][parameters].keys():
                n=PRIVLOG_SEARCH[jid][parameters]['str']-5
                b=n+10
                if os.path.exists(PRIVLOG_SEARCH[jid][parameters]['file']):
                        file=PRIVLOG_SEARCH[jid][parameters]['file']
                        fp=open(file, 'r')
                        text=fp.read()
                        fp.close()
                        if text:
                                lines=text.splitlines()
                                for x in range(n, b):
                                        try:
                                                lines[x]=decode_log(lines[x])
                                                if not lines[x].isspace():
                                                        rep+=lines[x]+'\n'
                                        except:
                                                pass
                                if rep=='' or rep.isspace():
                                        reply(type, source, u'не получилось')
                                        return
                                reply(type, source, rep)

       
        
def my_log_sea_(type, source, parameters):
        if not PUBLIC_LOG_DIR :
                reply(type, source, u'Запись логов не активна')
                return
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        jid=get_true_jid(source[1]+'/'+source[2])
        log=PUBLIC_LOG_DIR
        rep=''
        result=0
        size=0
        if not os.path.exists(log):
                reply(type, source, u'Запись логов либо отключена, либо папка осутствует!')
                return
        reply(type, source, u'Поиск начат')
        for conference in os.listdir(log):
                pth=log+'/'+conference+'/'+str(year)
                if os.path.exists(pth):
                        try:
                                for month_ in os.listdir(log+'/'+conference+'/'+str(year)):
                                        for day_ in os.listdir(log+'/'+conference+'/'+str(year)+'/'+month_):
                                                file=log+'/'+conference+'/'+str(year)+'/'+month_+'/'+day_
                                                fp=open(file, 'r')
                                                txt=fp.read()
                                                fp.close()
                                                size+=os.path.getsize(log+'/'+conference+'/'+str(year)+'/'+month_+'/'+day_)
                                                if txt.count(parameters.encode('utf-8','replace')):
                                                        txt=txt.splitlines()
                                                        st=0
                                                        for l in txt:
                                                                st+=1
                                                                if l.count(parameters.encode('utf-8','replace')):
                                                                        l=decode_log(l)
                                                                        if l!='' and not l.isspace():
                                                                                result+=1
                                                                                if len(l)>160:
                                                                                        l=l[:160]+'...'
                                                                                l=l.decode('utf-8','replace')
                                                                                rep+=conference+'\n'+str(result)+') '+l+'\n'
                                                                                if not jid in PRIVLOG_SEARCH:
                                                                                        PRIVLOG_SEARCH[jid]={}
                                                                                PRIVLOG_SEARCH[jid][result]={'file':log+'/'+conference+'/'+str(year)+'/'+month_+'/'+day_,'str':st}
                        except:
                                pass
                                                                        
        if rep=='' or rep.isspace():
                reply(type, source, u'Поиск не дал результатов')
                return
        sizeinfo=u'Проверено '+str(size//1024)+u' кб; Результатов '+str(result)+'\n'
        if len(rep)>3000:
                reply(type, source, sizeinfo+rep[:3000])
                rep=rep[3000:]
                sizeinfo=''
        reply(type, source, sizeinfo+rep)

GLOBLOG_NEW={'start':0,'dir':[],'rep':[],'dic':{},'size':0,'result':0,'show':0}

def globlog_new(type, source, parameters):
        global GLOBLOG_NEW
        if not PUBLIC_LOG_DIR :
                reply(type, source, u'Запись логов не активна')
                return
        if GLOBLOG_NEW['start']:
                reply(type, source, u'Сейчас выполняеться поиск,попробуйте позже!')
                return
        GLOBLOG_NEW['start']=1
        GLOBLOG_NEW['rep']=[]
        GLOBLOG_NEW['result']=0
        GLOBLOG_NEW['size']=0
        GLOBLOG_NEW['dic'].clear()
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        jid=get_true_jid(source[1]+'/'+source[2])
        log=PUBLIC_LOG_DIR
        rep=''
        result=0
        size=0
        if not os.path.exists(log):
                reply(type, source, u'Запись логов либо отключена, либо папка отсутствует!')
                GLOBLOG_NEW['start']=0
                return
        reply(type, source, u'Поиск начат, это может занять несколько минут')
        for conference in os.listdir(log):
                pth=log+'/'+conference+'/'+str(year)
                if os.path.exists(pth):
                        GLOBLOG_NEW['dir'].extend(os.listdir(log+'/'+conference+'/'+str(year)))
                        for month_ in os.listdir(log+'/'+conference+'/'+str(year)):
                                threading.Thread(None, globlog_thread, 'globlog'+str(random.randrange(0, 999)), (jid, month_, log+'/'+conference+'/'+str(year)+'/'+month_,parameters)).start()
                        while GLOBLOG_NEW['dir']:
                                pass
        rep="\n".join(GLOBLOG_NEW['rep'])
        if not rep or rep.isspace():
                reply(type, source, u'Поиск не дал результатов')
                GLOBLOG_NEW['start']=0
                return
        sizeinfo=u'Проверено '+str(GLOBLOG_NEW['size']//1024)+u' кб; Результатов '+str(GLOBLOG_NEW['result'])+u' ; Показано '+str(GLOBLOG_NEW['show'])+'\n'
        #if len(rep)>3000:
        #        globlog_answ(type, source, sizeinfo+rep[:3000])
        #        rep=rep[3000:]
        #        sizeinfo=''
        res=''
        n=0
        for x in GLOBLOG_NEW['dic'].keys():
                res+=u'Конфа '+x+':\n'
                for c in GLOBLOG_NEW['dic'][x]:
                        n+=1
                        res+=str(n)+') '+c
        try:
                globlog_answ(type, source, sizeinfo+res)
        except:
                pass
        GLOBLOG_NEW['start']=0

                                

def globlog_thread(jid, mn, dir, data):
        try:
                globlog_thread_try(jid, mn, dir, data)
        except:
                if mn in GLOBLOG_NEW['dir']:
                        GLOBLOG_NEW['dir'].remove(mn)

def globlog_thread_try(jid, mn, dir, data):
        result=''
        log=PUBLIC_LOG_DIR
        conference='???'
        try:
                conference=[x for x in dir.split('/') if x.count('@conf')]
                conference=conference[0]
        except:
                pass
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        for day_ in os.listdir(dir):
                find=''
                file=dir+'/'+day_
                fp=open(file, 'r')
                txt=decode_log(fp.read())
                fp.close()
                GLOBLOG_NEW['size']+=os.path.getsize(dir+'/'+day_)
                res=re.findall('\n.*'+data.encode('utf-8','replace')+'.*\n',txt)
                if res:
                        try:
                                find=[x for x in res if not x.isspace() and len(x)>3]
                        except:
                                pass
                        if find:
                                for x in find:
                                        GLOBLOG_NEW['result']+=1
                                        if len(GLOBLOG_NEW['rep'])<5800:
                                                GLOBLOG_NEW['show']+=1
                                                GLOBLOG_NEW['rep'].append(conference+'\n'+str(GLOBLOG_NEW['result'])+') '+x.decode('utf8','replace'))
                                                if not conference in GLOBLOG_NEW['dic'].keys():
                                                        GLOBLOG_NEW['dic'][conference]=[]
                                                GLOBLOG_NEW['dic'][conference].append(x.decode('utf8','replace'))
                                        if not jid in PRIVLOG_SEARCH:
                                                PRIVLOG_SEARCH[jid]={}
                                        PRIVLOG_SEARCH[jid][GLOBLOG_NEW['result']]={'file':dir+'/'+day_,'str':st}
        if mn in GLOBLOG_NEW['dir']:
                GLOBLOG_NEW['dir'].remove(mn)

def globlog_answ(type, source, body):
        jid=source[1]
        type='chat'
        if source[1] in GROUPCHATS.keys():
                jid=source[1]+'/'+source[2]
                type='groupchat'
        if type=='groupchat' and len(body)>1000:
                if len(body)>6000:
                        body=body[:6000]
                JCON.send(xmpp.Message(source[1], body[:800]+u'..\n >>> смотри приват!', 'groupchat'))
                time.sleep(3)
                JCON.send(xmpp.Message(source[1]+'/'+source[2], body[800:], 'chat'))
                return
        JCON.send(xmpp.Message(jid, body, type))


register_command_handler(globlog_new, '!чатлог', ['все'], 100, 'поиск глобально в логах конференций', '!чатлог <текст>', ['!чатлог смысл жизни'])                        
register_command_handler(my_log_sea_, '!глоблог', ['все'], 100, 'поиск глобально в логах конференций', '!глоблог <текст>', ['!глоблог смысл жизни'])
register_command_handler(handler_privlog_q, '!привлог', ['все'], 100, 'поиск по привлогам, можно указывать месяц и число.', '!привлог <текст>', ['!привлог 3 30 Вася'])
register_command_handler(handler_privlog_more, '!подробно', ['все'], 100, 'выводит более детальный результат при поиске в привлогах см.помощь !привлог', '!подробно <номер в списке>', ['!подробно 1'])
