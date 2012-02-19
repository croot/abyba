#===istalismanplugin===
# -*- coding: utf-8 -*-

import sys

LAST_AERR = {}

ADMIN_ERR = []

ERR_L = {'t':0,'m':[]}

class err:
        def write(self, text):
                h=u'Хьюстон, у нас проблемы: \n'
                if JCON.isConnected():
                        if text.isspace():
                                return
                        err_write(text)
                        if time.time() - globals()['ERR_L']['t']>2:
                                globals()['ERR_L']['m']=[]
                        globals()['ERR_L']['m'].append(text)
                        globals()['ERR_L']['t']=time.time()
                        ADM=has_all_acess_err()
                        print u'Registered some ERROR, look at err.html!'
                        for x in ADM:
                                if not x in LAST_AERR:
                                        LAST_AERR[x]={'time':time.time()}
                                else:
                                        if time.time() - LAST_AERR[x]['time']<60:
                                                return
                                        else:
                                                LAST_AERR[x]['time']=time.time()
                                if not '1' in ADMIN_ERR:
                                        return
                                try:
                                        if not isinstance(text, unicode):
                                                text = text.decode('utf8', 'replace')
                                        JCON.send(xmpp.Message(x,h+text[:1300],'chat'))
                                        pass
                                except:
                                        text=text.split(':')[0]
                                        msg(x,h+text)
                                        pass
                else:
                        print text

sys.stderr = err()

def err_write(text):
        try: hnd_err_add(text)
        except: pass

def hnd_err_add(text):
  (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
  tm=str(hour)+':'+str(minute)+':'+str(second)
  data=str(year)+':'+str(month)+':'+str(day)
  fName='err.html'
  if os.path.exists(fName) and os.path.getsize(fName)>500000:
          os.remove(fName)
  try: open(fName)
  except:
    open(fName,'w').write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="ru-RU" lang="ru-RU" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>error log</title>
    </head>
    <body>
""")
  open(fName,'a').write(("%s[%s]:<br />%s<br />"%(data,tm,text)))

def err_load():
        if check_file('err','err.txt'):
                txt=eval(read_file('dynamic/err/err.txt'))
                if txt:
                        if '1' in txt:
                                ADMIN_ERR.append('1')

def handler_er_wrk(type,source,parameters):
        if check_file('err','err.txt'):
                txt=eval(read_file('dynamic/err/err.txt'))
                if not '1' in txt:
                        ADMIN_ERR.append('1')
                        txt['1']={}
                        write_file('dynamic/err/err.txt', str(txt))
                        reply(type,source,u'включил оповещение об ошибках')
                        return
                else:
                        write_file('dynamic/err/err.txt', '{}')
                        ADMIN_ERR.remove('1')
                        reply(type,source,u'отключил оповещение об ошибках')

def hand_err_lshow(type,source,parameters):
        rep=''
        if not ERR_L['m']:
                reply(type,source,u'пусто')
                return
        ltim=int(time.time() - ERR_L['t'])
        tim = timeElapsed(ltim)
        i=u'Последнее исключение зарегестрировано '+tim+u' назад:\n'
        for x in ERR_L['m']:
                rep+=x
        reply(type,source,i+rep[:1300])

def has_all_acess_err():
        MAS=[]
        txt=eval(read_file(GLOBACCESS_FILE))
        for x in txt:
                if txt[x]:
                        if txt[x]=='100' or txt[x]==100:
                                MAS.append(x)
        return MAS
                                
register_stage0_init(err_load)
register_command_handler(handler_er_wrk, '!ошибки', ['суперадмин','все'], 100, 'включает/откл. оповещение об ошибках бота', '!ошибки', ['!ошибки'])
register_command_handler(hand_err_lshow, '!ошибки_лог', ['суперадмин','все'], 100, 'покажет последнее исключение', '!ошибки_лог', ['!ошибки_лог'])

