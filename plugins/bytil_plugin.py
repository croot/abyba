#===istalismanplugin===
# -*- coding: utf-8 -*-

BUTIL=[]


def handler_bytil(type,source,parameters):
        if source[1] not in GROUPCHATS:
                return
        if not parameters or parameters == '':
                return
        BT = 'dynamic/bytil.txt'
        fp = open(BT, 'r')
        txt = eval(fp.read())
        fp.close()
        for x in GROUPCHATS[source[1]]:
                if GROUPCHATS[source[1]][x]['ishere']==1:
                        if x != parameters and x != get_bot_nick(source[1]):
                                globals()['BUTIL'].append(x)
        s = random.choice(globals()['BUTIL'])
        r = random.choice(txt)
        reply(type,source,u'бутылочка крутиться крутиться и указывает на '+s)
        time.sleep(2)
        reply(type,source,r % (parameters,s))
        globals()['BUTIL'] = ['']

def bytil_append(type,source,parameters):
        BT = 'dynamic/bytil.txt'
        fp = open(BT, 'r')
        txt = eval(fp.read())
        fp.close()
        if parameters.count('%s')<2:
                reply(type,source,u'read help')
                return
        if parameters not in txt:
                txt.append(parameters)
                write_file(BT,str(txt))
                reply(type,source,u'ok')

def bytil_all(type,source,parameters):
        BT = 'dynamic/bytil.txt'
        fp = open(BT, 'r')
        txt = eval(fp.read())
        fp.close()
        p =1
        spisok = ''
        for usr in txt:
                spisok += str(p)+'. '+usr+'\n'
                p +=1
        reply(type, source, u'(всего '+str(len(txt))+u'):\n'+spisok)
                
def bytil_del(type,source,parameters):
        BT = 'dynamic/bytil.txt'
        fp = open(BT, 'r')
        txt = eval(fp.read())
        fp.close()
        write_file(BT,str('[]'))
        reply(type, source, u'done')
        

register_command_handler(handler_bytil, 'бутыль', ['мод'], 0, 'бутылочка', 'бутыль <ник>', ['бутыль Вася'])
register_command_handler(bytil_append, 'бутыль_адд', ['мод','админ'], 20, 'добавляет шуточки в базу,где сочетание %s - это будет значение ника указанного при команде "бутылочка",а второе %s -случайный ник из чата.', 'бутыль_адд', ['бутыль_адд теперь %s целует взасос %s'])
register_command_handler(bytil_all, 'бутыль_все', ['мод'], 0, 'показывает шуточки из базы', 'бутыль_все', ['бутыль_все'])
#register_command_handler(bytil_del, 'бутыль_дел', ['все'], 0, 'очистить базу', 'бутыль_дел', ['бутыль_дел'])
