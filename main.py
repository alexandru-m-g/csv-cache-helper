import json
import csv
import codecs
import urllib.request as url_req
import shutil


def create_file():
    with open('sources.json') as sources_json:
        sources = json.load(sources_json)
        for source in sources:
            url = source.get('url')
            data = None
            type = source.get('type')
            filename = '{}.{}'.format(source.get('name'), source.get('extension'))
            if type == 'json-objects':
                data = json_object_pull_data(url)
                if not data:
                    raise NoDataException('No data to write to file')
            elif type == 'simple':
                simple_pull_data(url, filename)
            if data:
                with open(filename, 'w') as out:
                    out.write(data)


def json_object_pull_data(url):
    r = url_req.urlopen(url, timeout=60)
    csv_reader = csv.reader(codecs.iterdecode(r, 'utf-8'))
    keys = []
    objs = []
    first = True
    for row in csv_reader:
        if first:
            first = False
            keys = row
        else:
            obj = {}
            for i, key in enumerate(keys):
                obj[key] = row[i] if len(row) > i else ''
            objs.append(obj)

    return json.dumps(objs)


def simple_pull_data(url, filename):
    with url_req.urlopen(url) as response, open(filename, 'wb') as out:
        shutil.copyfileobj(response, out)



class NoDataException(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


if __name__ == '__main__':
    create_file()
