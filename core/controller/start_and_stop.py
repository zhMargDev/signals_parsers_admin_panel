import os, subprocess, json, asyncio

from datetime import datetime

DATA_FILE = "data.json"
PARSER_PROCESS = None
PACKAGER_PROCESS = None

async def load_data():
    """
        Данная фукнция открывает файлдата в котором прописаны данные об парсере и расфасофщике
    """
    # Загрузка данных о парсере и упаковщике
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    # Инициализация структуры данных, если файл не существует
    return {
        "parser": {
            "status": "stopped",
            "last_changed": str(datetime.now())
        },
        "packager": {
            "status": "stopped",
            "last_changed": str(datetime.now())
        }
    }

async def save_data(data):
    """
        Данная фукнция сохраняет изменения в про парсер и расфасофщик
    """
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

async def monitor_process(process, name):
    """
        Данная функция добавляет лог файл если его нет и выводит туда все данные 
        которые должны выводиться в терминал
    """
    log_dir = "/root/projects/signals_parsers_admin_panel/logs/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = f"{log_dir}{name}_log.txt"
    with open(log_file, "a") as file:
        while True:
            line = await process.stdout.readline()
            if line:
                file.write(f"{datetime.now()}: {line.decode().strip()}\n")
                file.flush()
            else:
                break

async def start_stop_parser():
    """
        Данная фукнция запускает или останавливает парсер
        Который собирает данные из каналов
    """
    global PARSER_PROCESS
    data = await load_data()

    if data is None:
        return 'Problem with Datafile'

    if data["parser"]["status"] == "stopped":
        # Запуск процесса
        PARSER_PROCESS = await asyncio.create_subprocess_exec(
            "python3", "run.py",
            cwd="/root/projects/signals_parser",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        asyncio.create_task(monitor_process(PARSER_PROCESS, "Parser"))
        data["parser"]["status"] = "running"
        data["parser"]["last_changed"] = str(datetime.now())
    else:
        # Остановка процесса
        if PARSER_PROCESS:
            PARSER_PROCESS.terminate()
            await PARSER_PROCESS.wait()
            PARSER_PROCESS = None
        data["parser"]["status"] = "stopped"
        data["parser"]["last_changed"] = str(datetime.now())

    await save_data(data)
    return data

async def start_stop_packager():
    """
        Данная фукнция запускает или останавливает расфасовщик
        Который отправляет данные в каналы по группам
    """
    global PACKAGER_PROCESS
    data = await load_data()

    if data is None:
        return 'Problem with Datafile'

    if data["packager"]["status"] == "stopped":
        # Запуск процесса
        PACKAGER_PROCESS = await asyncio.create_subprocess_exec(
            "python3", "main.py",
            cwd="/root/projects/signals_packager",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        asyncio.create_task(monitor_process(PACKAGER_PROCESS, "Packager"))
        data["packager"]["status"] = "running"
        data["packager"]["last_changed"] = str(datetime.now())
    else:
        # Остановка процесса
        if PACKAGER_PROCESS:
            PACKAGER_PROCESS.terminate()
            await PACKAGER_PROCESS.wait()
            PACKAGER_PROCESS = None
        data["packager"]["status"] = "stopped"
        data["packager"]["last_changed"] = str(datetime.now())

    await save_data(data)
    return data

async def restart():
    """
        Данная фукнция перезапускает парсер
        Который собирает данные из каналов
        И расфасовщик
        Который отправляет данные в каналы по группам
    """
    global PACKAGER_PROCESS
    global PARSER_PROCESS
    data = await load_data()

    if data is None:
        return 'Problem with Datafile'

    # Рестарт бота расфасофщика
    if PACKAGER_PROCESS:
        PACKAGER_PROCESS.terminate()
        await PACKAGER_PROCESS.wait()
        PACKAGER_PROCESS = None
    PACKAGER_PROCESS = await asyncio.create_subprocess_exec(
        "python3", "main.py",
        cwd="/root/projects/signals_packager",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    asyncio.create_task(monitor_process(PACKAGER_PROCESS, "Packager"))
    data["packager"]["status"] = "stopped"
    data["packager"]["last_changed"] = str(datetime.now())

    # Рестарт парсера
    if PARSER_PROCESS:
        PARSER_PROCESS.terminate()
        await PARSER_PROCESS.wait()
        PARSER_PROCESS = None
    PARSER_PROCESS = await asyncio.create_subprocess_exec(
        "python3", "run.py",
        cwd="/root/projects/signals_parser",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    asyncio.create_task(monitor_process(PARSER_PROCESS, "Parser"))
    data["parser"]["status"] = "running"
    data["parser"]["last_changed"] = str(datetime.now())

    await save_data(data)
    return data