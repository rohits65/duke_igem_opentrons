from opentrons import protocol_api

metadata = {
    'protocolName': '09022024 Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

# requirements = {"robotType": "OT-2", "apiLevel": "2.13"}

def run(protocol: protocol_api.ProtocolContext):
   # # Get thermocycler
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    tc_plate = tc_mod.load_labware(name="nest_96_wellplate_100ul_pcr_full_skirt")

    tc_mod.close_lid()
    tc_mod.set_block_temperature(temperature=72, hold_time_minutes=2)
    tc_mod.set_block_temperature(temperature=4)
