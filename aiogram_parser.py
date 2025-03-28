import asyncio
import zipfile

import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import os

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Вставьте ссылки для поиска картинок")


@dp.message()
async def get_link(message: types.Message):
    urls = message.text.replace(" ", "%20").split()
    tasks = [get_pic(url) for url in urls]
    await asyncio.gather(*tasks)
    await message.answer("Скачивание завершено")
    await zipped()
    await bot.send_document(chat_id=message.from_user.id, document=FSInputFile("zip/files.zip"))
    await delete_file()


async def get_pic(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.read()
            if "?" in url:
                with open(f'files/{url.split("?")[-1]}.{url.split(".")[-1].split("?")[0]}', "wb") as file:
                    file.write(result)
            else:
                with open(f'files/{url.split("/")[-1]}', "wb") as file:
                    file.write(result)



async def zipped():
    path = "files"
    file_dir = os.listdir("files")
    with zipfile.ZipFile('zip/files.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file in file_dir:
            add_file = os.path.join(path, file)
            zf.write(add_file)


async def delete_file():
    path = "files"
    file_dir = os.listdir(path)
    for file in file_dir:
        del_file = os.path.join(path, file)
        os.remove(del_file)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
