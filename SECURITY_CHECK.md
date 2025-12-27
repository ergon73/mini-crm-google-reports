# Проверка безопасности перед коммитом

## ✅ Защищённые файлы

Все следующие файлы **НЕ попадут** в Git репозиторий:

1. ✅ `secrets/*.json` - все JSON файлы с credentials
2. ✅ `token.pickle` - OAuth токен
3. ✅ `data/*.db` - база данных
4. ✅ `data/*.json` - настройки (могут содержать пути)
5. ✅ `__pycache__/` - кеш Python
6. ✅ `.venv/` - виртуальное окружение

## Проверка перед коммитом

Перед коммитом выполните:

```bash
# Проверить, что секреты игнорируются
git status --ignored | grep secrets
git status --ignored | grep token

# Убедиться, что JSON файлы не добавятся
git check-ignore -v secrets/*.json
git check-ignore -v token.pickle
```

## Если файлы уже были добавлены

Если вы случайно добавили секреты в Git до того, как добавили их в .gitignore:

```bash
# Удалить файлы из индекса (но оставить на диске)
git rm --cached secrets/*.json
git rm --cached token.pickle

# Закоммитить удаление
git commit -m "chore: remove secrets from git tracking"

# Если уже был push, нужно отозвать секреты:
# 1. Смените все credentials
# 2. Используйте git filter-branch или BFG Repo-Cleaner
```

## Рекомендации

- ✅ Всегда проверяйте `git status` перед коммитом
- ✅ Используйте `git status --ignored` для проверки игнорируемых файлов
- ✅ Не коммитьте файлы с реальными credentials
- ✅ Используйте `.env.example` для примеров конфигурации

