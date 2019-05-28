from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Reagent Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# create custom labware
outlet_tray_name = 'outlet-tray-12row'
if outlet_tray_name not in labware.list():
    labware.create(
        outlet_tray_name,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=5,
        depth=30,
        volume=22000
    )

inlet_tray_name = 'inlet-tray-96'
if inlet_tray_name not in labware.list():
    labware.create(
        inlet_tray_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=30,
        volume=900
    )

# load labware
inlet_tray = labware.load(inlet_tray_name, '1')
outlet_tray = labware.load(outlet_tray_name, '4')
tubes50 = labware.load('opentrons-tuberack-50ml', '7')
tubes15 = labware.load('opentrons-tuberack-15ml', '8')
tips1000 = labware.load('tiprack-1000ul', '11')

# pipette
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])

# reagent setup
h2o = tubes50.wells('A1', 'A2', 'A3', 'B1')
anolyte = tubes50.wells('B2', 'B3')
catholyte = tubes15.wells('A1', 'A2')
cief_gel = tubes15.wells('B1', 'B2')
sls = tubes15.wells('C1', 'C2')
chem_mob = tubes15.wells('A3', 'A4')

# variables for height tracking 50 ml tubes
heights_50 = {
    'h2o1': -15,
    'h2o2': -15,
    'anolyte': -15
}
r_cyl_50 = 13.4


# 50 ml reagent height tracking function
def track_50(tube, vol):
    global heights_50

    # update height from which to aspirate
    dh = vol/(math.pi*(r_cyl_50**2))
    heights_50[tube] -= dh


# variables for height tracking 50 ml tubes
heights_15 = {
    'catholyte': -18,
    'chem mob1': -18,
    'chem mob2': -18,
    'sls': -18,
    'cief gel': -18
}
r_cyl_15 = 7.52


# 50 ml reagent height tracking function
def track_15(tube, vol):
    global heights_15

    # update height from which to aspirate
    dh = vol/(math.pi*(r_cyl_15**2))
    heights_15[tube] -= dh


"""reagent outlet filling"""
# H2O
h2o_channels = ['1', '2', '5', '6', '7', '8', '9', '12']
p1000.pick_up_tip()
for c in h2o_channels:
    dest = outlet_tray.wells('A'+c)
    for _ in range(5):
        track_50('h2o1', 3250/5)
        p1000.transfer(
            3250/5,
            h2o[0].top(heights_50['h2o1']),
            dest.top(),
            new_tip='never'
            )
p1000.drop_tip()

# catholyte
catholye_channels = ['3', '10']
p1000.pick_up_tip()
for c in catholye_channels:
    dest = outlet_tray.wells('A'+c)
    for _ in range(10):
        track_15('catholyte', 6500/10)
        p1000.transfer(
            6500/10,
            catholyte[0].top(heights_15['catholyte']),
            dest.top(),
            new_tip='never'
        )
p1000.drop_tip()

# chem_mob
chem_mob_channels = ['4', '11']
p1000.pick_up_tip()
for c in chem_mob_channels:
    dest = outlet_tray.wells('A'+c)
    for _ in range(10):
        track_15('chem mob1', 6500/10)
        p1000.transfer(
            6500/10,
            chem_mob[0].top(heights_15['chem mob1']),
            dest.top(),
            new_tip='never'
        )
p1000.drop_tip()

"""reagent inlet filling"""
# H2O
h2o_columns = ['1', '2', '5', '8', '9']
dests = [well for el in h2o_columns
         for well in inlet_tray.columns(el)]
p1000.pick_up_tip()
for d in dests:
    track_50('h2o2', 900)
    p1000.transfer(
        900,
        h2o[1].top(heights_50['h2o2']),
        d.top(),
        new_tip='never'
    )
p1000.drop_tip()

# anolyte
anolyte_columns = ['3', '4', '10', '11']
dests = [well for el in anolyte_columns
         for well in inlet_tray.columns(el)]
p1000.pick_up_tip()
for d in dests:
    track_50('anolyte', 900)
    p1000.transfer(
        900,
        anolyte[0].top(heights_50['anolyte']),
        d.top(),
        new_tip='never'
    )
p1000.drop_tip()

# chem mob
dests = [well for well in inlet_tray.columns('6')]
p1000.pick_up_tip()
for d in dests:
    track_15('chem mob2', 900)
    p1000.transfer(
        900,
        chem_mob[1].top(heights_15['chem mob2']),
        d.top(),
        new_tip='never'
    )
p1000.drop_tip()

# SLS
dests = [well for well in inlet_tray.columns('12')]
p1000.pick_up_tip()
for d in dests:
    track_15('sls', 900)
    p1000.transfer(
        900,
        sls[0].top(heights_15['sls']),
        d.top(),
        new_tip='never'
    )
p1000.drop_tip()

# cIEF gel
p1000.set_flow_rate(aspirate=100, dispense=100)

dests = [well for well in inlet_tray.columns('7')]
for d in dests:
    track_15('cief gel', 900)
    p1000.transfer(
        900,
        cief_gel[0].top(heights_15['cief gel']),
        d.top(),
        disposal_vol=100
    )
