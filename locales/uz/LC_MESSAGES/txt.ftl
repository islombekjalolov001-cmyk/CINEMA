## Umumiy
start-greeting = Assalomu alaykum, { $name }! 🎬 Cinema botga xush kelibsiz.
sub-required = Botdan foydalanish uchun quyidagi kanal(lar)ga obuna bo'ling:
sub-button = 📢 Obuna bo'lish
sub-check-button = ✅ Tekshirish
sub-not-yet = ❌ Siz hali barcha kanallarga obuna bo'lmadingiz. Obuna bo'lib, qaytadan tekshiring.
sub-success = ✅ Rahmat! Endi botdan bemalol foydalanishingiz mumkin.

## Reply menu
menu-search-code = 🔍 Kod orqali qidirish
menu-search-name = 🎬 Kino nomi orqali qidirish
menu-search-genre = 🎭 Janr bo'yicha qidirish
menu-search-country = 🌍 Davlat bo'yicha qidirish
menu-settings = ⚙️ Sozlamalar
menu-request-movie = 🎬 Kino so'rash
menu-back = ⬅️ Orqaga

## Sozlamalar
settings-title = ⚙️ Sozlamalar bo'limi
settings-language = 🌐 Tilni o'zgartirish
settings-favorites = ❤️ Sevimli kinolarim
settings-requests = 📩 Kino so'rovlarim
language-choose = Tilni tanlang:
language-changed = ✅ Til muvaffaqiyatli o'zgartirildi!

## Qidiruv - kod
ask-code-again = 🎬 Yana kod orqali kinolar topishingiz mumkin. Marhamat, keyingi kino kodini yuboring:
ask-code = Kino kodini kiriting (masalan: 1001):
code-not-found = ❌ Bu kodga mos kino topilmadi.
invalid-code = ⚠️ Iltimos, faqat raqam kiriting.

## Qidiruv - nom
ask-name = Kino nomini kiriting:
name-not-found = ❌ Bunday nomdagi kino topilmadi.
name-results = 🔎 Qidiruv natijalari:

## Janr / Davlat
choose-genre = 🎭 Janrni tanlang:
choose-country = 🌍 Davlatni tanlang:
no-movies-in-category = Bu bo'limda hozircha kino yo'q.

## Kino kartochkasi
movie-card =
    🎬 <b>{ $title }</b>

    🌍 Davlat: { $country }
    🎭 Janr: { $genre }
    📅 Yili: { $year }
    ⭐️ Reyting: { $rating }

    📝 { $description }
movie-like-button = ❤️ Like ({ $count })
movie-liked = ❤️ Like bosildi!
movie-already-liked = Siz bu kinoni allaqachon layk bosgansiz.

## Sevimlilar
favorites-title = ❤️ Sevimli kinolaringiz:
favorites-empty = Sizda hali sevimli kino yo'q.

## So'rovlar
ask-request-name = Qaysi kinoni qidiryapsiz? Nomini yozing, biz admin bilan bo'lishamiz:
request-sent = ✅ So'rovingiz qabul qilindi. Tez orada ko'rib chiqiladi!

## Pagination
page-indicator = { $current }/{ $total }
prev-button = ⬅️
next-button = ➡️

## Xatolar
error-generic = ⚠️ Xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.
access-denied = ⛔️ Sizda bu buyruqdan foydalanish huquqi yo'q.
blocked-user-message = ⛔️ Siz botdan bloklangansiz. Admin bilan bog'laning.

