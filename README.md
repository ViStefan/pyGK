# pyGK
SDK for clients and bots for govnokod.ru in `python`

Also contains `govnomatrix` — chat-bot for [#govnokod:matrix.org](https://riot.im/app/#/room/#govnokod:matrix.org)

# TODO
- [x] использовать общий конфиг-файл (`.gitignore` + `pyGK.cfg.sample`)
- [x] отрефакторить `comment['']` в объект
- [ ] переписать также построение дерева на `comment.parent` и `comment.children`
- [ ] поддержка поиска `ngk api search`
- [ ] настраиваемые системные уведомления (`notify-send`)
  - упоминание по имени
  - явное упоминание через `@`
  - любой комментарий
  - комментарий в треде пользователя
  - ответ на комментарий
  - звуковые уведомления (звук, чтение комментария вслух `spd-say`)
- [ ] возможность отвечать прямо из терминала 

# TODO (govnomatrix)

- [x] использовать `/ngk/api/post` для взятия родителя
- [ ] конвертер `html → bb` для обратного постинга
- [ ] распознавать цитирование `>`
- [ ] распознавать ответы пользователей и кросс-постить их
