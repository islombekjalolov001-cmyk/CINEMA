# 🎬 Cinema Telegram Bot

Aiogram 3.x asosida yozilgan, to'liq professional va modulli kino-bot. UZ/RU/EN
tillarini Fluent (.ftl) va Fluentogram orqali qo'llab-quvvatlaydi.

## Xususiyatlar

- Majburiy obuna tekshiruvi (kanal(lar)ga obuna bo'lmaguncha bot ishlamaydi)
- Kod, nom, janr va davlat bo'yicha qidiruv (barchasi pagination bilan)
- ❤️ Like tizimi va "Sevimli kinolarim"
- 📩 Kino so'rovlari (foydalanuvchi -> admin)
- To'liq admin panel: kino qo'shish/tahrirlash/o'chirish, kanal boshqaruvi,
  broadcast (progress bilan), statistika, Excel export, barcha kino kodlari
  ro'yxati (pagination + har biriga tahrirlash/o'chirish)
- Async SQLite (aiosqlite), FSM (aiogram StatesGroup), custom middleware va
  filterlar, global error handler, fayl asosidagi logging (info/warning/error)

## O'rnatish

```bash
cd cinema_bot
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

1. `.env.example` faylini `.env` nomiga nusxalang va o'z qiymatlaringizni kiriting:

```bash
cp .env.example .env
```

```
BOT_TOKEN=123456:ABC-your-telegram-bot-token   # @BotFather dan oling
ADMIN_IDS=8560459628                           # vergul bilan bir nechta admin ID
DB_PATH=data/database.db
LOG_PATH=logs/bot.log
```

2. Botni ishga tushiring:

```bash
python3 main.py
```

## Muhim eslatmalar

- Botni **admin** qilib qo'shing `@uzbmediakino` kanaliga (majburiy kanal), aks
  holda `bot.get_chat_member` chaqiruvi xato qaytaradi va obuna tekshiruvi
  har doim "obuna emas" deb hisoblaydi.
- Yangi majburiy/majburiy bo'lmagan kanallarni admin panel orqali (`📡 Kanallar`)
  qo'shishingiz mumkin — botni o'sha kanallarga ham admin qilib qo'shishni
  unutmang.
- Kino qo'shishda fayl sifatida **video** yuboriladi (`message.video.file_id`
  saqlanadi). Agar hujjat (document) sifatida yuboriladigan fayllar bilan
  ishlamoqchi bo'lsangiz, `handlers/admin/movie_manage.py` dagi `F.video`
  filtrini kengaytiring.
- `locales/{uz,ru,en}/LC_MESSAGES/txt.ftl` fayllarini tahrirlab, istalgan
  matnni yoki yangi tilni qo'shishingiz mumkin — kodni qayta yozishga hojat
  yo'q.
- Standart baza fayli `data/database.db` da, loglar esa `logs/` papkasida
  (`info.log`, `warning.log`, `error.log`) saqlanadi.

## Papka strukturasi

```
cinema_bot/
├── handlers/
│   ├── admin/      # /admin va barcha admin funksiyalari
│   └── user/       # /start, qidiruv, sozlamalar va h.k.
├── keyboards/
│   ├── inline/     # pagination, til, obuna, kino, admin klaviaturalari
│   └── reply/      # asosiy menyu va admin menyu
├── db/             # aiosqlite asosidagi async Database klassi
├── middlewares/     # i18n, database, throttling
├── filters/         # AdminFilter, SubscribedFilter
├── states/           # barcha FSM StatesGroup lar
├── services/         # subscription, broadcast, excel export
├── utils/             # logger, pagination helperlar
├── locales/            # uz/ru/en .ftl fayllari
├── data/                # SQLite baza va Excel export shu yerda yaraladi
├── logs/                 # info/warning/error log fayllari
├── main.py                # ishga tushirish nuqtasi
├── loader.py               # Bot, Dispatcher, Database, TranslatorHub
└── config.py                # .env dan sozlamalarni o'qish
```


### Cheklangan admin buyruqlari
- `/adlimited USER_ID` yoki `/addlimited USER_ID` — cheklangan admin qo‘shish.
- `/removelimited USER_ID` — cheklangan adminni olib tashlash.

`ADMIN_IDS` qiymatiga faqat super admin Telegram ID raqamlarini yozing. `.env.example` faylini `.env` nomi bilan nusxalab, BOT_TOKEN va ADMIN_IDS ni o‘zingiz to‘ldiring.


### Eski ma'lumotlar bazasi bilan moslik
Bot ishga tushganda `movies.created_by`, `movies.is_trending`, `admins.role` va
`trend_requests.action` ustunlari mavjudligi tekshiriladi. Yetishmayotgan ustunlar
`ALTER TABLE` orqali qo'shiladi; mavjud kinolar va boshqa yozuvlar o'chirilmaydi.
