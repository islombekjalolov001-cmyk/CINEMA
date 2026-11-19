"""Subscription checks driven only by channels configured in the admin panel."""
from __future__ import annotations

import logging
from urllib.parse import urlparse

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from db import get_db

NOT_MEMBER_STATUSES = {"left", "kicked"}
logger = logging.getLogger(__name__)


def normalize_channel_reference(raw: str) -> str:
    """Normalize public Telegram channel links/usernames to @username."""
    value = (raw or "").strip()
    if not value:
        return ""
    if value.startswith(("https://", "http://")):
        parsed = urlparse(value)
        host = parsed.netloc.lower().removeprefix("www.")
        if host not in {"t.me", "telegram.me"}:
            return ""
        path = parsed.path.strip("/")
        if not path or path.startswith(("+", "joinchat/")):
            return ""
        path = path.split("/")[0].split("?")[0].lstrip("@")
        return f"@{path}" if path else ""
    if value.startswith(("t.me/", "telegram.me/")):
        return normalize_channel_reference("https://" + value)
    if value.startswith("@"):
        username = value[1:].strip()
        return f"@{username}" if username else ""
    if value.startswith("-100") or value.isdigit():
        return value
    return f"@{value}"


def _is_telegram_subscription_target(chat_id: str) -> bool:
    value = normalize_channel_reference(chat_id)
    return value.startswith("@") or value.startswith("-100") or value.isdigit()


async def get_mandatory_channel_ids() -> list[str]:
    """Only mandatory channels stored in the database are enforced."""
    rows = await get_db().mandatory_channels()
    result: list[str] = []
    seen: set[str] = set()
    for row in rows:
        channel = normalize_channel_reference(row["chat_id"])
        if channel and channel not in seen:
            result.append(channel)
            seen.add(channel)
    return result


async def get_unsubscribed_channels(bot: Bot, user_id: int) -> list[str]:
    missing: list[str] = []
    for chat_id in await get_mandatory_channel_ids():
        if not _is_telegram_subscription_target(chat_id):
            continue
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in NOT_MEMBER_STATUSES:
                missing.append(chat_id)
        except TelegramAPIError as exc:
            # Fail closed: inaccessible channels are shown as not verified.
            logger.warning("Obuna tekshiruvi amalga oshmadi (%s): %s", chat_id, exc)
            missing.append(chat_id)
    return missing
