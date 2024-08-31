from opentrons import protocol_api

encoded_input = {'plasmids': [['p_1', 'p_2', 'p_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'p_4', 'p_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'forward_primers': [['f_1', 'f_2', 'f_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'f_4', 'f_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'reverse_primers': [['r_1', 'r_2', 'r_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'r_4', 'r_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'mappings': [[1, 'p_1', 'f_1', 'r_1', ''], [2, 'p_2', 'f_2', 'r_2', ''], [3, 'p_3', 'f_3', 'r_3', ''], [4, 'p_4', 'f_4', 'r_4', ''], [5, 'p_5', 'f_5', 'r_5', '']]}

metadata = {
    'protocolName': 'PCR Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_20ul", 9)
    plasmid_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    forward_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 2)
    reverse_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 1)

    pipette = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tips])

    # Get thermocycler
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    tc_mod.open_lid()

    # Close lid
    if tc_mod.lid_position != 'closed':
        tc_mod.close_lid()

    # TODO User input for start tip location
    pipette.pick_up_tip(tips["A3"])

    '''
    0. set block temp to 4? lid temp to 105?
    1. iterate through mappings
        for each:
            1.25 primer, 1.25 other primer, 1 plasmid
    2. 9 water to each
    3. ask user to put in master mix
    4. 12.5 master mix in each
    '''


    pipette.aspirate(15, reservoir["A1"])
    pipette.dispense(15, plate["A3"], rate=2.0)

