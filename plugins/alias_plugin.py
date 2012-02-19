#===istalismanplugin===
# -*- coding: utf-8 -*-

ALIAS = {}

def handler_alias_msg(raw, type, source, parameters):
        rep=''
        global ALIAS
        if source[1] in ALIAS.keys():
                if parameters.lower() in ALIAS or parameters.split()[0].lower() in ALIAS[source[1]]:
                        m=ALIAS[source[1]][parameters.split()[0].lower()]['code']
                        if m.count('%CONF%'):
                                m=m.replace('%CONF%',source[1])
                        if m.count('%TIME1%'):
                                m=m.replace('%TIME1%','')
                                n=random.randrange(2,3)
                                time.sleep(n)
                        if m.count('%NICK%'):
                                m=m.replace('%NICK%',source[2])
                        if m.count('%PARAMETERS%'):
                                m=m.replace('%PARAMETERS%',parameters)
                        if m.count('%JID%'):
                                m=m.replace('%JID%',get_true_jid(source[1]+'/'+source[2]))
                        if m.count('%SERV%'):
                                try: m=m.replace('%SERV%',get_true_jid(source[1]+'/'+source[2]).split('@')[1])
                                except: pass
                        if m.count('%RAND1%'):
                                m=m.replace('%RAND1%', str(random.randrange(1,10)))
                        if m.count('%RAND2%'):
                                m=m.replace('%RAND2%', str(random.randrange(10,100)))
                        cmd=ALIAS[source[1]][parameters.split()[0].lower()]['cmd']
                        cmd_hnd = COMMAND_HANDLERS[cmd]
                        try:
                                INFO['thr'] += 1
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = u'command%d.%s.%s' % (INFO['thr'],cmd_hnd.func_name,st_time)
				thr = threading.Thread(None,cmd_hnd,thr_name,(type, source, m,))
				thr.start()
			except: pass
                        #call_command_handlers(cmd, type, source, m, cmd)

register_message_handler(handler_alias_msg)

def handler_alias_add(type, source, parameters):
        if not source[1] in GROUPCHATS: return
        if not parameters or len(parameters)>300: reply(type, source, u'и?')
        else:
                if not check_file(source[1],'al.txt'): return
                if not parameters.count('='): reply(type, source, u'Синтаксис инвалид!')
                else:
                        p=parameters.split('=')
                        if p[0].lower() in COMMANDS:
                                reply(type, source, p[0]+u' являеться командой!')
                                return
                        if p[0]=='': return
                        if not p[1].count(' '):
                                cmd=p[1].lower()
                                code=''
                        else:
                                cmd=p[1].split()[0].lower()
                                code=' '.join(p[1].split()[1:])
                        if not cmd in COMMANDS:
                                reply(type, source, cmd+u' не являеться командой!')
                                return
                        real_access = COMMANDS[cmd]['access']
                        if not has_access(source, real_access, source[1]):
                                reply(type, source, u'Необходимый доступ для этой команды:'+str(real_access))
                                return
                        txt=eval(read_file('dynamic/'+source[1]+'/al.txt'))
                        if len(txt)>20:
                                reply(type, source, u'Более 20-ти алиасов запрещено!')
                                return
                        txt[p[0].lower()]={'cmd':cmd,'code':code}
                        write_file('dynamic/'+source[1]+'/al.txt',str(txt))
                        reply(type, source, u'Добавил!')
                        alias_init(source[1])

def alias_init(chat):
        global ALIAS
        if not check_file(chat,'al.txt'): return
        txt=eval(read_file('dynamic/'+chat+'/al.txt'))
        if txt:
                if not chat in ALIAS.keys():
                        ALIAS[chat]={}
                for x in txt:
                        ALIAS[chat][x]=txt[x]

def handler_alias_del(type, source, parameters):
        if not source[1] in GROUPCHATS or not check_file(source[1],'al.txt'): return
        txt=eval(read_file('dynamic/'+source[1]+'/al.txt'))
        if txt:
                if parameters.lower() in txt:
                        del txt[parameters.lower()]
                        try: del ALIAS[source[1]][parameters.lower()]
                        except: pass
                        write_file('dynamic/'+source[1]+'/al.txt',str(txt))
                        reply(type, source, u'Удалил!')

def handler_alias_list(type, source, parameters):
        if not source[1] in GROUPCHATS: return
        txt=eval(read_file('dynamic/'+source[1]+'/al.txt'))
        if not txt:
                reply(type, source, u'Пусто!')
                return
        rep, n = '', 0
        for x in txt:
                n+=1
                rep+=str(n)+') '+x+'='+txt[x]['cmd']+' '+txt[x]['code']+'\n'
        reply(type, source, rep)

register_stage1_init(alias_init)
register_command_handler(handler_alias_add, 'алиас', ['админу','все'], 20, 'Добавляет алиас.\nДоступные параметры:\n %NICK% - возвращает ник написавшего,\n%SERVER% - сервер,\n %CONF% - текущая конференция,\n %TIME1%-задержка 2-3 секунды.\n%RAND1%, %RAND2% - произвольное целое число от 1 до 9 и от 10 до 99\n %PARAMETERS% - параметры', 'алиас <слово>=<команда>', ['алиас квас=сказать /me налил %PARAMETERS% примерно 0,%RAND1%л свежего кваску','алиас куку=сказать %NICK%: приветствую тебя в конференции %CONF%'])
register_command_handler(handler_alias_list, 'алиас_лист', ['админу','все'], 20, 'Просмотр списка алиасов.', 'алиас_лист', ['алиас_лист'])
register_command_handler(handler_alias_del, 'алиас_дел', ['админу','все'], 20, 'Удаление алиаса.', 'алиас_дел <алиас>', ['алиас_дел квас'])
