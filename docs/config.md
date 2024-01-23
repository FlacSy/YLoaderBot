# Документация по файлу настроек (`settings.ini`)

Файл `settings.ini` содержит основные настройки бота.

### Структура файла:

```ini
[Loging]
LOG_DIR = logs
LOG_MAX_SIZE = 15
LOG_BACKUP_COUNT = 3
```

### Пояснения:

- `LOG_DIR`: Путь к директории, в которой будут храниться логи.
- `LOG_MAX_SIZE`: Максимальный размер лога в мегабайтах (MB).
- `LOG_BACKUP_COUNT`: Количество резервных копий лога, которые будут сохранены.

---

# Документация по файлу с секретами (`secrets.ini`)

Файл `secrets.ini` содержит конфиденциальные данные, такие как токены, ключи и другие приватные данные.

### Структура файла:

```ini
[Bot]
BOT_TOKEN = <значение_токена_бота>

[Admin]
ADMIN_ID = <значение_ID_админа>

[Spotify]
client_id = <значение_client_id_Spotify>
secret = <значение_secret_Spotify>

[TikTokApi]
X-RapidAPI-Host = <значение_X-RapidAPI-Host_TikTokApi>
X-RapidAPI-Key = <значение_X-RapidAPI-Key_TikTokApi>
```

### Пояснения:

- `BOT_TOKEN`: Токен вашего бота для взаимодействия с платформой Telegram.
- `ADMIN_ID`: ID администратора бота, необходим для управления некоторыми функциями.
- `client_id` и `secret`: Идентификационные данные для взаимодействия с API Spotify.
- `X-RapidAPI-Host` и `X-RapidAPI-Key`: Значения заголовков для взаимодействия с API TikTok.

---
