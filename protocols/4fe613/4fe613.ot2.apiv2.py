def get_values(*names):
    import json
    _all_values = json.loads("""{"pcr_samples":"17", "p20s_mount": "right", "p20m_mount": "left"}""")
    return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'PCR/qPCR prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}

def run(protocol):

    [pcr_samples, p20s_mount, p20m_mount] = get_values(  # noqa: F821
        "pcr_samples", "p20s_mount", "p20m_mount")

    pcr_samples = int(pcr_samples)

    # Load Tip Racks
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', 1)
    tiprack_10ul = protocol.load_labware('opentrons_96_tiprack_10ul', 4)

    # Load Pipettes
    p20s = protocol.load_instrument('p20_single_gen2', p20s_mount, tip_racks=[tiprack_20ul])
    p20m = protocol.load_instrument('p20_multi_gen2', p20m_mount, tip_racks=[tiprack_10ul])

    qpcr_mix = protocol.load_labware('opentrons_24_tuberack_generic_2ml_screwcap', 2)['A1']
    cdna_source = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 5) # Replace with USA Scientific PCR tube strip (#1402-3900) + Biorad 96 well rack (#TRC0501)
    pcr_plate = protocol.load_labware('microampoptical_384_wellplate', 3)

    print(pcr_plate.columns()[0])

# How is the qPCR Mix and cDNA being held?

# Step1: Transfer 5.5 µL of qPCR mix to 384 well plate
# Step2: Transfer 4.5 µL of cDNA to 384 well plate and mix
# Select the number of qPCR mix (eg. 8 different genes) and number of cDNA samples without making new protocol
