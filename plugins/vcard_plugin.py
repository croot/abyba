#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  vcard_plugin.py

# Modifications Evgеn


vcard_pending=[]
IUSR={}
IUSR_LAST={}

def handler_vcardget(type, source, parameters):
        sp='0'
        hnd_getvcard(type, source, parameters, sp)

def hnd_getvcard(type, source, parameters, sp):
	vcard_iq = xmpp.Iq('get')
	id='vcard'+str(random.randrange(1000, 9999))
	globals()['vcard_pending'].append(id)
	vcard_iq.setID(id)
	vcard_iq.addChild('vCard', {}, [], 'vcard-temp');
	rjid = get_true_jid(source[1]+'/'+source[2])
	nicks={}
	nick=''
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			nick = parameters.strip()
			if not nick in nicks:
				vcard_iq.setTo(nick)
			else:
				if GROUPCHATS[source[1]][nick]['ishere']==0:
					if sp!='1':
                                                reply(type, source, u'а он тут? :-O')
                                                return				
				jid=source[1]+'/'+nick
				vcard_iq.setTo(jid)
		else:
                       vcard_iq.setTo(parameters) 
                        
	else:
		jid=source[1]+'/'+source[2]
		vcard_iq.setTo(jid)
		nick=''
	JCON.SendAndCallForResponse(vcard_iq, handler_vcardget_answ, {'type': type, 'source': source, 'nick': nick, 'sp': sp, 'rjid': rjid})
		

def handler_vcardget_answ(coze, res, type, source, nick, sp, rjid):
        try:
                handler_vcardget_answ_try(coze, res, type, source, nick, sp, rjid)
        except:
                pass

