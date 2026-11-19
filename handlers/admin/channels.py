"""Reliable admin flows for mandatory and optional channel management."""
from __future__ import annotations

from filters.admin import SuperAdminFilter

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner

from db import Database
from services.subscription import normalize_channel_reference
from states.states import AddChannel, RemoveChannel

router = Router(name="admin_channels")
router.message.filter(SuperAdminFilter())
router.callback_query.filter(SuperAdminFilter())

ADD_MANDATORY_TEXTS = {"➕ Majburiy kanal qo'shish", "➕ Добавить обязательный канал", "➕ Add mandatory channel"}
REMOVE_MANDATORY_TEXTS = {"➖ Majburiy kanal o'chirish", "➖ Удалить обязательный канал", "➖ Remove mandatory channel"}
ADD_OPTIONAL_TEXTS = {"➕ Majburiy bo'lmagan kanal qo'shish", "➕ Добавить необязательный канал", "➕ Add optional channel"}
REMOVE_OPTIONAL_TEXTS = {"➖ Majburiy bo'lmagan kanal o'chirish", "➖ Удалить необязательный канал", "➖ Remove optional channel"}


@router.message(F.text.in_(ADD_MANDATORY_TEXTS))
async def start_add_mandatory(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(mandatory=True)
    await state.set_state(AddChannel.waiting_chat_id)
    await message.answer("Majburiy kanal username yoki havolasini yuboring. Masalan: @kanal yoki https://t.me/kanal")


@router.message(F.text.in_(ADD_OPTIONAL_TEXTS))
async def start_add_optional(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(mandatory=False)
    await state.set_state(AddChannel.waiting_chat_id)
    await message.answer("Majburiy bo'lmagan kanal username yoki havolasini yuboring. Masalan: @kanal yoki https://t.me/kanal")


@router.message(AddChannel.waiting_chat_id)
async def add_channel_id(message: Message, state: FSMContext) -> None:
    normalized = normalize_channel_reference(message.text or "")
    if not normalized:
        await message.answer("Kanal noto'g'ri. Ommaviy kanal username yoki https://t.me/kanal havolasini yuboring.")
        return
    await state.update_data(chat_id=normalized)
    await state.set_state(AddChannel.waiting_title)
    await message.answer("Kanal nomini yuboring (masalan: Kino olami).")


@router.message(AddChannel.waiting_title)
async def add_channel_title(message: Message, db: Database, state: FSMContext) -> None:
    data = await state.get_data()
    chat_id = str(data.get("chat_id", "")).strip()
    title = (message.text or "").strip()
    mandatory = bool(data.get("mandatory", False))
    if not chat_id or not title:
        await message.answer("Kanal nomi bo'sh bo'lmasin. Qayta yuboring.")
        return

    await db.add_channel(chat_id, title[:100], mandatory)
    await state.clear()
    kind = "majburiy" if mandatory else "majburiy bo'lmagan"
    await message.answer(f"✅ {chat_id} kanali {kind} ro'yxatiga qo'shildi.")


async def _begin_remove(message: Message, db: Database, state: FSMContext, mandatory: bool) -> None:
    rows = await (db.mandatory_channels() if mandatory else db.optional_channels())
    if not rows:
        label = "majburiy" if mandatory else "majburiy bo'lmagan"
        await message.answer(f"Hozircha {label} kanallar yo'q.")
        return
    listing = "\\n".join(f"• {row['chat_id']} — {row['title'] or 'Nomsiz'}" for row in rows)
    await state.clear()
    await state.update_data(remove_mandatory=mandatory)
    await state.set_state(RemoveChannel.waiting_chat_id)
    await message.answer(f"O'chirmoqchi bo'lgan kanal username yoki havolasini yuboring:\\n\\n{listing}")


@router.message(F.text.in_(REMOVE_MANDATORY_TEXTS))
async def start_remove_mandatory(message: Message, db: Database, state: FSMContext) -> None:
    await _begin_remove(message, db, state, mandatory=True)


@router.message(F.text.in_(REMOVE_OPTIONAL_TEXTS))
async def start_remove_optional(message: Message, db: Database, state: FSMContext) -> None:
    await _begin_remove(message, db, state, mandatory=False)


@router.message(RemoveChannel.waiting_chat_id)
async def remove_channel(message: Message, db: Database, state: FSMContext) -> None:
    data = await state.get_data()
    mandatory = bool(data.get("remove_mandatory", True))
    channel = normalize_channel_reference(message.text or "")
    if not channel:
        await message.answer("Kanal username yoki t.me havolasini to'g'ri yuboring.")
        return
    removed = await db.remove_channel(channel, mandatory=mandatory)
    await state.clear()
    if removed:
        await message.answer(f"✅ {channel} kanal ro'yxatdan butunlay o'chirildi.")
    else:
        await message.answer(f"❌ {channel} bu ro'yxatda topilmadi. Kanal turi yoki username'ni tekshiring.")
