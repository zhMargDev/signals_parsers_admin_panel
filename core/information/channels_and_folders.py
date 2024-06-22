import sqlite3

async def get_channels_info():
    conn = sqlite3.connect('parser.db')
    cursor = conn.cursor()

    # Получение всех папок
    cursor.execute('SELECT * FROM folders')
    folders = cursor.fetchall()

    # Получение всех каналов
    cursor.execute('SELECT * FROM channels')
    channels = cursor.fetchall()

    result = {
        "global_info" : {
            "channels_count": len(channels),
            "folders_count": len(folders)
        },
        "all_info": [],
        "folders_channels_count": {
            "active": 0,
            "test": 0,
            "disable": 0
        }
    }

    # Рассфасофка данных по количеству включенных, отключенных и тестовых каналов по папкам
    for folder in folders:
        folder_name = folder[2]
        folder_id = folder[1]

        deactive = 0
        active = 0
        test = 0

        for channel in channels:
            if channel[1] == folder_id:
                if channel[4] == 'test': 
                    test += 1
                    result['folders_channels_count']['test'] += 1
                elif channel[4] == 'active': 
                    active += 1
                    result['folders_channels_count']['active'] += 1
                elif channel[4] == 'disable': 
                    deactive += 1
                    result['folders_channels_count']['disable'] += 1

        result["all_info"].append({
            'folder_name': folder_name,
            'deactive': deactive,
            'test': test,
            'active': active
        })

    cursor.close()
    conn.close()

    return result