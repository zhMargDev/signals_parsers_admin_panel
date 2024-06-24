import core.controller.start_and_stop as start_stop
import core.core as core

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключаем папку с шаблонами и статическими файлами
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Определяем маршрут для каждой страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, period: str = Query(None), folder_name: str = Query(None)):
    parsers_info = await core.get_parsers_info()
    get_system_usage = await core.get_system_usage()
    get_channels_info = await core.get_channels_info()
    get_signals_by_period = await core.get_signals_by_period(period)
    get_signals_info_by_period = await core.get_signals_info_by_period(period)
    get_long_and_short_diagram = await core.get_long_and_short_diagram(get_signals_by_period['long_signals_count'], get_signals_by_period['short_signals_count'])
    get_channels_diagram = await core.get_channels_diagram(get_channels_info['folders_channels_count']['active'], get_channels_info['folders_channels_count']['disable'], get_channels_info['folders_channels_count']['test'])
    get_folders_channels_info = await core.get_folders_channels_info(period, folder_name)
    data = {
        "parsers_info": parsers_info,
        "get_system_usage": get_system_usage,
        "get_channels_info": get_channels_info,
        "get_signals_by_period": get_signals_by_period,
        "get_signals_info_by_period": get_signals_info_by_period,
        "period":period,
        "get_long_and_short_diagram": get_long_and_short_diagram,
        "get_channels_diagram": get_channels_diagram,
        "get_folders_channels_info": get_folders_channels_info
    }
    return templates.TemplateResponse("PageOne.html", {"request": request, "data": data})

@app.get("/folders_and_channels", response_class=HTMLResponse)
async def read_page_two(request: Request):
    parsers_info = await core.get_parsers_info()
    get_system_usage = await core.get_system_usage()
    data = {
        "parsers_info": parsers_info,
        "get_system_usage": get_system_usage
    }
    return templates.TemplateResponse("PageTwo.html", {"request": request, "data": data})

@app.get("/settings", response_class=HTMLResponse)
async def read_page_three(request: Request):
    parsers_info = await core.get_parsers_info()
    get_system_usage = await core.get_system_usage()
    data = {
        "parsers_info": parsers_info,
        "get_system_usage": get_system_usage
    }
    return templates.TemplateResponse("PageThree.html", {"request": request, "data": data})

@app.get("/start_or_stop_parser", response_class=HTMLResponse)
async def start_or_stop_parser():
    await start_stop.start_stop_parser()
    return RedirectResponse(url="/")

@app.get("/start_or_stop_packeger", response_class=HTMLResponse)
async def start_or_stop_packeger():
    await start_stop.start_stop_packager()
    return RedirectResponse(url="/")

@app.get("/restart_packager_and_parser", response_class=HTMLResponse)
async def restart():
    await start_stop.restart()
    return RedirectResponse(url="/")
