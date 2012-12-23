#! /usr/bin/env python
# -*- coding: utf-8 -*-

#  Talisman core
#  pybot.py

# fix by 40tman


from __future__ import with_statement
import sys

import os
os.chdir(os.path.dirname(sys.argv[0]))

sys.path.insert(1, 'modules')
#sys.stdout=open('console.txt','w')

import warnings
warnings.filterwarnings('ignore', message='.*', category=UnicodeWarning)

import xmpp
import time
import datetime
import threading
import random
import types
import traceback
import codecs


################################################################################
GENERAL_CONFIG_FILE = 'config.list'
def GENERAL_CONFIG(name):
        try:
                fp = open(GENERAL_CONFIG_FILE, 'r')
                txt = fp.read()
                fp.close()
                k = txt.splitlines()
        except:
                print u'Error in config.list file!!!\n'
                time.sleep(1)
                return
        for x in k:
                s=x.split(u'=')
                if s[0].count(name):
                        in_put=s[1]
                        if in_put.count('#'):
                                in_put=in_put.split('#')[0]
                        answ=in_put.strip()
                        if name==u'ADMINS':
                                return answ.split(',')
                        else:
                                return answ
        return ''

CONNECT_SERVER = GENERAL_CONFIG('CONNECT_SERVER')
PORT = GENERAL_CONFIG('PORT')
JID = GENERAL_CONFIG('JID')
PASSWORD = GENERAL_CONFIG('PASSWORD')
RESOURCE = GENERAL_CONFIG('RESOURCE')

GROUPCHAT_CACHE_FILE = 'dynamic/chatrooms.list'
GLOBACCESS_FILE = 'dynamic/globaccess.cfg'
ACCBYCONF_FILE = 'dynamic/accbyconf.cfg'
PLUGIN_DIR = 'plugins'

DEFAULT_NICK = GENERAL_CONFIG('DEFAULT_NICK')
ADMINS = GENERAL_CONFIG('ADMINS')
ADMIN_PASSWORD = GENERAL_CONFIG('ADMIN_PASSWORD')

AUTO_RESTART = GENERAL_CONFIG('AUTO_RESTART')

PUBLIC_LOG_DIR = GENERAL_CONFIG('PUBLIC_LOG_DIR')
PRIVATE_LOG_DIR = GENERAL_CONFIG('PRIVATE_LOG_DIR')
AUTO_PUBLIC_COMOFF = GENERAL_CONFIG('AUTO_PUBLIC_COMOFF')
INVITE_JOIN = GENERAL_CONFIG('INVITE_JOIN')

ROLES={'none':0, 'visitor':0, 'participant':10, 'moderator':15}
AFFILIATIONS={'none':0, 'member':1, 'admin':5, 'owner':15}

LAST = {'c':'', 't':0, 'gch':{}}
INFO = {'start': 0, 'msg': 0, 'prs':0, 'iq':0, 'cmd':0, 'thr':0, 'itr':0}
BOT_VER = { 'botver': {'name': u'Talisman', 'ver': 'Mod based 86rev.', 'os': ''}}
################################################################################

COMMANDS = {}
MACROS = {}

GROUPCHATS = {}
NOACCESS = []

BOT_CMD={}

############ lists handlers ############
MESSAGE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []
IQ_HANDLERS = []
PRESENCE_HANDLERS = []
STAGE0_INIT =[]
STAGE1_INIT =[]
STAGE2_INIT =[]
INVITE_HANDLERS = []
SUBJECT_HANDLERS =[]
########################

COMMAND_HANDLERS = {}

GLOBACCESS = {}
ACCBYCONF = {}
ACCBYCONFFILE = {}

COMMOFF = {}
GREETZ={}

GCHCFGS={}

JCON = None

smph = threading.BoundedSemaphore(value=100)
mtx = threading.Lock()
wsmph = threading.BoundedSemaphore(value=1)
################################################################################

def initialize_file(filename, data=''):
	if not os.access(filename, os.F_OK):
		fp = file(filename, 'w')
		if data:
			fp.write(data)
		fp.close()

def read_file(filename):
	try:
                fp = file(filename)
                data = fp.read()
                fp.close()
                return data
        except:
                return str()

def write_file_gag(filename, data):
	mtx.acquire()
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
	mtx.release()

def db_file(filename, typ=dict):
        attr, i = {dict:'{}',list:'[]'}, None
        if not os.path.exists(filename):
                fp = file(filename, 'w')
                fp.write(attr[typ])
                fp.close()
        else:
                fp = read_file(filename)
                try: i=eval(fp)
                except: write_file(filename, attr[typ])
                if not isinstance(i, typ):
                        write_file(filename, attr[typ])

def write_file(filename, data):
        try:
                with wsmph:
                        write_file_gag(filename, data)
        except:
                pass

def check_file(gch='',file=''):
	pth,pthf='',''
	if gch:
		pthf='dynamic/'+gch+'/'+file
		pth='dynamic/'+gch
	else:
		pthf='dynamic/'+file
		pth='dynamic'
	if os.path.exists(pthf):
		return 1
	else:
		try:
			if not os.path.exists(pth):
				os.mkdir(pth,0755)
			if os.access(pthf, os.F_OK):
				fp = file(pthf, 'w')
			else:
				fp = open(pthf, 'w')
			fp.write('{}')
			fp.close()
			return 1
		except:
			return 0

