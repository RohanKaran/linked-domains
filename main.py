from datetime import datetime
from gsp.gsp import read, writeLog, update, addUnique
from scrapper.scrapper import Scraper
from fastapi import FastAPI, BackgroundTasks, HTTPException

app = FastAPI()


async def scraper():
    try:
        sheet1 = read()
        with Scraper(teardown=True) as bot:
            bot.login('rahulthepcl@gmail.com', 'Adsense007##')
            for i, web in enumerate(sheet1):
                try:
                    updated_date_link = bot.scrape(web[0], web[1], web[2])
                    print(updated_date_link)
                    update([updated_date_link], i+2)
                except Exception as e:
                    print(e)
                    continue
        writeLog([[str(datetime.now()) + " Status: Success"]])
        addUnique()

    except HTTPException as e:
        print(e)
        writeLog([[str(datetime.now()) + " Status:" + str(e)]])


@app.get("/")
async def root():
    return {"message": "Go to https://something/docs"}


@app.get("/start/")
async def start():
    await scraper()
    return {"message": "Scraping started. Please open spreadsheet to view output."}
