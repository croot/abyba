#===istalismanplugin===
# -*- coding: utf-8 -*-



def handler_absurd(type, source, parameters):
    try:
        if parameters:
            if parameters.count(' '):
                parameters=parameters.replace(' ','_')
            req = urllib2.Request('http://absurdopedia.wikia.com/wiki/'+parameters.encode('utf-8'))
            req.add_header = ('User-agent', 'Mozilla/5.0')
            r = urllib2.urlopen(req)
            target = r.read()
            od = re.search('<p><b>',target)
            message = target[od.end():]
            message = message[:re.search('<nav class="RelatedPagesModule noprint">',message).start()]
            script = re.compile(r"<script>.*</script>")
            message=script.sub("",message)
            try:
                message=decode(message)
            except:
                message=decode_s(message)
            message = message.replace('<','').replace('" target="_blank">','\n').replace('>','').replace('&','').replace('_','').replace('#','')
            reply(type, source, unicode(message,'UTF-8'))
        else:
            reply(type, source, u'а что искать то?')
    except:
        reply(type, source, u'По вашему запросу ничего не найдено')

register_command_handler(handler_absurd, 'абсурд', ['все','mod','инфо'], 0, 'Поиск статьи в http://absurdopedia.wikia.com', 'абсурд <слово>', ['абсурд пиво'])
