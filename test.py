import sqlite3

# Создаем соединение с базой данных SQLite
conn = sqlite3.connect('parser.db')
c = conn.cursor()

create_signals_table = """
CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER,
    message_id INTEGER,
    channel_name TEXT,
    date TEXT,
    time TEXT,
    coin TEXT,
    trend TEXT,
    tvh TEXT,
    rvh TEXT,
    lvh TEXT,
    targets TEXT,
    stop_loss TEXT,
    leverage TEXT,
    margin TEXT
);
"""

insert_data = """
INSERT INTO signals (channel_id, message_id, channel_name, date, time, coin, trend, tvh, rvh, lvh, targets, stop_loss, leverage, margin)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

# Данные для вставки
data_to_insert = [
    (1817625686, 2559, 'EVERESTTRADE', '2024-06-24', '12:08:00', 'XRP', 'LONG', '0.4969', 'False', '[]', "['0.5234']", 'Def', '20', 'Def'),
    (1817625686, 2560, 'EVERESTTRADE', '2024-06-24', '12:08:00', 'XRP', 'LONG', '0.4969', 'False', '[]', "['0.5234']", 'Def', '20', 'Def'),
    (1661883373, 565, 'самурайское чтиво катаны', '2024-06-24', '12:08:00', 'BTC', 'SHORT', '1,', 'False', "['2', '65900']", "['63393,', '62400,', '59800,', '50500']", 'Def', 'Def', 'Def'),
    (1678343787, 533, 'Масонское Логово', '2024-06-24', '12:08:00', 'LINK', 'LONG', '13.349', 'False', "['13.110']", "['14.171', '15.396', '16.895']", 'Def', 'Def', 'Def')
]

# Функция для выполнения SQL-запросов
def execute_sql_query(query, data=None):
    connection = sqlite3.connect('parser.db')  # Укажите имя вашей SQLite базы данных
    cursor = connection.cursor()
    if data:
        cursor.executemany(query, data)
    else:
        cursor.execute(query)
    connection.commit()
    connection.close()

# Создание таблицы
execute_sql_query(create_signals_table)

# Вставка данных
execute_sql_query(insert_data, data_to_insert)
create_testing_signals_table = """
CREATE TABLE IF NOT EXISTS testing_signals (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER,
    message_id INTEGER,
    channel_name TEXT,
    date TEXT,
    time TEXT,
    coin TEXT,
    trend TEXT,
    tvh TEXT,
    rvh TEXT,
    lvh TEXT,
    targets TEXT,
    stop_loss TEXT,
    leverage TEXT,
    margin TEXT
);
"""
insert_data_testing = """
INSERT INTO testing_signals (channel_id, message_id, channel_name, date, time, coin, trend, tvh, rvh, lvh, targets, stop_loss, leverage, margin)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
# Данные для вставки
data_to_insert = [
    (1817625686, 2559, 'EVERESTTRADE', '2024-06-24', '12:08:00', 'XRP', 'LONG', '0.4969', 'False', '[]', "['0.5234']", 'Def', '20', 'Def'),
    (1817625686, 2560, 'EVERESTTRADE', '2024-06-24', '12:08:00', 'XRP', 'LONG', '0.4969', 'False', '[]', "['0.5234']", 'Def', '20', 'Def'),
    (1661883373, 565, 'самурайское чтиво катаны', '2024-06-24', '12:08:00', 'BTC', 'SHORT', '1,', 'False', "['2', '65900']", "['63393,', '62400,', '59800,', '50500']", 'Def', 'Def', 'Def'),
    (1678343787, 533, 'Масонское Логово', '2024-06-24', '12:08:00', 'LINK', 'LONG', '13.349', 'False', "['13.110']", "['14.171', '15.396', '16.895']", 'Def', 'Def', 'Def')
]

def execute_sql_query(query, data=None):
    connection = sqlite3.connect('parser.db')  # Укажите имя вашей SQLite базы данных
    cursor = connection.cursor()
    if data:
        cursor.executemany(query, data)
    else:
        cursor.execute(query)
    connection.commit()
    connection.close()

# Вставка данных в testing_signals
execute_sql_query(insert_data_testing, data_to_insert)

# Добавляем записи в таблицу folders
folders_data = [
    (1, 'analytics', 'disable'),
    (2, 'news', 'disable'),
    (3, 'RV', 'disable'),
    (4, 'RP', 'disable'),
    (5, 'RF', 'active'),
    (6, 'TEST', 'disable'),
    (7, 'TEST', 'active')
]

c.executemany('INSERT INTO folders (folder_id, folder_title, folder_status) VALUES (?, ?, ?)', folders_data)

# Добавляем запись в таблицу signals
signals_data = [
    (1, 1679964750, 'CryptoComandos', 'test'),
    (1, 14479964750, 'grghehgeth', 'active'),
    (1, 1679954750, 'asfaffgeg', 'disable'),
    (1, 16794634750, 'fhbdfgbsfh', 'test'),
    (1, 16719964750, 'hthtjyjryj', 'active'),
    (1, 16799654750, 'qwerqewrqwer', 'test'),
    (2, 167994564750, 'erwererwet', 'test'),
    (2, 16739964750, 'wetwegggwgw', 'active'),
    (2, 167992364750, 'llpmkjkl', 'disable'),
    (2, 16793964750, 'uotukondfh', 'test'),
    (2, 16799647520, 'fyjdftuunssdry', 'test'),
    (2, 167996354750, 'tutfmutmut', 'test'),
    (3, 167996564750, 'srfghbsdfra', 'active'),
    (3, 167964750, 'hthtrujthte', 'disable'),
    (3, 1664750, 'avrfawvfawvbh', 'test'),
    (3, 79964750, 'edtbtggjqq', 'test'),
    (3, 679964750, 'hfjmfdcbzse', 'active'),
    (3, 19964750, 'pjkfffvv', 'active'),
    (3, 16799647, 'QEWEWAE', 'test'),
    (4, 167996475, 'CryptoCstggrg', 'active'),
    (4, 167996470, 'thjdfhoComandos', 'test'),
    (4, 167996450, 'rgsrgsdfgn', 'disable'),
    (4, 1679964, 'jnjfggfjfyu', 'test'),
    (4, 1679750, 'bryhyrhrtybh', 'test'),
    (4, 1679965574750, 'hbthuyrtgv', 'active'),
    (5, 16799655554750, 'gdfyftf', 'disable'),
    (5, 167994455764750, 'tnhtrhnrtu', 'active'),
    (5, 1679242750, 'geyeyndh', 'test'),
    (5, 167996424244750, 'hbrthdsfsy', 'test'),
    (6, 57575757721, 'thdhbrhyf', 'test'),
    (6, 92424264750, 'svtgvfgvrdbyb', 'active'),
    (6, 577774750, 'vsrttutseryv', 'disable'),
    (6, 16792224750, 'yvsetdfybrts', 'test'),
    (6, 167911111, 'ryetsvhurtwt', 'test'),
    (7, 16733333, 'vydftgwestv', 'active'),
    (7, 1677777554750, 'vvrbygbvdv', 'disable'),
    (7, 75757854750, 'fwegbgtydgfcfvb', 'active'),
    (7, 167242427750, 'tgthuhrryhrty', 'test'),
]

c.executemany('INSERT INTO channels  (folder_id, channel_id, channel_name, channel_stats) VALUES (?, ?, ?, ?)', signals_data)

# Применяем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()