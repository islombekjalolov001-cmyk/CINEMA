"""📣 Broadcast a message to every bot user, with live progress."""
from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner
from config import config
from db import Database

from keyboards.inline.callback_data import BroadcastConfirmCallback, BroadcastRequestCallback
from services.broadcast_service import broadcast_message
from states.states import Broadcast

router = Router(name="admin_broadcast")

BROADCAST_TEXTS = {"📣 Broadcast", "📣 Рассылка", "📣 Broadcast"}


def _confirm_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get("admin-broadcast-yes"), callback_data=BroadcastConfirmCallback(yes=True))
    builder.button(text=i18n.get("admin-broadcast-no"), callback_data=BroadcastConfirmCallback(yes=False))
    return builder.as_markup()


@router.message(F.text.in_(BROADCAST_TEXTS))
async def start_broadcast(message: Message, i18n: TranslatorRunner, state: FSMContext, db: Database) -> None:
    if not await db.is_admin(message.from_user.id, config.admin_ids): return
    await state.set_state(Broadcast.waiting_content)
    await message.answer(i18n.get("admin-ask-broadcast"))


@router.message(Broadcast.waiting_content)
async def receive_broadcast_content(message: Message, i18n: TranslatorRunner, state: FSMContext,
                                    db: Database, bot: Bot) -> None:
    if await db.is_super_admin(message.from_user.id, config.admin_ids):
        await state.update_data(source_message=message)
        await state.set_state(Broadcast.confirm)
        await message.answer(i18n.get("admin-broadcast-confirm"), reply_markup=_confirm_keyboard(i18n))
        return
    request_id = await db.save_broadcast_request(message.from_user.id, message.chat.id, message.message_id)
    for super_id in config.admin_ids:
        builder = InlineKeyboardBuilder()
        builder.button(text=i18n.get("admin-yes"),
            callback_data=BroadcastRequestCallback(request_id=request_id, yes=True))
        builder.button(text=i18n.get("admin-no"),
            callback_data=BroadcastRequestCallback(request_id=request_id, yes=False))
        try:
            await bot.copy_message(super_id, message.chat.id, message.message_id,
                reply_markup=builder.as_markup())
        except Exception:
            pass
    await state.clear()
    await message.answer(i18n.get("broadcast-permission-requested"))


@router.callback_query(Broadcast.confirm, BroadcastConfirmCallback.filter())
async def confirm_broadcast(
    callback: CallbackQuery,
    callback_data: BroadcastConfirmCallback,
    bot: Bot,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    await state.clear()
    await callback.answer()

    if not callback_data.yes:
        await callback.message.edit_text(i18n.get("admin-cancelled"))
        return

    source_message: Message = data["source_message"]

    await callback.message.edit_text(i18n.get("admin-broadcast-started"))
    status_message = await callback.message.answer(i18n.get("admin-broadcast-progress", sent=0, total="?"))

    async def progress(sent: int, total: int) -> None:
        try:
            await status_message.edit_text(i18n.get("admin-broadcast-progress", sent=sent, total=total))
        except Exception:
            pass

    result = await broadcast_message(bot, source_message, progress_callback=progress)

    await status_message.edit_text(
        i18n.get("admin-broadcast-done", sent=result.sent, failed=result.failed, blocked=result.blocked)
    )


@router.callback_query(BroadcastRequestCallback.filter())
async def decide_limited_broadcast(callback: CallbackQuery, callback_data: BroadcastRequestCallback,
                                   db: Database, bot: Bot, i18n: TranslatorRunner) -> None:
    if not await db.is_super_admin(callback.from_user.id, config.admin_ids):
        await callback.answer(i18n.get("access-denied"), show_alert=True); return
    request = await db.get_broadcast_request(callback_data.request_id)
    if request is None:
        await callback.answer(i18n.get("broadcast-request-expired"), show_alert=True); return
    await db.remove_broadcast_request(callback_data.request_id)
    await callback.answer()
    if not callback_data.yes:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(i18n.get("broadcast-request-denied"))
        try: await bot.send_message(request["admin_id"], i18n.get("broadcast-permission-denied"))
        except Exception: pass
        return
    user_ids = await db.all_user_ids()
    sent = failed = blocked = 0
    from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
    import asyncio
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(i18n.get("admin-broadcast-started"))
    for uid in user_ids:
        try:
            await bot.copy_message(uid, request["message_chat_id"], request["message_id"])
            sent += 1
        except TelegramForbiddenError:
            blocked += 1
            await db.set_blocked(uid, True)
        except TelegramRetryAfter as exc:
            await asyncio.sleep(exc.retry_after)
            try:
                await bot.copy_message(uid, request["message_chat_id"], request["message_id"]); sent += 1
            except Exception: failed += 1
        except Exception: failed += 1
        await asyncio.sleep(0.05)
    await callback.message.answer(i18n.get("admin-broadcast-done", sent=sent, failed=failed, blocked=blocked))
    try: await bot.send_message(request["admin_id"], i18n.get("broadcast-permission-approved"))
    except Exception: pass
