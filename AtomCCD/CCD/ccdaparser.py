import subprocess
import json
from pprint import pprint
# if node isn't on your path, the first arg should instead be a path to the node bin
"""
path_to_file must be intialized with the correct path of the ccd document
Also npm and node must be installed before running this script

"""

def parse_ccda(path_to_file):
    cmd_list = ['node', 'CCD/parseClinicalXml.js', path_to_file]

    p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = p.communicate()
    p.stdin.close()

    if p.returncode != 0:
        print error
        raise ValueError("Failed to parse clinical XML at %s" % \
            path_to_file)

    json_data = json.loads(result)
    return json_data

