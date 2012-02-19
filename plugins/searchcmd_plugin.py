#===istalismanplugin===
# -*- coding: utf-8 -*-

import inspect


def plugin_search_hnd(type, source, parameters):
    if not parameters: return
    if not parameters.lower() in COMMANDS:
        reply(type, source, u'Такой команды не существует!')
        return
    cmd=COMMAND_HANDLERS[parameters.lower()]
    file=inspect.getfile(cmd)
    size=str(os.path.getsize(file)//1024)+'Kb.'
    last=timeElapsed(time.time()-os.path.getmtime(file))
    name=cmd.func_name
    reply(type, source, u'Информация о команде \"'+parameters.lower()+u'\":\n Файл:'+file+u'\nИмя функции:'+name+u'\nВремя последнего изменения:\n'+last+u'\nРазмер всего плагина:'+size)

                

register_command_handler(plugin_search_hnd, '!плагин', ['все','суперадмин'], 20, 'Поиск команды в плагинах', '!плагин <команда>', ['!плагин тест'])
