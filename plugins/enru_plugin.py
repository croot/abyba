#===istalismanplugin===
# -*- coding: utf-8 -*-


def isrus_text(type, source, parameters):
    rus=0
    eng=0
    R={}
    E={}
    n=0
    if parameters and len(parameters)<100:
        for x in parameters:
            n+=1
            try:
                
                if ord(x)>127:
                    rus+=1
                    R[n]=x
                else:
                    eng+=1
                    E[n]=x
            except:
                pass
    if rus and not eng:
        reply(type, source, u'только русский')
        return
    if eng and not rus:
        reply(type, source, u'только латинница')
        return
    if rus>eng:
        rep=''
        for x in E:
            rep+=str(x)+'->'+E[x]+', '
        reply(type, source, u'В тексте \"'+parameters+u'\" следущие символы являються латинницей:\n'+rep)
        return
    rep=''
    for x in R:
        rep+=str(x)+'->'+R[x]+', '
    reply(type, source, u'В тексте \"'+parameters+u'\" следущие символы являються русскими:\n'+rep)
    return

register_command_handler(isrus_text, '!раскладка', ['все'], 0, 'показывает из каких символов состоит текст', '!раскладка <текст>', ['!раскладка Вася'])

