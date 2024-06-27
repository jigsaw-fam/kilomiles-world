import json
from pprint import pprint as pp

from_id     = 331
to_id       = 600
json_path   = "./json/{}.json"
ipfs_new    = "ipfs://bafkreiaqrau527memgnrbtgq7244h62c3pdrf3gtlmx4usjcayb2g2awnq"

for id in range(from_id, to_id+1):
    out_path = json_path.format(id)
    data = json.load(open(out_path))
    data['image'] = ipfs_new

    # write file
    print(out_path)
    with open(out_path, "w") as f:
        json.dump(data, f)
