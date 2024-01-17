import logging
import re
from aiogram import types

async def url_handler(message: types.Message):
    if re.match(r'https?://(?:www\.)?youtu(?:be\.com/.*v/|\.be/)([\w-]+)', message.text):
        await download_youtube(url=message.text)
    elif re.match(r'https?://(?:www\.)?tiktok\.com/.*', message.text):
        await download_tiktok(url=message.text)
    else:
        await message.answer("Этот бот принимает только ссылки на YouTube и TikTok.")

async def download_tiktok(url):
    pass

async def download_youtube(url):
    pass