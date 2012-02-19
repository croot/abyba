#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman

SRCIAFL=[]
SRCIAFLON=[]
SRCLAST={}
SRN_BASE={}
SRJ_RES={'n':0}

def now_srch_start(type,source,parameters):
        h, k, z, n, al, arl = '','','','','',''
        if not parameters:
                reply(type,source,u'введите ключевые символы для поиска по нику или Jabber-ID!')
                return
        acc = int(user_level(source[1]+'/'+source[2], source[1]))
        if len(parameters)>35:
                reply(type,source,u'а не много написал?')
                return
        jid=get_true_jid(source[1]+'/'+source[2])
        if jid in SRCLAST:
                if time.time() - SRCLAST[jid]['time']<60:
                        reply(type,source,u'лимит команды 1 минута.')
                        return
                else:
                        SRCLAST[jid]['time']=time.time()
        else:
                SRCLAST[jid]={'time':time.time()}
        if parameters.count(' ')>0 and parameters.count(u'жид')>0:
                if acc<40:
                        reply(type, source, u'Для поиска по ключу жид нужен доступ 40')
                        return
                parameters=parameters.split()[1]
                reply(type,source,u'поиск начат')
                handler_srchk_list(type,source,parameters)
                return
        if parameters.count(' ')>0 and parameters.count(u'все')>0:
                if acc<40:
                        reply(type, source, u'Для поиска по ключу все нужен доступ 40')
                        return
                reply(type,source,u'поиск начат')
                h, z, n =parameters.split(), '', 0
                k = h[1]
                al=0
                alr=0
                dir_chat=os.listdir('dynamic')
                for x in dir_chat:
                        if os.path.isdir(x):
                                file='dynamic/'+x+'/search.txt'
                                if os.path.exists(file):
                                        txt=eval(read_file(file))
                                        if not isinstance(txt, dict):
                                                write_file(file, '{}')
                                                txt='{}'
                                        ver=''
                                        ax=0
                                        for c in txt:
                                                al+=1
                                                if c.count(unicode(k)):
                                                        n+=1
                                                        if len(z)<1800:
                                                                alr+=1
                                                                if len(c)>50:
                                                                        del txt[c]
                                                                        write_file(file,str(txt))
                                                                z+=c+' ('+x+')'+ver+';\n'
                                
                if z=='':
                        reply(type,source,'Совпадений нет!')
                        return
                if type=='public':
                        reply(type,source,u'смотри в привате!')
                reply('private',source,u'всего найдено '+unicode(al)+u' | совпадений '+unicode(n)+u' | показано '+unicode(alr)+'\n'+z[:2000])
                return
        else:
                if not parameters.count(u'все'):
                        if not source[1] in GROUPCHATS:
                                reply(type,source,u'Команда работает только в чате!')
                                return
                        srch='dynamic/'+source[1]+'/search.txt'
                        if not os.path.exists(srch):
                                return
                        txt=eval(read_file(srch))
                        if not isinstance(txt, dict):
                                write_file(srch, '{}')
                                txt = '{}'
                        answ=''
                        rs=0
                        ral=0
                        ran=0
                        for x in txt:
                                rs+=1
                                if x.count(parameters):
                                        ral+=1
                                        if len(x)>60:
                                                del txt[x]
                                                write_file(srch,str(txt))
                                        if len(answ)<900:
                                                ran+=1
                                                answ+=x+';\n'
                        if len(answ)<2:
                                reply(type,source,u'Совпадений нет!')
                                return
                        if answ.isspace():
                                reply(type,source,u'Совпадений нет!')
                                return
                        if type=='public':
                                reply(type,source,u'смотри в привате!')
                        reply('private',source,u'Всего найдено '+unicode(rs)+u' | совпадений '+unicode(ral)+u' | показано '+unicode(ran)+'\n'+answ[:900])

register_command_handler(now_srch_start, '!найти', ['мод','админ'], 20, 'Поиск в базе бота по совпадениям в нике или жиде.Ключ команды \"все\"-исп. для поиска по всем базам конференций.Ключ \"жид\"-поиск жида по совпадениям в овнер,админ,мембер и бан-листе.\nКлюч ver-поиск по версии из презенса.', '!найти <кого-то>', ['!найти васю','!найти все васю','!найти жид 40t'])


def all_nick_get(type, source, parameters):
        if parameters and not parameters.isspace():
                reply(type,source,u'выполняеться поиск по базе')
                jid=''
                gch=os.listdir('dynamic')
                for x in gch:
                        file='dynamic/'+x+'/search.txt'
                        if os.path.exists(file):
                                fp=open(file, 'r')
                                txt=eval(fp.read())
                                fp.close()
                                for c in txt:
                                        if c.count(' '):
                                                m=c.split()
                                                if m[0]==parameters and not m[1].count('conference.'):
                                                        if not jid:
                                                                jid=m[1]
                                                                break
                if not jid:
                        reply(type, source, u'Ник не найден!')
                        return
                all_nick=''
                SP=[]
                gch=os.listdir('dynamic')
                for x in gch:
                        if os.path.isdir(x):
                                file='dynamic/'+x+'/search.txt'
                                if os.path.exists(file):
                                        fp=open(file, 'r')
                                        txt=eval(fp.read())
                                        fp.close()
                                        for c in txt:
                                                if c.count(jid) and c.count(' '):
                                                        m=c.split()
                                                        if not m[0] in SP and m[0]!=parameters:
                                                                SP.append(m[0])
                if not SP:
                        reply(type, source, u'дополнительных ников для этого пользователя не найдено')
                        return
                reply(type, source, "\n".join(SP))

