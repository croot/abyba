#===istalismanplugin===
# -*- coding: utf-8 -*-


def send_top(type, source, parameters):
    if not parameters or not source[1] in GROUPCHATS.keys():
        return
    STANZA="""<message type="groupchat" to="%s" >
    <subject>%s</subject>
  </message>""" % (source[1], parameters)
    node=xmpp.simplexml.XML2Node(unicode(STANZA).encode('utf8'))
    JCON.send(node)
    reply(type, source, u'ok')



   

register_command_handler(send_top, 'топик', ['все'], 0, 'установка темы конфы через бота', 'топик текст', ['топик хобана!'])

