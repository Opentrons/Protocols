from opentrons import robot, containers, instruments


def find_aspirate_volume(vol, pipette):
    aspirate_volume = 0
    if isinstance(vol, (int, float, complex)):
        remaining_volume = pipette.max_volume - pipette.current_volume
        aspirate_volume = min(vol, remaining_volume)
    elif isinstance(vol, (list, iter)):
        n = 0
        total_aspirated = pipette.current_volume
        while n < len(vol):
            if total_aspirated + vol[n] > pipette.max_volume:
                break
            aspirate_volume += vol[n]
            total_aspirated += aspirate_volume
            n += 1

    if not aspirate_volume:
        aspirate_volume = vol[0] if isinstance(vol, list) else vol
    return min(aspirate_volume, pipette.max_volume)


def match_volume_and_wells(volumes, sources, targets):

    volumes = [volumes] if not isinstance(volumes, list) else volumes
    sources = [sources] if not isinstance(sources, list) else sources
    targets = [targets] if not isinstance(targets, list) else targets
    length = max(len(sources), len(targets))
    if length > min(len(sources), len(targets)) > 1:
        raise RuntimeError('Sources and Targets list lengths do not match')
    if len(volumes) != length:
        if len(volumes) == 1:
            volumes *= length
        else:
            raise RuntimeError(
                'Length of volumes does not match length of wells')
    return (volumes, sources, targets)


def transfer_single(pipette, volumes, source, target, **kwargs):

    tips = kwargs.get('tips', 1)
    rate = kwargs.get('rate', 1)
    delay = kwargs.get('delay', 0.5)
    touch = kwargs.get('touch', True)
    mix = kwargs.get('mix', (0, 0))
    blow = kwargs.get('blow', True)
    trash = kwargs.get('trash', True)
    separate = kwargs.get('separate', False)

    if not isinstance(volumes, list):
        volumes = [volumes]

    if tips > 0:
        pipette.pick_up_tip()

    amount_remaining = volumes[0]
    while amount_remaining > 0:

        volumes[0] = min(volumes[0], amount_remaining)
        if pipette.current_volume < volumes[0]:
            if separate:
                aspirate_volume = find_aspirate_volume(volumes[0], pipette)
            else:
                aspirate_volume = find_aspirate_volume(volumes, pipette)
            pipette.aspirate(aspirate_volume, source, rate=rate)

            if delay:
                pipette.delay(delay)
            if touch:
                pipette.touch_tip()

        dispense_volume = min(volumes[0], pipette.current_volume)
        amount_remaining -= dispense_volume
        pipette.dispense(dispense_volume, target, rate=rate)

        if isinstance(mix, tuple) and len(mix) > 1 and sum(mix):
            pipette.mix(mix[0], mix[1])
        if touch:
            pipette.touch_tip()
        if blow and pipette.current_volume == 0:
            pipette.blow_out()

    if tips > 0:
        if trash:
            pipette.drop_tip()
        else:
            pipette.return_tip()


def transfer(pipette, volumes, sources, targets, **kwargs):

    tips = kwargs.get('tips', 1)
    trash = kwargs.get('trash', True)

    volumes, sources, targets = match_volume_and_wells(
        volumes, sources, targets)

    if tips == 1:
        pipette.pick_up_tip()

    for i in range(len(volumes)):
        s = sources[i] if len(sources) > 1 else sources[0]
        t = targets[i] if len(targets) > 1 else targets[0]
        kwargs['tips'] = 0 if tips <= 1 else 1
        kwargs['separate'] = kwargs.get(
            'separate',
            True if len(sources) > 1 else False)
        transfer_single(pipette, volumes[i:], s, t, **kwargs)

    if tips == 1:
        if trash:
            pipette.drop_tip()
        else:
            pipette.return_tip()


instruments.Pipette.transfer = transfer

if __name__ == '__main__':
    rack = containers.load('tiprack-200ul', 'A1')
    plate = containers.load('96-flat', 'B1')
    p = instruments.Pipette(axis='b', max_volume=200, tip_racks=[rack])
    p.transfer(100, plate[0:5], plate[1:6])
    for c in robot.commands():
        print(c)