register_command_handler(all_nick_get, '!ники', ['все'], 0, 'Показывает все ники под которыми заходил пользователь.', '!ники <ник>', ['!ники 40tman'])

SRC_LJ={}
SRCGR=['jabe.info','jabbon.ru','qabber.ru','myjabber.ru','ya.ru','jabber.perm.ru','gmail.com','jabber.ru','xmpp.ru', 'jabbers.ru', 'xmpps.ru', 'qip.ru', 'talkonaut.com', 'jabbus.org','gtalk.com','jabber.cz','jabberon.ru','jabberid.org','linuxoids.net','jabber.kiev.ua','jabber.ufanet.ru','jabber.corbina.ru','jabbrik.ru','jabber.ua','jabnet.ru']

def search_handler_join(groupchat, nick, aff, role):
        if not groupchat in GROUPCHATS:
                return
        if len(nick)>20:
                return
        if groupchat not in SRC_LJ:
                SRC_LJ[groupchat]={'time':time.time(),'lim':0}
        else:
                if time.time() - SRC_LJ[groupchat]['time']<3:
                        SRC_LJ[groupchat]['time']=time.time()
                        return
                else:
                        SRC_LJ[groupchat]['time']=time.time()
        if check_file(groupchat,'search.txt'):
                jid=get_true_jid(groupchat+'/'+nick)
                try:
                        if jid.count('@con'):
                                return
                except:
                        pass
                if len(jid)>40:
                        return
                serv=jid.split('@')[1]
                if serv not in SRCGR:
                        if SRC_LJ[groupchat]['lim']>2:
                                return
                        SRC_LJ[groupchat]['lim']+=1
                i=nick+' '+jid
                if not bas_count_srch(groupchat,jid):
                        if not groupchat in SRN_BASE.keys():
                                return
                        if i not in SRN_BASE[groupchat].keys():
                                if len(i)>50:
                                        return
                                try:
                                        file='dynamic/'+groupchat+'/search.txt'
                                        txt=eval(read_file(file))
                                        if not isinstance(txt, dict):
                                                write_file(file, '{}')
                                                txt = '{}'
                                        txt[i]={}
                                        write_file(file, str(txt))
                                        SRN_BASE[groupchat][i]={}
                                except:
                                        write_file(file, ('{}'))
                                        pass
                        
register_join_handler(search_handler_join)


def bas_count_srch(groupchat,jid):
        if check_file(groupchat,'search.txt'):
                n=0
                if not groupchat in SRN_BASE:
                        return
                for x in SRN_BASE[groupchat]:
                        if x.count(jid):
                                n+=1
                if n>5:
                        return 1
        return 0

def handler_srchk_list(type,source,parameters):
        if '1' in globals()['SRCIAFLON']:
                reply(type,source,u'идет поиск,попробуй через минуту')
                return
        globals()['SRCIAFLON'].append('1')
        afl=['owner','admin','member','outcast']
        for x in GROUPCHATS:
                for s in afl:
                        iq = xmpp.Iq('get')
                        id='item'+str(random.randrange(1000, 9999))
                        iq.setTo(x)
                        iq.setID(id)
                        query = xmpp.Node('query')
                        query.setNamespace('http://jabber.org/protocol/muc#admin')
                        ban=query.addChild('item', {'affiliation':s})
                        iq.addChild(node=query)
                        JCON.SendAndCallForResponse(iq, handler_srchi_ans, {'type': type, 'source': source,'parameters':parameters})
        time.sleep(7)
        handler_srchi_time(type,source)
                
def handler_srchi_time(type,source):
        LIST=[]
        p=''
        n=0
        calc=0
        for x in globals()['SRCIAFL']:
                if x!='':
                        n+=1
                        if n<13:
                                calc+=1
                                p+=unicode(n)+')'+x
        if p=='':
                reply(type,source,u'not found')
                globals()['SRCIAFLON'].remove('1')
                return
        if type=='public':
                reply(type,source,u'смотри в привате!')
        reply('private',source, u'всего найдено '+unicode(SRJ_RES['n'])+u' | совпадений '+unicode(n)+u' | показано '+unicode(calc)+'\n'+p)
        globals()['SRCIAFLON'].remove('1')
        globals()['SRCIAFL']=['']
        try:
                SRJ_RES['n']=0
        except:
                pass
	
def handler_srchi_ans(coze, res, type, source, parameters):
	id=res.getID()
	rep =''
	allinf=''
	n=0
	al=0
	if res:
		if res.getType() == 'result':
                        at=res.getFrom()
                        dask=res.getQueryChildren()
                        for x in dask:
                                SRJ_RES['n']+=1
                                dm=x.getAttrs()['affiliation']
                                dx=x.getAttrs()['jid']
                                al+=1
                                if dx.count(parameters):
                                        allinf=dm+u' '+dx+u' в '+unicode(at)+';\n'
                                        if allinf not in globals()['SRCIAFL']:
                                                if '1' in globals()['SRCIAFLON']:
                                                        n+=1
                                                        if n>10:
                                                                return
                                                        globals()['SRCIAFL'].append(allinf)


def srcn_load(groupchat):
        if check_file(groupchat,'search.txt'):
                file='dynamic/'+groupchat+'/search.txt'
                try:
                        txt=eval(read_file(file))
                except:
                        write_file(file,'{}')
                        txt=eval(read_file(file))
                if not groupchat in SRN_BASE:
                        SRN_BASE[groupchat]={}
                for x in txt.keys():
                        SRN_BASE[groupchat][x]=txt[x]


register_stage1_init(srcn_load)
