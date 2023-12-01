# 🤖 AI Task Manager Bot Documentation

The AI Task Manager Bot 📋🤖 is designed to assist users in managing their tasks on Telegram. It allows task addition and deletion using specific commands. The bot utilizes a Docker image named `ai_task_manager_bot` and relies on Redis 5 as its database. Additionally, it leverages LangChain and GIGACHAT from Sber as AI models.

## Getting Started 🚀

To start the bot, you can follow these steps:

### Manual Run

1. Ensure you have all the necessary key files for the bot.
2. Run the `main.py` file in your preferred Python environment.

### Docker Container 🐳

Alternatively, you can run the bot using Docker by executing the following command:

```bash
docker run -d ai_task_manager_bot
```

## Bot Commands (Russian) 🇷🇺

The bot understands commands in Russian. Here are the available commands:

- **Добавь задачи к списку:** Вход в режим добавления задачи.
- **Удалить из списка:** Вход в режим удаления задачи из списка.
- **Зови помощника:** Вызов помощника (по умолчанию имя помощника - Аади).
- **Покажи задачи:** Просмотр всех своих задач.

Additionally, the following commands can be used to interact with the bot:

- `/start`: Запуск бота.
- `/help`: Получение справки.
- `/gen`: Информация о работе бота.
- `/delete_all`: Удаление всех задач из списка.

## Usage 📝

### Task Management

When entering the "Добавление/Удаление" task mode, any input will be added or removed from the database. To exit the mode, input "End". The bot remains in the specified mode until it receives the "end" command.

### Additional Notes ℹ️

- Ensure all necessary key files are plugged in while running the bot, especially when using the Docker container.
- For any assistance or queries, feel free to utilize the `/help` command.

## Disclaimer ⚠️

Please note that the functionality and features of the bot may vary based on updates and improvements.
