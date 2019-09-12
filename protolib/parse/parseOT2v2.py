import json
import sys


def parse(protocol_path):
    if not protocol_path:
        return {}
    print('Parsing protocol: {}'.format(protocol_path))
    return {"pathDEBUG": protocol_path}


if __name__ == '__main__':
    sourceFilePath = sys.argv[1]
    destFilePath = sys.argv[2]
    print('OT2 APIv2: parsing {} to {}'.format(sourceFilePath, destFilePath))

    result = parse(sourceFilePath)
    with open(destFilePath, 'w') as f:
        json.dump(result, f)
