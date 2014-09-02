#!/usr/bin/env python
from nbt.nbt import NBTFile
from os import listdir
import json

DIMENSIONS = {
    0: 'Overworld',
    1: 'Nether',
    2: 'End'
}

whitelist = json.loads(open('whitelist.json').read())
playermap = {}
for o in whitelist:
    playermap[o['uuid']] = o['name']


for f in listdir('./world/playerdata/'):
    p = NBTFile(filename='world/playerdata/{}'.format(f))
    print '*******************************************'
    print "{} {} {}".format(playermap.get(f.replace('.dat', ''), 'unknown'), [i.value for i in p['Pos']], DIMENSIONS[p['Dimension'].value])
    print '*******************************************'
    print 'Inventory >'
    for i in p['Inventory']:
        name = ""
        try:
            name = "(%s)" % (i['tag']['display']['Name'])
        except: pass
        print " * %02d %s %s" % (i['Count'].value, i['id'], name)
    print 'Enderchest >'
    for i in p['EnderItems']:
        name = ""
        try:
            name = "(%s)" % (i['tag']['display']['Name'])
        except: pass
        print " * %02d %s %s" % (i['Count'].value, i['id'], name)
