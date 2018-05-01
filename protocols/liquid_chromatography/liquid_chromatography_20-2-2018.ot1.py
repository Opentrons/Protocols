from opentrons import containers, instruments

containers.create(
    'TLC_plate',                    # name of you container
    grid=(10, 14),                    # specify amount of (columns, rows)
    spacing=(8, 8),               # distances (mm) between each (column, row)
    diameter=8,                     # diameter (mm) of each well on the plate
    depth=1)                       # depth (mm) of each well on the plate

tiprack200 = containers.load('tiprack-200ul', 'A2')
tiprack50 = containers.load('tiprack-200ul', 'E2')
tuberack = containers.load('tube-rack-2ml', 'B2')
trash = containers.load('trash-box', 'C2')
plate = containers.load('TLC_plate', 'B1')

p200 = instruments.Pipette(
    axis="b",
    min_volume=20,
    max_volume=200,
    tip_racks=[tiprack200],
    trash_container=trash
)

p50 = instruments.Pipette(
	axis="a",
	min_volume=5,
	max_volume=50,
	tip_racks=[tiprack50],
	trash_container=trash
)

AMW = tuberack.wells('A1')
Acetonitrile = tuberack.wells('B1')
Methanol = tuberack.wells('C1')
Water = tuberack.wells('D1')
R_81p8uM = tuberack.wells('A2')
DOX900uM = tuberack.wells('B2')
DOL900uM = tuberack.wells('C2')
EPI900uM = tuberack.wells('D2')
R_9p09uM = tuberack.wells('A3')
R_2098nM = tuberack.wells('A4')
R_1049nM = tuberack.wells('B4')
R_525nM = tuberack.wells('C4')
R_262nM = tuberack.wells('A5')
R_131nM = tuberack.wells('B5')
R_65p6nM = tuberack.wells('C5')
R_32p8nM = tuberack.wells('A6')
R_16p4nM = tuberack.wells('B6')
R_8p2nM = tuberack.wells('C6')

#transfer volume from Acetonitrile to AMW
aceto_vol = 780
p200.transfer(
	aceto_vol,
	Acetonitrile,
	AMW,
	touch_tip=True,
	blow_out=True,
	mix_before=(1,200),
	new_tip='once'
)

#transfer volume from methanol to AMW
methanol_vol = 390
p200.transfer(
	methanol_vol,
	Methanol,
	AMW,
	touch_tip=True,
	blow_out=True,
	mix_before=(1,200),
	new_tip='once'
)

#transfer volume from water to AMW
p200.pick_up_tip()
water_vol = 156
p200.transfer(
	water_vol,
	Water,
	AMW,
	touch_tip=True,
	blow_out=True,
	mix_before=(1,200),
	new_tip='never'
)

#mix AMW 5 times
p200.mix(5, 200, AMW)

#transfer volume from AMW to R_81p8uM
amw_R_81p8uM_vol = 360
p200.transfer(
	amw_R_81p8uM_vol,
	AMW,
	R_81p8uM,
	touch_tip=True,
	blow_out=True,
	new_tip='never'
)

#transfer volume from AMW to R_9p09uM
amw_R_9p09uM_vol = 360
p200.transfer(
	amw_R_9p09uM_vol,
	AMW,
	R_9p09uM,
	touch_tip=True,
	blow_out=True,
	new_tip='never'
)

#transfer volume from AMW to R_2098nM
amw_R_2098nM_vol = 150
p200.transfer(
	amw_R_2098nM_vol,
	AMW,
	R_2098nM,
	touch_tip=True,
	blow_out=True,
	new_tip='never'
)
p200.drop_tip()

#transfer volume from AMW to R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM, R_8p2nM
AMW_dest_list = [well.bottom() for well in [R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM, R_8p2nM]]
AMW_list_vol = 45
p50.pick_up_tip()
p50.transfer(
	AMW_list_vol,
	AMW,
	AMW_dest_list,
	touch_tip=True,
	blow_out=True,
	new_tip='never',
	mix_before=(1,50)
)
p50.drop_tip()

#transfer volume from DOX900uM, DOL900uM, EPI900uM to R_81p8uM 
R_81p8uM_dest_vol = 45
p50.transfer(
	R_81p8uM_dest_vol,
	DOX900uM,
	R_81p8uM,
	touch_tip=True,
	blow_out=True,
	new_tip='once',
	mix_before=(1,50)
)
p50.transfer(
	R_81p8uM_dest_vol,
	DOL900uM,
	R_81p8uM,
	touch_tip=True,
	blow_out=True,
	new_tip='once',
	mix_before=(1,50)
)
p50.pick_up_tip()
p50.transfer(
	R_81p8uM_dest_vol,
	EPI900uM,
	R_81p8uM,
	touch_tip=True,
	blow_out=True,
	new_tip='never',
	mix_before=(1,50)
)
#mix R_81p8uM 10 times
p50.mix(10, 50, R_81p8uM)

#transfer volume from R_81p8uM to R_9p09uM
R_81p8uM_to_R_9p09uM_vol = 45
p50.transfer(
	R_81p8uM_to_R_9p09uM_vol,
	R_81p8uM,
	R_9p09uM,
	touch_tip=True,
	blow_out=True,
	new_tip='never'
)
#mix R_9p09uM 5 times
p50.mix(10, 50, R_9p09uM)

#transfer volumes from R_9p09uM, R_2098nM, R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM to R_2098nM, R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM, R_8p2nM
source_list = [R_81p8uM, R_9p09uM, R_2098nM, R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM]
dest_list = [well.bottom() for well in [R_9p09uM, R_2098nM, R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM, R_8p2nM]]
source_to_dest_vol = 45
p50.transfer(
	source_to_dest_vol,
	source_list,
	dest_list,
	touch_tip=True,
	blow_out=True,
	new_tip='never',
	mix_after=(5, 50)
)

#transfer volumes from R_2098nM, R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM, R_8p2nM to TLC_plate
#dispense speed needs to be slow
p50.set_speed(dispense=120)
TLC_vol = 5
TLC_source_list = [R_2098nM, R_1049nM, R_525nM, R_262nM, R_131nM, R_65p6nM, R_32p8nM, R_16p4nM, R_8p2nM]
TLC_dest_list = [well.bottom() for well in plate.wells('A1', to='I1')]
p50.transfer(
	TLC_vol,
	TLC_source_list,
	TLC_dest_list,
	touch_tip=True,
	blow_out=True,
	new_tip='always'
)
