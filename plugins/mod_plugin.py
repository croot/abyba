#===istalismanplugin===
# -*- coding: utf-8 -*-


def hand_probability(type, source, parameters):
    if not parameters or len(parameters)<6:
        return
    if len(parameters)>100:
        return
    num=str(random.randrange(0, 100))
    reply(type,source,u'ваше утверждение верно на '+unicode(num)+u'% процентов')
		
		
register_command_handler(hand_probability, 'вероятность', ['все'], 0, 'вероятность чего-то там,шуточная команда.', 'вероятность <word>', ['вероятность что все сошли с ума'])