################################################################################

def register_message_handler(instance):
	MESSAGE_HANDLERS.append(instance)
def register_outgoing_message_handler(instance):
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	JOIN_HANDLERS.append(instance)
def register_leave_handler(instance):
	LEAVE_HANDLERS.append(instance)
def register_iq_handler(instance):
	IQ_HANDLERS.append(instance)
def register_presence_handler(instance):
	PRESENCE_HANDLERS.append(instance)
def register_stage0_init(instance):
	STAGE0_INIT.append(instance)
def register_stage1_init(instance):
	STAGE1_INIT.append(instance)
def register_stage2_init(instance):
	STAGE2_INIT.append(instance)
def register_invite_handler(instance):
        INVITE_HANDLERS.append(instance)
def register_subject_handler(instance):
        SUBJECT_HANDLERS.append(instance)
        
def call_invite_handlers(msg):
        for handler in INVITE_HANDLERS:
		with smph:
			INFO['thr'] += 1
			try:
                                threading.Thread(None,handler,'invite'+str(INFO['thr']),(msg,)).start()
                        except:
                                pass

def call_subject_handlers(gch,nick,sub):
	for handler in SUBJECT_HANDLERS:
		with smph:
			INFO['thr'] += 1
			try:
                                threading.Thread(None,handler,'subject'+str(INFO['thr']),(gch,nick,sub,)).start()
                        except:
                                pass

def register_command_handler(instance, command, category=[], access=0, desc='', syntax='', examples=[]):
	command = command.decode('utf-8')
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

def call_message_handlers(raw, type, source, body):
	for handler in MESSAGE_HANDLERS:
                inmsg_hnd = handler
		try:
                        with smph:
                                INFO['thr'] += 1
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = 'inmsg%d.%s.%s' % (INFO['thr'],inmsg_hnd.func_name,st_time)
				thr = threading.Thread(None,inmsg_hnd,thr_name,(raw, type, source, body,))
				thr.start()
                except:
                        pass
                        
def call_outgoing_message_handlers(target, body, obody):
        for handler in OUTGOING_MESSAGE_HANDLERS:
                omsg_hnd = handler
                with smph:
                        try:
                                INFO['thr'] += 1
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = 'outmsg%d.%s.%s' % (INFO['thr'],omsg_hnd.func_name,st_time)
				thr = threading.Thread(None,omsg_hnd,thr_name,(target, body, obody,))
				thr.start()
			except:
                                pass

def call_subject_handler(groupchat,nick,body):
	for handler in SUBJECT_MESSAGE:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,handler,'subject'+str(INFO['thr']),(target, body, obody,)).start()
                        
def call_join_handlers(groupchat, nick, afl, role):
	for handler in JOIN_HANDLERS:
                join_hnd = handler
                with smph:
                        try:
                                INFO['thr'] += 1
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = 'join%d.%s.%s' % (INFO['thr'],join_hnd.func_name,st_time)
				thr = threading.Thread(None,join_hnd,thr_name,(groupchat, nick, afl, role,))
				thr.start()
			except:
                                pass
                        
def call_leave_handlers(groupchat, nick, reason, code):
	for handler in LEAVE_HANDLERS:
		try:
                        with smph:
                                INFO['thr'] += 1
                                threading.Thread(None,handler,'leave'+str(INFO['thr']),(groupchat, nick, reason, code,)).start()
                except:
                        pass
def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
                iq_hnd = handler
                INFO['thr'] += 1
		with smph:
                        try:
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = 'iq%d.%s.%s' % (INFO['thr'],iq_hnd.func_name,st_time)
				thr = threading.Thread(None,iq_hnd,thr_name,(iq,))
				thr.start()
			except:
                                pass
def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
                prs_hnd = handler
		with smph:
                        try:
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = 'prs%d.%s.%s' % (INFO['thr'],prs_hnd.func_name,st_time)
				thr = threading.Thread(None,prs_hnd,thr_name,(prs,))
				thr.start()
			except:
                                pass

CRASH_LAST = {}

def call_command_handlers(command, type, source, parameters, callee):
        if type=='public':
                if source[1] in BOT_CMD:
                        if BOT_CMD[source[1]]:
                                return
	real_access = COMMANDS[command]['access']
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source, real_access, source[1]):
                        cmd_hnd = COMMAND_HANDLERS[command]
                        try:
                                threading.Thread(None,hnd_bot_ping,'bot_ping'+str(INFO['thr']),(type,source)).start()
                                CRASH_LAST['cmd']=command
                        except:
                                pass
                        INFO['thr'] += 1
			try:
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
				thr_name = u'command%d.%s.%s' % (INFO['thr'],cmd_hnd.func_name,st_time)
				thr = threading.Thread(None,cmd_try,thr_name,(cmd_hnd, type, source, parameters,))
				thr.start()
			except: pass
		else:
			reply(type, source, u'недостаточно прав')

