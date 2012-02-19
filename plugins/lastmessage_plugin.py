#===istalismanplugin===
# -*- coding: utf-8 -*-

LAST_MESSAGE={}

def last_message(raw, type, source, parameters):
    if source[1] not in GROUPCHATS.keys() or type=='private':
        return
    if len(parameters)>500 or parameters.isspace():
        return
    if not source[1] in LAST_MESSAGE.keys():
        LAST_MESSAGE[source[1]]={'body':[]}
        LAST_MESSAGE[source[1]]['body'].append(source[2]+': '+parameters)
    else:
        if len(LAST_MESSAGE[source[1]]['body'])>10:
            LAST_MESSAGE[source[1]]['body'].pop(0)
        LAST_MESSAGE[source[1]]['body'].append(source[2]+': '+parameters)


def last_message_hnd(type, source, parameters):
    if source[1] in LAST_MESSAGE.keys():
        if type!='private':
            reply(type, source, u'look at private!')
        reply('private', source, "\n".join(LAST_MESSAGE[source[1]]['body']))

register_message_handler(last_message)
register_command_handler(last_message_hnd, '!сс', ['все'], 0, 'Выводит последние 10 сообщений в чате', '!сс', ['!сс'])

