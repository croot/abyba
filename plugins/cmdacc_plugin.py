#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman

def cmd_acc_set(type,source,parameters):
    global COMMANDS
    if not parameters:
        reply(type,source,u'and?')
        return
    if not parameters.count(' '):
        reply(type,source,u'read help!')
        return
    s=parameters.split()
    if s[0].lower() not in COMMANDS:
        reply(type,source,u'команда '+s[0]+u' не найдена!')
        return
    if not s[1].isdigit():
        reply(type,source,s[1]+u' не являеться числом')
        return
    try:
        file='dynamic/cmdacc.txt'
        txt=eval(read_file(file))
        txt[s[0].lower()]=s[1]
        write_file(file, str(txt))
        COMMANDS[s[0]]['access']=int(s[1])
        reply(type,source,u'доступ на команду '+s[0]+u' установлен '+s[1])
    except:
        reply(type,source,u'uknown error')
        pass

def cmd_acc_init():
    global COMMANDS
    try:
        file='dynamic/cmdacc.txt'
        if not os.path.exists(file):
            print 'Ok, created file cmdacc.txt'
            fp=open(pth, 'w')
            fp.write('{}')
            fp.close()
        txt=eval(read_file(file))
        for x in txt.keys():
            if x in COMMANDS.keys():
                COMMANDS[x]['access']=txt[x]
    except:
        print 'error in cmd_acc_init'



register_stage0_init(cmd_acc_init)
register_command_handler(cmd_acc_set, 'комдоступ', ['суперадмин','все'], 100, 'меняет доступ команды', 'комдоступ <command> <access>', ['комдоступ диско 10'])
