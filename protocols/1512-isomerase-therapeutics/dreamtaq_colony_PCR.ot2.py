from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Dreamtaq Colony PCR Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# module
module = modules.load('tempdeck', '2')
strips = labware.load(
    'opentrons-aluminum-block-PCR-strips-200ul',
    '2',
    share=True
    )
module.set_temperature(4)
module.wait_for_temp()

# labware
tuberack = labware.load('tube-rack-2ml', '1')
tiprack = labware.load('tiprack-10ul', '4')

# pipettes
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tiprack]
)

# reagent and PCR strip setup
h2o = tuberack.wells('A1')
primer1 = tuberack.wells('A2')
primer2 = tuberack.wells('A3')
dreamtaq_buffer = tuberack.wells('A4')
dNTP = tuberack.wells('A5')
dreamtaq_polymerase = tuberack.wells('A6')
mastermix = tuberack.wells('B1')

strip1 = strips.wells('A1', length=8)
strip2 = strips.wells('A2', length=8)


def run_custom_protocol(
    h2o_Ecoli_vol=10,
    h2o_mastermix_vol=9.75,
    primer1_vol=1.25,
    primer2_vol=1.25,
    dreamtaq_buffer_vol=2.5,
    dNTP_vol=2.5,
    dreamtaq_polymerase_vol=0.25
):

    # create mastermix with 10:1:1 ratio of greentaq:primer1:primer2
    p10.transfer(h2o_mastermix_vol*10, h2o, mastermix.top(), blow_out=True)
    p10.transfer(primer1_vol*10, primer1, mastermix.top(), blow_out=True)
    p10.transfer(primer2_vol*10, primer2, mastermix.top(), blow_out=True)
    p10.transfer(dreamtaq_buffer_vol*10,
                 dreamtaq_buffer,
                 mastermix.top(),
                 blow_out=True)
    p10.transfer(dNTP_vol*10, dNTP, mastermix.top(), blow_out=True)
    p10.transfer(dreamtaq_polymerase_vol*10,
                 dreamtaq_polymerase,
                 mastermix.top(),
                 blow_out=True)

    # mix mastermix
    p10.pick_up_tip()
    p10.mix(10, 10, mastermix)
    p10.blow_out()
    p10.drop_tip()

    # transfer nuclease-free H2O
    p10.transfer(
        h2o_Ecoli_vol*2,
        h2o,
        strips.wells('A1', length=8),
        blow_out=True
        )

    # pause for E. coli transfer and resuspension
    robot.pause('Add E. coli to strip 1 and resuspend')

    # transfer from strip 1 to strip 2
    p10.transfer(
        h2o_Ecoli_vol,
        strip1,
        strip2,
        new_tip='always',
        blow_out=True
        )

    # add master mix to each strip tube
    mm_total_vol = h2o_mastermix_vol + primer1_vol + primer2_vol +\
        dreamtaq_buffer_vol + dNTP_vol + dreamtaq_polymerase_vol
    p10.transfer(mm_total_vol,
                 mastermix.top(),
                 strip1,
                 blow_out=True,
                 new_tip='always')
