#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')


LS_SRCL={}



def decode_log(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')


def srclog_get(type,source,parameters):
    if not source[1] in GROUPCHATS:
        reply(type,source,u'only chat can do it!')
        return
    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
    if not PUBLIC_LOG_DIR:
        reply(type,source,u'запись логов не активна!')
        return
    if not parameters:
        reply(type,source,u'что искать?')
        return
    if parameters.isspace():
        return
    if len(parameters)>45:
        reply(type,source,u'слишком большой запрос!')
        return
    if not '1' in LS_SRCL:
        LS_SRCL['1']={'time':time.time()}
    else:
        if time.time() - LS_SRCL['1']['time']<60:
            reply(type,source,u'подождите 60 секунд.')
            return
        else:
            LS_SRCL['1']['time']=time.time()
    if parameters.count(' ')>1:
        s=parameters.split()
        text=' '.join(s[2:])
        if text=='' or text.isspace():
            print 'no text'
            return
        if s[0].lower()==u'месяц' and s[1].isdigit():
            if not os.path.exists(PUBLIC_LOG_DIR+'/'+source[1]+'/'+str(year)+'/'+s[1]):
                reply(type,source,u'файл не найден!')
                return
            else:
                li=os.listdir(PUBLIC_LOG_DIR+'/'+source[1]+'/'+str(year)+'/'+s[1])
                rep=''
                n=0
                for x in li:
                    try:
                        fp=PUBLIC_LOG_DIR+'/'+source[1]+'/'+str(year)+'/'+s[1]+'/'+x
                        rd=open(fp,'r')
                        data=rd.read()
                        rd.close()
                        if data.count(text.encode('utf-8','replace')):
                            rep+=('\nLog from /'+s[1]+'/'+x+'\n').encode('utf-8','replace')
                        m=data.splitlines()
                        for i in m:
                            if i.count(text.encode('utf-8','replace')) and not i.count(u'!лог'.encode('utf-8','replace')):
                                i=decode_log(i)
                                if i!='' and i.isspace()==False:
                                    n+=1
                                    if n<51:
                                        if n>2 and len(i)>160:
                                            i=i[:160]+' ...'
                                        rep+=str(n)+') '+i+'\n'
                    except:
                        reply(type,source,u'произошла ошибка')
                if rep=='':
                    reply(type,source,u'no found')
                    return
                if len(rep)>2600:
                    rep=rep[:2600]+' (limit)...'
                reply(type,source,rep)
                return
    try:
        if parameters.count(' '):
            s=parameters.split()
            if s[0].lower()==u'вчера':
                if day==1:
                    reply(type,source,u'логи за вчера скорее всего в директории за другой месяц!')
                    return
                else:
                    day=day-1
                    parameters=' '.join(s[1:])
        fp = file(PUBLIC_LOG_DIR+'/'+source[1]+'/'+str(year)+'/'+str(month)+'/'+str(day)+'.html')
        data = fp.read()
        if not data.count(parameters.encode('utf-8', 'replace')):
            reply(type,source,u'no found')
            return
        else:
            od=''
            m=data.splitlines()
            n=0
            for i in m:
                if i.count(parameters.encode('utf-8', 'replace')):
                    i=decode_log(i)
                    if i!='' and i.isspace()==False:
                        n+=1
                        if n<51:
                            if n>2 and len(i)>160:
                                i=i[:160]+' ...'
                            od+=str(n)+') '+i+'\n'
            if od=='':
                reply(type,source,u'no found')
                return
            if len(od)>2600:
                od=od[:2600]+' (limit)...'
            reply(type,source,od)
    except:
        reply(type,source,u'не получилось')

    

register_command_handler(srclog_get, '!лог', ['все','мод'], 20, 'Поиск текста в логах бота.Ключи команды - <вчера>, <месяц>.Без ключа будет искать в логах за сегодня.', '!лог <ключ> <текст>', ['!лог месяц 6 40tman','!лог 40tman','!лог вчера 40tman'])
