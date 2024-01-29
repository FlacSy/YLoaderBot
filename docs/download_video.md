### Документация по utils/wnload_video.py

#### Функция `get_tiktok_video_id`

```python
async def get_tiktok_video_id(url):
    """
    Получает идентификатор видео TikTok из переданного URL.

    Параметры:
        - url (str): URL-адрес TikTok видео.

    Возвращает:
        - str: Идентификатор видео TikTok или None, если не найден.
    """
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)
    return None
```

#### Функция `download_tiktok`

```python
async def download_tiktok(url, output_path="downloads", message=None):
    """
    Загружает видео TikTok по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес TikTok видео.
        - output_path (str): Путь для сохранения загруженного видео (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки видео.

    Примечание:
        - Если указан параметр `message`, после загрузки видео отправляет его пользователю.
        - Видео сохраняется в формате MP4 в указанной директории.
    """
    response = requests.get(url)
    video_id = await get_tiktok_video_id(response.url)
    response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')
    filename = f"{output_path}/{video_id}.mp4"
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
            
        if os.path.exists(filename) and message:
            await message.answer_video(video=types.InputFile(filename))
            os.remove(filename)
```

#### Функция `download_youtube`

```python
async def download_youtube(url, output_path="downloads", message=None):
    """
    Загружает видео с YouTube по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес YouTube видео.
        - output_path (str): Путь для сохранения загруженного видео (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки видео.

    Примечание:
        - Если указан параметр `message`, после загрузки видео отправляет его пользователю.
        - Видео сохраняется в формате, указанном в метаданных YouTube видео.
    """
    options = {
        'format': 'bestvideo[filesize<50M]+bestaudio/best[filesize<50M]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'video')
        filename = ydl.prepare_filename(info_dict)

        ydl.download([url])

        # Check if the file exists before sending
        if os.path.exists(filename) and message:
            await message.answer_video(caption=title, video=types.InputFile(filename))
            os.remove(filename)
```

#### Общая информация

- Используется библиотека `yt_dlp` для работы с YouTube API.
- Для обработки URL TikTok видео используется регулярное выражение.
- Загруженные видео сохраняются в указанной директории, и, если указан параметр `message`, отправляются пользователю.
- В случае YouTube видео, выбирается наилучшее качество видео и аудио, при условии, что размер файла не превышает 50 МБ.