from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Custom Cartridge Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
adapter_name = '6x8-cartridge-adapter'
if adapter_name not in labware.list():
    labware.create(
        adapter_name,
        grid=(8, 6),
        spacing=(15, 12.5),
        diameter=3,
        depth=5.3,
        volume=500
    )

reservoir_name = 'Nalgene-300ml-resorvoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=79.30,
        depth=36.7,
        volume=300000
    )

# labware and modules
tempdeck = modules.load('tempdeck', '1')
reservoir = labware.load(reservoir_name, '1', share=True)
tips = labware.load('tiprack-1000ul', '2')

# reagent
oil = reservoir.wells('A1')


def run_custom_protocol(
        number_of_cartridges_to_fill: int = 192,
        number_of_adapters_on_deck: int = 4,
        volume_to_fill_in_microliters: float = 350,
        pipette_mount: StringSelection('right', 'left') = 'right',
        oil_temperature_in_degrees_Celsius: int = 37):

    # pipettes
    p1000 = instruments.P1000_Single(mount=pipette_mount, tip_racks=[tips])

    # set dispense and aspirate speed to acommodate viscous solution
    p1000.set_flow_rate(aspirate=100, dispense=200)

    # check for valid volume
    if volume_to_fill_in_microliters < 100:
        raise Exception("P1000 cannot accommodate volumes less than 100ul.")

    # set tempdeck temperature
    if not robot.is_simulating():
        tempdeck.set_temperature(oil_temperature_in_degrees_Celsius)
        tempdeck.wait_for_temp()

    # load cartridges and set up fill sequence
    cartridges_on_deck = number_of_adapters_on_deck*48
    num_decks = math.ceil(number_of_cartridges_to_fill/cartridges_on_deck)
    num_total_adapters = math.ceil(number_of_cartridges_to_fill/48)
    number_of_adapters_on_deck

    adapters = [labware.load(adapter_name, str(slot))
                for slot in range(3, 3+number_of_adapters_on_deck)]

    # perform transfer
    cartridge_count = 0
    adapter_count = 0
    p1000.pick_up_tip()
    for deck in range(num_decks):
        for adapter in adapters:
            adapter_count += 1
            if adapter_count > num_total_adapters:
                break
            for cartridge in adapter.wells():
                cartridge_count += 1
                if cartridge_count > number_of_cartridges_to_fill:
                    break
                p1000.transfer(
                    volume_to_fill_in_microliters,
                    oil,
                    cartridge.top(),
                    air_gap=50,
                    new_tip='never'
                )
                p1000.blow_out(cartridge.top())
        if deck < num_decks - 1:
            robot.pause('Please replace oil if necessary and cartridges on '
                        'the deck. ' +
                        str(number_of_cartridges_to_fill - cartridge_count) +
                        ' cartridges remaining.')
    p1000.drop_tip()
