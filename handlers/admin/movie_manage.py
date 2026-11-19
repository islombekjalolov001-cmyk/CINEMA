"""Admin flows for adding, editing and deleting movies (all via FSM)."""
from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from db import Database
from config import config
from keyboards.inline.admin import (
    admin_confirm_add_keyboard,
    admin_confirm_delete_keyboard,
    admin_country_pick_keyboard,
    admin_edit_fields_keyboard,
    admin_genre_pick_keyboard,
)
from keyboards.inline.callback_data import (
    AdminConfirmCallback,
    AdminCountrySelectCallback,
    AdminEditFieldCallback,
    AdminGenreSelectCallback,
    TrendDecisionCallback, TrendRequestDecisionCallback, LimitedTrendChoiceCallback,
)
from states.states import AddMovie, DeleteMovie, EditMovie, TrendAdminAction

router = Router(name="admin_movie_manage")

ADD_MOVIE_TEXTS = {"➕ Qo'shish", "➕ Добавить", "➕ Add"}
EDIT_MOVIE_TEXTS = {"✏️ Tahrirlash", "✏️ Редактировать", "✏️ Edit"}
DELETE_MOVIE_TEXTS = {"🗑 O'chirish", "🗑 Удалить", "🗑 Delete"}
ADD_TREND_TEXTS = {"🔥 Trendga kino qo'shish", "🔥 Добавить фильм в тренды", "🔥 Add trend movie"}
REMOVE_TREND_TEXTS = {"➖ Trenddan kino o'chirish", "➖ Убрать фильм из трендов", "➖ Remove trend movie"}


