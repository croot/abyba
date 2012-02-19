#===istalismanplugin===
# -*- coding: utf-8 -*-

def hnd_www(type, source, parameters):
    if not parameters:
        return
    if not parameters.count('.'):
        reply(type, source, u'Неверный адрес!')
    if parameters.count('http://'):
        parameters=parameters.replace('http://','')
    try:
        page=''
        data = urllib.urlopen('http://'+parameters.encode('utf8')).read()
        cod = chardet.detect(data)['encoding']
        data = unicode(data, cod)
        data = re.compile(r'<style[^<>]*?>.*?</style>',re.DOTALL | re.IGNORECASE).sub('', data)
        data = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', data)
        if data.count('</style>'):
            data = ''.join(data.split('style')[2:])
        page = re.compile(r'<[^<>]*>').sub('', data)
        page = page.replace('\n\n','').replace('&nbsp;','').replace('&gt;','')
        page = '\n'.join([x for x in page.splitlines() if not x.isspace()])
        #page = ''.join(map(lambda x: x.strip(), page.splitlines()))
        reply(type, source, page)
    except:
        traceback.print_exc()
        reply(type, source, u'Ошибочка!')

register_command_handler(hnd_www, 'www', ['все'], 0, 'Получить содержимое веб страницы', 'www url', ['www mail.ru'])
