#===istalismanplugin===
# -*- coding: utf-8 -*-

# (C) Gigabyte
# * Распространять без указания ссылки на ресурс и автора ЗАПРЕЩЕНО!
# * Применимо только в личных целях, никакой коммерции!!!


import random, time

board_list = {}
comp_marker = None
marker = None

TTT_SCORE = {}

def ttt_load_score(conf):
    global TTT_SCORE
    try:
        fp = open('dynamic/%s/tictactoe.txt' % (conf), 'r')
        tmp = eval(fp.read())
        fp.close()
    except:
#        print 'Create new config for TTT'
        tmp = {}
    TTT_SCORE[conf] = tmp

def ttt_save_score(conf):
    global TTT_SCORE
#    print 'Save config %s' % (str(TTT_SCORE))
    try:
        fp = open('dynamic/%s/tictactoe.txt' % (conf), 'w')
        fp.write( str(TTT_SCORE[conf]) )
        fp.close()
    except:
        print 'Unable to save tic tac toe base'


def ttt_start_game(conf, jid):
    global board_list
    global TTT_SCORE
    if not conf in TTT_SCORE:
        ttt_load_score(conf)
        print 'TTT - for room %s create new config' % (conf)
    if not get_true_jid(conf+'/'+jid) in TTT_SCORE[conf]:
        TTT_SCORE[conf][get_true_jid(conf+'/'+jid)] = {'score':0,'win':0,'lose':0,'draw':0,'game_x':0,'game_o':0}
    if not conf in board_list:
        board_list[conf] = {}
    board_list[conf][jid] = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

#        board[conf] = {jid:update_board(board_list[conf][jid])}


#start_game('test@conference.jabbrik.ru', 'gigabyte@jabbrik.ru')


def update_board(conf, jid, l):
    if not conf in board_list:
        board_list[conf] = {}
    board_list[conf][jid] = l
    board = """
   %s   |   %s   |   %s
-----------------------
   %s   |   %s   |   %s
-----------------------
   %s   |   %s   |   %s""" % (board_list[conf][jid][0],
                              board_list[conf][jid][1],
                              board_list[conf][jid][2],
                              board_list[conf][jid][3],
                              board_list[conf][jid][4],
                              board_list[conf][jid][5],
                              board_list[conf][jid][6],
                              board_list[conf][jid][7],
                              board_list[conf][jid][8]) 
    return board

def see_if_win(conf, jid, mode="normal"):
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5
    g = 6
    h = 7
    i = 8
    winlist = [(a,b,c), (d,e,f), (g,h,i), (a,d,g,), (b,e,h), (c,f,i), (a,e,i), (g,e,c)]
    if mode == "normal":
        for win_type in winlist:
            if board_list[conf][jid][win_type[0]] == board_list[conf][jid][win_type[1]] == board_list[conf][jid][win_type[2]]:
                if board_list[conf][jid][win_type[0]] in ["X","O"]:
                    return board_list[conf][jid][win_type[0]]
        else:
            if not " " in board_list[conf][jid]:
                return "6"

    elif mode == "computer_turn":
        for win_type in winlist:
            if (board_list[conf][jid][win_type[0]] == board_list[conf][jid][win_type[1]]) and board_list[conf][jid][win_type[2]] == " " and board_list[conf][jid][win_type[0]] == comp_marker:
                board_list[conf][jid][win_type[2]] = comp_marker
                return board_list[conf][jid]
            elif (board_list[conf][jid][win_type[0]] == board_list[conf][jid][win_type[2]]) and board_list[conf][jid][win_type[1]] == " " and board_list[conf][jid][win_type[0]] == comp_marker:
                board_list[conf][jid][win_type[1]] = comp_marker
                return board_list[conf][jid]
            elif (board_list[conf][jid][win_type[1]] == board_list[conf][jid][win_type[2]]) and board_list[conf][jid][win_type[0]] == " " and board_list[conf][jid][win_type[1]] == comp_marker:
                board_list[conf][jid][win_type[0]] = comp_marker
                return board_list[conf][jid]
        for win_type in winlist:
            if (board_list[conf][jid][win_type[0]] == board_list[conf][jid][win_type[1]]) and board_list[conf][jid][win_type[2]] == " " and board_list[conf][jid][win_type[0]] == marker:
                board_list[conf][jid][win_type[2]] = comp_marker
                return board_list[conf][jid]
            elif (board_list[conf][jid][win_type[0]] == board_list[conf][jid][win_type[2]]) and board_list[conf][jid][win_type[1]] == " " and board_list[conf][jid][win_type[0]] == marker:
                board_list[conf][jid][win_type[1]] = comp_marker
                return board_list[conf][jid]
            elif (board_list[conf][jid][win_type[1]] == board_list[conf][jid][win_type[2]]) and board_list[conf][jid][win_type[0]] == " " and board_list[conf][jid][win_type[1]] == marker:
                board_list[conf][jid][win_type[0]] = comp_marker
                return board_list[conf][jid]

        return None

def comp_turn(conf, jid):
    possible_comp_moves = []
    blah = see_if_win(conf, jid, "computer_turn")
    if blah == None: # No way for the computer to win
        for index in range(len(board_list[conf][jid])):
