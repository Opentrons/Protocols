from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}


def run_custom_protocol(
    number_of_samples: int=96,
    mastermix_volume: float=40,
    sample_volume: float=1.5
        ):

    # labware setup
    module = modules.load('tempdeck', '8')
    plate = labware.load('96-PCR-tall', '8', share=True)
    epp_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
    epp_rack2 = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
    epp_rack4 = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
    epp_rack5 = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
    mastermix = labware.load('opentrons-tuberack-15ml', '3').wells('A1')
    tiprack10 = labware.load('tiprack-10ul', '10')
    tiprack300 = labware.load('opentrons-tiprack-300ul', '11')

    # instrument setup
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=[tiprack300])
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tiprack10])

    module.set_temperature(4)
    module.wait_for_temp()

    sample_racks = [epp_rack4, epp_rack5, epp_rack1, epp_rack2]
    samples = [
        well for rack in sample_racks for row in rack.rows()
        for well in row][:number_of_samples]

    dests = [well for row in plate.rows() for well in row][:number_of_samples]

    # distribute master mix to PCR wells, mix master mix after every row
    count = 0
    p300.pick_up_tip()
    p300.mix(3, 300, mastermix.bottom(2))
    for dest in dests:
        if p300.current_volume < sample_volume:
            if count >= 12:
                p300.dispense(mastermix.bottom(10))
                p300.mix(3, 300, mastermix.bottom(2))
                count = 0
            p300.aspirate(mastermix.bottom(2))
        p300.dispense(sample_volume, dest)
        count += 1
    p300.dispense(mastermix.bottom(10))
    p300.drop_tip()

    # transfer sample to each well
    for sample, dest in zip(samples, dests):
        p10.pick_up_tip()
        p10.set_flow_rate(aspirate=2, dispense=5)
        p10.transfer(sample_volume, sample, dest, new_tip='never')
        p10.set_flow_rate(dispense=15)
        p10.blow_out(dest)
        p10.touch_tip(dest)
        p10.drop_tip()