## ---- ADMIN ----
admin-panel-title = 🛠 Admin panel
admin-movies = 🎬 Kinolar
admin-add-movie = ➕ Qo'shish
admin-delete-movie = 🗑 O'chirish
admin-edit-movie = ✏️ Tahrirlash
admin-channels = 📡 Kanallar
admin-add-mandatory = ➕ Majburiy kanal qo'shish
admin-remove-mandatory = ➖ Majburiy kanal o'chirish
admin-add-optional = ➕ Majburiy bo'lmagan kanal qo'shish
admin-remove-optional = ➖ Majburiy bo'lmagan kanal o'chirish
admin-broadcast = 📣 Broadcast
admin-stats = 📊 Statistika
admin-export = 📊 Excel Export
admin-all-codes = 📋 Barcha kino kodlari
admin-block-user = 🚫 Foydalanuvchini bloklash
admin-blocked-users = 🚫 Bloklangan foydalanuvchilar
admin-back = ⬅️ Admin menyu
admin-block-user-inline = 🚫 Bloklash
admin-unblock-user-inline = ✅ Blokdan chiqarish
admin-all-users-title = 👥 Barcha foydalanuvchilar:
admin-blocked-users-title = 🚫 Bloklangan foydalanuvchilar:
admin-no-users = Hozircha foydalanuvchilar yo'q.
admin-ask-user-id-or-username = Bloklamoqchi bo'lgan foydalanuvchini ID yoki username bilan kiriting:
admin-ask-user-id-or-username-unblock = Blokdan ochmoqchi bo'lgan foydalanuvchini ID yoki username bilan kiriting:
admin-invalid-user-target = ⚠️ Iltimos, ID yoki username kiriting.
admin-user-not-found = ❌ Bunday foydalanuvchi topilmadi.
admin-user-already-blocked = ⚠️ Bu foydalanuvchi allaqachon bloklangan.
admin-user-not-blocked = ⚠️ Bu foydalanuvchi blokda emas.
admin-confirm-block-user = Ro‘stdan ham ushbu foydalanuvchini bloklamoqchimisiz?
    • ID: { $user_id }
    • Username: @{ $username }
    • Nickname: { $nickname }
admin-confirm-unblock-user = Ro‘stdan ham ushbu foydalanuvchini blokdan chiqarishni xohlaysizmi?
    • ID: { $user_id }
    • Username: @{ $username }
    • Nickname: { $nickname }
admin-user-blocked = ✅ Foydalanuvchi bloklandi.
admin-user-unblocked = ✅ Foydalanuvchi blokdan chiqarildi.

admin-ask-code = Kino kodini kiriting (butun son):
admin-code-exists = ⚠️ Bu kod band. Boshqa kod kiriting.
admin-ask-title = Kino nomini kiriting:
admin-ask-genre = Janrni tanlang:
admin-ask-country = Davlatni tanlang:
admin-ask-year = Chiqarilgan yilini kiriting:
admin-ask-rating = Reytingini kiriting (masalan 8.5):
admin-ask-description = Tavsifini kiriting:
admin-ask-file = Endi kino faylini (video) yuboring:
admin-confirm-add = Quyidagi ma'lumotlar bilan kino qo'shilsinmi?
admin-movie-added = ✅ Kino muvaffaqiyatli qo'shildi!
admin-movie-deleted = ✅ Kino o'chirildi.
admin-movie-updated = ✅ Kino yangilandi.
admin-choose-field = Qaysi maydonni tahrirlaysiz?
admin-field-title = Nomi
admin-field-genre = Janr
admin-field-country = Davlat
admin-field-year = Yili
admin-field-rating = Reyting
admin-field-description = Tavsif
admin-field-file = Fayl
admin-ask-new-value = Yangi qiymatni kiriting:

admin-ask-channel-id = Kanal ID yoki username kiriting (masalan @kanal yoki -100123456):
admin-ask-channel-title = Kanal nomini kiriting:
admin-channel-added = ✅ Kanal qo'shildi.
admin-channel-removed = ✅ Kanal o'chirildi.
admin-no-channels = Hozircha kanallar yo'q.

admin-ask-broadcast = Yubormoqchi bo'lgan xabaringizni yuboring (matn, rasm, video va h.k.):
admin-broadcast-confirm = Ushbu xabarni barcha foydalanuvchilarga yuborishni tasdiqlaysizmi?
admin-broadcast-yes = ✅ Ha, yuborish
admin-broadcast-no = ❌ Bekor qilish
admin-broadcast-started = 📣 Yuborish boshlandi...
admin-broadcast-progress = 📊 Yuborilmoqda: { $sent }/{ $total }
admin-broadcast-done =
    ✅ Yuborish yakunlandi!

    ✅ Yuborildi: { $sent }
    ❌ Xato: { $failed }
    🚫 Bloklagan: { $blocked }

admin-stats-title =
    📊 <b>Statistika</b>

    👥 Jami foydalanuvchilar: { $total }
    📅 Bugungi: { $today }
    📆 Haftalik: { $week }
    🗓 Oylik: { $month }

admin-export-caption = 📊 Foydalanuvchilar ro'yxati (Excel)

admin-all-codes-title = 📋 Barcha kino kodlari:
admin-code-item = { $code } - { $title }
admin-confirm-delete = ❗️ "{ $title }" ({ $code }) kinosini o'chirishni tasdiqlaysizmi?
admin-yes = ✅ Ha
admin-no = ❌ Yo'q
admin-cancelled = Bekor qilindi.

