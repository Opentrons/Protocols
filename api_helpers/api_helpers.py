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


def transfer(source, targets, volumes, pipette, rate=1.0, mix=None, tip=1):
    if isinstance(source, list) and isinstance(targets, list):
        if not len(source) == len(targets):
            raise RuntimeError('Sources and Targets list lengths do not match')
    if not isinstance(source, list) and not isinstance(targets, list):
        targets = [targets]
    if not isinstance(volumes, list):
        if isinstance(source, list):
            volumes = [volumes] * len(source)
        else:
            volumes = [volumes] * len(targets)

    if tip == 1:
        pipette.pick_up_tip()

    for i, well in enumerate(targets):

        # keep track of how much we've dispensed
        amount_remaining = volumes[i] * 1
        while amount_remaining > 0:

            if tip > 1:
                pipette.pick_up_tip()

            # aspirate
            if pipette.current_volume < volumes[i]:
                aspirate_volume = find_aspirate_volume(volumes[i:], pipette)
                pipette.aspirate(aspirate_volume, rate=rate)
                pipette.delay(1).touch_tip()

            pipette.dispense(volumes[i], well, rate=rate)

            # mix if specified
            if isinstance(mix, tuple) and len(mix) > 1:
                pipette.mix(mix[0], mix[1])

            pipette.touch_tip()

            # blowout if we're able to
            if pipette.current_volume == 0:
                pipette.blow_out()

            amount_remaining -= volumes[i]

            if tip > 1:
                pipette.drop_tip()

    pipette.blow_out()
    if tip == 1:
        pipette.drop_tip()