def handler_vcardget_answ_try(coze, res, type, source, nick, sp, rjid):
	qw=unicode(res)
	id=res.getID()
	if id in globals()['vcard_pending']:
		globals()['vcard_pending'].remove(id)
	else:
		print 'ooops!'
		return
	rep =''
	arep=u'Инфо из Vcard '+nick[:19]+':\n'
	if res:
		if res.getType()=='error':
			if not nick:
                                if sp!='1':
                                        reply(type,source,u'хехе, твой клиент ничего не знает про вкарды')
                                        return
                                else:
                                        msg(source[1],arep+u'его клиент не поддерживает vcard')
                                        return
			else:
                                if sp!='1':
                                        reply(type,source,u'хехе, его клиент ничего не знает про вкарды')
                                        return
                                else:
                                        msg(source[1],arep+u'его клиент не поддерживает vcard')
                                        if 'vcheck' in IUSR[source[1]]:
                                                visitor_vcheck(source[1], source[2], 'visitor')
                                                msg(source[1]+'/'+source[2],u'твой клиент не поддерживает vcard,голос проси у админов!')
                                        return
		elif res.getType() == 'result':
                        print res.getTagAttr('PHOTO','BINVAL')
			nickname,url,email,desc,bday,orgname,orgunit,title,gender,given,family,country,pcode,region,locality,street,country2,pcode2,region2,locality2,street2,number,number2,number3,number4,number5,name = '','','','','','','','','','','','','','','','','','','','','','','','','','',''
			if res.getChildren():
				props = res.getChildren()[0].getChildren()
			else:
				if not nick:
					reply(type,source,u'вкард заполни сначала')
					return
				else:
                                        if sp!='1':
                                                reply(type,source,u'передай ему, чтобы он свой вкард сначала заполнил')
                                                return
                                        else:
                                                msg(source[1],arep+u'vcard не заполнен')
                                                if 'vcheck' in IUSR[source[1]]:
                                                        visitor_vcheck(source[1], source[2], 'visitor')
                                                        msg(source[1]+'/'+source[2],u'Заполни vCard и перезайди')
                                                iusr_append(source[1],rjid)
                                                iusr_load(source[1])
                                                return
			for p in props:
				if p.getName() == 'NICKNAME':
					nickname = p.getData()
					nickname = nickname.strip()
				if p.getName() == 'FN':
					name = p.getData()
					name = name.strip()
				if p.getName() == 'BDAY':
					bday = p.getData()
					bday = bday.strip()
				if p.getName() == 'URL':
					url = p.getData()
					url = url.strip()
				if p.getName() == 'EMAIL':
					email = p.getData()
					email = email.strip()
				if p.getName() == 'GENDER':
					gender = p.getData()
					gender = gender.strip()
				if p.getName() == 'DESC':
					desc = p.getData()
					desc = desc.strip()
				if p.getName() == 'TITLE':
					title = p.getData()
					title = title.strip()
			if qw.count('<GIVEN>')>=1:
				given = qw.replace('</GIVEN>', '<GIVEN>')
				given = given.split('<GIVEN>')
				given = given[1]
				given = given.replace('&lt;', '<')
				given = given.replace('&amp;', '&')
				given = given.replace('&quot;', '"')
				given = given.replace('&gt;', '>')
				given = given.strip()
			if qw.count('<FAMILY>')>=1:
				family = qw.replace('</FAMILY>', '<FAMILY>')
				family = family.split('<FAMILY>')
				family = family[1]
				family = family.replace('&lt;', '<')
				family = family.replace('&amp;', '&')
				family = family.replace('&quot;', '"')
				family = family.replace('&gt;', '>')
				family = family.strip()
			if qw.count('<ADR>')>=1:
				ADR = qw.split('<ADR>')
				if len(ADR)>=2:
					ADR = ADR[1]
					if ADR.count('<PCODE>')>=1:
						pcode = ADR.replace('</PCODE>', '<PCODE>')
						pcode = pcode.split('<PCODE>')
						pcode = pcode[1] # индекс
						pcode = pcode.replace('&lt;', '<')
						pcode = pcode.replace('&amp;', '&')
						pcode = pcode.replace('&quot;', '"')
						pcode = pcode.replace('&gt;', '>')
						pcode = pcode.strip()
					if ADR.count('<COUNTRY>')>=1:
						country = ADR.replace('</COUNTRY>', '<COUNTRY>')
						country = country.split('<COUNTRY>')
						country = country[1] # страна
						country = country.replace('&lt;', '<')
						country = country.replace('&amp;', '&')
						country = country.replace('&quot;', '"')
						country = country.replace('&gt;', '>')
						country = country.strip()
					if ADR.count('<LOCALITY>')>=1:
						locality = ADR.replace('</LOCALITY>', '<LOCALITY>')
						locality = locality.split('<LOCALITY>')
						locality = locality[1] # город
						locality = locality.replace('&lt;', '<')
						locality = locality.replace('&amp;', '&')
						locality = locality.replace('&quot;', '"')
						locality = locality.replace('&gt;', '>')
						locality = locality.strip()
					if ADR.count('<REGION>')>=1:
						region = ADR.replace('</REGION>', '<REGION>')
						region = region.split('<REGION>')
						region = region[1] # регион
						region = region.replace('&lt;', '<')
						region = region.replace('&amp;', '&')
						region = region.replace('&quot;', '"')
						region = region.replace('&gt;', '>')
						region = region.strip()
					if ADR.count('<STREET>')>=1:
						street = ADR.replace('</STREET>', '<STREET>')
						street = street.split('<STREET>')
						street = street[1] # улица
						street = street.replace('&lt;', '<')
						street = street.replace('&amp;', '&')
						street = street.replace('&quot;', '"')
						street = street.replace('&gt;', '>')
						street = street.strip()
			if qw.count('<ADR>')>=1:
				ADR2 = qw.split('<ADR>')
				if len(ADR2)>=3:
					ADR2 = ADR2[2]
					if ADR2.count('<PCODE>')>=1:
						pcode2 = ADR2.replace('</PCODE>', '<PCODE>')
						pcode2 = pcode2.split('<PCODE>')
						pcode2 = pcode2[1] # индекс работы
						pcode2 = pcode2.replace('&lt;', '<')
						pcode2 = pcode2.replace('&amp;', '&')
						pcode2 = pcode2.replace('&quot;', '"')
						pcode2 = pcode2.replace('&gt;', '>')
						pcode2 = pcode2.strip()
					if ADR2.count('<COUNTRY>')>=1:
						country2 = ADR2.replace('</COUNTRY>', '<COUNTRY>')
						country2 = country2.split('<COUNTRY>')
						country2 = country2[1] # страна работы
						country2 = country2.replace('&lt;', '<')
						country2 = country2.replace('&amp;', '&')
						country2 = country2.replace('&quot;', '"')
						country2 = country2.replace('&gt;', '>')
						country2 = country2.strip()
					if ADR2.count('<LOCALITY>')>=1:
						locality2 = ADR2.replace('</LOCALITY>', '<LOCALITY>')
						locality2 = locality2.split('<LOCALITY>')
						locality2 = locality2[1] # город работы
						locality2 = locality2.replace('&lt;', '<')
						locality2 = locality2.replace('&amp;', '&')
						locality2 = locality2.replace('&quot;', '"')
						locality2 = locality2.replace('&gt;', '>')
						locality2 = locality2.strip()
					if ADR2.count('<REGION>')>=1:
						region2 = ADR2.replace('</REGION>', '<REGION>')
						region2 = region2.split('<REGION>')
						region2 = region2[1] # регион работы
						region2 = region2.replace('&lt;', '<')
						region2 = region2.replace('&amp;', '&')
						region2 = region2.replace('&quot;', '"')
						region2 = region2.replace('&gt;', '>')
						region2 = region2.strip()
					if ADR2.count('<STREET>')>=1:
						street2 = ADR2.replace('</STREET>', '<STREET>')
						street2 = street2.split('<STREET>')
						street2 = street2[1] # улица работы
						street2 = street2.replace('&lt;', '<')
						street2 = street2.replace('&amp;', '&')
						street2 = street2.replace('&quot;', '"')
						street2 = street2.replace('&gt;', '>')
						street2 = street2.strip()
			if qw.count('<ORGNAME>')>=1:
				orgname = qw.replace('</ORGNAME>', '<ORGNAME>')
				orgname = orgname.split('<ORGNAME>')
				orgname = orgname[1]
				orgname = orgname.replace('&lt;', '<')
				orgname = orgname.replace('&amp;', '&')
				orgname = orgname.replace('&quot;', '"')
				orgname = orgname.replace('&gt;', '>')
				orgname = orgname.strip()
			if qw.count('<ORGUNIT>')>=1:
				orgunit = qw.replace('</ORGUNIT>', '<ORGUNIT>')
				orgunit = orgunit.split('<ORGUNIT>')
				orgunit = orgunit[1]
				orgunit = orgunit.replace('&lt;', '<')
				orgunit = orgunit.replace('&amp;', '&')
				orgunit = orgunit.replace('&quot;', '"')
				orgunit = orgunit.replace('&gt;', '>')
				orgunit = orgunit.strip()
			if qw.count('<TEL>')>=1:
				tel = qw.split('<TEL>')
				for w in tel:
					if w.count('</NUMBER><HOME /></TEL>'):
						number = w.replace('<NUMBER>', '</NUMBER><HOME />')
						number = number.replace('</NUMBER><HOME /></TEL>', '</NUMBER><HOME />')
						number = number.split('</NUMBER><HOME />')
						number = number[1]
						number = number.replace('&lt;', '<')
						number = number.replace('&amp;', '&')
						number = number.replace('&quot;', '"')
						number = number.replace('&gt;', '>')
						number = number.strip()
			if qw.count('<TEL>')>=1:
				tel = qw.split('<TEL>')
				for w in tel:
					if w.count('</NUMBER><HOME /><CELL /></TEL>'):
						number2 = w.replace('<NUMBER>', '</NUMBER><HOME />')
						number2 = number2.replace('</NUMBER><HOME /><CELL /></TEL>', '</NUMBER><HOME />')
						number2 = number2.split('</NUMBER><HOME />')
						number2 = number2[1]
						number2 = number2.replace('&lt;', '<')
						number2 = number2.replace('&amp;', '&')
						number2 = number2.replace('&quot;', '"')
						number2 = number2.replace('&gt;', '>')
						number2 = number2.strip()
			if qw.count('<TEL>')>=1:
				tel = qw.split('<TEL>')
				for w in tel:
					if w.count('</NUMBER><HOME /><FAX /></TEL>'):
						number3 = w.replace('<NUMBER>', '</NUMBER><HOME />')
						number3 = number3.replace('</NUMBER><HOME /><FAX /></TEL>', '</NUMBER><HOME />')
						number3 = number3.split('</NUMBER><HOME />')
						number3 = number3[1]
						number3 = number3.replace('&lt;', '<')
						number3 = number3.replace('&amp;', '&')
						number3 = number3.replace('&quot;', '"')
						number3 = number3.replace('&gt;', '>')
						number3 = number3.strip()
			if qw.count('<TEL>')>=1:
				tel = qw.split('<TEL>')
				for w in tel:
					if w.count('</NUMBER><WORK /></TEL>'):
						number4 = w.replace('<NUMBER>', '</NUMBER><HOME />')
						number4 = number4.replace('</NUMBER><WORK /></TEL>', '</NUMBER><HOME />')
						number4 = number4.split('</NUMBER><HOME />')
						number4 = number4[1]
						number4 = number4.replace('&lt;', '<')
						number4 = number4.replace('&amp;', '&')
						number4 = number4.replace('&quot;', '"')
						number4 = number4.replace('&gt;', '>')
						number4 = number4.strip()
			if qw.count('<TEL>')>=1:
				tel = qw.split('<TEL>')
				for w in tel:
					if w.count('</NUMBER><WORK /><FAX /></TEL>'):
						number5 = w.replace('<NUMBER>', '</NUMBER><HOME />')
						number5 = number5.replace('</NUMBER><WORK /><FAX /></TEL>', '</NUMBER><HOME />')
						number5 = number5.split('</NUMBER><HOME />')
						number5 = number5[1]
						number5 = number5.replace('&lt;', '<')
						number5 = number5.replace('&amp;', '&')
						number5 = number5.replace('&quot;', '"')
						number5 = number5.replace('&gt;', '>')
						number5 = number5.strip()
			if name == given+u' '+family:
				name = ''
			if name == given:
				name = ''
			if not name=='':
				rep += u'Имя: '+name+u'\n'
			if not nickname=='':
				rep +=u'Ник: '+nickname+u'\n'
			if not given=='':
				rep +=u'Имя: '+given
				if family=='':
					rep +=u'\n'
			if not family=='':
				rep +=u' '+family+u'\n'
			if not email=='':
				rep +=u'Email: '+email+u'\n'
			if not pcode=='' or not country=='' or not locality=='' or not region=='':
				rep +=u'Дом: '
			if not pcode=='':
				rep += pcode
				if country=='' and region=='' and locality=='':
					rep +=u'\n'
				else:
					rep += u', '
			if not country=='':
				if country=='Russia':
					country = u'Россия'
				rep += country
				if region=='' and locality=='':
					rep +=u'\n'
				else:
					rep += u', '
			if not locality=='':
				rep += locality
				if region=='':
					rep +=u'\n'
				else:
					rep += u', '
			if not region=='':
				rep += region+u'\n'
			if not pcode=='' or not country=='' or not locality=='' or not region=='':
				if not street=='':
					rep +=u'        '
			if not street=='':
				rep += u'Адрес: '+street+u'\n'
			if not pcode=='' or not country=='' or not locality=='' or not region=='' or not street=='':
				if not number=='' or not number2=='' or not number3=='' or not number4=='' or not number5=='':
					rep +=u'        '
			if not number=='':
				rep += u'Телефон: '+number+u'   '
				if number2=='' and number3=='':
					rep += u'\n'
			if not number3=='':
				rep += u'Факс: '+number3+u'   '
				if number2=='':
					rep += u'\n'
			if not number2=='':
				rep += u'Сотовый: '+number2+u'\n'
			if not pcode2=='' or not country2=='' or not locality2=='' or not region2=='':
				rep +=u'Работа: '
			if not pcode2=='':
				rep += pcode2
				if country2=='' and region2=='' and locality2=='':
					rep +=u'\n'
				else:
					rep += u', '
			if not country2=='':
				if country2=='Russia':
					country2 = u'Россия'
				rep += country2
				if region2=='' and locality2=='':
					rep +=u'\n'
				else:
					rep += u', '
			if not locality2=='':
				rep += locality2
				if region2=='':
					rep +=u'\n'
				else:
					rep += u', '
			if not region2=='':
				rep += region2+u'\n'
			if not pcode2=='' or not country2=='' or not locality2=='' or not region2=='':
				if not street2=='':
					rep +=u'        '
			if not street2=='':
				rep += u'Адрес: '+street2+u'\n'
			if not pcode2=='' or not country2=='' or not locality2=='' or not region2=='' or not street2=='':
				if not number4=='' or not number5=='':
					rep +=u'        '
			if not number4=='':
				rep += u'Телефон: '+number4+u'   '
				if number5=='':
					rep += u'\n'
			if not number5=='':
				rep += u'Факс: '+number5+u'\n'
			if not orgname=='':
				rep += u'Компания: '+orgname+u'   '
				if orgunit=='' and title=='':
					rep += u'\n'
			if not orgunit=='':
				rep += u'Отдел: '+orgunit+u'   '
				if title=='':
					rep += u'\n'
			if not title=='':
				rep +=u'Должность: '+title+u'\n'
			if not gender=='':
				gender=gender.lower()
				if gender=='male':
					rep +=u'Пол: Мужской\n'
				if gender=='female':
					rep +=u'Пол: Женский\n'
			if not bday=='':
				bday2 = bday[0:4]
				if bday2.isdecimal() == True:
					bday2 = int(bday2)
					if bday2 < 1910:
						bday = ''
					if not bday=='':
						if bday.count('-')>=1:
							bday = bday.split('-')
							if len(bday)>=2:
								bday3 = bday[1]
								bday4=''
								if bday3.isdecimal() == True:
									bday4 = int(bday3)
							if len(bday)>=3:
								bday5 = bday[2]
								bday6=''
								if bday5.isdecimal() == True:
									bday6 = int(bday5)
								bday7=''
								if not bday4=='' and not bday6=='':
									if bday4==1 and bday6>=1 and bday6<=20:
										bday7=u'(Козерог)'
									if bday4==1 and bday6>=21 and bday6<=31:
										bday7=u'(Водолей)'
									if bday4==2 and bday6>=1 and bday6<=20:
										bday7=u'(Водолей)'
									if bday4==2 and bday6>=21:
										bday7=u'(Рыбы)'
									if bday4==3 and bday6>=1 and bday6<=20:
										bday7=u'(Рыбы)'
									if bday4==3 and bday6>=21 and bday6<=31:
										bday7=u'(Овен)'
									if bday4==4 and bday6>=1 and bday6<=20:
										bday7=u'(Овен)'
									if bday4==4 and bday6>=21 and bday6<=30:
										bday7=u'(Телец)'
									if bday4==5 and bday6>=1 and bday6<=20:
										bday7=u'(Телец)'
									if bday4==5 and bday6>=21 and bday6<=31:
										bday7=u'(Близнецы)'
									if bday4==6 and bday6>=1 and bday6<=21:
										bday7=u'(Близнецы)'
									if bday4==6 and bday6>=22 and bday6<=30:
										bday7=u'(Рак)'
									if bday4==7 and bday6>=1 and bday6<=22:
										bday7=u'(Рак)'
									if bday4==7 and bday6>=23 and bday6<=31:
										bday7=u'(Лев)'
									if bday4==8 and bday6>=1 and bday6<=23:
										bday7=u'(Лев)'
									if bday4==8 and bday6>=24 and bday6<=31:
										bday7=u'(Дева)'
									if bday4==9 and bday6>=1 and bday6<=23:
										bday7=u'(Дева)'
									if bday4==9 and bday6>=24 and bday6<=30:
										bday7=u'(Весы)'
									if bday4==10 and bday6>=1 and bday6<=23:
										bday7=u'(Весы)'
									if bday4==10 and bday6>=24 and bday6<=31:
										bday7=u'(Скорпион)'
									if bday4==11 and bday6>=1 and bday6<=22:
										bday7=u'(Скорпион)'
									if bday4==11 and bday6>=23 and bday6<=30:
										bday7=u'(Стрелец)'
									if bday4==12 and bday6>=1 and bday6<=21:
										bday7=u'(Стрелец)'
									if bday4==12 and bday6>=22 and bday6<=31:
										bday7=u'(Козерог)'
									bday2 = unicode(bday2)
									rep +=u'Дата рождения: '+bday5+u'.'+bday3+u'.'+bday2+u'  '+bday7+u'\n'
			if not url=='':
				rep +=u'Домашняя страница: '+url+u'\n'
			if not desc=='':
				rep +=u'\nabout: '+desc
			if rep=='' or rep.isspace():
				rep = u'пустой вкард'
			else:
				if not nick and type!='private':
					rep2 = u'про тебя я знаю следующее:\n'
					rep3 = [rep2, rep]
					rep = ''.join(rep3)
				else:
                                        if sp!='1':
                                                if not nick:
                                                        nick=u'него'
                                                rep2 = u'про '+nick+u' я знаю следующее:\n'
                                                rep3 = [rep2, rep]
                                                rep = ''.join(rep3)
                                        else:
                                                if rjid in IUSR[source[1]]:
                                                        return
                                                if len(rep)>900:
                                                        rep=rep[:900]+u' (лимит)...'
                                                msg(source[1],arep+rep)
                                                iusr_append(source[1],rjid)
                                                iusr_load(source[1])
                                                return
		else:
			rep = u'он зашифровался'
	else:
		rep = u'что-то никак...'
	reply(type, source, rep.strip())

