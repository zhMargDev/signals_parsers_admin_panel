import sqlite3

# Создаем соединение с базой данных SQLite
conn = sqlite3.connect('parser.db')
c = conn.cursor()

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