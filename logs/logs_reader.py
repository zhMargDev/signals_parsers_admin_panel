import os

async def read_parser_log():
    log_file = "/root/projects/signals_parsers_admin_panel/logs/Parser_log.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            print(f"--- Parser Log ---")
            print(file.read())

async def read_packager_log():
    log_file = "/root/projects/signals_parsers_admin_panel/logs/Packager_log.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            print(f"--- Packager Log ---")
            print(file.read())
