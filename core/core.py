import core.controller.controls_info as controls_info

async def get_parsers_info():
    return await controls_info.get_controll_info()

async def get_system_usage():
    return await controls_info.get_system_usage()