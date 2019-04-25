from opentrons import labware, instruments, modules, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Biorad-96-high-unskirted'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   depth=19.85,
                   diameter=5.5,
                   volume=300)

# labware
start_plate = labware.load(plate_name, '2')
new_plate = labware.load(plate_name, '3')
trough = labware.load('trough-12row', '4')
tips10 = labware.load('tiprack-10ul', '5')
sample_tips = labware.load('opentrons-tiprack-300ul', '6')
reagent_tips = labware.load('opentrons-tiprack-300ul', '7')

# modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(plate_name, '1', share=True)

# pipette
m300 = instruments.P300_Multi(mount='left')

# reagent setup
isopropanol = trough.wells('A1')
beads = trough.wells('A2')
wash_buffer = trough.wells('A3')
DNase = trough.wells('A4')
binding_buffer = trough.wells('A5')
autoclave_ddH2O = trough.wells('A6')
waste = trough.wells('A12')

# tips setup
beads_tip = reagent_tips.wells('A1')
wash_buffer_tip = reagent_tips.wells('A2')
DNase_tip = reagent_tips.wells('A3')
binding_buffer_tip = reagent_tips.wells('A4')
autoclave_ddH2O_tip = reagent_tips.wells('A5')

example = """1,2,3,4,5,6,7,8,9,10,11,12"""


def get_cols_from_csv(file_string):
    whole_file = file_string.splitlines()
    cols = whole_file[0]
    els = cols.split(',')
    return(els)


def run_custom_protocol(volume_autoclave_ddH2O: float = 30,
                        file: FileInput = example):

    # wash function
    def wash():
        magdeck.disengage()
        m300.pick_up_tip(wash_buffer_tip)
        m300.set_flow_rate(aspirate=150)
        m300.distribute(150,
                        wash_buffer,
                        [well.top() for well in mag_samples],
                        new_tip='never')
        m300.return_tip()

        for tip, s in zip(s_tips, mag_samples):
            m300.pick_up_tip(tip)
            m300.mix(10, 150, s)
            m300.return_tip()

        m300.delay(minutes=2)
        robot._driver.run_flag.wait()
        magdeck.engage(height=18)
        m300.delay(minutes=3)
        m300.set_flow_rate(aspirate=25)

        for tip, s in zip(s_tips, mag_samples):
            m300.pick_up_tip(tip)
            m300.transfer(150, s, waste, new_tip='never')
            m300.return_tip()

    # setup samples and tips
    cols = get_cols_from_csv(file)
    start_samples = [start_plate.rows['A'][col] for col in cols]
    mag_samples = [mag_plate.rows['A'][col] for col in cols]
    new_samples = [new_plate.rows['A'][col] for col in cols]
    s_tips = [sample_tips.rows['A'][col] for col in cols]

    for tip, s in zip(s_tips, start_samples):
        m300.pick_up_tip(tip)
        m300.transfer(60,
                      isopropanol,
                      s,
                      new_tip='never')
        m300.mix(10, 60, s)
        m300.return_tip()

    m300.delay(minutes=1)

    m300.pick_up_tip(beads_tip)
    m300.mix(10, 300, beads),
    m300.distribute(100,
                    beads,
                    mag_samples,
                    new_tip='never')
    m300.return_tip()

    for tip, source, dest in zip(s_tips, start_samples, mag_samples):
        m300.pick_up_tip(tip)
        m300.transfer(160,
                      source,
                      dest,
                      new_tip='never')
        m300.mix(15, 160, dest)
        m300.return_tip()

    m300.delay(minutes=10)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)
    m300.set_flow_rate(aspirate=25)

    for tip, s in zip(s_tips, mag_samples):
        m300.pick_up_tip(tip)
        m300.transfer(160, s, waste, new_tip='never')
        m300.return_tip()

    # 2x buffer wash
    for _ in range(2):
        wash()

    magdeck.disengage()

    # distribute DNase, mix, and incubate
    m300.pick_up_tip(DNase_tip)
    m300.distribute(30, DNase, mag_samples, new_tip='never')
    m300.return_tip()
    for tip, s in zip(s_tips, mag_samples):
        m300.pick_up_tip(tip)
        m300.mix(10, 30, s)
        m300.return_tip()
    m300.delay(minutes=30)

    # distribute binding buffer, mix, and incubate
    m300.pick_up_tip(binding_buffer_tip)
    m300.distribute(30, binding_buffer, mag_samples, new_tip='never')
    m300.return_tip()
    for tip, s in zip(s_tips, mag_samples):
        m300.pick_up_tip(tip)
        m300.mix(10, 130, s)
        m300.return_tip()
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)
    for tip, s in zip(s_tips, mag_samples):
        m300.pick_up_tip(tip)
        m300.transfer(130, s, waste, new_tip='never')
        m300.return_tip()

    # 2x buffer wash
    for _ in range(2):
        wash()

    # dry beads
    m300.delay(minutes=3)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # distribute autoclave ddH2O, mix, and incubate
    m300.pick_up_tip(autoclave_ddH2O_tip)
    m300.distribute(volume_autoclave_ddH2O,
                    autoclave_ddH2O,
                    mag_samples,
                    new_tip='never')
    m300.return_tip()
    for tip, s in zip(s_tips, mag_samples):
        m300.pick_up_tip(tip)
        m300.mix(10, volume_autoclave_ddH2O, s)
        m300.return_tip()
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)
    for tip, source, dest in zip(s_tips, mag_samples, new_samples):
        m300.pick_up_tip(tip)
        m300.transfer(volume_autoclave_ddH2O-2, source, dest, new_tip='never')
        m300.drop_tip()
    magdeck.disengage()
