# Checklist релиза MVP

## 1. Версия и изменения

- [ ] Обновлен `src/solidflow/core/config.py` (`Config.VERSION`)
- [ ] Обновлен `pyproject.toml` (`[project].version`)
- [ ] Обновлен `docs/CHANGELOG.md`
- [ ] Тэг в git: `vX.Y.Z`

## 2. Тестирование

### Unit tests

- [ ] `pytest tests/unit`

### Integration tests (опционально)

- [ ] `SOLIDFLOW_RUN_INTEGRATION=1 pytest -m integration`

### Ручное тестирование (минимум)

- [ ] Открыть STL
- [ ] Проверить 3D viewport (вращение/масштаб/панорама)
- [ ] Выполнить анализ
- [ ] Выполнить ремонт
- [ ] Сохранить как новый файл STL
- [ ] Открыть сохраненный STL (проверка экспорта)
- [ ] Проверить предупреждение о несохраненных изменениях (закрытие/открытие)

## 3. Сборка дистрибутивов

### Локально

- [ ] `scripts/build.sh` (Linux/macOS) или `scripts/build.bat` (Windows)
- [ ] Проверить запуск файла из `dist/`

### CI artifacts

- [ ] GitHub Actions build job успешно завершен
- [ ] Артефакты скачиваются и запускаются

## 4. Документация

- [ ] `README.md` актуален
- [ ] `docs/USER_GUIDE.md` актуален
- [ ] `docs/FAQ.md` актуален
- [ ] `docs/TESTING.md` актуален

## 5. GitHub Release

- [ ] Создан Release
- [ ] Прикреплены артефакты сборки
- [ ] В Release notes указан краткий changelog


