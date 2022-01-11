# Opentrons Cookbook

At Opentrons, we’ve written a lot of protocols with our users and automated all kinds of different processes. While some protocols are truly one-of-a-kind, many protocols do the exact same thing. Basic processes like magnetic bead washes, liquid level tracking in tubes, keeping track of tip use, etc, etc, get coded into almost every protocol.

We are sharing the code that the Opentrons team has developed to run these processes in the hopes that others can re-use the same code and continue to improve these methods. Please reach out to cookbook@opentrons.com with questions or if you’d like to submit something to the cookbook!

Table of Contents:
* [Basic Skeleton Protocol](#basic-skeleton-protocol)
* [Liquid Level Tracking](#liquid-level-tracking)
* [Refill Tips Mid-Protocol](#refill-tips-mid-protocol)
* [Wash Steps](#wash-steps)
* [Remove Supernatant](#remove-supernatant)
* [Loop](#loop)
* [Using CSVs](#using-csvs)
* [Track Data Across Protocol Runs](track-data-across-protocol-runs)
* [Tip Tracking with Refills](#tip-tracking-with-refills)
* [Picking Up Fewer Than 8 Tips with a Multi-Channel Pipette](picking-up-fewer-than-8-tips-with-a-multi-channel-pipette)

## Basic Skeleton Protocol

#### Everything you need to copy-paste for a Opentrons protocol

```
from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@address.com>',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.4'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    """ load labware """
    # my_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1')
    # my_tiprack = protocol.load_tiprack('opentrons_96_wellplate_300ul', '2')

    """ Variables"""
    # numSamps is the number of samples and should be 1-96 (int)
    numSamps = _numSamps

    """ load pipettes """
    # p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[my_tiprack])

    """ helper functions """
    # def my_helper_fxn():
    #     protocol.comment('I am helping!')

    """ liquid transfer commands """
    # p300.transfer(100, my_plate.wells()[0], my_plate.wells()[1])
```


## Liquid Level Tracking

```
import math

def run(protocol):

    plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1')
    tiprack = protocol.load_labware('opentrons_96_wellplate_300ul', '2')
    tuberack = protocol.load_labware('opentrons_6_tuberack_nest_50ml_conical', '3')

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[my_tiprack])

    min_height = 1  # depth at which the pipette tip will stop descending into the tube
    compensation_coeff = 1.1  # ensures tip is below liquid level even with theoretical volume loss
    initial_heights = 50  # heights that the tubes will be filled to initially
    heights = {tube: initial_heights for tube in tuberack.wells()}

    def h_track(vol, tube):
        nonlocal heights

        # calculate height decrement based on volume
        dh = (vol/(math.pi*((tube.diameter/2)**2)))*compensation_coeff

        # make sure height decrement will not crash into the bottom of the tube
        h = heights[tube] - dh if heights[tube] - dh > min_height else min_height
        heights[tube] = h

        return h

    h = h_track(200, tuberack.wells()[0])
    p300.transfer(200, tuberack.wells()[0].bottom(h), plate.wells()[0])
```

## Refill Tips Mid-Protocol

```
try:
    p_single.pick_up_tip()
except protocol_api.labware.OutOfTipsError:
    protocol.pause("Replace the tips")
    p_single.reset_tipracks()
    p_single.pick_up_tip()
```

## Wash Steps

```
def wash_step(src, vol, mtimes, tips, usedtips, msg, trash_tips=False):
        protocol.comment(f'Wash Step {msg} - Adding to samples:')
        for well, tip, tret, s in zip(magsamps, tips, usedtips, src):
            p300.pick_up_tip(tip)
            asp_ctr2 = 0
            mvol = vol
            while mvol > 180:
                p300.aspirate(180, s)
                p300.dispense(180, well.top(-3))
                p300.aspirate(10, well.top(-3))
                asp_ctr2 += 1
                mvol -= 180
            p300.aspirate(mvol, s)
            dvol = 10*asp_ctr2 + mvol
            p300.dispense(dvol, well.bottom(5))
            wash_mix(mtimes, well, 180)
            p300.blow_out()
            p300.drop_tip(tret)

        magdeck.engage(height=magheight)
        protocol.comment('Incubating on MagDeck for 3 minutes.')
        protocol.delay(minutes=3)

        protocol.comment(f'Removing supernatant from Wash {msg}:')
        svol = vol if vol == 900 else vol+40
        for well, tip in zip(magsamps, usedtips):
            p300.pick_up_tip(tip)
            supernatant_removal(svol, well, waste, -1)
            p300.aspirate(20, waste)
            if trash_tips:
                p300.drop_tip()
            else:
                p300.return_tip()
        magdeck.disengage()
```
Note that this code references two other functions, `wash_mix` and `supernatant_removal` (below)

## Remove Supernatant

```
def supernatant_removal(vol, src, dest, side):
        p300.flow_rate.aspirate = 20
        asp_ctr = 0
        while vol > 180:
            p300.aspirate(
                180, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
            p300.dispense(180, dest)
            p300.aspirate(10, dest)
            vol -= 180
            asp_ctr += 1
        p300.aspirate(
            vol, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
        dvol = 10*asp_ctr + vol
        p300.dispense(dvol, dest)
        p300.flow_rate.aspirate = 50
```

## Loop

```
for _ in range(5):
        pipette.pick_up_tip()
        pipette.mix(10, 200, reagent)
        pipette.blow_out()
        pipette.return_tip()
```

## Using CSVs

In this CSV example, 96 wells (in a 96 well plate) are each going to receive a different volume from a reservoir. Well 1 (A1) will get 1ul, Well 2 (A2) will get 2ul,..., Well 96 (H12) will get 96ul.

### 2 Approaches:
1. Copy and Paste:
In this approach, CSV_DATA is a multi-line string (there was some weird formatting with ? when I copied and pasted over the code) that is then parsed. What’s really nice about this approach is that the each cell corresponds to a well, so it visually matches up.

```
metadata = {'apiLevel': '2.5'}

CSV_DATA = """
1?2?3?4?5?6?7?8?9?10?11?12
13?14?15?16?17?18?19?20?21?22?23?24
25?26?27?28?29?30?31?32?33?34?35?36
37?38?39?40?41?42?43?44?45?46?47?48
49?50?51?52?53?54?55?56?57?58?59?60
61?62?63?64?65?66?67?68?69?70?71?72
73?74?75?76?77?78?79?80?81?82?83?84
85?86?87?88?89?90?91?92?93?94?95?96
"""


def run(protocol):
    tips = [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips)
    reservoir = protocol.load_labware('nest_1_reservoir_195ml', '2').wells()[0]
    plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '3')

    well_volumes = [""] * 96
    for i, row in enumerate(CSV_DATA.strip('\n ').split('\n')):
        for j, volume in enumerate(row.split('\t')):
            well_volumes[i*12+j] = int(volume)

   plate_wells = [well for row in plate.rows() for well in row]
   for vol, dest in zip(well_volumes, plate_wells):
       pipette.transfer(vol, reservoir, dest)

```

2. Accessing CSV:
With this approach, the CSV is transferred to the directory /data/csv and is named well_data.csv

```
import csv
import os

metadata = {'apiLevel': '2.5'}


def run(protocol):
    tips = [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips)
    reservoir = protocol.load_labware('nest_1_reservoir_195ml', '2').wells()[0]
    plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '3')

    if not protocol.is_simulating():
        file_path = '/data/csv/well_data.csv'
        # check for file; if not there, raise exception
        if not os.path.isfile(file_path):
            raise Exception("No CSV named well_data")

    well_volumes = []
    if protocol.is_simulating():
        well_volumes = [1, 2]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                for well in row:
                    well_volumes.append(int(well))

    plate_wells = [well for row in plate.rows() for well in row]
    for vol, dest in zip(well_volumes, plate_wells):
        pipette.transfer(vol, reservoir, dest)
```

## Track Data Across Protocol Runs

Writing and reading sample or tip data to .json file on robot.

```
import csv
import os

metadata = {'apiLevel': '2.5'}


def run(protocol):

    # Tip tracking between runs
    if not protocol.is_simulating():
        file_path = '/data/csv/tiptracking.csv'
        file_dir = os.path.dirname(file_path)
        # check for file directory
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # check for file; if not there, create initial tip count tracking
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as outfile:
                outfile.write("0, 0\n")

    tip_count_list = []
    if protocol.is_simulating():
        tip_count_list = [0, 0]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            tip_count_list = next(csv_reader)

    num_one = int(tip_count_list[0])
    num_two = int(tip_count_list[1])

    """
    protocol goes here
    """

    # write updated tipcount to CSV
    new_tip_count = str(num_one)+", "+str(num_two)+"\n"
    if not protocol.is_simulating():
        with open(file_path, 'w') as outfile:
            outfile.write(new_tip_count)
```

## Tip Tracking with Refills

```
import json
import os
import math

def run(ctx):

    tip_track = True

    # load tipracks
    tips300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot,
                            '200µl filtertiprack')
           for slot in ['3', '6', '8', '9', '10']]

    # load pipette
    m300 = ctx.load_instrument(
        'p300_multi_gen2', 'left', tip_racks=tips300)

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    folder_path = '/data/your_path'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    """ All of your protocol steps go here. Be sure to use _pick_up(pip) to keep track of your tips rather than the standard in pip.pick_up_tip() function. """

    # track final used tip
    if tip_track and not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
```

## Picking Up Fewer Than 8 Tips with a Multi-Channel Pipette

```
def run(ctx):
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', '4')]
    m300 = ctx.load_instrument('p300_multi_gen2', 'right')

    num_channels_per_pickup = 1  # (only pickup tips on front-most channel)
    tips_ordered = [
        tip for rack in tipracks
        for row in rack.rows()[
       len(rack.rows())-num_channels_per_pickup::-1*num_channels_per_pickup]
        for tip in row]

    tip_count = 0

    def pick_up(pip):
        nonlocal tip_count
        pip.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    for i in range(len(tips_ordered)):
        pick_up(m300)
        # perform some step
        m300.drop_tip()
```
