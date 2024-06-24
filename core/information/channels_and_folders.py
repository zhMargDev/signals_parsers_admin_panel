import sqlite3

from datetime import datetime, timedelta
from collections import defaultdict

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


async def get_signals_by_period(period):
    # Определяем текущую дату и время
    now = datetime.now()

    # Устанавливаем период по умолчанию как 1 день
    if period is None: 
        period = '1d'

    # Определяем дату начала периода
    if period == '1d':
        start_date = now - timedelta(days=1)
    elif period == '1w':
        start_date = now - timedelta(weeks=1)
    elif period == '1m':
        start_date = now - timedelta(days=30)  # Приблизительно 1 месяц
    elif period == '1y':
        start_date = now - timedelta(days=365)  # Приблизительно 1 год
    elif period == 'all':
        start_date = None  # Не будет фильтровать по дате
    else:
        raise ValueError("Unsupported period value")

    # Форматируем дату начала в строку для SQL-запроса
    if start_date:
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('parser.db')
    cursor = conn.cursor()

    # Формируем SQL-запрос в зависимости от периода для получения всех сигналов
    if start_date:
        cursor.execute('''
            SELECT * FROM signals 
            WHERE datetime(date || ' ' || time) >= ?
        ''', (start_date_str,))
    else:
        cursor.execute('SELECT * FROM signals')

    # Получаем результаты
    signals = cursor.fetchall()

    # Формируем SQL-запрос в зависимости от периода для получения всех тестовых сигналов
    if start_date:
        cursor.execute('''
            SELECT * FROM testing_signals 
            WHERE datetime(date || ' ' || time) >= ?
        ''', (start_date_str,))
    else:
        cursor.execute('SELECT * FROM testing_signals')

    # Получаем результаты
    test_signals = cursor.fetchall()

    # Определяем общее количество каналов из которых были сигналы
    channels = []

    # Определяем общее количество сигналов в лонг и шорт 
    long_signals = 0
    short_signals = 0

    for signal in signals:
        if signal[1] not in channels: 
            channels.append(signal[1])
        if signal[7] == 'LONG': 
            long_signals += 1
        else: 
            short_signals += 1

    for signal in test_signals:
        if signal[1] not in channels: 
            channels.append(signal[1])
        if signal[7] == 'LONG': 
            long_signals += 1
        else: 
            short_signals += 1

    # Подсчет количества одинаковых сигналов
    signal_counts = defaultdict(int)
    for signal in signals:
        signal_key = (signal[6], signal[7], signal[8], signal[9], signal[10], signal[11], signal[12], signal[13], signal[14])  # Используйте нужные столбцы для группировки
        signal_counts[signal_key] += 1

    # Подсчет количества одинаковых тестовых сигналов
    test_signal_counts = defaultdict(int)
    for signal in test_signals:
        test_signal_key = (signal[6], signal[7], signal[8], signal[9], signal[10], signal[11], signal[12], signal[13], signal[14])  # Используйте нужные столбцы для группировки
        test_signal_counts[test_signal_key] += 1

    # Подсчет количества похожих сигналов
    similar_signal_counts = defaultdict(int)
    for signal in signals:
        similar_signal_key = (signal[6], signal[7])  # Группируем по coin и trend
        similar_signal_counts[similar_signal_key] += 1

    # Подсчет количества похожих тестовых сигналов
    similar_test_signal_counts = defaultdict(int)
    for signal in test_signals:
        similar_test_signal_key = (signal[6], signal[7])  # Группируем по coin и trend
        similar_test_signal_counts[similar_test_signal_key] += 1

    result = {
        "channels_count": len(channels), # Общее количество каналов
        "testing_signals": len(test_signals), # Количество тестовых сигналов
        "monitoring_signals": len(signals), # Количество сигналов
        "long_signals_count": long_signals, # Общее количество лонг сигналов
        "short_signals_count": short_signals, # Общее количество шорт сигналов
        "duplicate_signals_count": sum(count > 1 for count in signal_counts.values()),  # Количество дублирующихся сигналов
        "duplicate_test_signals_count": sum(count > 1 for count in test_signal_counts.values()),  # Количество дублирующихся тестовых сигналов
        "similar_signals_count": sum(count > 1 for count in similar_signal_counts.values()),  # Количество похожих сигналов
        "similar_test_signals_count": sum(count > 1 for count in similar_test_signal_counts.values())  # Количество похожих тестовых сигналов
    }

    cursor.close()
    conn.close()

    return result


