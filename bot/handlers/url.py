import logging
import re
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.download_video import download_tiktok, download_youtube
from utils.download_music import download_spotify, download_soundcloud

async def url_handler(message: types.Message):
    if re.match(r'https?://(?:www\.)?tiktok\.com/.*', message.text) or re.match(r'https?://(?:www\.)?(?:youtube\.com/.*[=/]|youtu\.be/)([\w-]+)', message.text):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('MP4', callback_data='format_mp4'))
        markup.add(InlineKeyboardButton('MP3', callback_data='format_mp3'))

        await message.answer(message.text, reply_markup=markup)
    else:
        await download_handler(message=message, format='mp4') 

async def handle_format_choice(callback_query: types.CallbackQuery):
    if callback_query.data == 'format_mp4':
        await callback_query.message.answer("Ожидайте... Скачивание в формате MP4.")
        await download_handler(message=callback_query.message, format='mp4')
    elif callback_query.data == 'format_mp3':
        await callback_query.message.answer("Ожидайте... Скачивание в формате MP3.")
        await download_handler(message=callback_query.message, format='mp3')

async def download_handler(message: types.Message, format: str):
    if re.match(r'https?://(?:www\.)?(?:youtube\.com/.*[=/]|youtu\.be/)([\w-]+)', message.text):
        await download_youtube(url=message.text, message=message, format=format)

    elif re.match(r'https?://vm.tiktok.com/', message.text) or re.match(r'https?://(?:www\.)?tiktok\.com/.*', message.text):
        await download_tiktok(url=message.text, message=message, format=format)

    elif re.match(r'https?://open\.spotify\.com/track/([\w-]+)', message.text):
        await message.answer("Ожидайте...")
        await download_spotify(url=message.text, message=message)
    elif re.match(r'https?://soundcloud\.com/([\w-]+)/([\w-]+)', message.text):
        await message.answer("Ожидайте...")
        await download_soundcloud(url=message.text, message=message)
