#===istalismanplugin===
# -*- coding: utf-8 -*-


def handler_pod_pl(type,source,parameters):
  if not parameters: return

  fp = 'plugins/' + parameters+'_plugin.py'

  if not os.path.exists(fp):
    fp = 'plugins/' + parameters+'.py'
  if not os.path.exists(fp):
    fp = 'plugins/' + parameters
  if not os.path.exists(fp):
    reply(type, source, u'Такого плагина нету')
    return

  i = handlers_load_checker(fp)
  stage0 = list_of_stage0(fp)
  
  try:
    if i:
      for x in i:
        if x in globals().keys():
          for c in JOIN_HANDLERS:
            if hasattr(c, 'func_name') and c.func_name==x:
              JOIN_HANDLERS.remove(c)
          for c in MESSAGE_HANDLERS:
            if hasattr(c, 'func_name') and c.func_name==x:
              MESSAGE_HANDLERS.remove(c)
          for c in LEAVE_HANDLERS:
            if hasattr(c, 'func_name') and c.func_name==x:
              LEAVE_HANDLERS.remove(c)
          for c in PRESENCE_HANDLERS:
            if hasattr(c, 'func_name') and c.func_name==x:
              PRESENCE_HANDLERS.remove(c)
          for c in COMMAND_HANDLERS.keys():
            if hasattr(c, 'func_name') and c.func_name==x:
              del COMMAND_HANDLERS[x]
          del globals()[x]
  except: pass
  try:
    fp = file(fp)
    exec fp in globals()
    fp.close()
    reply(type,source,u'ok')
    if stage0:
      for x in stage0:
        if inspect.getargs(eval(x).func_code)[0]>0 and 'CLIENTS' in globals().keys():
          for c in CLIENTS:
            eval(x+'(\''+c+'\')')
        else:
          eval(x+'()')
  except:
    reply(type,source,unicode(traceback.format_exc()))

def hnd_deload_pl(t, s, p):
  if not p: return
  fp = 'plugins/' + p+'_plugin.py'
  if not os.path.exists(fp):
    fp = 'plugins/' + p+'.py'
  if not os.path.exists(fp):
    fp = 'plugins/' + p

  i = handlers_load_checker(fp)
  stage0 = list_of_stage0(fp)
  glist = [v for v in globals().keys() if v.count('_HANDLERS') or v=='COMMANDS']
  for x in i:
    for y in COMMAND_HANDLERS.keys():
      
      if hasattr(COMMAND_HANDLERS[y], 'func_name') and COMMAND_HANDLERS[y].func_name==x.strip():
        del COMMAND_HANDLERS[y]
        if y in COMMANDS.keys():
          del COMMANDS[y]
        
    if x in globals().keys():
      
      for var in glist:
        for c in globals()[var]:
          if hasattr(c, 'func_name') and c.func_name==x.strip():
            if isinstance(globals()[var], dict):
              del globals()[var][c]
            if isinstance(globals()[var], list):
              globals()[var].remove(c)
          if isinstance(c, basestring) and c==x:
            if isinstance(globals()[var], dict):
              del globals()[var][x]
            if isinstance(globals()[var], list):
              globals()[var].remove(x)
    del globals()[x]

  reply(t, s, u'Разгрузил плагин '+fp+u'\nВсего функций '+str(len(i)))

register_command_handler(hnd_deload_pl, 'deload', ['все'], 100, 'deload anywhere plugin', 'deload <names plugin>', ['deload admin'])        
        

def svn_update_plugin(t, s, p):
  if not p:
    reply(t, s, u'И какой мне плагин обновить?')
    return
  ss = [p]
  if p.count(' '):
    ss = p.split()
  if ss[0][-3:] != '.py':
    reply(t, s, u'Смотри помощь по команде!')
    return
  reply(t, s, u'Выбрано обновление плагина '+ss[0]+(u' до ревизии '+ss[1] if len(ss)>1 else ''))
  url = 'http://abyba.googlecode.com/svn/trunk/'+('/!svn/bc/'+ss[1]+'/trunk' if len(ss)>1 and ss[1].isdigit() else '')+'/plugins/'+ss[0]
  try: string = urllib.urlopen(url).read()
  except:
    reply(t, s, u'Бот не смог открыть адрес '+url)
    return
  if not re.findall('def (.*?)\(', string,  re.IGNORECASE):
    reply(t, s, u'Попытка чтения плагина завершилась ошибкой!')
    return
  write_file(os.path.join('plugins/',ss[0]),str(string))
  handler_pod_pl(t, s, ss[0])


register_command_handler(svn_update_plugin, 'обновиплаг', ['все'], 100, 'Обновляет плаг с свн', 'обновиплаг <plugin>', ['обновиплаг ibb_plugin.py','обновиплаг admin.py'])
  

def handlers_load_checker(fp):
  try:
    source = read_file(fp)
  except: return []
  list = re.findall('def (.*?)\(', source,  re.IGNORECASE)
  return list

def list_of_stage0(fp):
  try:
    source = read_file(fp)
  except: return []
  list = re.findall('[^#]register_stage0_init\((.*?)\)', source,  re.IGNORECASE)
  return list

register_command_handler(handler_pod_pl, 'load', ['все'], 99, 'load anywhere plugin', 'load <names plugin>', ['load admin'])

