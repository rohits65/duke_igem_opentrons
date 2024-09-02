from opentrons import protocol_api


metadata = {
    'protocolName': 'iGEM PCR Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

# encoded_input = {'plasmids': [['p_1', 'p_2', 'p_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'p_4', 'p_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'forward_primers': [['f_1', 'f_2', 'f_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'f_4', 'f_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'reverse_primers': [['r_1', 'r_2', 'r_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', 'r_4', 'r_5'], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'mappings': [[1, 'p_1', 'f_1', 'r_1', ''], [2, 'p_2', 'f_2', 'r_2', ''], [3, 'p_3', 'f_3', 'r_3', ''], [4, 'p_4', 'f_4', 'r_4', ''], [5, 'p_5', 'f_5', 'r_5', '']]}

encoded_input = {'plasmids': [['p_1', 'p_2', 'p_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'forward_primers': [['', '', '', '', '', '', '', '', '', '', '', ''], ['f_1', 'f_2', 'f_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'reverse_primers': [['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['r_1', 'r_2', 'r_3', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '']], 'mappings': [[1, 'p_1', 'f_1', 'r_1', ''], [2, 'p_1', 'f_2', 'r_2', ''], [3, 'p_2', 'f_2', 'r_2', '']]}

plasmid_locations = {}
forward_primers_locations = {}
reverse_primers_locations = {}

plasmids = {}
forward_primers = {}
reverse_primers = {}

pcr_plate = {}

def setup():
    # Store locations of samples    
    for i in range(0, 8):
        for j in range(0, 12):
            if encoded_input['plasmids'][i][j] != '':
                plasmid_locations[encoded_input['plasmids'][i][j]] = chr(ord('A')+i) + str(j+1)
            if encoded_input['forward_primers'][i][j] != '':
                forward_primers_locations[encoded_input['forward_primers'][i][j]] = chr(ord('A')+i) + str(j+1)
            if encoded_input['reverse_primers'][i][j] != '':
                reverse_primers_locations[encoded_input['reverse_primers'][i][j]] = chr(ord('A')+i) + str(j+1)

    row = 'A'
    col = 1

    for run in encoded_input['mappings']:
        if row > 'H':  # After H, reset to A and move to the next column
            row = 'A'
            col += 1
        if col > 12:  
            raise ValueError("Exceeded column limit.")

        if run[1] in plasmids.keys():
            plasmids[run[1]].append(row + str(col))
        else:
            plasmids[run[1]] = [row + str(col)]
        
        if run[2] in forward_primers.keys():
            forward_primers[run[2]].append(row + str(col))
        else:
            forward_primers[run[2]] = [row + str(col)]
        
        if run[3] in reverse_primers.keys():
            reverse_primers[run[3]].append(row + str(col))
        else:
            reverse_primers[run[3]] = [row + str(col)]
        
        pcr_plate[run[0]] = row + str(col)
        
        row = chr(ord(row) + 1) 


def run(protocol: protocol_api.ProtocolContext):
    setup()

    tips = protocol.load_labware("opentrons_96_tiprack_20ul", 9)

    # plasmid_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 1)
    # forward_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 2)
    # reverse_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)

    plate = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 3)
    gel_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 1)

    # master_mix_tube = protocol.load_labware("opentrons_15_tuberack_falcon_15ml_conical", 4)

    # Remove for Final
    # reservoir = protocol.load_labware("nest_12_reservoir_15ml", 6)
    # End remove

    pipette = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tips])
    multichannel = protocol.load_instrument("p20_multi_gen2", "left", tip_racks=[tips])

    # Get thermocycler
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    tc_plate = tc_mod.load_labware(name="nest_96_wellplate_100ul_pcr_full_skirt")


    # Close lid
    if tc_mod.lid_position != 'closed':
        tc_mod.close_lid()

    # TODO User input for start tip location
    multichannel.pick_up_tip()
    multichannel.drop_tip()

    pipette.pick_up_tip()
    pipette.drop_tip()

    
    # 0. set block temp to 4? lid temp to 105?
    # 1. iterate through mappings
    #     for each:
    #         1.25 primer, 1.25 other primer, 1 plasmid
    # 2. 9 water to each
    # 3. ask user to put in master mix
    # 4. 12.5 master mix in each
    
    
    tc_mod.open_lid()
    tc_mod.set_block_temperature(temperature=4)

    for plasmid in plasmids.keys():
        pipette.pick_up_tip()
        for location in plasmids[plasmid]:
            pipette.aspirate(1, plate[plasmid_locations[plasmid]])
            pipette.dispense(1, tc_plate[location], rate=3)
            pipette.blow_out()
        pipette.drop_tip()

    for primer in forward_primers.keys():
        pipette.pick_up_tip()
        for location in forward_primers[primer]:
            pipette.aspirate(1.25, plate[forward_primers_locations[primer]])
            pipette.dispense(1.25, tc_plate[location], rate=3)
            pipette.blow_out()
        pipette.drop_tip()
    
    for primer in reverse_primers.keys():
        pipette.pick_up_tip()
        for location in reverse_primers[primer]:
            pipette.aspirate(1.25, plate[reverse_primers_locations[primer]])
            pipette.dispense(1.25, tc_plate[location], rate=3)
            pipette.blow_out()
        pipette.drop_tip()
    
    # Add water
    row = 'A'
    col = 1
    pipette.pick_up_tip()
    for run in encoded_input['mappings']:
        if row > 'H':  # After row H, reset to A and move to the next column
            row = 'A'
            col += 1
        if col > 12:
            raise ValueError("Exceeded column limit.")
        
        pipette.aspirate(9, plate['D5'])
        pipette.dispense(9, tc_plate[row + str(col)], rate=2)
        
        row = chr(ord(row) + 1)  # Move to the next row (A -> B -> C -> D)
    pipette.drop_tip()

    # Add mastermix
    row = 'A'
    col = 1
    pipette.pick_up_tip()
    for run in encoded_input['mappings']:
        if row > 'H':  # After row H, reset to A and move to the next column
            row = 'A'
            col += 1
        if col > 12:
            raise ValueError("Exceeded column limit.")
        
        pipette.aspirate(12.5, plate['D6'])
        pipette.dispense(12.5, tc_plate[row + str(col)], rate=2)
        
        row = chr(ord(row) + 1)  # Move to the next row (A -> B -> C -> D)
    pipette.drop_tip()

    # Mixing
    multichannel.pick_up_tip()
    multichannel.mix(5, 15, tc_plate['A1'])
    multichannel.blow_out()
    multichannel.touch_tip()
    multichannel.drop_tip()

    # Thermocycler
    tc_mod.close_lid()
    
    tc_mod.set_lid_temperature(temperature=105)

    tc_mod.set_block_temperature(temperature=94, hold_time_minutes=2)

    profile = [
        {"temperature":94, "hold_time_seconds":25},
        {"temperature":57, "hold_time_seconds":25}, 
        {"temperature":72, "hold_time_seconds":60},
        {"temperature":72, "hold_time_seconds":420}, 
    ]

    tc_mod.execute_profile(steps=profile, repetitions=2, block_max_volume=25)

    tc_mod.open_lid()

    tc_mod.set_block_temperature(temperature=4)
    tc_mod.deactivate_lid()


    # Transfer to well plate and add loading dye
    # Add loading dye
    row = 'A'
    col = 1
    pipette.pick_up_tip()
    for run in encoded_input['mappings']:
        if row > 'H':  # After row H, reset to A and move to the next column
            row = 'A'
            col += 1
        if col > 12:
            raise ValueError("Exceeded column limit.")
        
        pipette.aspirate(1, plate['D4'])
        pipette.dispense(1, gel_plate[row + str(col)], rate=3)
        pipette.blow_out()
        
        row = chr(ord(row) + 1)  # Move to the next row (A -> B -> C -> D)
    pipette.drop_tip()

    row = 'A'
    col = 1
    
    for run in encoded_input['mappings']:
        pipette.pick_up_tip()
        if row > 'H':  # After row H, reset to A and move to the next column
            row = 'A'
            col += 1
        if col > 12:
            raise ValueError("Exceeded column limit.")
        
        pipette.aspirate(5, tc_plate[row + str(col)])
        pipette.dispense(5, gel_plate[row + str(col)], rate=2)
        pipette.blow_out()
        
        row = chr(ord(row) + 1)  # Move to the next row (A -> B -> C -> D)
        pipette.drop_tip()

   




    # pipette.aspirate(1.25, plate["D5"])
    # # pipette.touch_tip(reverse_plate["A6"],
    # #               radius=0.75,
    # #               v_offset=-2)
    # pipette.dispense(1.25, plate["A6"], rate=3)
    # pipette.blow_out()



# setup()
# print(pcr_plate)
# print(plasmids)
# print(forward_primers)
# print(reverse_primers)
# print(plasmid_locations)
# print(forward_primers_locations)
# print(reverse_primers_locations)