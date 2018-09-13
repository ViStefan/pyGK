# pyGK
SDK for clients and bots for [govnokod.ru](http://govnokod.ru) in `python`

Also contains `govnomatrix` — chat-bot for [#govnokod:matrix.org](https://riot.im/app/#/room/#govnokod:matrix.org)

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
