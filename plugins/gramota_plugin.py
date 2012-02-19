#===istalismanplugin===
# -*- coding: utf-8 -*-


def gramota_q(type, source, parameters):
    try:
        if len(parameters)>27:
            return
        if not parameters:
            return
        p=''
        adr='http://www.gramota.ru/slovari/dic/?lop=x&bts=x&word='
        z=urllib.quote(parameters.encode('cp1251'))
        page = urllib.urlopen(adr+z)
        r=page.read()
        r=unicode(r,'cp1251')
        f=re.findall('<div style="p[^>]*?>(.+)</',r)
        p=u'Орфографический словарь:\n'+f[0]+u' Большой толковый словарь:\n'+f[1]#"\n".join(f)
        try:
            p=decode_log(p)
        except:
            p=decode(p)
        if p=='':
            reply(type, source, u'Нет результатов!')
            return
        reply(type, source, p)#unicode(p,'cp1251'))
    except Exception, err:
        reply(type, source, u'Произошла ошибка!')
    

register_command_handler(gramota_q, '!словарь', ['все'], 0, 'Проверка слова в грамматическом словаре, поиск слова в большом толковом словаре http://gramota.ru', '!словарь <слово>', ['!словарь чес*ный'])

