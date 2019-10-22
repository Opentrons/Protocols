from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Nucleic Acid Polymerization Validation',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create labware

plates = 'eppendorf_96_wellplate_200ul_pcr'
if plates not in labware.list():
    labware.create(
        plates,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=14.6,
        volume=200
    )

tr6 = labware.load('opentrons_6_tuberack_falcon_50ml_conical', '9',
                   '6 Tube Rack')
tr24a = labware.load('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                     '1', '24 Tube Rack A')
tr24b = labware.load('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                     '2', '24 Tube Rack B')

final = labware.load(plates, '3', 'Final Ortho Reaction')
istock9 = labware.load(plates, '4', '9uM Initiator Stock')
istock45 = labware.load(plates, '5', '0.45uM Initiator Stock')
coolhp = labware.load(plates, '6', 'Snap Cooled HP')

tiprack300_name = 'tipone_96_tiprack_300ul'
if tiprack300_name not in labware.list():
    labware.create(
        tiprack300_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.23,
        depth=59.30
    )

tiprack10_name = 'tipone_96_tiprack_10ul'
if tiprack10_name not in labware.list():
    labware.create(
        tiprack10_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=34
    )

tips10 = [labware.load(tiprack10_name, slot, '10uL Tips')
          for slot in ['7', '8', '11']]
tips300 = [labware.load(tiprack300_name, '10', '300uL Tips')]

aa = ['A' + str(n) for n in range(1, 11)]
bb = ['B' + str(n) for n in range(1, 11)]
cc = ['C' + str(n) for n in range(1, 11)]
dd = ['D' + str(n) for n in [1, 2, 3, 4, 5, 9, 10, 12]]
ee = ['E' + str(n) for n in [1, 2, 3, 4, 5, 9, 10, 12]]
ff = ['F' + str(n) for n in range(1, 11)]
gg = ['G' + str(n) for n in range(1, 11)]
hh = ['H' + str(n) for n in range(1, 11)]

eleven = [l + '11' for l in 'ABCDEFGH']

h2o = tr6.wells('A1')
obuff = tr6.wells('A3')


def run_custom_protocol(p10_mount: StringSelection('left', 'right') = 'left',
                        p300_mount: StringSelection('right', 'left') = 'right'
                        ):

    pip10 = instruments.P10_Single(mount=p10_mount, tip_racks=tips10)
    pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)

    tip10count = 0
    tip300count = 0
    tip10max = len(tips10)*96
    tip300max = len(tips300)*96

    def pick_up(pip):
        nonlocal tip10count
        nonlocal tip300count

        if pip == pip10:
            if tip10count == tip10max:
                robot.pause(
                    'Replace 10ul tips in slots 7, 8, and 11 before resuming.')
                pip10.reset()
                tip10count = 0
            pip10.pick_up_tip()
            tip10count += 1
        else:
            if tip300count == tip300max:
                robot.pause('Replace 300ul tips in slot 10 before resuming.')
                pip300.reset()
                tip300count = 0
            pip300.pick_up_tip()
            tip300count += 1

    # initiator dilution to 0.45uM/system specific mastermix
    iwells = aa + bb + dd + ee + gg + hh
    pick_up(pip300)

    for well in iwells:
        pip300.aspirate(95, h2o)
        pip300.dispense(95, istock45.wells(well).top(-1))

    pip300.drop_tip()

    pick_up(pip10)
    pip10.transfer(12, h2o, tr24a.wells('A3'), new_tip='never')
    pip10.drop_tip()

    d1 = aa + bb
    d2 = dd + ee
    d3 = gg + hh

    for src, dest in zip([d1, d2, d3], ['A1', 'A3', 'A5']):
        for well in src:
            pick_up(pip10)
            pip10.aspirate(8, istock9.wells(well))
            pip10.dispense(5, istock45.wells(well).bottom(5))
            pip10.dispense(3, tr24a.wells(dest).top(-5))
            pip10.blow_out()
            pip10.drop_tip()

    robot.pause('Dilution to 0.45uM complete. When ready, click RESUME.')

    # mixing the mixes
    pick_up(pip300)
    pip300.mix(3, 25, tr24a.wells('A1'))
    pip300.drop_tip()

    for well in iwells:
        pick_up(pip300)
        pip300.mix(3, 40, istock45.wells(well))
        pip300.blow_out(istock45.wells(well).top())
        pip300.drop_tip()

    # initiator in purple to create 0.01x orhton ON
    pick_up(pip300)
    pip300.distribute(57, h2o.bottom(26), istock45.wells(cc+ff+eleven),
                      new_tip='never', disposal_vol=5)
    pip300.drop_tip()

    for src, dest in zip(aa+dd+gg, cc+eleven+ff):
        pick_up(pip10)
        pip10.transfer(3, istock45.wells(src).bottom(8),
                       istock45.wells(dest), new_tip='never')
        pip10.drop_tip()

    robot.pause('Please remove plate from slot 5 to mix/vortex mastermixes. \
    After mixing, replace the plate and click RESUME.')

    # initiator in purple to create 0.01x Crosstalk

    pick_up(pip10)
    pip10.distribute(3, tr24a.wells('A3'), istock9.wells(cc+ff).top(-4))

    pick_up(pip10)
    pip10.distribute(3, tr24a.wells('A1'), istock9.wells(ff).top(-4))

    pick_up(pip10)
    pip10.distribute(3, tr24a.wells('A1'), istock9.wells(eleven[3:]).top(-4))

    pick_up(pip10)
    pip10.distribute(3, tr24a.wells('A1'), istock9.wells('G11', 'H11').top(-4))

    for well in cc+eleven:
        pick_up(pip10)
        pip10.transfer(3, tr24a.wells('A5').bottom(8),
                       istock9.wells(well).top(-4), new_tip='never')
        pip10.drop_tip()

    for i, (src1, src2) in enumerate(zip(aa, bb)):
        d = cc[:i]+cc[i+1:]
        for well in d:
            pick_up(pip10)
            pip10.transfer(3, istock9.wells(src1),
                           istock9.wells(well), new_tip='never')
            pip10.drop_tip()
            pick_up(pip10)
            pip10.transfer(3, istock9.wells(src2),
                           istock9.wells(well), new_tip='never')
            pip10.drop_tip()

    for i, (src1, src2) in enumerate(zip(gg, hh)):
        d = ff[:i]+ff[i+1:]
        for well in d:
            pick_up(pip10)
            pip10.transfer(3, istock9.wells(src1),
                           istock9.wells(well), new_tip='never')
            pip10.drop_tip()
            pick_up(pip10)
            pip10.transfer(3, istock9.wells(src2),
                           istock9.wells(well), new_tip='never')
            pip10.drop_tip()

    for i, (src1, src2) in enumerate(zip(dd, ee)):
        d = eleven[:i]+eleven[i+1:]
        for well in d:
            pick_up(pip10)
            pip10.transfer(3, istock9.wells(src1),
                           istock9.wells(well), new_tip='never')
            pip10.drop_tip()
            pick_up(pip10)
            pip10.transfer(3, istock9.wells(src2),
                           istock9.wells(well), new_tip='never')
            pip10.drop_tip()

    robot.pause('Crosstalk complete. Please remove plate from slot 4 and mix/\
    vortex. After replacing the plate, click RESUME.')

    # mastermix

    pick_up(pip300)
    pick_up(pip10)

    mmlist = (tr24b.rows('A')+tr24b.rows('B')+tr24b.rows('C')
              + tr24b.rows('D')+tr24a.wells('D3', 'D4', 'D5', 'D6'))

    for well in mmlist:
        pip300.transfer(470, obuff.bottom(30), well.top(-4), new_tip='never')
        pip10.transfer(1.9, obuff.bottom(30), well.top(-4), new_tip='never')

    pip300.drop_tip()
    pip10.drop_tip()

    for src1, src2, dest in zip(aa+dd+gg, bb+ee+hh, mmlist):
        for src in [src1, src2]:
            pick_up(pip10)
            pip10.transfer(9.9, coolhp.wells(src), dest, new_tip='never')
            pip10.blow_out(dest.top())
            pip10.drop_tip()

    robot.pause('Mastermix prep is complete. Please remove plates from deck \
    for mixing/vortex. When ready, replace plates and click RESUME.')

    # Setting up Ortho Reaction

    orlist = [i + str(k) for i in 'ABCDEFGH' for k in range(1, 13)]
    for j in range(7, 13):
        orlist.remove('C'+str(j))
        orlist.remove('H'+str(j))

    pick_up(pip10)
    pip10.distribute(4, tr24a.wells('D2').top(-25), final.wells(orlist))

    n = 3
    orchunk = [orlist[i * n:(i + 1) * n]
               for i in range((len(orlist) + n - 1) // n)]

    for src, dest in zip(mmlist, orchunk):
        pick_up(pip300)
        pip300.mix(4, 180, src)
        for d in dest:
            pip300.transfer(146, src, final.wells(d), new_tip='never')
        pip300.drop_tip()

    orl1 = orlist[1::3]
    orl2 = orlist[2::3]

    robot.pause('Remove plates and vortex/spin. When ready, replace plate and \
    click RESUME.')

    for src, dest in zip(cc+eleven+ff, orl1):
        pick_up(pip10)
        pip10.transfer(4, istock45.wells(src),
                       final.wells(dest).bottom(8), new_tip='never')
        pip10.drop_tip()

    for src, dest in zip(cc+eleven+ff, orl2):
        pick_up(pip10)
        pip10.transfer(4, istock9.wells(src),
                       final.wells(dest).bottom(8), new_tip='never')
        pip10.drop_tip()

    robot.comment('Congrats! The protocol is now complete!')
