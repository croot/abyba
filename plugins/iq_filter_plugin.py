#===istalismanplugin===
# -*- coding: utf-8 -*-


#Coded by 40tman

LSEND_IQ={}

MUC_FCON={}
MUC_STAT={'prs':0,'msg':0,'except':0}
MUC_SERV=[u'jabber.ufanet.ru',u'gajim.org',u'jabberon.ru',u'jabbus.org',u'jabber.kiev.ua',u'jabber.ru',u'qip.ru',u'xmpp.ru',u'xmpps.ru',u'talkonaut.com',u'gmail.com']
MUC_REPLACE=[u'пук']

def hnd_filter_iq(coze, iq):
        print 'Iq muc filt'
        fromjid = iq.getFrom()
        type= iq.getType()
        fromjid = fromjid.getStripped()
        if not fromjid in GROUPCHATS or not fromjid in MUC_FCON:
                return
        if not iq.getChildren():
                return
        mas=iq.getChildren()[0].getChildren()
        for i in mas:
                mesfrom=i.getAttrs()['from']
                mesto=i.getAttrs()['to']
                true_jid=mesfrom
                if mesfrom.count('/'):
                        true_jid=mesfrom.split('/')[0]
                if i.getTag('body'):
                        mestype=i.getAttrs()['type']
                else:
                        MUC_STAT['prs']+=1
                        aserv=mesfrom.split('@')[1]
                        serv=aserv.split('/')[0]
                        if serv not in MUC_SERV:
                                if 'vipe' in MUC_FCON[fromjid]:
                                        if MUC_FCON[fromjid]['vipe']!='0':
                                                MUC_STAT['except']+=1
                                                return
                        try:
                                handler_send_filtered(iq)
                        except:
                                pass
                        return
                nick=find_chat_nick(fromjid,mesfrom)
                gh=i.getTag('body')
                zh=gh.getData()
                zh=zh.lower()
                zh=unicode(zh)
                MUC_STAT['msg']+=1
                if mestype=='chat':
                        if 'priv' in MUC_FCON[fromjid]:
                                if MUC_FCON[fromjid]['priv']!='0':
                                        mm=fromjid+'/'+nick
                                        msg(mm,u'ваши сообщения к '+mesto+u' блокируються, приват закрыт!')
                                        MUC_STAT['except']+=1
                                        return
                if not fromjid+mesfrom in LSEND_IQ:
                        LSEND_IQ[fromjid+mesfrom]={'time':time.time(),'msg':zh}
                else:
                        if time.time()-LSEND_IQ[fromjid+mesfrom]['time']<2.2:
                                if MUC_FCON[fromjid]['spam']=='1':
                                        msg(fromjid+'/'+nick,u'слишком быстро отправляешь!')
                                        MUC_STAT['except']+=1
                                        return
                                if MUC_FCON[fromjid]['spam']=='2':
                                        order_kick(fromjid, nick, u'слишком быстро отправляешь!')
                                        return
                                if MUC_FCON[fromjid]['spam']=='3':
                                        order_ban(fromjid, nick, u'слишком быстро отправляешь!')
                                        return
                        if LSEND_IQ[fromjid+mesfrom]['msg']==zh:
                                if MUC_FCON[fromjid]['spam']=='1':
                                        msg(fromjid+'/'+nick,u'сообщения слишком похожи!')
                                        MUC_STAT['except']+=1
                                        return
                                if MUC_FCON[fromjid]['spam']=='2':
                                        order_kick(fromjid, nick, u'сообщения слишком похожи!')
                                        return
                                if MUC_FCON[fromjid]['spam']=='3':
                                        order_ban(fromjid, nick, u'сообщения слишком похожи!')
                                        return
                        else:
                                LSEND_IQ[fromjid+mesfrom]['time']=time.time()
                                LSEND_IQ[fromjid+mesfrom]['msg']=zh
                if len(zh)>int(MUC_FCON[fromjid]['len']):
                        if MUC_FCON[fromjid]['msg']=='1':
                                MUC_STAT['except']+=1
                                msg(fromjid+'/'+nick,u'слишком большое сообщение!')
                                return
                        if MUC_FCON[fromjid]['msg']=='2':
                                order_kick(fromjid, nick, u'слишком большое сообщение!')
                                return
                        if MUC_FCON[fromjid]['msg']=='3':
                                order_ban(fromjid, nick, u'слишком большое сообщение!')
                                return
                if (zh.count('http://')) | (zh.count('@con')) | (zh.count('c.j.r')) | (zh.count(u'заходите')):
                        zh=reg_rek(zh)#zh.replace(u'http://','').replace(u'@con','').replace(u'c.j.r','')
                        if MUC_FCON[fromjid]['rek']=='1':
                                msg(fromjid+'/'+nick,u'рекламить запрещено!')
                                MUC_STAT['except']+=1
                                return
                        if MUC_FCON[fromjid]['rek']=='2':
                                order_kick(fromjid, nick, u'рекламить запрещено!')
                                return
                        if MUC_FCON[fromjid]['rek']=='3':
                                order_ban(fromjid, nick, u'рекламить запрещено!')
                                return
                if iq_censor(zh):
                        if MUC_FCON[fromjid]['obs']=='1':
                                msg(fromjid+'/'+nick,u'матюги ф топку!')
                                MUC_STAT['except']+=1
                                return
                        if MUC_FCON[fromjid]['obs']=='2':
                                order_kick(fromjid, nick, u'матюги ф топку!')
                                return
                        if MUC_FCON[fromjid]['obs']=='3':
                                order_ban(fromjid, nick, u'матюги ф топку!')
                                return
                        zh=zh.replace(u'хуя','***').replace(u'ебал','****').replace(u'бля','***').replace(u'хуй','***').replace(u'нах','***').replace(u'пизд','*****').replace(u'пидор','*****').replace(u'мудак','*****').replace(u'лох','***').replace(u'мудил','*****')
                if len(zh)>int(MUC_FCON[fromjid]['len']):
                        zh=zh[:int(MUC_FCON[fromjid]['len'])]+' ...>'
        if 'blacklist' in MUC_FCON[fromjid]:
                if true_jid in MUC_FCON[fromjid]['blacklist']:
                        zh=random.choice(MUC_REPLACE)
        result = xmpp.Iq('result')
	result.setTo(iq.getFrom())
	result.setID(iq.getID())
	query = xmpp.Node('query')
	query.setNamespace("http://jabber.ru/muc-filter")
	bz = xmpp.Node("message", {"from":mesfrom,"to":mesto,"type":mestype})
	bz.setTagData("body",zh.strip())
	query.addChild(node=bz)
	result.addChild(node=query)
	JCON.send(result)
	
