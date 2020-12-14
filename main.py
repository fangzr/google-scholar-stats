from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime

scholar_ids = ['RwMPs-8AAAAJ&hl']

for id in scholar_ids:
    author = scholarly.search_author_id(id)
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    name = author['name']
    author['updated'] = str(datetime.now)
    scholarly.pprint(author)
    author = jsonpickle.encode(author)

    with open(f'{name}.json', 'w') as outfile:
        json.dump(author, outfile)
