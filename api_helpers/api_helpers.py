def find_aspirate_volume(vol, pipette):
    aspirate_volume = 0
    if isinstance(vol, (int, float, complex)):
        remaining_volume = pipette.max_volume - pipette.current_volume
        aspirate_volume = vol * int(remaining_volume / vol)
    elif isinstance(vol, (list, iter)):
        n = 0
        while n >= len(vol):
            if pipette.current_volume + vol[n] > pipette.max_volume:
                break
            aspirate_volume += vol[n]
            n += 1

    if not aspirate_volume:
        aspirate_volume = pipette.max_volume
    return aspirate_volume


def match_volume_and_wells(volume, sources, targets):
    # if both are lists, check they're the same length
    if isinstance(sources, list) and isinstance(targets, list):
        if not len(sources) == len(targets):
            raise RuntimeError('Sources and Targets list lengths do not match')

    if not isinstance(sources, list):
        sources = [sources]
    if not isinstance(targets, list):
        targets = [targets]

    # determine how long the volumes list should be
    length = max(len(sources), len(targets))

    if isinstance(volume, list) and len(volume) != length:
        raise RuntimeError('Length of volumes does not match length of wells')
    else:
        volume = [volume] * length

    return (volume, sources, targets)


def transfer(pipette, volumes, sources, targets, **kwargs):

    tips = kwargs.get('tips', 1)
    rate = kwargs.get('rate', 1.0)
    mix = kwargs.get('mix', (0, 0))
    touch = kwargs.get('touch', True)
    blow = kwargs.get('blow', True)

    volumes, sources, targets = match_volume_and_wells(
        volumes, sources, targets)

    if tips == 1:
        pipette.pick_up_tip()

    for i in range(len(volumes)):
        t = targets[i] if len(targets) > 1 else targets[0]
        s = sources[i] if len(sources) > 1 else sources[0]
        if tips > 1:
            pipette.pick_up_tip()
        amount_remaining = volumes[i] + 0
        while amount_remaining > 0:
            if pipette.current_volume < volumes[i]:
                v = find_aspirate_volume(volumes[i:], pipette)
                pipette.aspirate(v, s, rate=rate)
                pipette.delay(1)
                if touch:
                    pipette.touch_tip()
            dispense_volume = min(volumes[i], pipette.current_volume)
            amount_remaining -= dispense_volume
            pipette.dispense(dispense_volume, t, rate=rate)
            if isinstance(mix, tuple) and len(mix) > 1:
                if mix[0] and mix[1]:
                    pipette.mix(mix[0], mix[1])
            if touch:
                pipette.touch_tip()
            if blow and pipette.current_volume == 0:
                pipette.blow_out()
        if tips > 1:
            pipette.drop_tip()

    if tips == 1:
        pipette.drop_tip()






