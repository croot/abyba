#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin

#  Автор: 40tman

MORZE={u' ':'-...-',u'a':'.-',u'а':'.-',u'b':'-...',u'б':'-...',u'в':'.--',u'w':'.--',u'g':'--.',u'г':'--.',u'д':'-..',u'd':'-..',u'e':'.',u'е':'.',u'ж':'...-',u'v':'...-',u'з':'--..',u'z':'--..',u'i':'..',u'и':'..',u'j':'.---',u'й':'.---',u'k':'-.-',u'к':'-.-',u'л':'.-..',u'l':'.-..',u'm':'--',u'м':'--',u'n':'-.',u'н':'-.',u'o':'---',u'о':'---',u'p':'.--.',u'п':'.--.',u'r':'.-.',u'р':'.-.',u's':'...',u'с':'...',u't':'-',u'т':'-',u'u':'..-',u'у':'..-',u'f':'..-.',u'ф':'..-.',u'x':'....',u'х':'....',u'c':'-.-.',u'ц':'-.-.',u'ч':'---.',u'ш':'----',u'щ':'--.-',u'q':'--.-',u'ъ':'--.--',u'ы':'-.--',u'y':'-.--',u'x':'-..-',u'ь':'-..-',u'э':'..-..',u'ю':'..--',u'я':'.-.-',u'1':'.----',u'2':'..---',u'3':'...--',u'4':'....-',u'5':'.....',u'6':'-....',u'7':'--...',u'8':'---..',u'9':'----.',u'0':'-----',u'.':'......',u'-':'-....-',u',':'.-.-.-',u':':'---...',u'?':'..--..',u'!':'--..--',u'@':'.--.-.'}


def morze_cod_decod(type, source, parameters):
        if not parameters:
                reply(type, source, u'Доступно :\n'+','.join(MORZE.keys()))
                return
        if len(parameters)>150:
                reply(type, source, u'а не много?')
                return
        if parameters.count(chr(10)):
                parameters=parameters.replace(chr(10),'')
        parameters=parameters.lower()
        dec=0
        rep=''
        for x in parameters:
                if x in MORZE.keys():
                        if x not in ['-','.',' ']:
                                dec=1
                                break
        if dec:
                for x in parameters:
                        if x in MORZE.keys():
                                rep+=MORZE[x]+' '
                reply(type, source, rep)
                return
        else:
                if not parameters.count(' '):
                        if parameters in MORZE.values():
                                for x in MORZE.keys():
                                        if MORZE[x]==parameters:
                                                parameters=parameters.replace(parameters, x)
                                reply(type, source, parameters)
                                return
                        else:
                                reply(type, source, u'символа нет в списке')
                                return
                else:
                        rep=''
                        if parameters.count(unicode('·','UTF-8')):
                                parameters=parameters.replace(unicode('·','UTF-8'),'.')
                        if parameters.count(unicode('–','UTF-8')):
                                parameters=parameters.replace(unicode('–','UTF-8'),'-')
                        list=parameters.split()
                        for x in list:
                                if x in MORZE.values():
                                        for c in MORZE.keys():
                                                if MORZE[c]==x:
                                                        if ord(c)==32 or ord(c)>125:
                                                                rep+=c
                        reply(type, source, rep)

register_command_handler(morze_cod_decod, 'морзе', ['все', 'инфо'], 0, 'морзянка', 'морзе <слово>', ['морзе привет','морзе ---. --- - -- .- -. -...- .-.. ..- ---. ---- .. .---'])
