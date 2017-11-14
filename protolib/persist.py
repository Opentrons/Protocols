import json


def write_json_to_file(json_data, output_path):
    """
    Given a json object, writes every valid object into a file
    :param json_data:
    :return:
    """
    with open(output_path, 'w') as ofile:
        ofile.write(json.dumps(json_data))
