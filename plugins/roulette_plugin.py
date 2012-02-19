#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  roulette_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007-2008 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_roulette_one(type, source, parameters):
	groupchat = source[1]
	nick = source[2]
	rep =''
	if not user_level(source,groupchat)>=15:
		if GROUPCHATS.has_key(groupchat):
			if nick:
				random.seed(int(time.time()))
				if random.randrange(0,2) == 0:
					order_kick(source[1], nick, u'ПТЫДЫЩЬ!!!')
				else:
					rep = u'ЩЁЛК!'
		else:
			rep = u'что-то вглюкнуло...'
		if rep:
			reply(type, source, rep)
		else:
			msg(source[1],  u'/me выстрелил в '+nick)
	else:
		reply(type, source, u'не поднимается рука в модера стрелять :(')
	
#def handler_roulette_many(type, source, parameters):
	
	

register_command_handler(handler_roulette_one, 'рр', ['фан','инфо','все'], 10, 'Старая добрая русская рулетка.', 'рр (русские буквы)', ['рр'])