def cmd_try(cmd_hnd, type, source, parameters):
        try: cmd_hnd(type, source, parameters)
        except: reply(type, source, u'При выполнении команды зарегестрирована ошибка!')

################################################################################

def find_plugins():
	print '\nLOADING PLUGINS'
	valid_plugins = []
	invalid_plugins = []
	possibilities = os.listdir('plugins')
	for possibility in possibilities:
		if possibility[-3:].lower() == '.py':
			try:
				fp = file(PLUGIN_DIR + '/' + possibility)
				data = fp.read(23)
				if data == '#===istalismanplugin===':
					valid_plugins.append(possibility)
				else:
					invalid_plugins.append(possibility)
			except:
				pass
	if invalid_plugins:
		print '\nfailed to load',len(invalid_plugins),'plug-ins:'
		invalid_plugins.sort()
		invp=', '.join(invalid_plugins)
		print invp
		print 'plugins header is not corresponding\n'
	else:
		print '\nthere are not unloadable plug-ins'
	return valid_plugins



################################################################################

def load_plugins():
	plugins = find_plugins()
	for plugin in plugins:
		try:
			fp = file(PLUGIN_DIR + '/' + plugin)
			exec fp in globals()
			fp.close()
		except:
                        raise
	plugins.sort()
	print '\nloaded',len(plugins),'plug-ins:'
	loaded=', '.join(plugins)
	print loaded,'\n'

def get_gch_cfg(gch):
	cfgfile='dynamic/'+gch+'/config.cfg'
	try:
                if not check_file(gch,'config.cfg'):
                        print 'unable to create config file for new groupchat!'
                        raise
        except TypeError:
                pass
	try:
		cfg = eval(read_file(cfgfile))
		GCHCFGS[gch]=cfg
		LAST['gch'][gch]={}
	except:
		pass

def upkeep():
	tmr=threading.Timer(60, upkeep)
	tmr.start()
	sys.exc_clear()
	if os.name == 'nt':
		try:
			import msvcrt
			msvcrt.heapmin()
		except:
			pass
	import gc
	gc.collect()

################################################################################


def get_true_jid(jid):
	true_jid = ''
	
	if type(jid) is types.ListType:
		jid = jid[0]
	if type(jid) is types.InstanceType:
		jid = unicode(jid)
	stripped_jid = jid.split('/', 1)[0]
	resource = ''
	if len(jid.split('/', 1)) == 2:
		resource = jid.split('/', 1)[1]
	if GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			true_jid = unicode(GROUPCHATS[stripped_jid][resource]['jid']).split('/', 1)[0]
			
			if GROUPCHATS.has_key(true_jid):
				return unicode(GROUPCHATS[stripped_jid][resource]['jid'])
		else:
			true_jid = stripped_jid
	else:
		true_jid = stripped_jid
	return true_jid

GET_BOT_NICK = {}

def get_bot_nick(groupchat):
        global GET_BOT_NICK
        if not groupchat in GET_BOT_NICK:
                GET_BOT_NICK[groupchat]={}
                if check_file(groupchat,'bot.list'):
                        file='dynamic/'+groupchat+'/bot.list'
                        try:
                                gchdb = eval(read_file(file))
                        except:
                                return DEFAULT_NICK
                        if gchdb.has_key(groupchat) and gchdb[groupchat]['nick']:
                                GET_BOT_NICK[groupchat]=gchdb[groupchat]['nick']
                                return gchdb[groupchat]['nick']
                        else:
                                return DEFAULT_NICK
        else:
                if isinstance(GET_BOT_NICK[groupchat],dict):
                        return DEFAULT_NICK
                else:
                        return GET_BOT_NICK[groupchat]

def get_gch_info(gch, info):
	if check_file(gch,'bot.list'):
                file='dynamic/'+gch+'/bot.list'
		try:
                        gchdb = eval(read_file(file))
                except:
                        write_file(file,'{}')
                        gchdb = eval(read_file(file))
		if gchdb.has_key(gch):	return gchdb[gch].get(info)
		else:	return None
	else:
		print 'Error adding groupchat to groupchats list file!'

def add_gch(groupchat=None, nick=None, passw=None):
	if check_file(groupchat,'bot.list'):
                file='dynamic/'+groupchat+'/bot.list'
		try:
                        gchdb = eval(read_file(file))
                except:
                        write_file(file,'{}')
                        gchdb = eval(read_file(file))
		if not groupchat in gchdb:
			gchdb[groupchat] = groupchat
			gchdb[groupchat] = {}
			gchdb[groupchat]['nick'] = nick
			gchdb[groupchat]['passw'] = passw
		else:
			if nick and groupchat and passw:
				gchdb[groupchat]['nick'] = nick
				gchdb[groupchat]['passw'] = passw
			elif nick and groupchat:
				gchdb[groupchat]['nick'] = nick
			elif groupchat:
				del gchdb[groupchat]
			elif passw:
				gchdb[groupchat]['passw'] = passw
			else:
				return 0
		write_file(file, str(gchdb))
		return 1
	else:
		print 'Error adding groupchat to groupchats list file!'

