from opentrons import protocol_api

#Paste your layout lists here: 
MM_wells = [[0, 1, 2, 8, 9, 10, 16, 17, 18, 24, 25, 26, 32, 33, 34, 40, 41, 42, 48, 49, 50, 56, 57, 58, 64, 65, 66], [3, 4, 5, 11, 12, 13, 19, 20, 21, 27, 28, 29, 35, 36, 37, 43, 44, 45, 51, 52, 53, 59, 60, 61, 67, 68, 69]]
template_wells = [[0, 1, 2, 3, 4, 5], [8, 9, 10, 11, 12, 13], [16, 17, 18, 19, 20, 21], [24, 25, 26, 27, 28, 29], [32, 33, 34, 35, 36, 37], [40, 41, 42, 43, 44, 45], [48, 49, 50, 51, 52, 53], [56, 57, 58, 59, 60, 61], [64, 65, 66, 67, 68, 69]]

# metadata
metadata = {
    "protocolName": "aPCR protocol",
    "author": "rk320",
    "description": "qPCR  pipetting",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.19"}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    
    # labware
    reagent_rack = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", location="3"
    )
    
    plate = protocol.load_labware(
        "microampfastoptical_96_wellplate_100ul", location="1"
    )
    tiprack = protocol.load_labware(
        "opentrons_96_tiprack_20ul", location="6"
    )
    
    template_plate = protocol.load_labware(
        "nest_96_wellplate_100ul_pcr_full_skirt", location="2"
    )
    
    # pipettes
    p20 = protocol.load_instrument(
        "p20_single_gen2", mount="right", tip_racks=[tiprack]
    )
    
    #Adding Master mix
    for i in range(len(MM_wells)):

        p20.pick_up_tip()
        for j in MM_wells[i]:
            p20.transfer(9, reagent_rack.wells()[i], plate.wells()[j], new_tip = 'never') #the same tip will be used for all MM dispensing
            
        p20.drop_tip()
    
    #Adding template
    for i in range(len(template_wells)): 
        for j in template_wells[i]:
            p20.pick_up_tip()
            p20.transfer(1, template_plate.wells()[i], plate.wells()[j], new_tip= 'never')
            p20.mix(3, 8)  #mix 8ul in current location 
            p20.drop_tip()
    
