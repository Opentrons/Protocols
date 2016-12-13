from opentrons import containers, instruments

p200rack = containers.load('tiprack-200ul', 'B1')
trough = containers.load('trough-12row', 'C1')
plate = containers.load('96-PCR-flat', 'D1')
trash = containers.load('point', 'D2')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack]
)

b = trough['A1']  # blue food coloring
y = trough['A2']  # yellow food coloring

pixel_volumes = {
    b: 50,  # blue pixels will have 50uL
    y: 100  # yellow pixels will have 100uL
}

_ = None
pixels = [
    _, _, _, _, _, _, y, b,  # 12
    _, _, _, _, y, y, b, _,  # 11
    _, _, _, _, y, b, _, _,  # 10
    _, _, y, y, b, b, b, b,  # 9
    _, _, y, b, b, b, b, b,  # 8
    y, y, b, b, b, b, b, _,  # 7
    _, y, b, b, b, b, b, _,  # 6
    y, y, b, b, b, b, b, _,  # 5
    _, y, b, b, b, b, b, b,  # 4
    _, _, y, b, b, b, b, b,  # 3
    _, _, _, b, b, _, _, _,  # 2
    _, _, _, b, b, _, _, _   # 1
]
#   A  B  C  D  E  F  G  H


def index_to_well(index):
    """
    Returns a well index from an index inside the pixels array
    """
    row = 11 - int(index / 8)
    column = index % 8
    well_index = (row * 8) + column
    return plate[well_index]


def spread_color(source):
    # find all the pixels for this source
    source_pixels = [i for i, val in enumerate(pixels) if val == source]
    if not source_pixels or not source:
        return

    volume = pixel_volumes[source]

    # use a new tip for this source
    p200.pick_up_tip()
    for index in source_pixels:

        # refill the whenever it is empty
        if p200.current_volume < volume:
            p200.aspirate().delay(1).touch_tip()

        # convert the pixel index to the plate well index
        well = index_to_well(index)
        p200.dispense(volume, well).touch_tip()

    # return leftover liquid to the source
    # then return this tip to the tip rack
    p200.blow_out(source).return_tip()


spread_color(b)
spread_color(y)
