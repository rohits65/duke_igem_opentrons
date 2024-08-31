from opentrons import protocol_api

metadata = {
    'protocolName': 'Thermocycler Test Protocol',
    'author': 'rohit',
    'apiLevel': '2.13'
}

# requirements = {"robotType": "OT-2", "apiLevel": "2.13"}

def run(protocol: protocol_api.ProtocolContext):
    # Get thermocycler
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    tc_mod.open_lid()
    # Close lid
    if tc_mod.lid_position != 'closed':
        tc_mod.close_lid()



    # lid temperature set
    tc_mod.set_lid_temperature(40)

    tc_mod.open_lid()
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(30)
    tc_mod.open_lid()
    tc_mod.close_lid()
    # # initialization
    # tc_mod.set_block_temperature(init_temp, hold_time_seconds=init_time,
    #                              block_max_volume=well_vol)

    # # run profile
    # profile = [
    #     {'temperature': d_temp, 'hold_time_seconds': d_time},
    #     {'temperature': a_temp, 'hold_time_seconds': a_time},
    #     {'temperature': e_temp, 'hold_time_seconds': e_time}
    # ]

    # tc_mod.execute_profile(steps=profile, repetitions=no_cycles,
    #                        block_max_volume=well_vol)

    # # final elongation

    # tc_mod.set_block_temperature(fe_temp, hold_time_seconds=fe_time,
    #                              block_max_volume=well_vol)

    # # final hold
    # tc_mod.deactivate_lid()
    # tc_mod.set_block_temperature(final_temp)


