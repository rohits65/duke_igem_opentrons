from opentrons import protocol_api

metadata = {
    'protocolName': 'Pipette Tips Test Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

# requirements = {"robotType": "OT-2", "apiLevel": "2.13"}

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_20ul", 6)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 3)
    # reservoir = plate = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 3)
    plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 2)

    pipette = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tips])

    row = 'B'
    col = 2
    for i in range(0,4):
        if row > 'H':  # After H, reset to A and move to the next column
            row = 'A'
            col += 1
        if col > 12:  
            raise ValueError("Exceeded column limit.")
        
        pipette.pick_up_tip()
        pipette.aspirate(20, reservoir['A3'], rate=0.5)
        pipette.dispense(20, plate[row+str(col)], rate=3)
        pipette.blow_out()
        pipette.drop_tip()
        
        row = chr(ord(row) + 1) 



