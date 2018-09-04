from protolib2 import merge
from protolib2.traversals import PROTOCOLS_BUILD_DIR

print(PROTOCOLS_BUILD_DIR)
merge.merge_protocols(PROTOCOLS_BUILD_DIR)
