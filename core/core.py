import core.controller.controls_info as controls_info
import core.information.channels_and_folders as channels_and_folders

async def get_parsers_info():
    return await controls_info.get_controll_info()

async def get_system_usage():
    return await controls_info.get_system_usage()

async def get_channels_info():
    return await channels_and_folders.get_channels_info()