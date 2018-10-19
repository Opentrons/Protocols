from opentrons import labware, instruments

# labware setup
output = labware.load('96-flat', '2')
fwd_primers = labware.load('96-flat', '1')
rvs_primers = labware.load('96-flat', '3')
dna = labware.load('96-flat', '5')
mastermix = labware.load('opentrons-tuberack-2ml-eppendorf', '4').wells('A1')

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['6', '7', '8']]
tipracks_50 = labware.load('tiprack-200ul', '9')

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_10)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tipracks_50])


def run_custom_protocol(
        mastermix_volume: float=22.5,
        forward_primer_volume: float=0.5,
        reverse_primer_volume: float=1,
        DNA_volume: float=1):

    p50.distribute(mastermix_volume, mastermix, output.wells(), new_tip='once')

    m10.transfer(
        forward_primer_volume, fwd_primers.cols(), output.cols(),
        new_tip='always', blow_out=True)

    m10.transfer(
        reverse_primer_volume, rvs_primers.cols(), output.cols(),
        new_tip='always', blow_out=True)

    for source, dest in zip(dna.cols(), output.cols()):
        m10.pick_up_tip()
        m10.transfer(DNA_volume, source, dest, new_tip='never', blow_out=True)
        m10.mix(3, 10, dest)
        m10.drop_tip()
