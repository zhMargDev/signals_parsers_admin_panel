import json, psutil, os, time
from datetime import datetime, timedelta

DATA_FILE = "data.json"

async def get_controll_info():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        
        current_time = time.time()  # Current time in timestamp format
        result = {}
        
        for service in data:
            if data[service]['last_changed'] != '' and data[service]['status'] != "stopped":
                last_changed_str = data[service]['last_changed']
                
                # Parse last_changed string to datetime object
                last_changed_datetime = datetime.strptime(last_changed_str, '%Y-%m-%d %H:%M:%S.%f')
                
                # Convert datetime object to timestamp (float)
                last_changed_timestamp = last_changed_datetime.timestamp()
                
                time_passed = current_time - last_changed_timestamp

                # Calculate days, hours, and minutes
                td = timedelta(seconds=time_passed)
                days = td.days
                hours, remainder = divmod(td.seconds, 3600)
                minutes = remainder // 60

                # Format the time string appropriately
                formatted_time = ""
                if days > 0:
                    formatted_time += f"{days}d "
                if hours > 0:
                    formatted_time += f"{hours}h "
                if minutes > 0 or (days == 0 and hours == 0):
                    formatted_time += f"{minutes}m"

                result[service] = {
                    "status": data[service]["status"],
                    "last_changed": formatted_time.strip()  # Remove trailing space
                }
            else:
                result[service] = {
                    "status": "stopped",
                    "last_changed": "stopped"
                }

        return result
    else:
        print('Error: File not found - data.json')

async def get_system_usage():
    # Получаем использование памяти
    memory_usage = psutil.virtual_memory().percent
    
    # Получаем использование процессора
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Формируем результат
    result = {
        "memory_usage_percent": int(memory_usage),
        "cpu_usage_percent": int(cpu_usage)
    }
    
    return result