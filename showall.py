#!/usr/bin/env python
from nbt.nbt import NBTFile
from os import listdir, environ
import json
from enchantments import ENCHANTMENTS, LEVELS

DIMENSIONS = {
    0: 'Overworld',
    -1: 'Nether',
    1: 'End'
}

def out(msg):
    if not environ.get('JSON'):
        print(msg)

data = {}
whitelist = json.loads(open('whitelist.json').read())
playermap = {}
for o in whitelist:
    playermap[o['uuid']] = o['name']

def procitem(i):
    name = ""
    enchantment = ""
    if i.get('tag'):
        if i['tag'].get('display'):
            name = "(%s)" % (i['tag']['display']['Name'])
        if i['tag'].get('ench') and len(i['tag']['ench']) > 0:
            parts = []
            for e in i['tag']['ench']:
                parts.append("%s %s" % (LEVELS[e['lvl'].value], ENCHANTMENTS[e['id'].value]))
            enchantment = "[%s]" % (", ".join(parts))

    count = i['Count'].value
    iid = i['id']
    return {
        'id': iid.value.split(':')[1],
        'count': count,
        'enchantment': enchantment,
        'name': name,
    }

for f in listdir('./world/playerdata/'):
    p = NBTFile(filename='world/playerdata/{}'.format(f))
    name = playermap.get(f.replace('.dat', ''), 'unknown')
    pos = [i.value for i in p['Pos']]
    dim = DIMENSIONS[p['Dimension'].value]
    data[name] = {}
    data[name]['pos'] = pos
    data[name]['dim'] = dim
    data[name]['inventory'] = []
    data[name]['enderchest'] = []
    out('*' * 80)
    out("{} {} {}".format(name, pos, dim))
    out('*' * 80)
    if len(p['Inventory']) > 0:
        out('Inventory >')
        for i in p['Inventory']:
            item = procitem(i)
            data[name]['inventory'].append(item)
            out(" %2s %s %s %s" % (item['count'], item['id'], item['enchantment'], item['name']))
    if len(p['EnderItems']) > 0:
        out('Enderchest >')
        for i in p['EnderItems']:
            item = procitem(i)
            data[name]['enderchest'].append(item)
            out(" %2s %s %s %s" % (item['count'], item['id'], item['enchantment'], item['name']))

if environ.get('JSON'):
    print json.dumps(data, indent=2)
