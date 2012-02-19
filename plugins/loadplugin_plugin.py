#===istalismanplugin===
# -*- coding: utf-8 -*-


def handler_pod_pl(type,source,parameters):
  if not parameters:
    return
  try:
    fp = file(PLUGIN_DIR + '/' + parameters+'_plugin.py')
    exec fp in globals()
    fp.close()
    reply(type,source,u'ok')
  except:
    reply(type,source,unicode(traceback.format_exc()))

register_command_handler(handler_pod_pl, 'load', ['все'], 99, 'load anywhere plugin', 'load <names plugin>', ['load admin'])