def find_chat_nick(gch,jid):
        if gch in GROUPCHATS:
                for x in GROUPCHATS[gch]:
                        if GROUPCHATS[gch][x]['ishere']==1 and 'jid' in GROUPCHATS[gch][x]:
                                if GROUPCHATS[gch][x]['jid']==jid:
                                        return unicode(x)
        return 'anything'

MPAR_LIST={u'blacklist':u'blacklist',u'вайп':u'vipe',u'len':u'len',u'реклама':u'rek',u'мат':u'obs',u'приват':u'priv',u'спам':u'spam',u'мессага':u'msg'}

def muc_filter(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if check_file(source[1],'muc_filt.txt'):
                fp=open('dynamic/'+source[1]+'/muc_filt.txt','r')
                txt=eval(fp.read())
                fp.close()
        if not txt:
                return
        if parameters.count(' '):
                s=parameters.split()
                if s[0]=='len':
                        try:
                                if int(s[1])<1000:
                                        reply(type,source,'ok')
                                        txt[s[0]]=s[1]
                                        write_file('dynamic/'+source[1]+'/muc_filt.txt',str(txt))
                                        muc_filter_load(source[1])
                                        return
                                else:
                                        reply(type,source,'1000 symbols max!')
                                        return
                        except (ValueError,UnicodeEncodeError):
                                reply(type,source,'read help!')
                                return
                if s[0]=='blacklist':
                        if len(s[1])>3:
                                reply(type,source,'ok')
                                if not 'blacklist' in txt:
                                        txt['blacklist']=[]
                                        write_file('dynamic/'+source[1]+'/muc_filt.txt',str(txt))
                                        muc_filter_load(source[1])
                                if s[1] not in txt['blacklist']:
                                        txt['blacklist'].append(s[1])
                                else:
                                        txt['blacklist'].remove(s[1])
                                write_file('dynamic/'+source[1]+'/muc_filt.txt',str(txt))
                                muc_filter_load(source[1])
                                return
                if not s[0] in MPAR_LIST:
                        reply(type,source,u'read help!')
                        return
                par=['0','1','2','3']
                if not s[1] in par:
                        reply(type,source,u'read help!')
                        return
                txt[MPAR_LIST[s[0]]]=s[1]
                write_file('dynamic/'+source[1]+'/muc_filt.txt',str(txt))
                reply(type,source,u'ok')
                muc_filter_load(source[1])
                return
        else:
                rep=''
                for d in txt:
                        inf=''
                        if txt[d]==0 or txt[d]=='0':
                                inf=u' (пассивный режим)'
                        if txt[d]==1 or txt[d]=='1':
                                inf=u' (блокировать)'
                        if txt[d]==2 or txt[d]=='2':
                                inf=u' (кик)'
                        if txt[d]==3 or txt[d]=='3':
                                inf=u' (ban)'
                        if d!='blacklist':
                                rep+=d+' : '+str(txt[d])+inf+'\n'
                        else:
                                p=''
                                for x in txt[d]:
                                        p+=x+'; '
                                if len(p)<3:
                                        p=u' пусто'
                                rep+=d+' : '+p+'\n'
                rep=rep.replace('vipe',u'вайп').replace('priv',u'приват').replace('obs',u'мат').replace('spam',u'спам').replace('msg',u'мессага').replace('rek',u'реклама')
                reply(type,source,rep+u'\nГлобальная статистика: сообщений через фильтр:'+unicode(MUC_STAT['msg'])+u'\nпрезенсов:'+unicode(MUC_STAT['prs'])+u'\nотказов:'+unicode(MUC_STAT['except']))
                
        
def muc_filter_load(groupchat):
        if check_file(groupchat,'muc_filt.txt'):
                fp=open('dynamic/'+groupchat+'/muc_filt.txt','r')
                txt=eval(fp.read())
                fp.close()
                if not txt:
                        txt['blacklist']=[]
                        txt['rek']='0'
                        txt['obs']='0'
                        txt['priv']='0'
                        txt['spam']='0'
                        txt['msg']='0'
                        txt['len']='1000'
                        txt['vipe']='0'
                        write_file('dynamic/'+groupchat+'/muc_filt.txt',str(txt))
                if not groupchat in MUC_FCON:
                        MUC_FCON[groupchat]={'blacklist':[],'vipe':'0','rek':'0','obs':'0','priv':'0','spam':'0','msg':'0','len':'1000'}
                for x in txt:
                        if x in MUC_FCON[groupchat]:
                                MUC_FCON[groupchat][x]=txt[x]
        

def reg_rek(body):
        if body.count(' '):
                s=body.split()
                rep=''
                for i in s:
                        if i.count(u'заходи'):
                                rep+=u'*реклама*'
                        if (i.count('conference')) | (i.count('http://')) | (i.count('@con')) | (i.count('c.j.r')):
                                rep+=u'*реклама* '
                        else:
                                rep+=i+' '
                return rep
        else:
                if (body.count('http://')) | (body.count('@con')) | (body.count('c.j.r')):
                        return u'*реклама*'
        return ''

IQCEN=[u'выепу',u'суки',u'заеб',u'бля',u'бляд', u'блят', u'бля ', u'блять', u'плять ', u'хуй', u'ибал', u'ебал', u'нахуй', u'хуи', u'хуител', u'хуя', u'хуя', u' хую', u'хуе', u'ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог']


def iq_censor(body):
        for x in IQCEN:
                if body.count(x) or body==x:
                        return 1
        return 0

def iq_rep(body):
        rep=''
        i=body.lower()
        if not body.count(' '):
                for x in IQCEN:
                        if i.count(x) or i==x:
                                return u'censored'
                return body
        elif body.count(' '):
                s=body.split()
                for p in s:
                        if iq_censor(p.lower()):
                                rep+=u'censored'
                        else:
                                rep+=p
                return rep

def handler_send_filtered(iq):
        result=iq.buildReply('result')
        query = result.getTag('query')
        query.addChild(node=iq.getQueryChildren()[0])
        JCON.send(result)
        raise xmpp.NodeProcessed

def stanza_iq():
        JCON.RegisterHandler('iq', hnd_filter_iq, 'set', 'http://jabber.ru/muc-filter') 

                
register_stage0_init(stanza_iq)
register_stage1_init(muc_filter_load)
register_command_handler(muc_filter, 'mfilt', ['мод','антиспам','антивайп'], 20, 'Ключи команды: вайп 0 - бот пропускает все презенсы, вайп 1 - бот блокирует презенсы с небезопасных серверов,\n blacklist и жид-добавляет/удаляет жид юзера в черный список,посты такого юзера коверкает бот\nреклама 0- бот не реагирует на рекламу, реклама 1-сообщение блокируеться, реклама 2-кик, реклама 3-бан. \nКлюч приват 0 -сообщения в приват разрешены, приват 1 -запрещены. \nКлюч мессага 0- бот не реагирует на большие мессаги, урезаеться только длинна до 1000 символов(можно изменить набрав команду mfilt len <кол-во символов>). мессага 1 -блокировка сообщения превышающего лимит, мессага 2 - кик, мессага 3 - бан. \n Ключ спам, мат - см.предыдущие', 'mfilt <key> <0|1|2|3>', ['mfilt реклама 2'])
