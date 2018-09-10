import sys
import opentrons

allProtocolFiles = sys.argv[1:]

print('Opentrons verson: ', opentrons.__version__)
print('Parsing OT2. Files:')
print(allProtocolFiles)
print('*-' * 40)
