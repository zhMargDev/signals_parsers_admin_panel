import os
import subprocess
import json
import asyncio
from datetime import datetime

DATA_FILE = "data.json"
PARSER_PROCESS = None
PACKAGER_PROCESS= None

async def load_data():
    """
    Асинхронная функция для загрузки данных из JSON файла.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {
            "parser": {"status": "stopped", "last_changed": str(datetime.now())},
            "packager": {"status": "stopped", "last_changed": str(datetime.now())},
        }

async def save_data(data):
    """
    Асинхронная функция для сохранения данных в JSON файл.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


async def start_stop_parser():
    """
        Данная фукнция запускает или останавливает парсер
        Который собирает данные из каналов
    """

    global PARSER_PROCESS
    data = await load_data()

    if data is None:
        return 'Problem with Datafile'
# pizdeeeeeeeeeeeeeeeeeeeeec
    if data["parser"]["status"] == "stopped":
        process = subprocess.Popen(['python3', 'signals_parser/run.py'])
        try:
            # Запуск процесса
            PARSER_PROCESS = await asyncio.create_subprocess_exec(
                "python3", "run.py",
                cwd="signals_parser/",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            asyncio.create_task(monitor_process(PARSER_PROCESS, "Parser"))
        
            data["parser"]["status"] = "running"
            data["parser"]["last_changed"] = str(datetime.now())
            
        
        except:
            print('Mna')

    else:
        
        if PARSER_PROCESS:
            # Остановка процесса
            PARSER_PROCESS.terminate()
            await PARSER_PROCESS.wait()
            PARSER_PROCESS = None
       
        data["parser"]["status"] = "stopped"
        data["parser"]["last_changed"] = str(datetime.now())
      
        #

    await save_data(data)
    return data

async def restart():
    """
    Функция для перезапуска процессов парсера и распаковщика.
    """
    global PARSER_PROCESS, PACKAGER_PROCESS
    try:


        data = await load_data()
        data["parser"]["status"] = "running"
        data["parser"]["last_changed"] = str(datetime.now())
        data["packager"]["status"] = "running"
        data["packager"]["last_changed"] = str(datetime.now())

        await save_data(data)
        return data

    except Exception as e:
        print(f"Ошибка в функции restart: {e}")
        return f"Ошибка в функции restart: {e}"

async def monitor_process(process, name):
    """
    Функция для мониторинга вывода процесса и записи его в файл логов.
    """
    log_dir = "/logs/"
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



async def start_stop_packager():
    """Данная фукнция запускает или останавливает парсер Который собирает данные из каналов"""
    global PACKAGER_PROCESS
    data = await load_data()
    if data is None:
        return 'Problem with Datafile'
# pizdeeeeeeeeeeeeeeeeeeeeec
    if data["packager"]["status"] == "stopped":
        process = subprocess.Popen(['python3', 'signals_packager/main.py'])
        try:
            # Запуск процесса
            PACKAGER_PROCESS = await asyncio.create_subprocess_exec(
                "python3", "main.py",
                cwd="signals_packager/",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
           
            asyncio.create_task(monitor_process(PACKAGER_PROCESS, "packager"))
        
            data["packager"]["status"] = "running"
            data["packager"]["last_changed"] = str(datetime.now())
        except:
            print('Mna')

    else:
        
        if PACKAGER_PROCESS:
            # Остановка процесса
            PACKAGER_PROCESS.terminate()
            await PACKAGER_PROCESS.wait()
            PACKAGER_PROCESS = None
       
        data["packager"]["status"] = "stopped"
        data["packager"]["last_changed"] = str(datetime.now())
    await save_data(data)
    return data






    
async def main():
    await start_stop_parser()
    await start_stop_packager()

if __name__ == "__main__":
    asyncio.run(main())




