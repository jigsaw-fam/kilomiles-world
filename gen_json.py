import json
from pprint import pprint as pp

FROM_ID     = 1
TO_ID       = 1_000
NAME        = 'KilomilesWorld'
DESC        = 'Character fashion design # AI generated 1/1 edition only # Design prompt : Lung Jack'
IPFS_EGG    = 'ipfs://bafybeih6s6l6vl6fascgi6usajp45gay3we2u4pgvqkjwmycawibbehguu/KilomilesWorldEgg.png'
IPFS_1_100  = 'ipfs://bafybeih6s6l6vl6fascgi6usajp45gay3we2u4pgvqkjwmycawibbehguu/{}.png'
INPUT_PATH  = './csv/raw.csv'
OUTPUT_PATH = './json/{}.json'

chunk       = []
running_id  = FROM_ID

species_set = set()
aura_set    = set()
spirit_set  = set()

# load data from csv
rows = open(INPUT_PATH, 'r').read().splitlines()

# loop line by line
for row in rows:
    # clean up fields
    data = [ r.strip() for r in row.split(',') ]

    # skip #1
    if len(data) != 7:
        continue

    # extract fields
    (title, _, species, _, aura, _, spirit) = data

    # skip #2
    if not title.startswith(NAME):
        continue

    # skip #3
    if '' in (title, species, aura, spirit):
        continue

    # check id order
    ref_id = int(title.removeprefix(NAME))
    if running_id != ref_id:
        print('running_id not match ref_id')
        print(running_id, '<=>', data)
        exit()

    # append to chunk
    chunk.append((title, species, aura, spirit))

    # prepare next token
    running_id += 1

    # update trait data
    species_set.add(species)
    aura_set.add(aura)
    spirit_set.add(spirit)

# unrvealed: append null until end of album
for token_id in range(running_id, TO_ID+1):
    chunk.append(None)

# craft metadata + write to file
for (idx, info) in enumerate(chunk):
    token_id = idx + 1
    dest = OUTPUT_PATH.format(token_id)

    # craft data
    metadata = {
      'name'        : '{} #{}'.format(NAME, token_id),
      'description' : DESC,
      'image'       : IPFS_EGG,
      'attributes'  : [],
    }

    # update image, traits
    if info is not None:
        (img, species, aura, spirit) = info
        metadata['image'] = IPFS_1_100.format(img)
        metadata['attributes'].append({ 'trait_type': 'Species', 'value': species })
        metadata['attributes'].append({ 'trait_type': 'Aura',    'value': aura })
        metadata['attributes'].append({ 'trait_type': 'Spirit',  'value': spirit })

    # write file
    # print(dest)
    with open(dest, "w") as f:
        json.dump(metadata, f)

# recheck traits
print('Species:')
print(sorted(species_set))
print('Aura:')
print(sorted(aura_set))
print('Spirit:')
print(sorted(spirit_set))
