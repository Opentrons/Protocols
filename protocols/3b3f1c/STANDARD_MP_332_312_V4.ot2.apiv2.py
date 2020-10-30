import math

metadata = {
    'protocolName': 'STANDARD MP 332 312 V4',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    # input_csv = get_values(  # noqa: F821
    #     'input_csv')

    input_csv = """Genealogy:,,332 312,,,,,,,,,,,,,,,,
,,Liquid,"Initial
Volume (ul)","Starting
Height (mm)",Location,,,,,,,,,,,,,
STD:,,AZ60,500,14.5,1,H12,,System inputs,,,,,,,,,,
QC:,,AZ61,1000,22,1,H11,,,,,,,,,,,,
IS:,,AZ75,500,14.5,1,H1,,,,,,,,,,,,
Diluent:,,H2O,50000,91,3,A3,,,,,,,,,,,,
Mobile Phase:,,H2O/ACN,14000,100,3,C1,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,A,B,C,,,,,,,,,,,
P300 Polynominal Curve Fit    (Ax2 + Bx + C),,,,,-1.31669E-05,0.012851617,0.395873513,,,,,,,,,,,
P1000 Polynominal Curve Fit    (Ax2 + Bx + C),,,,,3.81294E-06,0.001352275,0.567650869,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
Dilution Template As Listed in Method,,,,,,,,,"OT2 Volume
Programming",Source Location,,Desitination Location,,"OT2 Volume
Programming",Destination Location,,,
STD,"Location
Slot           Well",,"Conc.
(ng/ml)","WS Conc.
(ng/ml)","Final Volume
(ml)","STD Conc.
(ng/ml)","STD Volume
(ul)","Diluent Volume
(ul)","STD Volume
(ul)",Slot,Well,Slot,Well,"Diluent Volume
(ul)",Slot,Well,,
DQC,2,A1,10000,200000,3,1000000,600,2400,596.6,1,H11,2,A1,2382,2,A1,,
ULOQC,2,A2,1000,20000,3,1000000,60,2940,58.9,1,H11,2,A2,2912,2,A2,,
8,2,A3,1000,20000,3,1000000,60,2940,58.9,1,H12,2,A3,2912,2,A3,,
7,2,A4,900,18000,3,1000000,54,2946,52.9,1,H12,2,A4,2917,2,A4,,
HQC,2,A5,800,16000,3,1000000,48,2952,47.0,1,H11,2,A5,2923,2,A5,,
6,2,B1,500,10000,3,1000000,30,2970,29.2,1,H12,2,B1,2941,2,B1,,
5,2,B2,100,2000,2,10000,400,1600,396.6,2,B1,2,B2,1593,2,B2,,
MQC,2,B3,30,600,2,16000,75,1925,73.7,2,A5,2,B3,1914,2,B3,,
4,2,B4,25,500,2,10000,100,1900,98.5,2,B1,2,B4,1889,2,B4,,
3,2,C1,5,100,3,10000,30,2970,29.2,2,B1,2,C1,2941,2,C1,,
LQC,2,C2,3,60,2,600,200,1800,197.6,2,B3,2,C2,1791,2,C2,,
2,2,C3,2,40,3,2000,60,2940,58.9,2,B2,2,C3,2912,2,C3,,
1,2,C4,1,20,3,2000,30,2970,29.2,2,B2,2,C4,2941,2,C4,,
LLOQC,2,C5,1,20,3,600,100,2900,98.5,2,B3,2,C5,2872,2,C5,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,

"""

    class tube():

        def __init__(self, tube, height=0, min_height=5, comp_coeff=1.1):
            self.tube = tube
            self.height = height
            self.radius = tube._diameter/2
            self.min_height = min_height
            self.comp_coeff = comp_coeff

        def height_dec(self, vol):
            dh = vol/(math.pi*(self.radius**2))
            if self.height - dh > self.min_height:
                self.height = self.height - dh
            else:
                self.height = self.min_height
            return(self.tube.bottom(self.height))

        def height_inc(self, vol):
            dh = vol/(math.pi*(self.radius**2))
            if self.height + dh < self.tube._depth:
                self.height = self.height + dh
            else:
                self.height = self.tube._depth
            return(self.tube.bottom(self.height))

    # load labware
    plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '1',
                             'TEST PLATE 2ML 96 WELL STANDARD, QC, AND IS')
    tuberack15 = ctx.load_labware('opentrons_15_tuberack_nest_15ml_conical',
                                  '2', 'WS AND QC SOLUTIONS')
    tuberack15_50 = ctx.load_labware(
        'opentrons_10_tuberack_nest_4x50ml_6x15ml_conical', '3',
        'DILUENT AND MOBILE PHASE')

    ws_1_4 = [
        ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', slot,
                         'WS ' + '1-4' + ' ' + let)
        for slot, let in zip(['7', '8'], 'AB')]
    ws_5_8 = [
        ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap',
                         slot, 'WS ' + '5-8' + ' ' + let)
        for slot, let in zip(['4', '5'], 'AB')]
    qc = [
        ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap',
                         slot, 'QC ' + let)
        for slot, let in zip(['9', '6'], 'AB')]
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '10')]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '11')]

    p300 = ctx.load_instrument('p300_single_gen2', 'left',
                               tip_racks=tiprack300)
    p1000 = ctx.load_instrument('p1000_single_gen2', 'right',
                                tip_racks=tiprack1000)
    p300.flow_rate.blow_out = 300
    p1000.flow_rate.blow_out = 1000

    # start reagent setup
    tubes_dict = {
        well: tube(well)
        for rack in [tuberack15_50, tuberack15, ]
        for well in rack.wells()
    }
    diluent = tuberack15_50.wells_by_name()['A3']
    tubes_dict[diluent].height = 90

    # tip conditioning
    dil_dest = tuberack15_50.wells()[0]

    def tip_condition(pip, vol):
        pip.pick_up_tip()
        pip.flow_rate.aspirate = pip.max_volume/2
        pip.flow_rate.dispense = pip.max_volume
        for i in range(2):
            mix_reps = 2 - i
            pip.transfer(vol, tubes_dict[diluent].height_dec(vol),
                         dil_dest.bottom(104),
                         mix_before=(mix_reps, pip.max_volume*2/3),
                         new_tip='never')
            tubes_dict[dil_dest].height_inc(vol)
            pip.blow_out(dil_dest.bottom(104))

    # create serial dilution from .csv file
    # data = [
    #     line.split(',')[9:17] for line in input_csv.splitlines()[14:28]
    #     if line and line.split(',')[0]]
    data = [
        line.split(',')[:17] for line in input_csv.splitlines()[27:41]
        if line and line.split(',')[0]]

    # first set of tip conditioning
    tip_condition(p1000, 500)

    # pre-add diluent in reverse
    for line in data[::-1]:
        dest = ctx.loaded_labwares[int(line[12])].wells_by_name()[line[13]]
        dil_vol = float(line[14])
        num_trans = math.ceil(dil_vol/p1000.max_volume)
        vol_per_trans = dil_vol/num_trans
        asp_rate = vol_per_trans if vol_per_trans < 150 else 150
        disp_rate = 2*vol_per_trans if vol_per_trans > 37 else 150
        p1000.flow_rate.aspirate = asp_rate
        p1000.flow_rate.dispense = disp_rate
        for n in range(num_trans):
            p1000.transfer(vol_per_trans,
                           tubes_dict[diluent].height_dec(vol_per_trans),
                           tubes_dict[dest].height_inc(vol_per_trans),
                           new_tip='never')
            p1000.blow_out(dest.bottom(tubes_dict[dest].height))
    p1000.drop_tip()

    # parse std sources
    std_dict = {}
    for line in data:
        std = ctx.loaded_labwares[int(line[10])].wells_by_name()[line[11]]
        dest = ctx.loaded_labwares[int(line[12])].wells_by_name()[line[13]]
        std_vol = float(line[9])
        if std in std_dict:
            std_dict[std].append({'dest': dest, 'vol': std_vol})
        else:
            std_dict[std] = [{'dest': dest, 'vol': std_vol}]

    # add standards to pre-added diluents
    for std, vals in std_dict.items():
        if std.parent.parent == '2':
            if p1000.hw_pipette['has_tip']:
                p1000.drop_tip()
            p1000.pick_up_tip()
            p1000.flow_rate.aspirate = 500
            p1000.flow_rate.dispense = 1000
            p1000.flow_rate.blow_out = 1000
            p1000.mix(5, 1000, std.bottom(tubes_dict[std].height))
            p1000.blow_out(std.top(-2))
            p1000.drop_tip()
        # p300 tip condition
        tip_condition(p300, 150)
        for val in vals:
            dest = val['dest']
            vol = val['vol']
            num_trans = math.ceil(vol/p300.max_volume)
            vol_per_trans = vol/num_trans
            dest_loc = tubes_dict[dest].height_inc(vol)
            asp_rate = vol_per_trans if vol_per_trans < 150 else 150
            disp_rate = 2*vol_per_trans if vol_per_trans > 37 else 150
            p300.flow_rate.aspirate = asp_rate
            p300.flow_rate.dispense = disp_rate
            for n in range(num_trans):
                dest_loc = dest.bottom(tubes_dict[dest].height)
                p300.transfer(vol_per_trans, std.bottom(1),
                              dest_loc, new_tip='never')
                p300.blow_out(dest_loc)
        p300.drop_tip()

    # aliquots
    ws_dests_1_4 = [
        well
        for set in [ws_1_4[0].rows()[i] + ws_1_4[1].rows()[i][:4]
                    for i in range(len(ws_1_4[0].rows()))]
        for well in set]
    ws_dests_5_8 = [
        well
        for set in [ws_5_8[0].rows()[i] + ws_5_8[1].rows()[i][:4]
                    for i in range(len(ws_5_8[0].rows()))]
        for well in set]
    ws_dests_all = ws_dests_1_4 + ws_dests_5_8
    # for line in data[:-1]:

    qc_dests = [
        well
        for set in [qc[0].columns()[i] + qc[1].columns()[i]
                    for i in range(len(qc[0].columns())-1, -1, -1)]
        for well in set]
    [qc_dests.remove(well) for well in [
        qc[0].wells_by_name()['B1'],
        qc[0].wells_by_name()['C1'],
        qc[1].wells_by_name()['B6']]]

    std_5x = ['DQC', 'ULOQC', 'LLOQC']
    ws_counter = 0
    qc_counter = 0
    for line in data[::-1]:
        std_name = line[0]
        std = ctx.loaded_labwares[int(line[12])].wells_by_name()[line[13]]
        dest_set = qc_dests if 'QC' in std_name else ws_dests_all
        counter = qc_counter if 'QC' in std_name else ws_counter
        num_aliquots = 5 if std_name in std_5x else 10
        aliquots = dest_set[counter:counter+num_aliquots]

        # mix
        if p1000.hw_pipette['has_tip']:
            p1000.drop_tip()
        p1000.pick_up_tip()
        p1000.flow_rate.aspirate = 500
        p1000.flow_rate.dispense = 1000
        p1000.flow_rate.blow_out = 1000
        p1000.mix(5, 1000, std.bottom(tubes_dict[std].height))
        p1000.blow_out(std.top(-2))
        for a in aliquots:
            p1000.flow_rate.aspirate = 150
            p1000.flow_rate.dispense = 320
            p1000.transfer(160, tubes_dict[std].height_dec(160), a.bottom(10),
                           new_tip='never')
            p1000.blow_out(a.top(-6))
        p1000.drop_tip()
        if 'QC' in std_name:
            qc_counter += num_aliquots
        else:
            ws_counter += num_aliquots

    # transfer mobile phase
    tip_condition(p1000, 1000)
    mobile_phase = tuberack15_50.wells_by_name()['B1']
    tubes_dict[mobile_phase].height = 85
    mobile_phase_dests = plate.rows()[0][:8] + plate.rows()[2][:6]
    for i in range(len(mobile_phase_dests)//2):
        p1000.flow_rate.aspirate = 150
        p1000.flow_rate.dispense = 800
        p1000.distribute(
            400, tubes_dict[mobile_phase].height_dec(800),
            [well.bottom(10) for well in mobile_phase_dests[i*2:i*2+2]],
            disposal_volume=100, new_tip='never')
        p1000.blow_out(mobile_phase.top())
    p1000.drop_tip()

    # # transfer IS
    is_ = plate.wells_by_name()['H1']
    tip_condition(p300, 150)
    for i, m in enumerate(mobile_phase_dests):
        if i < 5:
            h = 9
        elif i >= 5 and i < 8:
            h = 7
        else:
            h = 2
        p300.transfer(30, is_.bottom(h), m.bottom(14), new_tip='never')
        p300.blow_out(m.bottom(14))
    p300.drop_tip()

    # tests
    ws_counter = 0
    qc_counter = 0
    ws_dests = mobile_phase_dests[:8]
    qc_dests = mobile_phase_dests[8:]
    for line in data[::-1]:
        std_name = line[0]
        std = ctx.loaded_labwares[int(line[12])].wells_by_name()[line[13]]
        dest_set = qc_dests if 'QC' in std_name else ws_dests
        counter = qc_counter if 'QC' in std_name else ws_counter

        tip_condition(p300, 150)
        p300.flow_rate.aspirate = 30
        p300.flow_rate.dispense = 150
        p300.transfer(30, tubes_dict[std].height_dec(30),
                      dest_set[counter].bottom(14), new_tip='never')
        p300.blow_out(dest_set[counter].bottom(14))
        p300.drop_tip()

        if 'QC' in std_name:
            qc_counter += 1
        else:
            ws_counter += 1