def timeElapsed(time):
	minutes, seconds = divmod(time, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	months, days = divmod(days, 30)
	rep = u'%d сек' % (round(seconds))
	if time>=60: rep = u'%d мин %s' % (minutes, rep)
	if time>=3600: rep = u'%d час %s' % (hours, rep)
	if time>=86400: rep = u'%d дн %s' % (days, rep)
	if time>=2592000: rep = u'%d мес %s' % (months, rep)
	return rep

def change_bot_status(gch,status,show,auto=0):
	prs=xmpp.protocol.Presence(gch+'/'+get_bot_nick(gch))
	if status:
		prs.setStatus(status)
	if show:
		prs.setShow(show)
	JCON.send(prs)

################################################################################

def change_access_temp(gch, source, level=0):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	ACCBYCONF[gch][jid]=level

def change_access_perm(gch, source, level=None):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		pass
	temp_access = eval(read_file(ACCBYCONF_FILE))
	if not temp_access.has_key(gch):
		temp_access[gch] = gch
		temp_access[gch] = {}
	if not temp_access[gch].has_key(jid):
		temp_access[gch][jid]=jid
	if level:
		temp_access[gch][jid]=level
	else:
		del temp_access[gch][jid]
	write_file(ACCBYCONF_FILE, str(temp_access))
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	if level:
		ACCBYCONF[gch][jid]=level
	else:
		del ACCBYCONF[gch][jid]
	get_access_levels()

def change_access_perm_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	temp_access = eval(read_file(GLOBACCESS_FILE))
	if level:
		temp_access[jid] = level
	else:
		del temp_access[jid]
	write_file(GLOBACCESS_FILE, str(temp_access))
	get_access_levels()

def change_access_temp_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	if level:
		GLOBACCESS[jid] = level
	else:
		del GLOBACCESS[jid]


def user_level(source, gch):
	global ACCBYCONF
	global GLOBACCESS
	global ACCBYCONFFILE
	jid = get_true_jid(source)
	if GLOBACCESS.has_key(jid):
		return GLOBACCESS[jid]
	if ACCBYCONFFILE.has_key(gch):
		if ACCBYCONFFILE[gch].has_key(jid):
			return ACCBYCONFFILE[gch][jid]
	if ACCBYCONF.has_key(gch):
		if ACCBYCONF[gch].has_key(jid):
			return ACCBYCONF[gch][jid]
	return 0

def has_access(source, level, gch):
	jid = get_true_jid(source)
	if user_level(jid,gch) >= int(level):
		return 1
	return 0

def has_all_acess():
        MAS=[]
        txt=eval(read_file(GLOBACCESS_FILE))
        MAS=[x for x in txt if txt[x] in [100,'100']]
        return MAS

################################################################################

def join_groupchat(groupchat=None, nick=DEFAULT_NICK, passw=None):
	if not groupchat in GROUPCHATS:
		GROUPCHATS[groupchat] = {}
	if check_file(groupchat,'macros.txt'):
		pass
	else:
		print 'IO error when creating macros.txt for ',groupchat

	add_gch(groupchat, nick, passw)

	prs=xmpp.protocol.Presence(groupchat+'/'+nick)
	try:
                prs.setStatus(GCHCFGS[groupchat]['status']['status'])
                prs.setShow(GCHCFGS[groupchat]['status']['show'])
        except:
                pass
        pres=prs.setTag('x',namespace=xmpp.NS_MUC)
	pres.addChild('history',{'maxchars':'0'})
	if passw:
		pres.setTagData('password', passw)
	JCON.send(prs)

def leave_groupchat(groupchat,status=''):
	prs=xmpp.Presence(groupchat, 'unavailable')
	if status:
		prs.setStatus(status)
	JCON.send(prs)
	if GROUPCHATS.has_key(groupchat):
		del GROUPCHATS[groupchat]
		add_gch(groupchat)

def section(body, lenn, sys=0):
        rep=''
        k=' '
        if not body.count(' '):
                return body[:lenn]
        s=body.split(' ')
        if sys:
                if body.count('.'):
                        s=body.split('.')
                        k='.'
                if body.count('\n'):
                        s=body.split('\n')
                        k='\n'
        for x in s:
                if len(rep+k+x)<lenn:
                        rep+=k+x
                else:
                        break
        return rep

def msg(target, body):
        try: msg_try(target, body)
        except: pass

def msg_try(target, body):
	if not isinstance(body, unicode):
		body = body.decode('utf8', 'replace')
	obody=body
	if time.localtime()[1]==4 and time.localtime()[2]==1:
		body=remix_string(body)
	msg = xmpp.Message(target)
	if GROUPCHATS.has_key(target):
		msg.setType('groupchat')
		if len(body)>1000:
			body=body[:1000]+u' >>>>'
		msg.setBody(body.strip())
	else:
		msg.setType('chat')
		msg.setBody(body.strip())
	JCON.send(msg)
	call_outgoing_message_handlers(target, body, obody)



def reply(ltype, source, body):
        try: reply_try(ltype, source, body)
        except: pass

def reply_try(ltype, source, body):
    if not isinstance(body, unicode):
            body = body.decode('utf8', 'replace')
    body2 = None
    if len(body)>5000:
        n=2
        if len(body)>10000:
            n=len(body)/5000
        a = body
        body = section(body, 5000, 1)
        body = '[1/'+str(n)+'] '+body[:5000]
        body2 = a[len(body):]
        body2 = '[2/'+str(n)+'] '+section(body2, 5000, 1)
    for x in body:
        try:
            if ord(x)<32 and ord(x) not in [9, 10, 13]:
                    body = body.replace(x, str(ord(x)))
        except: pass
    if ltype == 'public':
        if len(body)>1000:
            msg(source[1], source[2]+u': '+section(body, 500)+u' >>> [смотри в привате!]')
            time.sleep(1.5)
            msg(source[1]+'/'+source[2], body[:5000])
        else:
                msg(source[1], source[2] + ': ' + body)
    elif ltype == 'private':
        if len(body)>5000:
            body=body[:5000]+'  >>>>>'
	msg(source[0], body)
    if body2: threading.Thread(None,reply,'reply_section_part2'+str(INFO['thr']),(ltype,source,body2)).start()

def isadmin(jid):
	if type(jid) is types.ListType:
		jid = jid[0]
	jid = str(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if stripped_jid in ADMINS:
		return 1
	elif GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			if string.split(str(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0] in ADMINS:
				return 1
	return 0

################################################################################
def findPresenceItem(node):
	for p in [x.getTag('item') for x in node.getTags('x',namespace=xmpp.NS_MUC_USER)]:
		if p != None:
			return p
	return None

def messageHnd(con, msg):
        try: bot_msg(con, msg)
        except: pass

def bot_msg(con, msg):
	msgtype = msg.getType()
	fromjid = msg.getFrom()
	try:
                INFO['msg'] += 1
                INFO['itr']+=sys.getsizeof(msg)
                if len(LOG_ST)>100:
                        LOG_ST.clear()
                LOG_ST[str(datetime.datetime.now())]=msg.__str__()
                if msgtype=='normal':
                        call_invite_handlers(msg)
                        print 'inv'
                if user_level(fromjid,fromjid.getStripped())==-100:
                        return
        except:
                pass
	if msg.timestamp:
		return
	body = msg.getBody()
	if msg.getTag('subject'):
                if time.time() - INFO['start']>60:
                        op = msg.getChildren()
                        for o in op:
                                if o.getName() =='subject':
                                        texts= o.getData()
                                        if fromjid.getResource():
                                                zj = fromjid.getResource()
                                        else:
                                                zj=''
                                        try:
                                                call_subject_handlers(fromjid.getStripped(),zj,texts)
                                        except:
                                                pass
                                        
	if body:
		body=body.strip()
	if not body:
		return
	if len(body)>2500:
		body=body[:2500]+u' >>>>'
	if msgtype == 'groupchat':
		mtype='public'
		if GROUPCHATS.has_key(fromjid.getStripped()) and GROUPCHATS[fromjid.getStripped()].has_key(fromjid.getResource()):
			GROUPCHATS[fromjid.getStripped()][fromjid.getResource()]['idle'] = time.time()
	elif msgtype == 'error':
		if msg.getErrorCode()=='500':
			time.sleep(0.6)
			JCON.send(xmpp.Message(fromjid, body, 'groupchat'))
		elif msg.getErrorCode()=='406':
			join_groupchat(fromjid.getStripped(), DEFAULT_NICK)
			time.sleep(0.6)
			JCON.send(xmpp.Message(fromjid, body, 'groupchat'))
		return
	else:
		mtype='private'
	call_message_handlers(msg, mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], body)

	bot_nick = get_bot_nick(fromjid.getStripped())
	if bot_nick == fromjid.getResource():
		return
	command,parameters,cbody,rcmd = '','','',''
	for x in [bot_nick+x for x in [':',',','>']]:
		body=body.replace(x,'')
	body=body.strip()
	if not body:
		return
	rcmd = body.split()[0].lower()
	if fromjid.getStripped() in COMMOFF and rcmd in COMMOFF[fromjid.getStripped()]:
		return
	cbody = body
	command=cbody.split()[0].lower()
	if cbody.count(' '):
		parameters = cbody[(cbody.find(' ') + 1):].strip()
	if command in COMMANDS:
		if fromjid.getStripped() in COMMOFF and command in COMMOFF[fromjid.getStripped()]:
			return
		else:
			call_command_handlers(command, mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], unicode(parameters), rcmd)
			INFO['cmd'] += 1
			LAST['t'] = time.time()
			LAST['c'] = command

ER_TIM=[]
RM_CONT={}
BOT_GET_ERRORCODE={}
			
def presenceHnd(con, prs):
        try: bot_prs(con, prs)
        except: pass

def bot_prs(con, prs):
	fromjid = prs.getFrom()
	try:
                INFO['itr']+=sys.getsizeof(prs)
                LOG_ST[str(datetime.datetime.now())]=prs.__str__()
                if user_level(fromjid,fromjid.getStripped())==-100:
                        return
        except: pass
	ptype = prs.getType()
	groupchat = fromjid.getStripped()
	nick = fromjid.getResource()
	item = findPresenceItem(prs)
	INFO['prs'] += 1

	if ptype == 'subscribe':
		JCON.send(xmpp.protocol.Presence(to=fromjid, typ='subscribed'))
		for x in ADMINS:
                        msg(x,groupchat[:45]+u' добавился в ростер')
	elif ptype == 'unsubscribe':
		JCON.send(xmpp.protocol.Presence(to=fromjid, typ='unsubscribed'))

	if groupchat not in GROUPCHATS and groupchat in NOACCESS:
                if not groupchat.count(u'conference.') and not groupchat.count(u'muc.') and not groupchat.count(u'chat.'):
                        return
                if ptype == 'available' or ptype == None:
                        jid = item['jid']
			afl=prs.getAffiliation()
			role=prs.getRole()
			if not jid: return
                        else:
                                leave_groupchat(groupchat)
                                time.sleep(2)
                                join_groupchat(groupchat)

	if groupchat in GROUPCHATS:
		if ptype == 'unavailable':
			if item:
                                jid = item['jid']
                                if not jid:
                                        jid=''
                        else:
                                jid=groupchat+'/'+nick
			scode = prs.getStatusCode()
			reason = prs.getReason() or prs.getStatus()
			if scode:
                                if scode=='301' or scode=='307':
                                        if nick==get_bot_nick(groupchat):
                                                rep=u'забанили'
                                                if scode=='307':
                                                        rep=u'кикнули'
                                                rs='None'
                                                if reason:
                                                        rs=reason
                                                adm_msg(u'бота '+rep+u' в '+groupchat+u'\nрезон: '+rs)
			if scode == '303':
				newnick = prs.getNick()
				GROUPCHATS[groupchat][newnick] = {'jid': jid, 'idle': time.time(), 'joined': GROUPCHATS[groupchat][nick]['joined'], 'ishere': 1}
				for x in ['idle','status','stmsg']:
					try:
						del GROUPCHATS[groupchat][nick][x]
						if GROUPCHATS[groupchat][nick]['ishere']==1:
							GROUPCHATS[groupchat][nick]['ishere']=0
					except:
						pass
			else:
				for x in ['idle','status','stmsg','joined']:
					try:
						del GROUPCHATS[groupchat][nick][x]
						if GROUPCHATS[groupchat][nick]['ishere']==1:
							GROUPCHATS[groupchat][nick]['ishere']=0
					except:
						pass
				call_leave_handlers(groupchat, nick, reason, scode)
		elif ptype == 'available' or ptype == None:
                        try:
                                if groupchat in RM_CONT:
                                        del RM_CONT[groupchat]
                        except:
                                pass
			jid = item['jid']
			if not jid:
                                jid=groupchat+'/'+nick
                        afl=prs.getAffiliation()
			role=prs.getRole()
			if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['jid']==jid and GROUPCHATS[groupchat][nick]['ishere']==1:
					pass
			else:
                                GROUPCHATS[groupchat][nick] = {'jid': jid, 'idle': time.time(), 'joined': time.time(), 'ishere': 1, 'status': '', 'stmsg': ''}
                                if role=='moderator' or user_level(jid,groupchat)>=15:
                                        GROUPCHATS[groupchat][nick]['ismoder'] = 1
                                else:
                                        GROUPCHATS[groupchat][nick]['ismoder'] = 0
                                call_join_handlers(groupchat, nick, afl, role)
		elif ptype == 'error':
			ecode = prs.getErrorCode()
			if ecode:
                                info=''
                                ERR={'404':u'Не найдено(не верный адрес конференции либо сервер упал)','409':u'Конфликт','401':u'Не авторизирован(конфа на пароле либо работает капча)','403':u'Запрещено(Бан)'}
                                if ecode in ERR:
                                        info=ERR[ecode]
                                if not groupchat in BOT_GET_ERRORCODE.keys():
                                        BOT_GET_ERRORCODE[groupchat]={}
                                        adm_msg(u'Немогу зайти в '+groupchat+u': \nКод ошибки: '+unicode(ecode)+' '+info)
				if ecode == '409':
					join_groupchat(groupchat, nick + '_')
					try:
                                                GET_BOT_NICK[groupchat]=nick+'_'
                                        except:
                                                pass
				elif ecode == '404':
                                        RM_CONT[groupchat]={'t':time.time(),'nick':get_bot_nick(groupchat)}
				elif ecode in ['401','403','405',]:
					try:
                                                del GROUPCHATS[groupchat]
                                                import shutil
                                                shutil.rmtree('dynamic/'+groupchat)
                                        except: pass
				elif ecode == '503':
                                        if threading.activeCount()>12:
                                                return
                                        tr=random.randrange(50, 70)
                                        time.sleep(tr)
                                        join_groupchat(groupchat, get_bot_nick(groupchat))
		else:
			pass
		call_presence_handlers(prs)

AL7={}

def adm_msg(msg):
        try: SP=[x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]
        except: SP=ADMINS
        for x in SP:
                if x not in AL7:
                        AL7[x]={'t':time.time(),'m':msg}
                        try:
                                JCON.send(xmpp.Message(x,msg,'chat'))
                        except:
                                pass
                else:
                        if time.time()-AL7[x]['t']<15:
                                return
                        if msg==AL7[x]['m']:
                                return
                        AL7[x]['t']=time.time()
                        AL7[x]['m']=msg
                        try:
                                JCON.send(xmpp.Message(x,msg,'chat'))
                        except:
                                pass
                        
def iqHnd(con, iq):
        try: bot_iq(con, iq)
        except: pass

def bot_iq(con, iq):
        global JCON, BOT_VER, LOG_ST
	fromjid = iq.getFrom()
	try:
                INFO['itr']+=sys.getsizeof(iq)
                LOG_ST[str(datetime.datetime.now())]=iq.__str__()
                if user_level(fromjid,fromjid.getStripped())==-100:
                        return
        except: pass
	if not iq.getType() == 'error':
		if iq.getTags('query', {}, xmpp.NS_VERSION):
			if not BOT_VER['botver']['os']:
				osver=''
				#if os.name=='nt':
				##	osname=os.popen("ver")
				#	osver=osname.read().strip().decode('cp866')+'\n'
				#	osname.close()
				#else:
				#	osname=os.popen("uname -sr", 'r')
				#	osver=osname.read().strip()+'\n'
				#	osname.close()
				pyver = 'some OS'
				BOT_VER['botver']['os'] = pyver
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setTagData('name', BOT_VER['botver']['name'])
			query.setTagData('version', BOT_VER['botver']['ver'])
			query.setTagData('os', BOT_VER['botver']['os'])
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('time', {}, 'urn:xmpp:time'):
			tzo=(lambda tup: tup[0]+"%02d:"%tup[1]+"%02d"%tup[2])((lambda t: tuple(['+' if t<0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
			utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
			result = iq.buildReply('result')
			reply=result.addChild('time', {}, [], 'urn:xmpp:time')
			reply.setTagData('tzo', tzo)
			reply.setTagData('utc', utc)
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('query', {}, xmpp.NS_DISCO_INFO):
			items=[]
			ids=[]
			ids.append({'category':'client','type':'bot','name':'Talisman MOD'})
			features=[xmpp.NS_DISCO_INFO,xmpp.NS_DISCO_ITEMS,xmpp.NS_MUC,xmpp.NS_IBB,xmpp.NS_FILE,xmpp.NS_SI,'http://jabber.org/protocol/feature-neg','http://jabber.org/protocol/si/profile/file-transfer','jabber:iq:inband','urn:xmpp:time','urn:xmpp:ping',xmpp.NS_VERSION,xmpp.NS_PRIVACY,xmpp.NS_ROSTER,xmpp.NS_VCARD,xmpp.NS_DATA,xmpp.NS_LAST,xmpp.NS_COMMANDS,'msglog','fullunicode',xmpp.NS_TIME]
			info={'ids':ids,'features':features}
			b=xmpp.browser.Browser()
			b.PlugIn(JCON)
			b.setDiscoHandler({'items':items,'info':info})
		elif iq.getTags('query', {}, xmpp.NS_LAST):
			last=time.time()-LAST['t']
			result = iq.buildReply('result')
			query = result.getTag('query')
			query.setAttr('seconds',int(last))
			query.setData(LAST['c'])
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('query', {}, xmpp.NS_TIME):
			timedisp=time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.localtime())
			timetz=time.strftime("%Z", time.localtime())
			timeutc=time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
			result = xmpp.Iq('result')
			result.setTo(fromjid)
			result.setID(iq.getID())
			query = result.addChild('query', {}, [], 'jabber:iq:time')
			query.setTagData('utc', timeutc)
			query.setTagData('display', timedisp)
			JCON.send(result)
			raise xmpp.NodeProcessed
		elif iq.getTags('ping', {}, 'urn:xmpp:ping'):
			result = xmpp.Iq('result')
			result.setTo(iq.getFrom())
			result.setID(iq.getID())
			JCON.send(result)
			raise xmpp.NodeProcessed
	call_iq_handlers(iq)
	INFO['iq'] += 1

def dcHnd():
	print 'DISCONNECTED'
	logger_stanza()
	if AUTO_RESTART:
                try:
                        if check_file(file='lastconnect.txt'):
                                file='dynamic/lastconnect.txt'
                                fp=open(file,'r')
                                txt=eval(fp.read())
                                fp.close()
                                if 'LAST' in txt:
                                        if not txt['LAST']['time']:
                                                txt['LAST']['time']=time.time()
                                                write_file(file,str(txt))
                                        else:
                                                if time.time() - txt['LAST']['time']<70:
                                                        if txt['LAST']['n']>2:
                                                                txt['LAST']['n']=0
                                                                write_file(file,str(txt))
                                                                os.abort()
                                                        else:
                                                                txt['LAST']['n']+=1
                                                                write_file(file,str(txt))
                                        txt['LAST']['time']=time.time()
                                        write_file(file,str(txt))
                except: pass
		print 'WAITING FOR RESTART...'
		time.sleep(10)
		print 'RESTARTING'
		os.execl(sys.executable, sys.executable, sys.argv[0])
	else: sys.exit(0)

LOG_ST = {}

def logger_stanza():
        data=''
        try:
                global LOG_ST
                txt=open('logger.txt','w')
                txt.write(str(LOG_ST))
                txt.close()
        except: pass


def load_rooms():
        rm=0
	dir_chat=os.listdir('dynamic')
	for x in dir_chat:
                try:
                        if os.path.isdir('dynamic/'+x):
                                file='dynamic/'+x+'/bot.list'
                                if os.path.exists(file):
                                        txt=eval(read_file(file))
                                        if txt:
                                                rm+=1
                                                get_gch_cfg(x)
                                                for process in STAGE1_INIT:
                                                        with smph:
                                                                INFO['thr'] += 1
                                                                threading.Thread(None,process,'stage1_init'+str(INFO['thr']),(x,)).start()
                                                write_file('dynamic/'+x+'/config.cfg', str(GCHCFGS[x]))
                                                with smph:
                                                        INFO['thr'] += 1
                                                        threading.Thread(None,join_groupchat,'join_gch'+str(INFO['thr']),(x,txt[x]['nick'] if txt[x]['nick'] else DEFAULT_NICK,txt[x]['passw'])).start()
                except: pass
        print "Ok. Now I'm ready to work!\n"



################################################################################

def start():
	try:
		(USERNAME, SERVER) = JID.split("/")[0].split("@")
	except:
		print 'Wrong, wrong JID %s' % JID
		os.abort()
	print '\n...---===STARTING BOT===---...\n'
	global JCON
	JCON = xmpp.Client(server=SERVER, port=PORT, debug=[])

	load_plugins()

	print 'Waiting For Connection...\n'

	con=JCON.connect(server=(CONNECT_SERVER, PORT), secure=0,use_srv=True)
	if not con:
		print 'COULDN\'T CONNECT\nSleep for 30 seconds'
		time.sleep(30)
		os.execl(sys.executable, sys.executable, sys.argv[0])
	else:
		print 'Connection Established'

	print 'Using',JCON.isConnected()

	print '\nWaiting For Authentication...'

	auth=JCON.auth(USERNAME, PASSWORD, RESOURCE)
	if not auth:
		print 'Auth Error. Incorrect login/password?\nError: ', JCON.lastErr, JCON.lastErrCode
		time.sleep(5)
		os.abort()
	else:
		print 'Logged In'
	if auth!='sasl':
		print 'Warning: unable to perform SASL auth. Old authentication method used!'

	for process in STAGE0_INIT:
		with smph:
			INFO['thr'] += 1
			threading.Thread(None,process,'stage0_init'+str(INFO['thr'])).start()

	JCON.RegisterHandler('message', messageHnd)
	JCON.RegisterHandler('presence', presenceHnd)
	JCON.RegisterHandler('iq', iqHnd)
	JCON.RegisterDisconnectHandler(dcHnd)
	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)
	print 'Handlers Registered'

	#R=JCON.getRoster()
	JCON.sendInitPresence()
	time.sleep(5)
	load_rooms()
#	load_plugins()


	INFO['start'] = time.time()
	upkeep()
	for process in STAGE2_INIT:
		with smph:
			INFO['thr'] += 1
		threading.Thread(None,process,'stage2_init'+str(INFO['thr'])).start()
	while True:
                try: JCON.Process(8)
                except xmpp.Conflict:
                        print 'CONFLICT!\n'
                        os.abort()
                #except xmpp.StreamError: pass
                except xmpp.simplexml.xml.parsers.expat.ExpatError:
                        if JCON.isConnected():
                                pass
                        else:
                                raise
		

if __name__ == "__main__":
	try:
                start()
	except KeyboardInterrupt:
		print '\nINTERUPT (Ctrl+C)'
		prs=xmpp.Presence(typ='unavailable')
		prs.setStatus(u'got Ctrl-C -> shutdown')
		JCON.send(prs)
		time.sleep(2)
		print 'DISCONNECTED'
		print '\n...---===BOT STOPPED===---...\n'
		sys.exit(0)
	except Exception, err:
                if JCON.isConnected():
                        for x in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
                                try:
                                        exc=traceback.format_exc()
                                        if not isinstance(exc, unicode):
                                                exc = exc.decode('utf8', 'replace')
                                        JCON.send(xmpp.Message(x,u'Возможен дисконнект из-за ошибки в Main:\n'+exc,'chat'))
                                        traceback.print_exc()
                                except:
                                        traceback.print_exc()
                        prs=xmpp.Presence(typ='unavailable')
                        prs.setStatus(u'Отановка бота из-за неустранимой ошибки!')
                        JCON.send(prs)
                        logger_stanza()
                        os.execl(sys.executable, sys.executable, sys.argv[0])
                else:
                        traceback.print_exc()
                        logger_stanza()
                        os.execl(sys.executable, sys.executable, sys.argv[0])
