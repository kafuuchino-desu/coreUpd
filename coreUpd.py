# -*- coding: utf-8 -*-
import os
from shutil import copyfile

#set proxy_mode to true if u are using bc/waterfall
proxy_mode = False

playerCount = 0
updateTask = False

def update_jar(server):
  server.stop()
  server.wait_for_start()
  try:
    copyfile('./update/server.jar', './server/server.jar')
  except:
    server.logger.critical('failed to overwrite server jar...attempting to start')
  else:
    server.logger.info('SUCCESSFULLY UPDATED SERVER JAR')
    os.remove('./update/server.jar')
  server.start()

def on_info(server, info):
  global updateTask
  global proxy_mode

  #creates a restart job
  if (info.source == 1) and (info.content == '!!upd'):
    server.logger.info('SUCCESSFULLY CREATED UPDATE TASK.')
    updateTask = True

  #detect player leave bc no on_player_left api for bc/waterfall parser
  #and executes a /glist command
  #fallen Reeeeeeeeeeeeeee
  if info.content.endswith('UpstreamBridge has disconnected') and proxy_mode:
    server.execute('glist')

  #update jar
  if info.content == 'Total players online: 0' and proxy_mode and updateTask:
    update_jar(server)

def on_player_joined(server, player):
  global playerCount
  playerCount += 1

def on_player_left(server, player):
  global updateTask
  global playerCount

  playerCount -= 1
  if (playerCount <=0) and updateTask and not proxy_mode:
    update_jar(server)