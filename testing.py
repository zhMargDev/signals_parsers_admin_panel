import sqlite3

# SQL-запросы для создания таблицы и вставки данных
create_signals_table = """
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY,
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
    (1817625686, 2559, 'EVERESTTRADE', '2024-06-24', '12:18:00', 'XRP', 'LONG', '0.4969', 'False', '[]', "['0.5234']", 'Def', '20', 'Def'),
    (1817625686, 2560, 'EVERESTTRADE', '2024-06-24', '12:18:00', 'XRP', 'LONG', '0.4969', 'False', '[]', "['0.5234']", 'Def', '20', 'Def'),
    (1661883373, 565, 'самурайское чтиво катаны', '2024-06-24', '12:18:00', 'BTC', 'SHORT', '1,', 'False', "['2', '65900']", "['63393,', '62400,', '59800,', '50500']", 'Def', 'Def', 'Def'),
    (1678343787, 533, 'Масонское Логово', '2024-06-24', '12:18:00', 'LINK', 'LONG', '13.349', 'False', "['13.110']", "['14.171', '15.396', '16.895']", 'Def', 'Def', 'Def')
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