def iusr_load(groupchat):
        if not check_file(groupchat,'infa.txt'):
                return
        if groupchat in IUSR:
                        del IUSR[groupchat]
        try:
                file='dynamic/'+groupchat+'/infa.txt'
                fp=open(file, 'r')
                txt=eval(fp.read())
                fp.close()
                if not groupchat in IUSR:
                        IUSR[groupchat]=[]
                for x in txt:
                        IUSR[groupchat].append(x)
        except:
                print 'err in vcard plugin'
                pass

def handler_infa_work(type,source,parameters):
        INFA = 'dynamic/'+source[1]+'/infa.txt'
        juk = eval(read_file(INFA))
        if 'on' in juk:
                del juk['on']
                write_file(INFA,str(juk))
                reply(type,source,u'Инфа о новечках Oтключена')
                iusr_load(source[1])
        else:
                        juk['on']={}
                        write_file(INFA,str(juk))
                        reply(type,source,u'Инфа о новечках Bключена')
                        iusr_load(source[1])

def handler_info_usr(groupchat, nick, afl, role):
        if not check_file(groupchat,'infa.txt'):
                return
        if len(nick)>19:
                return
        if time.time() - INFO['start']<60:
                return
        botnick = get_bot_nick(groupchat)
        if not groupchat in GROUPCHATS:
                return
        if nick == botnick:
                return
        if not groupchat in IUSR_LAST:
                IUSR_LAST[groupchat]={'time':time.time()}
        else:
                if time.time()-IUSR_LAST[groupchat]['time']<3:
                        return
                else:
                        IUSR_LAST[groupchat]['time']=time.time()
        if check_file(groupchat,'infa.txt'):
                sas = get_true_jid(groupchat+'/'+nick)
                juk = IUSR
                if not groupchat in IUSR:
                        return
                if role == 'moderator':
                        return
                if sas in IUSR[groupchat]:
                        return
                if not 'on' in IUSR[groupchat] and not 'vcheck' in IUSR[groupchat]:
                        return
                hnd_getvcard('public', [groupchat+'/'+nick,groupchat,nick], nick, '1')

