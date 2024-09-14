from opentrons import protocol_api

metadata = {
    'protocolName': 'iGEM Diffusion Assay Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}


# cell_row = 'D'
# cell_start_col = 1
# cell_end_col = 5

# assay_row = 'G'
# assay_start_col = 1
# assay_end_col = 5


loc = 'B1'


def run(protocol: protocol_api.ProtocolContext):
    tips_20 = protocol.load_labware("opentrons_96_tiprack_20ul", 4) 

    cell_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    assay_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 1)

    pipette_20 = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tips_20])

    # Add cell plate sample
    pipette_20.pick_up_tip()
    pipette_20.well_bottom_clearance.aspirate = 3.5

    pipette_20.aspirate(5, cell_plate[loc])
    pipette_20.dispense(5, assay_plate[loc])
    pipette_20.blow_out()
    pipette_20.drop_tip()