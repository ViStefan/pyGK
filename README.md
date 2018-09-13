# pyGK
SDK for clients and bots for [govnokod.ru](http://govnokod.ru) in `python`

Also contains `govnomatrix` — chat-bot for [#govnokod:matrix.org](https://riot.im/app/#/room/#govnokod:matrix.org)

# RTFM
- [ngkapi.py](ngkapi.py) — реализация api [gcode.cx](http://gcode.cx)
- [core.py](core.py) — обёртка для общего конфига и других вещей, которые могут быть глобально доступны всем частям приложения (пример конфига: [`pyGK.cfg.sample`](pyGK.cfg.sample))
- [govnomatrix.py](govnomatrix.py) — обёртка нескольких методов API matrix и преобразователь `html` для корректного отображения
- [stock.py](stock.py) — демон для отображения живого стока в терминале, он же, если govnomatrix включен в конфиге, ретранслирует новые комментарии на канал в matrix

# TODO
Методы GK:
- [ ] `/user/login`
- [ ] `/comments/:post/post?replyTo=:comment`

Методы ngk API:
- [x] `/comment`
- [x] `/post` (частично)
- [ ] `/search`

govnomatrix:
- [ ] нормализация `html → html` для `matrix` (`pandoc`)
- [ ] конвертер `html → bb` для обратного постинга (`pandoc`)
- [ ] распознавание ответов пользователей и кросс-постинг
