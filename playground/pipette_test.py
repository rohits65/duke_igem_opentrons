from opentrons import protocol_api

metadata = {
    'protocolName': 'Pipette Test Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

# requirements = {"robotType": "OT-2", "apiLevel": "2.13"}

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_20ul", 8)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 5)
    plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 2)

    pipette = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tips])

    pipette.pick_up_tip(tips["A3"])
    pipette.aspirate(15, reservoir["A1"])
    pipette.dispense(15, plate["A3"], rate=2.0)

