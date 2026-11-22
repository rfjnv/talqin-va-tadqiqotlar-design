# Talqin va tadqiqotlar — фирменный стиль и тема OJS

Логотип, макеты сайта и тема для Open Journal Systems научно-методического журнала «Talqin va tadqiqotlar» (ISSN 2181-3035).

Готовую тему берите на странице **Releases**: файл `tvt.tar.gz` загружается в OJS через «Модули → Загрузить новый модуль». Пошаговая установка: [`ojs-theme/README.md`](ojs-theme/README.md).

## Что где лежит

| Папка | Содержимое |
|---|---|
| `ojs-theme/tvt/` | исходники темы OJS 3.3 (дочерняя тема Default): LESS, шрифты, фото |
| `ojs-theme/snippets/` | HTML-вставки для настроек журнала: первый экран, правая колонка, разделы главной, подвал |
| `mockup-v3/` | актуальный макет: главная, статья, архив, «Mualliflarga», «Tahririyat», «Jurnal haqida»; страницы собирает `build_pages.py` из `data/` |
| `mockup/`, `mockup-v2/` | ранние варианты, оставлены для истории |
| `svg/`, `png/`, `favicon.ico` | логотип: горизонтальный, вертикальный, монограмма, favicon, иконки для телефонов |
| `photos/` | фотографии с Wikimedia Commons, авторы и лицензии в `photos/CREDITS.md` |
| `ornament/` | орнамент из ранней версии (в текущей теме не используется) |
| `_fonts/` | исходные шрифты для пересборки логотипа и темы (SIL OFL) |

## Логотип

| Файл | Где использовать |
|---|---|
| `svg/tvt-logo-horizontal-navy.svg`, `png/tvt-logo-horizontal-navy.png` | шапка сайта (светлый фон) |
| `svg/tvt-logo-horizontal-ivory.svg` | на тёмно-синем фоне |
| `svg/tvt-logo-stacked-*.svg` | обложка, титул PDF, сертификаты |
| `svg/tvt-monogram-*.svg` | знак отдельно |
| `favicon.ico`, `svg/favicon.svg`, `png/apple-touch-icon.png`, `png/icon-*.png` | иконки сайта |

Все SVG собраны из кривых, шрифты для них не нужны.

## Пересборка

```
python build_logo.py   # SVG логотипа (подпись и параметры монограммы — вверху файла)
python render_png.py   # PNG и favicon.ico (нужен Chrome)
```

Нужны Python 3 и пакеты `fonttools`, `skia-pathops`, `pillow`.

Пересобрать страницы макета после правки шапки, подвала или данных: `python mockup-v3/build_pages.py`.

Посмотреть макеты: `python -m http.server 8765`, затем открыть `http://localhost:8765/mockup-v3/index.html`.

## Лицензии

- Код (тема OJS в `ojs-theme/tvt`, HTML/CSS-макеты, скрипты сборки) — лицензия MIT, см. [`LICENSE`](LICENSE). Его можно свободно использовать и менять, в том числе для других журналов. MIT не распространяется на логотип, название журнала, шрифты и фотографии: для них действуют условия ниже.
- Шрифты Literata, Inter, IBM Plex Mono, Cormorant Garamond, Montserrat — SIL Open Font License 1.1.
- Фотографии — CC BY-SA, авторы указаны в `photos/CREDITS.md`. При использовании на сайте подпись с автором и лицензией обязательна.
- Логотип и тексты принадлежат редакции журнала.
- Логотип и название журнала «Talqin va tadqiqotlar» не являются свободными для использования: их нельзя применять в других проектах без письменного согласия редакции. Шрифты и фотографии распространяются по своим лицензиям, указанным выше.