#            print index
#            print board_list[conf][jid][index]
            if board_list[conf][jid][index] == " ":
                possible_comp_moves.append(index) # adds the index for each possible move
        move_index = random.choice(possible_comp_moves) # randomly chooses a possible move
        board_list[conf][jid][move_index] = comp_marker
        return update_board(conf, jid, board_list[conf][jid])
    else:
        return update_board(conf, jid, blah)

def player_turn(conf, jid, marker, pos):
    temp_list = []
    num = 1
    
    for item in board_list[conf][jid]:
        if item == " ":
            temp_list.append(item)
        else:
            temp_list.append(item)
        num = num + 1
    
    temp_board = update_board(conf, jid, temp_list)

    

    while 1:
        try:
            spot = pos
            while temp_list[int(spot)-1] in ["X","O"] or spot not in ["1","2","3","4","5","6","7","8","9"]:
                return -1
                time.sleep(10)
                spot = pos
        except IndexError:
            continue
        break

    spot = int(spot) - 1
    board_list[conf][jid][spot] = marker
    return update_board(conf, jid, board_list[conf][jid])

def print_pole(conf, jid):
    a = []
    for j, i in enumerate(board_list[conf][jid]):
        if i in ['X', 'O']:
            a.append(i)
        else:
            a.append(str(j+1))
    board = """
   %s   |   %s   |   %s
-----------------------
   %s   |   %s   |   %s
-----------------------
   %s   |   %s   |   %s""" % (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8])

    return board

"""
while 1:
    a = raw_input('>')
    if a == 'quit':
        break
    player_turn('test@conference.jabbrik.ru', 'gigabyte@jabbrik.ru', 'X', a)
    out = comp_turn('test@conference.jabbrik.ru', 'gigabyte@jabbrik.ru')
    print print_pole('test@conference.jabbrik.ru', 'gigabyte@jabbrik.ru')
    a= see_if_win('test@conference.jabbrik.ru', 'gigabyte@jabbrik.ru')
    if a:
        print u'Win: %s' % (a)
        break
"""

def ttt_start_game_a(t, s, b):
        global comp_marker
        global marker
        if t=='private':
            return
        
        ttt_start_game(s[1], s[2] )

        if random.choice([0, 2]) == 0:
            comp_marker = 'X'
            marker = 'O'
            comp_turn(s[1], s[2])
            a= see_if_win(s[1], s[2])
        else:
            comp_marker = 'O'
            marker = 'X'

        msg(s[1], s[2]+u', новая игра.. ты - %s\n%s' % (marker, print_pole(s[1], s[2]) ) )

def ttt_stop_game(conf, nick):
        if conf in board_list:
            if nick in board_list[conf]:
                del board_list[conf][nick]
                return 1
            else:
                return 0
        else:
            return 0

def ttt_stop_game_a(t, s, b):
        global comp_marker
        global marker
        
        if ttt_stop_game(s[1], s[2]):
                msg(s[1], s[2]+u', игра остановлена')
        else:
                msg(s[1], s[2]+u', нет игры')

                

def ttt_go(w, t, s, b):
        if not s[1] in board_list:
            return
        if not s[2] in board_list[s[1]]:
            return

        if not b in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:

            return
        if player_turn(s[1], s[2], marker, b) == -1:
                reply(t, s, u'Не верный ввод')
                return
        a = see_if_win(s[1], s[2])
        if not a:
                comp_turn(s[1], s[2])
        a= see_if_win(s[1], s[2])
        if a == marker:
                reply(t, s, u'Ты выйграл!'+'\n'+print_pole(s[1], s[2]))
                TTT_SCORE[s[1]][get_true_jid(s[0])]['score']+=5
                TTT_SCORE[s[1]][get_true_jid(s[0])]['win']+=1
                if marker=='X':
                    TTT_SCORE[s[1]][get_true_jid(s[0])]['game_x']+=1
                else:
                    TTT_SCORE[s[1]][get_true_jid(s[0])]['game_o']+=1
                ttt_save_score(s[1])
                ttt_stop_game(s[1], s[2])
        elif a == comp_marker:
                reply(t, s, u'Компьютер выйграл!'+'\n'+print_pole(s[1], s[2]))
                TTT_SCORE[s[1]][get_true_jid(s[0])]['score']+=1
                TTT_SCORE[s[1]][get_true_jid(s[0])]['lose']+=1
                if marker=='X':
                    TTT_SCORE[s[1]][get_true_jid(s[0])]['game_x']+=1
                else:
                    TTT_SCORE[s[1]][get_true_jid(s[0])]['game_o']+=1
                ttt_save_score(s[1])
                ttt_stop_game(s[1], s[2])
        elif a in ['1','2','3','4','5','6','7','8','9']:
                reply(t, s, u'Ничья!'+'\n'+print_pole(s[1], s[2]))
                TTT_SCORE[s[1]][get_true_jid(s[0])]['score']+=3
                TTT_SCORE[s[1]][get_true_jid(s[0])]['draw']+=1
                if marker=='X':
                    TTT_SCORE[s[1]][get_true_jid(s[0])]['game_x']+=1
                else:
                    TTT_SCORE[s[1]][get_true_jid(s[0])]['game_o']+=1
                ttt_save_score(s[1])
                ttt_stop_game(s[1], s[2])
        else:
                if t == 'public':
                        msg(s[1], s[2]+'\n'+print_pole(s[1], s[2]))
                else:
                        msg(s[1]+'/'+s[2], s[2]+'\n'+print_pole(s[1], s[2]))

