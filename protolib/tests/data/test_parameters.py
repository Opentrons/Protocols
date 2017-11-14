from opentrons import containers, instruments


class StringSelection(object):
    def __init__(self, *containers):
        self.accepted_containers = containers

    def generate_options(self):
        def humanize(txt):
            return txt.replace('-', ' ').replace('_', ' ')

        return [
            {'value': option, 'text': humanize(option)}
            for option in self.accepted_containers]

    def get_json(self):
        # Of the form:
        # {type: 'StringSelection',
        # options: [{value: '96-flat', text: '96 flat'}, ...]}
        return {
            'type': 'StringSelection',
            'options': self.generate_options()}


def run_custom_protocol(
  a: int=12,
  b='woo',
  plate_type: StringSelection('96-flat', '96-PCR-flat', '96-PCR-tall')='96-flat'):  # noqa: E501

    p200rack = containers.load(
        'tiprack-200ul',  # container type
        'A1'             # slot
    )

    trough = containers.load(
        'trough-12row',
        'A3',
        'trough'
    )

    trash = containers.load(
        'point',
        'B2',
        'trash'
    )

    p200 = instruments.Pipette(
        trash_container=trash,
        tip_racks=[p200rack],
        min_volume=20,  # actual minimum volume of the pipette
        axis="a",
        channels=8
    )

    p200.transfer(100, trough.wells(0), trough.wells(1))
