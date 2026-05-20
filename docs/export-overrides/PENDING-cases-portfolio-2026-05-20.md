# PENDING — /cases/portfolio/ — 2026-05-20

> Статус страницы в чистом re-export `full-site-export-may21`.

## Что увидела

- HTTP 200, файл `cases/portfolio/index.html` весит 226KB, SSR-разметка есть.
- На viewport-скрине (1440×900) виден только Hero: «Latest Portfolio» + изображение, маленькая testimonial-карточка «Наталья CEO», credit «Разработали сайт мы :)».
- Сетки карточек кейсов **не видно** ни в visible viewport, ни ниже по innerText (после гидратации body innerText ≈ 865 символов — только nav + футер).

## Вывод

Коллекция cases пустая или не подключена к этой странице в Framer. Это не сломанная разметка — это пустой CMS-источник.

## Действие

- **Руками не чиним.** В рамках NoCodeExport-only — контент кейсов наполняется в Framer Studio, не в HTML.
- Помечено как PENDING для Вики: решить, наполнять коллекцию или менять источник кейсов в Framer.

## После наполнения cases в Framer

1. Re-export (`full-site-export-may22+`).
2. Перепроверить /cases/portfolio: ожидаемо сетка карточек кейсов под Hero.
3. Удалить этот PENDING-файл.