async def get_signals_info_by_period(period):
    """
        Получение подробных данных о сигналах за период
    """
    # Определяем текущую дату и время
    now = datetime.now()

    # Устанавливаем период по умолчанию как 1 день
    if period is None: 
        period = '1d'

    # Определяем дату начала периода
    if period == '1d':
        start_date = now - timedelta(days=1)
    elif period == '1w':
        start_date = now - timedelta(weeks=1)
    elif period == '1m':
        start_date = now - timedelta(days=30)  # Приблизительно 1 месяц
    elif period == '1y':
        start_date = now - timedelta(days=365)  # Приблизительно 1 год
    elif period == 'all':
        start_date = None  # Не будет фильтровать по дате
    else:
        raise ValueError("Unsupported period value")

    # Форматируем дату начала в строку для SQL-запроса
    if start_date:
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('parser.db')
    cursor = conn.cursor()

    # Формируем SQL-запрос в зависимости от периода для получения всех сигналов из двух таблиц
    if start_date:
        query = '''
            SELECT * FROM signals 
            WHERE datetime(date || ' ' || time) >= ?
            UNION ALL
            SELECT * FROM testing_signals 
            WHERE datetime(date || ' ' || time) >= ?
        '''
        params = (start_date_str, start_date_str)
    else:
        query = '''
            SELECT * FROM signals
            UNION ALL
            SELECT * FROM testing_signals
        '''
        params = ()

    cursor.execute(query, params)

    # Получаем результаты
    signals = cursor.fetchall()

    channels_count = []
    # Определение каналов
    for signal in signals:
        if signal[1] not in channels_count:
            channels_count.append(signal[1])

    # Получение всех каналов
    cursor.execute('SELECT * FROM channels')
    channels = cursor.fetchall()

    # Определяем сколько сигналов было добавляя id каналов в массив
    signals_count = []
    for signal in signals: signals_count.append(signal[1])

    # Получаем список папок
    cursor.execute('SELECT * FROM folders')
    folders = cursor.fetchall()

    # Создаем массив со всеми папками и 0 значением как количество
    folders_counts = []
    for folder in folders:
        folders_counts.append({
            'folder_id': folder[1],
            'folder_name': folder[2],
            'signals_count': 0
        })

    # Добавляем количество сигналов для каждой папки
    for folder in folders_counts:
        for channel_id in signals_count:
            for channel in channels:
                if channel[2] == channel_id and folder['folder_id'] == channel[1]:
                    folder["signals_count"] += 1

    # Удаляем папки у которых количество сигналов равен нулю
    flag_folders_counts = []
    for folder in folders_counts:
        if folder["signals_count"] != 0:
            flag_folders_counts.append(folder)
    folders_counts = flag_folders_counts

    # Определяем похожие кониы и тренд и общее их количество
    similar_signals = []
    # Сгруппируем сигналы по coin и trend
    grouped_signals = defaultdict(list)
    for signal in signals:
        coin = signal[6]
        trend = signal[7]
        grouped_signals[(coin, trend)].append(signal)

    # Подсчитываем количество сигналов в каждой группе и добавляем в similar_signals
    for (coin, trend), signals_group in grouped_signals.items():
        count = len(signals_group)
        similar_signals.append({
            "coin": coin,
            "trend": trend,
            "count": count
        })

    # Определяем похожие кониы и тренд и общее их количество
    dublicate_signals = []
    # Сгруппируем сигналы по coin и trend
    grouped_signals = defaultdict(list)
    for signal in signals:
        coin = signal[6]
        trend = signal[7]
        tvh = signal[8]
        rvh = signal[9]
        lvh = signal[10]
        targets = signal[11]
        stop_less = signal[12]
        leverage = signal[13]
        margin = signal[14]
        grouped_signals[(coin, trend, tvh, rvh, lvh, targets, stop_less, leverage, margin)].append(signal)

    # Подсчитываем количество сигналов в каждой группе и добавляем в dublicate_signals
    for (coin, trend, tvh, rvh, lvh, targets, stop_less, leverage, margin), signals_group in grouped_signals.items():
        count = len(signals_group)
        dublicate_signals.append({
            "coin": coin,
            "trend": trend,
            "count": count
        })

    result = {
        "signals_count": len(signals), # Общее количество каналов
        "folders_and_signals_count": folders_counts, # Название папок и количество сигналов в них
        "similar_signals": similar_signals, # Похожие сигналы
        "dublicate_signals" : dublicate_signals
    }

    cursor.close()
    conn.close()

    return result
