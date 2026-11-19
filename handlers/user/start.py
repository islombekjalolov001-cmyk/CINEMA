"""/start command: registers the user and enforces mandatory subscription."""
from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.callback_data import SubCheckCallback, TrendMovieCallback
from keyboards.inline.subscribe import subscribe_keyboard
from keyboards.reply.user import main_menu_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.subscription import get_unsubscribed_channels

router = Router(name="user_start")
logger = logging.getLogger(__name__)


async def _send_subscription_prompt(message: Message, missing: list[str], i18n: TranslatorRunner) -> None:
    await message.answer(i18n.get("sub-required"), reply_markup=subscribe_keyboard(missing, i18n))


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    user = message.from_user
    await db.add_user(user.id, user.username, user.full_name)

    missing = await get_unsubscribed_channels(bot, user.id)
    if missing:
        await _send_subscription_prompt(message, missing, i18n)
        return

    await message.answer(
        i18n.get("start-greeting", name=user.full_name),
        reply_markup=main_menu_keyboard(i18n),
    )


@router.callback_query(SubCheckCallback.filter())
async def check_subscription(callback: CallbackQuery, bot: Bot, i18n: TranslatorRunner) -> None:
    missing = await get_unsubscribed_channels(bot, callback.from_user.id)
    if missing:
        await callback.answer(i18n.get("sub-not-yet"), show_alert=True)
        return

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(i18n.get("sub-success"), reply_markup=main_menu_keyboard(i18n))


@router.message(Command("menu"))
@router.message(F.text.func(lambda t: t in ("⬅️ Orqaga", "⬅️ Назад", "⬅️ Back")))
async def back_to_main_menu(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await message.answer(i18n.get("start-greeting", name=message.from_user.full_name), reply_markup=main_menu_keyboard(i18n))


@router.message(F.text.in_({"🔥 Top trend kinolar", "🔥 Топ тренд фильмы", "🔥 Top trending movies"}))
async def show_trending_movies(message: Message, db: Database, i18n: TranslatorRunner) -> None:
    movies = await db.trending_movies()
    if not movies:
        await message.answer(i18n.get("trending-empty"))
        return
    builder = InlineKeyboardBuilder()
    for movie in movies:
        builder.button(text=f"🎬 {movie['title']} ({movie['year']})",
                       callback_data=TrendMovieCallback(code=movie["code"]))
    builder.adjust(1)
    await message.answer(i18n.get("trending-title"), reply_markup=builder.as_markup())


@router.callback_query(TrendMovieCallback.filter())
async def open_trending_movie(callback: CallbackQuery, callback_data: TrendMovieCallback,
                              db: Database, i18n: TranslatorRunner) -> None:
    movie = await db.get_movie(callback_data.code)
    if movie is None:
        await callback.answer(i18n.get("code-not-found"), show_alert=True)
        return
    await callback.answer()
    caption = i18n.get("movie-card", title=movie["title"],
        country=i18n.get(f"country-{movie['country']}"),
        genre=i18n.get(f"genre-{movie['genre']}"), year=movie["year"],
        rating=movie["rating"], description=movie["description"])
    await callback.message.answer_video(movie["file_id"], caption=caption)
