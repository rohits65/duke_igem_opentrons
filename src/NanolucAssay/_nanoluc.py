from opentrons import protocol_api

metadata = {
    'protocolName': 'iGEM Nanoluc Assay Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

# encoded_input = {'plasmids': [['p_1', 'p_2', 'p_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'p_4', 'p_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'forward_primers': [['f_1', 'f_2', 'f_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'f_4', 'f_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'reverse_primers': [['r_1', 'r_2', 'r_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'r_4', 'r_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'mappings': [[1, 'p_1', 'f_1', 'r_1', ''], [2, 'p_2', 'f_2', 'r_2', ''], [3, 'p_3', 'f_3', 'r_3', ''], [4, 'p_4', 'f_4', 'r_4', ''], [5, 'p_5', 'f_5', 'r_5', '']]}

cell_row = 'D'
cell_start_col = 1
cell_end_col = 7

assay_row = 'G'
assay_start_col = 1
assay_end_col = 7



def run(protocol: protocol_api.ProtocolContext):
    tips_300 = protocol.load_labware("opentrons_96_filtertiprack_200ul", 5) # TODO check if right
    tips_20 = protocol.load_labware("opentrons_96_tiprack_20ul", 4) 

    cell_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    assay_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 1)

    assay_tubes = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 4)

    pipette_300 = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips_300])
    pipette_20 = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tips_20])

    
    # Add media
    pipette_300.pick_up_tip()
    
    for col in range(cell_start_col, cell_end_col+1):
        
        pipette_300.aspirate(80, assay_tubes['A1'])
        pipette_300.dispense(80, assay_plate[assay_row+str(col)], rate=2.0)
        pipette_300.blow_out()

        pipette_300.aspirate(80, assay_tubes['A1'])
        pipette_300.dispense(80, assay_plate[chr(ord(assay_row) + 1)+str(col)], rate=2.0)
        pipette_300.blow_out()

    pipette_300.drop_tip()


    # Add cell plate sample
    pipette_20.well_bottom_clearance.aspirate = 2

    for col in range(cell_start_col, cell_end_col+1):
        pipette_20.pick_up_tip()
        pipette_20.aspirate(20, cell_plate[cell_row+str(col)], rate=0.5)
        pipette_20.dispense(20, assay_plate[assay_row+str(col)], rate=2.0)
        pipette_20.blow_out()
        pipette_20.drop_tip()

        pipette_20.pick_up_tip()
        pipette_20.aspirate(20, cell_plate[cell_row+str(col)], rate=0.5)
        pipette_20.dispense(20, assay_plate[chr(ord(assay_row) + 1)+str(col)], rate=2.0)
        pipette_20.blow_out()
        pipette_20.drop_tip()
    

    # Add reagent
    for col in range(cell_start_col, cell_end_col+1):
        pipette_300.pick_up_tip()
        pipette_300.aspirate(100, assay_tubes['A2'])
        pipette_300.dispense(100, assay_plate[assay_row+str(col)], rate=2.0)
        pipette_300.mix(3, 50, assay_plate[assay_row+str(col)])
        pipette_300.blow_out()
        pipette_300.drop_tip()

        pipette_300.pick_up_tip()
        pipette_300.aspirate(100, assay_tubes['A2'])
        pipette_300.dispense(100, assay_plate[chr(ord(assay_row) + 1)+str(col)], rate=2.0)
        pipette_300.mix(3, 50, assay_plate[chr(ord(assay_row) + 1)+str(col)])
        pipette_300.blow_out()
        pipette_300.drop_tip()


    
    