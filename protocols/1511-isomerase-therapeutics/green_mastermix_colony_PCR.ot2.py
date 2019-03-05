from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Green Mix Colony PCR Prep',
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
greentaq = tuberack.well('A4')
mastermix = tuberack.well('A5')

strip1 = strips.wells('A1', length=8)
strip2 = strips.wells('A2', length=8)


def run_custom_protocol(
    h2o_Ecoli_vol: float = 10.0,
    primer1_vol: float = 1.25,
    primer2_vol: float = 1.25,
    greentaq_vol: float = 12.5,
):

    # create mastermix with 10:1:1 ratio of greentaq:primer1:primer2
    p10.transfer(primer1_vol*10, primer1, mastermix.top(), blow_out=True)
    p10.transfer(primer2_vol*10, primer2, mastermix.top(), blow_out=True)
    p10.transfer(greentaq_vol*10, greentaq, mastermix.top(), blow_out=True)

    # mix mastermix
    p10.pick_up_tip()
    p10.mix(10, 10, mastermix)
    p10.blow_out()
    p10.drop_tip()

    # transfer nuclease-free H2O
    p10.pick_up_tip()
    p10.transfer(
        h2o_Ecoli_vol*2,
        h2o,
        strips.wells('A1', length=8),
        blow_out=True,
        new_tip='never'
        )
    p10.drop_tip()

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
    mm_total_vol = primer1_vol + primer2_vol + greentaq_vol

    p10.transfer(mm_total_vol,
                 mastermix.top(),
                 strip1,
                 blow_out=True,
                 new_tip='always')
