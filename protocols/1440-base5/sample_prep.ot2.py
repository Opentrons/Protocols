from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'MDA Sample Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

# labware setup
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
temp_module = modules.load('tempdeck', '4')
temp_rack = labware.load('opentrons-aluminum-block-2ml-eppendorf', '4',
                         share=True)
strip_block = labware.load('opentrons-aluminum-block-PCR-strips-200ul', '2')
pcr_strips = labware.load('PCR-strip-tall', '2', share=True)
tiprack = labware.load('tiprack-10ul', '5')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack])

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack])

# reagent setup
mastermix = temp_rack.wells('A1')
exo_res = temp_rack.wells('B1')
neut_buffer = temp_rack.wells('C1')
d1 = tuberack.wells('A1')
samples = pcr_strips.cols('1')
reactions = pcr_strips.cols('2')


def change_flow_rate(pipette, aspirate, dispense):
    pipette.set_flow_rate(aspirate=aspirate, dispense=dispense)


def use_default_flow_rate(pipette):
    pipette.set_flow_rate(aspirate=5, dispense=10)


def run_custom_protocol(
        mix_aspirate_speed: float=5,
        mix_dispense_speed: float=10):

    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    for well in samples:
        p10.pick_up_tip()
        p10.transfer(5, exo_res, well, new_tip='never')
        change_flow_rate(p10, mix_aspirate_speed, mix_dispense_speed)
        p10.mix(5, 4, well)
        use_default_flow_rate(p10)
        p10.blow_out(well.top())
        p10.drop_tip()

    p10.delay(minutes=5)

    m10.pick_up_tip(tiprack.cols('2'))
    m10.transfer(2, samples, reactions, new_tip='never')
    m10.blow_out()
    m10.drop_tip()

    p10.start_at_tip(tiprack.wells('A3'))
    for well in reactions:
        p10.pick_up_tip()
        p10.transfer(2, d1, well, new_tip='never')
        change_flow_rate(p10, mix_aspirate_speed, mix_dispense_speed)
        p10.mix(2, 2, well)
        use_default_flow_rate(p10)
        p10.blow_out(well.top())
        p10.drop_tip()

    p10.delay(minutes=3, seconds=30)

    for well in reactions:
        p10.pick_up_tip()
        p10.transfer(4, neut_buffer, well, new_tip='never')
        change_flow_rate(p10, mix_aspirate_speed, mix_dispense_speed)
        p10.mix(2, 4, well)
        use_default_flow_rate(p10)
        p10.blow_out(well.top())
        p10.drop_tip()

    for well in reactions:
        p10.pick_up_tip()
        p10.transfer(6, mastermix, well, new_tip='never')
        change_flow_rate(p10, mix_aspirate_speed, mix_dispense_speed)
        p10.mix(5, 10, well)
        use_default_flow_rate(p10)
        p10.blow_out(well.top())
        p10.drop_tip()
