import core.controller.controls_info as controls_info
import core.information.channels_and_folders as channels_and_folders

async def get_parsers_info():
    return await controls_info.get_controll_info()

async def get_system_usage():
    return await controls_info.get_system_usage()

async def get_channels_info():
    return await channels_and_folders.get_channels_info()

async def get_signals_by_period(period):
    return await channels_and_folders.get_signals_by_period(period)

async def get_signals_info_by_period(period):
    return await channels_and_folders.get_signals_info_by_period(period)

async def get_folders_channels_info(period):
    return await channels_and_folders.get_folders_channels_info(period)

async def get_long_and_short_diagram(long_x, short):
    """
        Вычесления процентное соотношение между лонг и шорт сообщениями для диаграммы на первой странице
    """
    # Общий объем сообщений
    total = long_x + short
    
    # Проверка, чтобы избежать деления на ноль
    if total == 0:
        return {"long": 0, "short": 0}
    
    # Вычисление процентного соотношения
    long_percent = (long_x / total) * 100
    short_percent = (short / total) * 100
    
    # Возвращение результата в виде словаря
    return {"long": long_percent, "short": short_percent}    

async def get_channels_diagram(active, disable, test):
    """
    Вычисление процентного соотношения между активными, неактивными и тестовыми каналами и возвращение результата в виде словаря.
    """
    # Общий объем каналов
    total = active + disable + test
    
    # Проверка, чтобы избежать деления на ноль
    if total == 0:
        return {"active": 0, "disable": 0, "test": 0, "css_gradient": "conic-gradient(yellow 0%, green 0%, red 0%)"}
    
    # Вычисление процентного соотношения
    active_percent = (active / total) * 100
    disable_percent = (disable / total) * 100
    test_percent = (test / total) * 100
    
    # Сортировка процентов и соответствующих цветов
    percentages = [(test_percent, 'yellow'), (active_percent, 'green'), (disable_percent, 'red')]
    percentages.sort(reverse=True, key=lambda x: x[0])
    
    # Формирование градиента для CSS
    first_percent, first_color = percentages[0]
    second_percent, second_color = percentages[1]
    third_percent, third_color = percentages[2]
    
    first_end = first_percent
    second_start = first_end
    second_end = second_start + second_percent
    third_start = second_end
    
    css_gradient = f"conic-gradient({first_color} 0% {first_end:.2f}%, {second_color} {first_end:.2f}% {second_end:.2f}%, {third_color} {second_end:.2f}% 100%)"
    
    # Возвращение результата в виде словаря
    return {
        "active": active_percent,
        "disable": disable_percent,
        "test": test_percent,
        "css_gradient": css_gradient
    }
