#===istalismanplugin===
# -*- coding: utf-8 -*-

WIKI={}


def wiki_q(type, source, parameters):
    try:
        if not parameters:
            reply(type, source, 'what?')
            return
        if parameters.count(' '):
            s=parameters.split()
            if s[1].isdigit() and s[0] in WIKI.keys():
                if WIKI[s[0]].has_key(int(s[1])-1):
                    reply(type, source, WIKI[s[0]][int(s[1])-1])
                    return
            else:
                parameters=parameters.replace(' ','_')
        adr='http://anonymouse.org/cgi-bin/anon-www.cgi/http://ru.wikipedia.org/wiki/'
        req = urllib2.Request(adr+parameters.encode('utf8','replace'))
        req.add_header = ('User-agent', 'Opera/9.8')
        page=urllib2.urlopen(req)
        r=page.read()
        f=re.findall('<p>(.*)</p>',r)
        p="\n".join(f)
        p=p.replace('&#160;','')
        try:
            p=decode_log(p)
        except:
            p=decode(p)
        if len(p)>2900:
            reply(type, source, p[:2900]+(u' >>> чтобы читать далее наберите вики '+parameters).encode('utf8','replace')+' 2')
            #time.sleep(2)
            #reply(type, source, '>>> '+p[3000:])
            z=len(p)
            i=len(p)//2900
            i=i+1
            for x in range(0, i):
                if x!=0:
                    print x
                    k=2900*x
                    if not parameters in WIKI.keys():
                        WIKI[parameters]={}
                    if not x in WIKI[parameters].keys():
                        WIKI[parameters][x]={}
                    WIKI[parameters][x]=p[k:]
            return
        if len(p)<100:
            reply(type, source, u'не найдено')
            return
        reply(type, source, p)
    except Exception, err:
        raise
        reply(type, source, u'не получилось')
    

register_command_handler(wiki_q, 'вики', ['все'], 0, 'показывает статью с http://ru.wikipedia.org/wiki/', 'вики слово', ['вики пиво'])