def ttt_get_score(t, s, b):
    if not b:
        JID = get_true_jid(s[0])
        if s[1] in TTT_SCORE:
            if JID in TTT_SCORE[s[1]]:
                xx = round(TTT_SCORE[s[1]][JID]['game_x'] * 100 / (TTT_SCORE[s[1]][JID]['game_x'] + TTT_SCORE[s[1]][JID]['game_o']), 2)
                oo = round(TTT_SCORE[s[1]][JID]['game_o'] * 100 / (TTT_SCORE[s[1]][JID]['game_x'] + TTT_SCORE[s[1]][JID]['game_o']), 2)
                ms = u'[%s]\nсчет: %i,\nпобед/пораж/ничья: %i/%i/%i\nигра X/O: %s/%s' % (s[2], TTT_SCORE[s[1]][JID]['score'], TTT_SCORE[s[1]][JID]['win'], TTT_SCORE[s[1]][JID]['lose'], TTT_SCORE[s[1]][JID]['draw'], str(xx)+'%', str(oo)+'%')
            else:
                ms = u'Нет статистики'
        else:
            ms = u'Не статистики в комнате'
    else:
        if b in GROUPCHATS[s[1]]:
            JID = get_true_jid(s[1]+'/'+b)
            if s[1] in TTT_SCORE:
                if JID in TTT_SCORE[s[1]]:
                    xx = round(TTT_SCORE[s[1]][JID]['game_x'] * 100 / (TTT_SCORE[s[1]][JID]['game_x'] + TTT_SCORE[s[1]][JID]['game_o']), 2)
                    oo = round(TTT_SCORE[s[1]][JID]['game_o'] * 100 / (TTT_SCORE[s[1]][JID]['game_x'] + TTT_SCORE[s[1]][JID]['game_o']), 2)
                    ms = u'[%s]\nсчет: %i,\nпобед/пораж/ничья: %i/%i/%i\nигра X/O: %s/%s' % (b, TTT_SCORE[s[1]][JID]['score'], TTT_SCORE[s[1]][JID]['win'], TTT_SCORE[s[1]][JID]['lose'], TTT_SCORE[s[1]][JID]['draw'], str(xx)+'%', str(oo)+'%')
                else:
                    ms = u'Нет статистики'
            else:
                ms = u'Не статистики в комнате'
        else:
            ms = u'Не знаю этого человека'
    reply(t, s, ms)

def ttt_help(t, s, b):
    OUT = u"""Игра Tic-Tac-Toe или просто крестики-нолики версии 1.00fpv - first public version by Gigabyte
(c)opyrights: Gigabyte
(i)dea: Grand_dizel
Игра проста до безумия, пишем команжу начала игры и играем! Ведется скромная локальная сатистика, обо всем ниже.
Команды:
1. хо-старт - начало новой игры, машина скажет чем вы играете X или O, естественно первыми ходят X
2. хо-стоп - завершение игры
3. хо-счет - вывод вашего локального счета, если чей нибудь ник параметром указать то его счет будет выведен.
--ВНИМАНИЕ! Все команды вводятся русскими буквами!--
Статистика представляет из себя примерно следущее:
----------
счет: 9,
побед/пораж/ничья: 0/3/2
игра X/O: 40.0%/60.0%
----------
Счет - это ваш счет, начисляется следущим способом: за победу +5, за ничью +3 и за проигрыш +1, дада, мы такие щедрые ))) На самом деле счет тут просто для вида.
побед, поражений и ничья тут все понятно, 0, 3 и 2 соответствует своим пунктам
Игра Х/О это процентное соотношение игр крестиками и ноликами
----------
Как играть? Легко! После запуска игры отправляй номер клетки на которую надо поставить Х или О и всё =)
"""
    reply(t, s, OUT)


register_command_handler(ttt_get_score, 'хо-счет', ['ХО','все'], 10, 'Вывод вашего счета в игре или чьего либо счета (ника)', 'хо-счет [ник]', ['хо-счет'])
register_stage1_init(ttt_load_score)
register_command_handler(ttt_start_game_a, 'хо-старт', ['ХО','все'], 10, 'Начало новой игры, машина сама выберет кем вы играете X или O', 'хо-старт', ['хо-старт'])
register_command_handler(ttt_stop_game_a, 'хо-стоп', ['ХО','все'], 10, 'Завершение игры', 'хо-стоп', ['хо-старт'])
register_command_handler(ttt_help, 'хо-помощь', ['игры','все'], 10, 'Показать помощь по игре', 'хо-помощь', ['хо-помощь'])
register_message_handler(ttt_go)
