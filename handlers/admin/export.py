"""📊 Export all users to an Excel file (pandas + openpyxl)."""
from __future__ import annotations

from filters.admin import SuperAdminFilter

from aiogram import F, Router
from aiogram.types import FSInputFile, Message
from fluentogram import TranslatorRunner

from services.excel_export import export_users_to_excel

router = Router(name="admin_export")
router.message.filter(SuperAdminFilter())
router.callback_query.filter(SuperAdminFilter())

EXPORT_TEXTS = {"📊 Excel Export"}


@router.message(F.text.in_(EXPORT_TEXTS))
async def export_users(message: Message, i18n: TranslatorRunner) -> None:
    path = await export_users_to_excel()
    await message.answer_document(FSInputFile(path), caption=i18n.get("admin-export-caption"))
