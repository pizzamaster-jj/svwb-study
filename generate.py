import json

D = json.load(open('off_all.json'))
det, tribe, sets = D['details'], D['tribe'], D['sets']

CLASS = {0:'Neutral',1:'Forestcraft',2:'Swordcraft',3:'Runecraft',
         4:'Dragoncraft',5:'Abysscraft',6:'Havencraft',7:'Portalcraft'}
TYPE = {1:'Follower',2:'Amulet',3:'Amulet',4:'Spell'}

def evo_text(evo):
    if not isinstance(evo, dict):
        return None
    t = (evo.get('skill_text') or '').strip()
    return t or None

out = []
for cid, d in det.items():
    if not isinstance(d, dict):
        continue
    c = d.get('common') or {}
    tribes = [tribe.get(str(t)) for t in (c.get('tribes') or [])]
    tribes = [t for t in tribes if t and t != '-']
    out.append({
        'id': str(c.get('card_id', cid)),
        'name': c.get('name') or '',
        'skill_text': c.get('skill_text') or '',
        'evo_skill_text': evo_text(d.get('evo')),
        'flavour_text': c.get('flavour_text') or '',
        'color': CLASS.get(c.get('class'), str(c.get('class'))),
        'type': TYPE.get(c.get('type'), 'Follower'),
        'cost': str(c.get('cost', 0)),
        'atk': str(c.get('atk', 0)),
        'life': str(c.get('life', 0)),
        'rarity': str(c.get('rarity', 1)),
        'tribes': tribes,
        'set_name': sets.get(str(c.get('card_set_id')), ''),
        'is_token': '1' if c.get('is_token') else '0',
        'is_include_rotation': '1' if c.get('is_include_rotation') else '0',
        'questions': c.get('questions') or [],
        'related_cards': [],
        'image': 'https://static.dotgg.gg/shadowverse/cards/%s.webp' % c.get('card_id', cid),
        'cv': c.get('cv') or '',
        'illustrator': c.get('illustrator') or '',
    })

# de-dup by id, keep first
seen = set(); uniq = []
for o in out:
    if o['id'] in seen: continue
    seen.add(o['id']); uniq.append(o)

with open('cards_ja.js', 'w', encoding='utf-8') as f:
    f.write('// Shadowverse: Worlds Beyond card data (Japanese)\n')
    f.write('// Source: shadowverse-wb.com official CardList API (lang=ja)\n')
    f.write('window.CARD_DATA = ')
    json.dump(uniq, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';\n')

from collections import Counter
print('cards written:', len(uniq))
print('with evo:', sum(1 for o in uniq if o['evo_skill_text']))
print('with Q&A:', sum(1 for o in uniq if o['questions']))
print('tokens:', sum(1 for o in uniq if o['is_token']=='1'))
print('type dist:', dict(Counter(o['type'] for o in uniq)))
print('color dist:', dict(Counter(o['color'] for o in uniq)))
print('sample:', uniq[0]['name'], '|', uniq[0]['color'], '|', uniq[0]['skill_text'][:30])
