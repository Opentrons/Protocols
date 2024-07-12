import math
from opentrons.protocol_api.labware import Well

metadata = {
    'protocolName': 'Tube Filling',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(protocol):
    [transferVol, tubeRacks, tubeType, numRacks, srcType, srcVol,
     pipType, pipMnt, startTip, dispMode, touchTip] = get_values(  # noqa: F821
     'transferVol', 'tubeRacks', 'tubeType', 'numRacks', 'srcType', 'srcVol',
     'pipType', 'pipMnt', 'startTip', 'dispMode', 'touchTip')

    # Load labware and pipettes

    tipNum = pipType.split('_')[0][1:]
    tipNum = '300' if tipNum == '50' else tipNum
    tipType = f'opentrons_96_tiprack_{tipNum}ul'
    tips = [protocol.load_labware(tipType, '11')]
    pip = protocol.load_instrument(pipType, pipMnt, tip_racks=tips)

    firstTip = startTip[0].upper()+str(int(startTip[1:]))
    pip.starting_tip = tips[0][firstTip]

    srcLabware = protocol.load_labware(srcType, '1')

    destRacks = [
        protocol.load_labware(tubeRacks+tubeType, slot) for slot in range(
            2, 2+numRacks)]

    # Functions and Class creation
    if not protocol.is_simulating:
        class WellH(Well):
            def __init__(self, well, min_height=5, comp_coeff=1.15,
                         current_volume=0):
                super().__init__(well._impl)
                self.well = well
                self.min_height = min_height
                self.comp_coeff = comp_coeff
                self.current_volume = current_volume
                if self.diameter is not None:
                    self.radius = self.diameter/2
                    cse = math.pi*(self.radius**2)
                elif self.length is not None:
                    cse = self.length*self.width
                self.height = (
                 current_volume/cse) - (0.2*pip._tip_racks[0].wells()[0].depth)
                if self.height < min_height:
                    self.height = min_height
                elif self.height > well.parent.highest_z:
                    raise Exception("""Specified liquid volume
                    can not exceed the height of the labware.""")

            def height_dec(self, vol):
                if self.diameter is not None:
                    cse = math.pi*(self.radius**2)
                elif self.length is not None:
                    cse = self.length*self.width
                dh = (vol/cse)*self.comp_coeff
                if self.height - dh > self.min_height:
                    self.height = self.height - dh
                else:
                    self.height = self.min_height
                if self.current_volume - vol > 0:
                    self.current_volume = self.current_volume - vol
                else:
                    self.current_volume = 0
                return(self.well.bottom(self.height))

            def height_inc(self, vol, top=False):
                if self.diameter is not None:
                    cse = math.pi*(self.radius**2)
                elif self.length is not None:
                    cse = self.length*self.width
                ih = (vol/cse)*self.comp_coeff
                if self.height < self.min_height:
                    self.height = self.min_height
                if self.height + ih < self.depth:
                    self.height = self.height + ih
                else:
                    self.height = self.depth
                self.current_volume += vol
                if top is False:
                    return(self.well.bottom(self.height))
                else:
                    return(self.well.top())

        def yield_groups(list, num):
            """
            yield lists based on number of items
            """
            for i in range(0, len(list), num):
                yield list[i:i+num]

        # get number of distributes pipette can handle
        distribute_num = pip.max_volume // transferVol
        if distribute_num < 1:
            # if transfer volume is greater than pipette max volume,
            # use Transfer mode
            dispMode = 'Transfer'

        # create source location with WellH
        source = WellH(
            srcLabware.wells()[0], min_height=3, current_volume=srcVol*1000)

        # Protocol: Tube filling
        pip.pick_up_tip()
        all_wells = [well for tuberack in destRacks for well in tuberack.wells()]
        if dispMode == 'Transfer':
            for dest in all_wells:
                pip.transfer(
                    transferVol, source.height_dec(transferVol), dest,
                    touch_tip=touchTip, new_tip='never')
        else:
            well_groups = list(yield_groups(all_wells, int(distribute_num)))
            for wells in well_groups:
                pip.distribute(
                    transferVol, source.height_dec(transferVol), wells,
                    blow_out=source, touch_tip=touchTip, new_tip='never')
        pip.drop_tip()
