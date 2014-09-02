#!/usr/bin/env python
from nbt.nbt import NBTFile
from os import listdir
import json

whitelist = json.loads(open('whitelist.json').read())
playermap = {}
for o in whitelist:
    playermap[o['uuid']] = o['name']


for f in listdir('./world/playerdata/'):
    p = NBTFile(filename='world/playerdata/{}'.format(f))
    print '*******************************************'
    print "{} {}".format(playermap.get(f.replace('.dat', ''), 'unknown'), [i.value for i in p['Pos']])
    print '*******************************************'
    print 'Inventory >'
    for i in p['Inventory']:
        print " * %02d %s" % (i['Count'].value, i['id'])
    print 'Enderchest >'
    for i in p['EnderItems']:
        print " * %02d %s" % (i['Count'].value, i['id'])
