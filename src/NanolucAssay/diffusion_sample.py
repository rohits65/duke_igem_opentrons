from opentrons import protocol_api

metadata = {
    'protocolName': 'iGEM Nanoluc Sample Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

col = 6

def run(protocol: protocol_api.ProtocolContext):
    tips_300 = protocol.load_labware("opentrons_96_filtertiprack_200ul", 5) # TODO check if right
    tips_20 = protocol.load_labware("opentrons_96_tiprack_20ul", 4) 

    cell_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    assay_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 1)

    assay_tubes = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 6)

    pipette_300 = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips_300])
    pipette_20 = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tips_20])

    
    # Add media
    pipette_300.pick_up_tip()
    
    for row in range(0, 1):
        
        pipette_300.aspirate(20, assay_tubes['A1'])
        pipette_300.dispense(20, assay_plate[chr(ord('A')+ row*2) +str(4)], rate=2.0)
        pipette_300.blow_out()


    pipette_300.drop_tip()


    # Add cell plate sample
    # pipette_20.well_bottom_clearance.aspirate = 5

    for row in range(0, 1):
        
        pipette_20.pick_up_tip()
        pipette_20.aspirate(5, cell_plate[chr(ord('A')+row) +str(col)], rate=0.5)
        pipette_20.dispense(5, assay_plate[chr(ord('A')+ row*2) +str(4)], rate=3.0)
        pipette_20.blow_out()
        pipette_20.drop_tip()
    

    # Add reagent
    pipette_300.well_bottom_clearance.dispense = 10
    pipette_300.pick_up_tip()
    
    for row in range(0, 1):
        
        pipette_300.aspirate(25, assay_tubes['A2'])
        pipette_300.dispense(25, assay_plate[chr(ord('A')+ row*2) +str(4)], rate=2.0)
        pipette_300.blow_out()



    pipette_300.drop_tip()

    
    