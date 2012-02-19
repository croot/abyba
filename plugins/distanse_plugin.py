#===istalismanplugin===
# -*- coding: utf-8 -*-


def distanse_q(type, source, parameters):
    try:
        if not parameters or not parameters.count(' '):
            return
        s=parameters.split()
        a=urllib.quote(s[0].encode('cp1251'))
        b=urllib.quote(s[1].encode('cp1251'))
        adr='http://www.ati.su/Trace/default.aspx?EntityType=Trace&City1=%s&City5=%s' % (a,b)
        page = urllib.urlopen(adr)
        r=page.read()
        r=r.decode('cp1251')
        city1=''
        city2=''
        rep=''
        f=re.findall('<span id="[^>]*?>(.+)</td>',r)
        w=re.findall('<input name=\"[^>]*?value=\"(.+)\"',r)
        if w and len(w)>1:
            city1=w[0].split('\"')[0]
            city2=w[1].split('\"')[0]
        rep=u'Расстояние между: '+city1+u' и '+city2+' '+decode_log(f[0])+u';\nВремя в пути: '+decode_log(f[1])
        reply(type, source, rep)
    except Exception, err:
        reply(type, source, u'расстояние неизвестно')
    

register_command_handler(distanse_q, 'расстояние', ['все'], 0, '/', '/', ['/'])