def iusr_append(groupchat,jid):
        try:
                INFA = 'dynamic/'+groupchat+'/infa.txt'
                juk = eval(read_file(INFA))
                if not jid in juk:
                        juk[jid]={}
                        write_file(INFA,str(juk))
        except:
                write_file('dynamic/'+groupchat+'/infa.txt',str('{}'))
                pass

def visitor_vcheck(groupchat, nick, role, reason=''):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':role})
	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def vcheck_on(type,source,parameters):
        if not check_file(source[1],'infa.txt'):
                return
        INFA = 'dynamic/'+source[1]+'/infa.txt'
        juk = eval(read_file(INFA))
        if 'vcheck' in juk:
                del juk['vcheck']
                write_file(INFA,str(juk))
                reply(type,source,u'проверка вкарда отключена')
                iusr_load(source[1])
        else:
                        juk['vcheck']={}
                        write_file(INFA,str(juk))
                        reply(type,source,u'проверка вкарда включена')
                        iusr_load(source[1])


        
register_stage1_init(iusr_load)
register_join_handler(handler_info_usr)
register_command_handler(vcheck_on, 'vcheck', ['мод','админ'], 20,'Включить/отключить проверку vCard,если вкард пуст делает входящего визитором', 'vcheck', ['vcheck'])
register_command_handler(handler_infa_work, 'юзеринфа', ['мод','админ'], 20,'Включить/отключить автопоказ инфы о новых пользователях ', 'юзеринфа', ['юзеринфа'])
register_command_handler(handler_vcardget, 'визитка', ['мук','инфо','все'], 11, 'Показывает vCard указанного пользователя.', 'визитка [ник]', ['визитка guy','визитка'])
