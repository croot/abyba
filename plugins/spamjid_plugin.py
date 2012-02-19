#===istalismanplugin===
# -*- coding: utf-8 -*-

LASTSPAM1 = {}

SP_STOP_TIM = {}


def generate_iq(_len = None, sg = None):
  if sg == None:
    sg = 'aoeuizxcvb_nmsdfghjklqwrtyp1234567890'
  if _len == None:
    _len = random.Random().randint(1, 100)
  s = ''
  l = len(sg)
  while _len > 0:
    s += sg[random.Random().randint(0, l - 1)]
    _len -= 1
  return s


    
def handler_spamjid_go(type,source,parameters):
  if globals().has_key('JID'):
    if parameters.lower()==JID:
      return
  if parameters.lower() in [x for x in GLOBACCESS.keys() if GLOBACCESS[x] in [100]]:
    reply(type, source, u'фигушки!')
    return
  acc=int(user_level(source[1]+'/'+source[2], source[1]))
  jid=get_true_jid(source[1]+'/'+source[2])
  s , n = parameters.split(), 0
  if parameters.count(' ')>0:
    n = int(s[1])
    if acc<100:
      if n>1:
        reply(type,source,u'с доступом меньше 100 разрешено количество 1!')
        return
  if parameters.count(' ')==0:
    n=1
  if n>100:
    reply(type,source,u'100-max.')
    return
  if not LASTSPAM1.has_key(jid):
    LASTSPAM1[jid] = {'timesend':time.time()}
  else:
    if acc<100 and time.time() - LASTSPAM1[jid]['timesend'] <= 60:
      reply(type,source,u'лимит минута!')
      return
    else:
      LASTSPAM1[jid]['timesend'] = time.time()
  reply(type,source,'Ok')
  p= s[0]
  n=str(n)
  try: spame_jid_log(jid,parameters)
  except: pass
  sh = '%s %s %s' % (os.path.join(os.getcwd(),'plugins/spamjid_shell.py'),p,n)
  if os.name=='posix':
    i=os.popen('python '+sh.encode('utf8'))
    reply(type, source, i.read()[:500])
  if os.name=='nt':
    i=os.popen('%s' % (sh.encode('utf8')))
    reply(type, source,i.read().decode('cp866')[:500])
  i.close
  

def spam_serv(type, source, parameters):
  SPAMS = 'dynamic/spamserv.txt'
  dcc = eval(read_file(SPAMS))
  if parameters :
    if parameters in dcc:
      dcc.remove(parameters)
      write_file(SPAMS,str(dcc))
      reply(type,source,parameters+u' удален!')
    else:
      dcc.append(parameters)
      write_file(SPAMS,str(dcc))
      reply(type,source,parameters+u' добавлен!')
  else:
    reply(type,source,u'ты что-то хотел добавить?')

def spame_jid_log(jid,parameters):
  (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
  if not os.path.exists(PUBLIC_LOG_DIR+'/spamjid/'+str(month)):
    os.makedirs(PUBLIC_LOG_DIR+'/spamjid/'+str(month))
  tm=str(hour)+':'+str(minute)+':'+str(second)
  fName='%s/%s/%s.html'%(PUBLIC_LOG_DIR+'/spamjid',month,day)
  try: open(fName)
  except:
    open(fName,'w').write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="ru-RU" lang="ru-RU" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>logs for spamjid command</title>
    </head>
    <body>
<table border="1"><tr><th>time</th><th>who</th><th>text</th></tr>
""")
  text='<pre>%s</pre>'%parameters
  open(fName,'a').write((u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,jid,parameters)).encode('utf-8'))

register_command_handler(handler_spamjid_go, 'спамжид', ['все'], 30, 'регистрирует отдельного бота и спамит с него на указанную учетку 10 минут.', 'спамжид <jid> <количество_ботов>', ['спамжид 40tman@jabber.perm.ru 10'])
register_command_handler(spam_serv, 'спамжид_серв', ['все'], 100, 'Удаляет/добавляет сервер для спама на jid', 'спамжид_серв <сервер>', ['спамжид_серв aqq.eu'])