## Janrlar
genre-action = Jangari
genre-comedy = Komediya
genre-drama = Drama
genre-horror = Qo'rqinchli
genre-romance = Romantik
genre-thriller = Triller
genre-fantasy = Fantastika
genre-scifi = Ilmiy fantastika
genre-animation = Multfilm
genre-documentary = Hujjatli
genre-adventure = Sarguzasht
genre-crime = Jinoiy
genre-family = Oilaviy
genre-musical = Musiqiy
genre-war = Urush
genre-history = Tarixiy
genre-mystery = Sirli
genre-sport = Sport

## Davlatlar
country-uzbekistan = O'zbekiston
country-turkey = Turkiya
country-usa = AQSH
country-russia = Rossiya
country-india = Hindiston
country-south_korea = Janubiy Koreya
country-france = Fransiya
country-germany = Germaniya
country-china = Xitoy
country-japan = Yaponiya
country-united_kingdom = Buyuk Britaniya
country-italy = Italiya
country-spain = Ispaniya
country-brazil = Braziliya
country-mexico = Meksika
country-canada = Kanada
country-iran = Eron
country-egypt = Misr
country-kazakhstan = Qozog'iston
country-other = Boshqa

menu-trending = 🔥 Top trend kinolar
trending-title = 🔥 Top trend kinolar:
trending-empty = Hozircha trend kinolar yo'q.
ask-add-trending = Ushbu kinoni Top trend ro'yxatiga ham qo'shasizmi?
trend-added = ✅ Kino Top trend ro'yxatiga qo'shildi.
trend-not-added = Kino Top trend ro'yxatiga qo'shilmadi.
limited-trend-request = 🔔 Cheklangan admin trendga kino qo'shmoqchi.
    🎬 { $title } (kod: { $code })
    Admin ID: { $admin_id }
trend-approval-pending = Trend ro'yxatiga qo'shish uchun super admin tasdig'i yuborildi.
trend-approved = ✅ Super admin trendga qo'shishga ruxsat berdi.
trend-rejected = ❌ Super admin trendga qo'shishga ruxsat bermadi.
trend-result-approved = ✅ "{ $title }" Top trend ro'yxatiga qo'shildi.
trend-result-rejected = ❌ "{ $title }" Top trendga qo'shilmadi.
trend-request-expired = Bu so'rov topilmadi yoki allaqachon ko'rib chiqilgan.
delete-own-only = Faqat o'zingiz qo'shgan kinoni o'chira olasiz.
limited-admin-usage = Foydalanish: /adlimited USER_ID (yoki /addlimited USER_ID), /removelimited USER_ID
limited-admin-is-super = Bu foydalanuvchi allaqachon super admin.
limited-admin-added = ✅ { $user_id } cheklangan admin qilindi.
limited-admin-removed = ✅ { $user_id } adminlar ro'yxatidan olindi.
broadcast-permission-requested = Broadcast so'rovingiz super adminga yuborildi. Tasdiqni kuting.
broadcast-request-expired = Broadcast so'rovi topilmadi yoki ko'rib chiqilgan.
broadcast-request-denied = ❌ Cheklangan admin broadcast so'rovi rad etildi.
broadcast-permission-denied = ❌ Super admin broadcast uchun ruxsat bermadi.
broadcast-permission-approved = ✅ Super admin broadcast so'rovingizni tasdiqladi. Xabar yuborildi.

## Trend admin boshqaruvi
admin-add-trend = 🔥 Trendga kino qo'shish
admin-remove-trend = ➖ Trenddan kino o'chirish
trend-admin-ask-add-code = Trendga qo'shmoqchi bo'lgan kino kodini kiriting:
trend-admin-ask-remove-code = Trenddan o'chirmoqchi bo'lgan kino kodini kiriting:
trend-movie-not-found = Bu koddagi kino topilmadi yoki trend ro'yxatida yo'q.
trend-request-add = Amal: kinoni Top trend ro'yxatiga qo'shish.
trend-request-remove = Amal: kinoni Top trend ro'yxatidan o'chirish.
trend-remove-approved = ✅ Kino Top trend ro'yxatidan o'chirildi.
trend-remove-rejected = ❌ Super admin trenddan o'chirishga ruxsat bermadi.
trend-remove-result-approved = ✅ "{ $title }" Top trend ro'yxatidan o'chirildi.
trend-remove-result-rejected = ❌ "{ $title }" Top trend ro'yxatidan o'chirilmadi.
