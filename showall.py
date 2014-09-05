#!/usr/bin/env python
from os import listdir, environ
import json

from nbt.nbt import NBTFile
from jinja2 import Environment, PackageLoader


DIMENSIONS = {
    0: 'Overworld',
    -1: 'Nether',
    1: 'End'
}

ENCHANTMENTS = {
  0: 'Protection',
  1: 'Fire Protection',
  2: 'Feather Failling',
  3: 'Blast Protection',
  4: 'Projectile Protection',
  5: 'Respiration',
  6: 'Aqua Affinity',
  7: 'Thorns',
  8: 'Depth Strider',
  16: 'Sharpness',
  17: 'Smite',
  18: 'Bane of Anthropods',
  19: 'Knockback',
  20: 'Fire Aspect',
  21: 'Looting',
  32: 'Efficiency',
  33: 'Silk Touch',
  34: 'Unbreaking',
  35: 'Fortune',
  48: 'Power',
  49: 'Punch',
  50: 'Flame',
  51: 'Infinity',
  61: 'Luck of the Sea',
  62: 'Lure',
}

LEVELS = {
  1: 'I',
  2: 'II',
  3: 'III',
  4: 'IV',
  5: 'V',
}


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


def process(dirname):
    data = {}
    whitelist = json.loads(open('whitelist.json').read())
    playermap = {}
    for o in whitelist:
        playermap[o['uuid']] = o['name']

    for f in listdir(dirname):
        p = NBTFile(filename='{}/{}'.format(dirname, f))
        name = playermap.get(f.replace('.dat', ''), 'unknown')
        pos = [i.value for i in p['Pos']]
        dim = DIMENSIONS[p['Dimension'].value]
        data[name] = {}
        data[name]['pos'] = pos
        data[name]['dim'] = dim
        data[name]['inventory'] = []
        data[name]['enderchest'] = []
        if len(p['Inventory']) > 0:
            for i in p['Inventory']:
                item = procitem(i)
                data[name]['inventory'].append(item)
        if len(p['EnderItems']) > 0:
            for i in p['EnderItems']:
                item = procitem(i)
                data[name]['enderchest'].append(item)
    return data


def serialize_text(data):
    for name, player in data.iteritems():
        print('*' * 80)
        print("{} {} {}".format(name, player['pos'], player['dim']))
        print('*' * 80)
        if len(player['inventory']) > 0:
            print('Inventory >')
            for item in player['inventory']:
                print(" %2s %s %s %s" % (item['count'], item['id'], item['enchantment'], item['name']))
        if len(player['enderchest']) > 0:
            print('Enderchest >')
            for item in player['enderchest']:
                print(" %2s %s %s %s" % (item['count'], item['id'], item['enchantment'], item['name']))


def serialize_json(data):
    print json.dumps(data, indent=2)


def serialize_html(data):
    env = Environment(loader=PackageLoader('showall', 'templates'))
    template = env.get_template('showall.html')
    print template.render(players=data.iteritems())


def command():
    data = process('./world/playerdata/')

    if environ.get('JSON'):
        serialize_json(data)
    elif environ.get('HTML'):
        serialize_html(data)
    else:
        serialize_text(data)

if __name__ == '__main__':
    command()