# ---------------------------------------------------------------- ADD ---- #
@router.message(F.text.in_(ADD_MOVIE_TEXTS))
async def start_add_movie(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(AddMovie.code)
    await message.answer(i18n.get("admin-ask-code"))


@router.message(AddMovie.code)
async def add_movie_code(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer(i18n.get("invalid-code"))
        return

    code = int(text)
    if await db.movie_exists(code):
        await message.answer(i18n.get("admin-code-exists"))
        return

    await state.update_data(code=code)
    await state.set_state(AddMovie.title)
    await message.answer(i18n.get("admin-ask-title"))


@router.message(AddMovie.title)
async def add_movie_title(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(title=(message.text or "").strip())
    await state.set_state(AddMovie.genre)
    await message.answer(i18n.get("admin-ask-genre"), reply_markup=admin_genre_pick_keyboard(i18n))


@router.callback_query(AddMovie.genre, AdminGenreSelectCallback.filter())
async def add_movie_genre(
    callback: CallbackQuery, callback_data: AdminGenreSelectCallback, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await state.update_data(genre=callback_data.key)
    await state.set_state(AddMovie.country)
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-ask-country"), reply_markup=admin_country_pick_keyboard(i18n))


@router.callback_query(AddMovie.country, AdminCountrySelectCallback.filter())
async def add_movie_country(
    callback: CallbackQuery, callback_data: AdminCountrySelectCallback, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await state.update_data(country=callback_data.key)
    await state.set_state(AddMovie.year)
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-ask-year"))


@router.message(AddMovie.year)
async def add_movie_year(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer(i18n.get("invalid-code"))
        return
    await state.update_data(year=int(text))
    await state.set_state(AddMovie.rating)
    await message.answer(i18n.get("admin-ask-rating"))


@router.message(AddMovie.rating)
async def add_movie_rating(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip().replace(",", ".")
    try:
        rating = float(text)
    except ValueError:
        await message.answer(i18n.get("invalid-code"))
        return
    await state.update_data(rating=rating)
    await state.set_state(AddMovie.description)
    await message.answer(i18n.get("admin-ask-description"))


@router.message(AddMovie.description)
async def add_movie_description(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(description=(message.text or "").strip())
    await state.set_state(AddMovie.file)
    await message.answer(i18n.get("admin-ask-file"))


@router.message(AddMovie.file, F.video)
async def add_movie_file(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(file_id=message.video.file_id)
    data = await state.get_data()
    await state.set_state(AddMovie.confirm)

    caption = i18n.get(
        "movie-card",
        title=data["title"],
        country=i18n.get(f"country-{data['country']}"),
        genre=i18n.get(f"genre-{data['genre']}"),
        year=data["year"],
        rating=data["rating"],
        description=data["description"],
    )
    await message.answer_video(
        video=data["file_id"],
        caption=i18n.get("admin-confirm-add") + "\n\n" + caption,
        reply_markup=admin_confirm_add_keyboard(data["code"], i18n),
    )


@router.callback_query(AddMovie.confirm, AdminConfirmCallback.filter(F.action == "add_movie"))
async def confirm_add_movie(
    callback: CallbackQuery,
    callback_data: AdminConfirmCallback,
    db: Database,
    i18n: TranslatorRunner,
    state: FSMContext,
    bot: Bot,
) -> None:
    data = await state.get_data()
    await state.clear()
    await callback.answer()

    if not callback_data.yes:
        await callback.message.edit_caption(caption=i18n.get("admin-cancelled"))
        return

    await db.add_movie(
        code=data["code"], title=data["title"], genre=data["genre"], country=data["country"],
        year=data["year"], rating=data["rating"], description=data["description"],
        file_id=data["file_id"], created_by=callback.from_user.id,
    )
    if await db.is_super_admin(callback.from_user.id, config.admin_ids):
        builder = InlineKeyboardBuilder()
        builder.button(text=i18n.get("admin-yes"),
                       callback_data=TrendDecisionCallback(code=data["code"], yes=True))
        builder.button(text=i18n.get("admin-no"),
                       callback_data=TrendDecisionCallback(code=data["code"], yes=False))
        await callback.message.edit_caption(
            caption=i18n.get("admin-movie-added") + "\n\n" + i18n.get("ask-add-trending"),
            reply_markup=builder.as_markup())
    else:
        # Limited admin chooses whether to request trend placement; super admin must approve it.
        builder = InlineKeyboardBuilder()
        builder.button(text=i18n.get("admin-yes"),
            callback_data=LimitedTrendChoiceCallback(code=data["code"], yes=True))
        builder.button(text=i18n.get("admin-no"),
            callback_data=LimitedTrendChoiceCallback(code=data["code"], yes=False))
        await callback.message.edit_caption(
            caption=i18n.get("admin-movie-added") + "\n\n" + i18n.get("ask-add-trending"),
            reply_markup=builder.as_markup())



@router.callback_query(LimitedTrendChoiceCallback.filter())
async def limited_admin_choose_trending(callback: CallbackQuery, callback_data: LimitedTrendChoiceCallback,
                                        db: Database, bot: Bot, i18n: TranslatorRunner) -> None:
    if not await db.is_limited_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    movie = await db.get_movie(callback_data.code)
    if movie is None or movie["created_by"] != callback.from_user.id:
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    await callback.answer()
    if not callback_data.yes:
        await callback.message.edit_caption(caption=i18n.get("trend-not-added"))
        return
    request_id = await db.add_trend_request(callback_data.code, callback.from_user.id)
    for super_id in config.admin_ids:
        approval = InlineKeyboardBuilder()
        approval.button(text=i18n.get("admin-yes"),
            callback_data=TrendRequestDecisionCallback(request_id=request_id, action="add", yes=True))
        approval.button(text=i18n.get("admin-no"),
            callback_data=TrendRequestDecisionCallback(request_id=request_id, action="add", yes=False))
        await bot.send_video(super_id, movie["file_id"],
            caption=i18n.get("limited-trend-request", title=movie["title"], code=movie["code"],
                admin_id=callback.from_user.id) + "\n" + i18n.get("trend-request-add"),
            reply_markup=approval.as_markup())
    await callback.message.edit_caption(caption=i18n.get("trend-approval-pending"))


@router.callback_query(TrendDecisionCallback.filter())
async def decide_super_trending(callback: CallbackQuery, callback_data: TrendDecisionCallback,
                                db: Database, i18n: TranslatorRunner) -> None:
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    await db.set_movie_trending(callback_data.code, callback_data.yes)
    await callback.answer()
    await callback.message.edit_caption(caption=i18n.get(
        "trend-added" if callback_data.yes else "trend-not-added"))


@router.callback_query(TrendRequestDecisionCallback.filter())
async def decide_limited_trend_request(callback: CallbackQuery, callback_data: TrendRequestDecisionCallback,
                                       db: Database, bot: Bot, i18n: TranslatorRunner) -> None:
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    request = await db.get_trend_request(callback_data.request_id)
    if request is None:
        await callback.answer(i18n.get("trend-request-expired"), show_alert=True); return
    movie = await db.get_movie(request["movie_code"])
    action = request["action"] if "action" in request.keys() else "add"
    if movie is not None and callback_data.yes:
        await db.set_movie_trending(movie["code"], action == "add")
    await db.remove_trend_request(callback_data.request_id)
    await callback.answer()
    await callback.message.edit_caption(caption=i18n.get(
        ("trend-approved" if action == "add" else "trend-remove-approved") if callback_data.yes else ("trend-rejected" if action == "add" else "trend-remove-rejected")))
    if movie is not None:
        try:
            await bot.send_message(request["requested_by"], i18n.get(
                ("trend-result-approved" if action == "add" else "trend-remove-result-approved") if callback_data.yes else ("trend-result-rejected" if action == "add" else "trend-remove-result-rejected"),
                title=movie["title"]))
        except Exception:
            pass

# ---------------------------------------------------------- TREND PANEL ---- #
@router.message(F.text.in_(ADD_TREND_TEXTS))
async def start_admin_add_trend(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    if not await db.is_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    await state.set_state(TrendAdminAction.waiting_add_code)
    await message.answer(i18n.get("trend-admin-ask-add-code"))


@router.message(TrendAdminAction.waiting_add_code)
async def receive_admin_add_trend_code(message: Message, db: Database, bot: Bot, i18n: TranslatorRunner,
                                       state: FSMContext) -> None:
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(i18n.get("invalid-code")); return
    movie = await db.get_movie(int(raw))
    if movie is None:
        await message.answer(i18n.get("code-not-found")); return
    await state.clear()
    if await db.is_super_admin(message.from_user.id, config.admin_ids):
        await db.set_movie_trending(movie["code"], True)
        await message.answer(i18n.get("trend-added"))
        return
    if not await db.is_limited_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    request_id = await db.add_trend_request(movie["code"], message.from_user.id, "add")
    await _send_trend_approval_request(bot, db, i18n, request_id, movie, message.from_user.id, "add")
    await message.answer(i18n.get("trend-approval-pending"))


@router.message(F.text.in_(REMOVE_TREND_TEXTS))
async def start_admin_remove_trend(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    if not await db.is_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    await state.set_state(TrendAdminAction.waiting_remove_code)
    await message.answer(i18n.get("trend-admin-ask-remove-code"))


@router.message(TrendAdminAction.waiting_remove_code)
async def receive_admin_remove_trend_code(message: Message, db: Database, bot: Bot, i18n: TranslatorRunner,
                                          state: FSMContext) -> None:
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(i18n.get("invalid-code")); return
    movie = await db.get_movie(int(raw))
    if movie is None or not movie["is_trending"]:
        await message.answer(i18n.get("trend-movie-not-found")); return
    await state.clear()
    if await db.is_super_admin(message.from_user.id, config.admin_ids):
        await db.set_movie_trending(movie["code"], False)
        await message.answer(i18n.get("trend-remove-approved"))
        return
    if not await db.is_limited_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    request_id = await db.add_trend_request(movie["code"], message.from_user.id, "remove")
    await _send_trend_approval_request(bot, db, i18n, request_id, movie, message.from_user.id, "remove")
    await message.answer(i18n.get("trend-approval-pending"))


async def _send_trend_approval_request(bot: Bot, db: Database, i18n: TranslatorRunner, request_id: int,
                                       movie, admin_id: int, action: str) -> None:
    for super_id in config.admin_ids:
        approval = InlineKeyboardBuilder()
        approval.button(text=i18n.get("admin-yes"),
            callback_data=TrendRequestDecisionCallback(request_id=request_id, action=action, yes=True))
        approval.button(text=i18n.get("admin-no"),
            callback_data=TrendRequestDecisionCallback(request_id=request_id, action=action, yes=False))
        await bot.send_video(super_id, movie["file_id"],
            caption=i18n.get("limited-trend-request", title=movie["title"], code=movie["code"], admin_id=admin_id)
                + "\n" + i18n.get("trend-request-add" if action == "add" else "trend-request-remove"),
            reply_markup=approval.as_markup())


# --------------------------------------------------------------- EDIT ---- #
@router.message(F.text.in_(EDIT_MOVIE_TEXTS))
async def start_edit_movie(message: Message, i18n: TranslatorRunner, state: FSMContext, db: Database) -> None:
    if not await db.is_super_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    await state.set_state(EditMovie.choose_field)
    await message.answer(i18n.get("admin-ask-code"))


@router.message(EditMovie.choose_field, F.text.regexp(r"^\d+$"))
async def edit_movie_lookup(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    if not await db.is_super_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    code = int(message.text.strip())
    movie = await db.get_movie(code)
    if movie is None:
        await message.answer(i18n.get("code-not-found"))
        return

    await state.update_data(edit_code=code)
    await message.answer(i18n.get("admin-choose-field"), reply_markup=admin_edit_fields_keyboard(code, i18n))


@router.callback_query(AdminEditFieldCallback.filter())
async def choose_edit_field(
    callback: CallbackQuery, callback_data: AdminEditFieldCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    await callback.answer()

    if callback_data.field == "genre":
        await state.update_data(edit_code=callback_data.code, edit_field="genre")
        await state.set_state(EditMovie.new_value)
        await callback.message.edit_text(i18n.get("admin-ask-genre"), reply_markup=admin_genre_pick_keyboard(i18n))
        return

    if callback_data.field == "country":
        await state.update_data(edit_code=callback_data.code, edit_field="country")
        await state.set_state(EditMovie.new_value)
        await callback.message.edit_text(i18n.get("admin-ask-country"), reply_markup=admin_country_pick_keyboard(i18n))
        return

    await state.update_data(edit_code=callback_data.code, edit_field=callback_data.field)
    await state.set_state(EditMovie.new_value)

    prompts = {
        "title": "admin-ask-title",
        "year": "admin-ask-year",
        "rating": "admin-ask-rating",
        "description": "admin-ask-description",
        "file": "admin-ask-file",
    }
    await callback.message.edit_text(i18n.get(prompts[callback_data.field]))


@router.callback_query(EditMovie.new_value, AdminGenreSelectCallback.filter())
async def edit_movie_genre_value(
    callback: CallbackQuery, callback_data: AdminGenreSelectCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    data = await state.get_data()
    await db.update_movie_field(data["edit_code"], "genre", callback_data.key)
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-movie-updated"))


@router.callback_query(EditMovie.new_value, AdminCountrySelectCallback.filter())
async def edit_movie_country_value(
    callback: CallbackQuery, callback_data: AdminCountrySelectCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    data = await state.get_data()
    await db.update_movie_field(data["edit_code"], "country", callback_data.key)
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-movie-updated"))


@router.message(EditMovie.new_value, F.video)
async def edit_movie_file_value(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    if not await db.is_super_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    data = await state.get_data()
    if data.get("edit_field") != "file":
        return
    await db.update_movie_field(data["edit_code"], "file_id", message.video.file_id)
    await state.clear()
    await message.answer(i18n.get("admin-movie-updated"))


@router.message(EditMovie.new_value)
async def edit_movie_text_value(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    if not await db.is_super_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    data = await state.get_data()
    field = data.get("edit_field")
    if field in (None, "genre", "country", "file"):
        return

    value: object = (message.text or "").strip()
    if field == "year":
        if not str(value).isdigit():
            await message.answer(i18n.get("invalid-code"))
            return
        value = int(value)
    elif field == "rating":
        try:
            value = float(str(value).replace(",", "."))
        except ValueError:
            await message.answer(i18n.get("invalid-code"))
            return

    db_field = "file_id" if field == "file" else field
    await db.update_movie_field(data["edit_code"], db_field, value)
    await state.clear()
    await message.answer(i18n.get("admin-movie-updated"))


# ------------------------------------------------------------- DELETE ---- #
@router.message(F.text.in_(DELETE_MOVIE_TEXTS))
async def start_delete_movie(message: Message, i18n: TranslatorRunner, state: FSMContext, db: Database) -> None:
    if not await db.is_admin(message.from_user.id, config.admin_ids):
        return
    await state.set_state(DeleteMovie.confirm)
    await message.answer(i18n.get("admin-ask-code"))


@router.message(DeleteMovie.confirm, F.text.regexp(r"^\d+$"))
async def delete_movie_lookup(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    if not await db.is_super_admin(message.from_user.id, config.admin_ids):
        await message.answer(i18n.get("access-denied")); return
    code = int(message.text.strip())
    movie = await db.get_movie(code)
    if movie is None:
        await message.answer(i18n.get("code-not-found"))
        return

    await message.answer(
        i18n.get("admin-confirm-delete", title=movie["title"], code=code),
        reply_markup=admin_confirm_delete_keyboard(code, i18n),
    )


@router.callback_query(AdminConfirmCallback.filter(F.action.in_(("delete_movie", "ask_delete"))))
async def confirm_delete_movie(
    callback: CallbackQuery, callback_data: AdminConfirmCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await state.clear()
    await callback.answer()
    code = int(callback_data.value)

    if callback_data.action == "ask_delete":
        movie = await db.get_movie(code)
        if movie is None:
            await callback.message.edit_text(i18n.get("code-not-found"))
            return
        if not await db.is_super_admin(callback.from_user.id, config.admin_ids) and movie["created_by"] != callback.from_user.id:
            await callback.message.answer(i18n.get("delete-own-only"))
            return
        await callback.message.edit_text(
            i18n.get("admin-confirm-delete", title=movie["title"], code=code),
            reply_markup=admin_confirm_delete_keyboard(code, i18n),
        )
        return

    if not callback_data.yes:
        await callback.message.edit_text(i18n.get("admin-cancelled"))
        return

    movie = await db.get_movie(code)
    if movie is None:
        await callback.message.edit_text(i18n.get("code-not-found")); return
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids) and movie["created_by"] != callback.from_user.id:
        await callback.message.answer(i18n.get("delete-own-only")); return
    await db.delete_movie(code)
    await callback.message.edit_text(i18n.get("admin-movie-deleted"))
