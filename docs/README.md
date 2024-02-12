# YLoaderBot

## Навигатор по README

1. [**Описание проекта**](#описание-проекта)
2. [**Начало работы**](#начало-работы)
   - [Клонирование репозитория](#1-клонирование-репозитория)
   - [Переход в директорию](#2-переход-в-директорию)
   - [Установка зависимостей](#3-установка-всех-зависимостей)
   - [Установка ffmpeg](#4-установка-ffmpeg)
   - [Настройка конфигурации](#5-настройка-конфигурации)
   - [Запуск бота](#6-запуск-бота)

## Описание проекта

Проект представляет собой Telegram бота для скачивания контента. Поддерживаются следующие источники:

- **YouTube**
- **YouTube Shorts**
- **TikTok**
- **Spotify**
- **SoundCloud**
- **Apple Music**

## Начало работы

### 1. Клонирование репозитория

```bash
git clone https://github.com/FlacSy/YLoaderBot.git
```

### 2. Переход в директорию

```bash
cd YLoaderBot
```

### 3. Установка всех зависимостей

- **Mac/Linux**

  ```bash
  pip3 install -r requirements.txt
  ```

- **Windows**

  ```bash
  pip install -r requirements.txt
  ```

### 4. Установка ffmpeg

- **Mac**

  ```bash
  brew install ffmpeg
  ```

- **Linux**

  ```bash
  sudo apt install ffmpeg
  ```

- **Windows**
  [Официальный сайт](https://ffmpeg.org/download.html#build-windows)

### 5. Настройка конфигурации

Подробнее в [config.md](./config.md)

### 6. Запуск бота

- **Mac/Linux**

  ```bash
  python3 main.py
  ```

- **Windows**

  ```bash
  python main.py
  ```

## Архитектура проекта

Подробнее в [architecture.md](./architecture.md)