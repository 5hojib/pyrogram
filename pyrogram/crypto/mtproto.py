from __future__ import annotations

import bisect
from hashlib import sha256
from io import BytesIO
from os import urandom

from pyrogram.errors import SecurityCheckMismatch
from pyrogram.raw.core import Long, Message
from pyrogram.session.internals import MsgId

from . import aes

STORED_MSG_IDS_MAX_SIZE = 1000 * 2


def kdf(auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    x = 0 if outgoing else 8

    sha256_a = sha256(msg_key + auth_key[x : x + 36]).digest()
    sha256_b = sha256(auth_key[x + 40 : x + 76] + msg_key).digest()

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def pack(
    message: Message,
    salt: int,
    session_id: bytes,
    auth_key: bytes,
    auth_key_id: bytes,
) -> bytes:
    data = Long(salt) + session_id + message.write()
    padding = urandom(-(len(data) + 12) % 16 + 12)

    msg_key_large = sha256(auth_key[88 : 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = kdf(auth_key, msg_key, True)

    return (
        auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)
    )


def unpack(
    b: BytesIO,
    session_id: bytes,
    auth_key: bytes,
    auth_key_id: bytes,
    stored_msg_ids: list[int],
) -> Message:
    SecurityCheckMismatch.check(b.read(8) == auth_key_id, "b.read(8) == auth_key_id")

    msg_key = b.read(16)
    aes_key, aes_iv = kdf(auth_key, msg_key, False)
    data = BytesIO(aes.ige256_decrypt(b.read(), aes_key, aes_iv))
    data.read(8)

    SecurityCheckMismatch.check(
        data.read(8) == session_id, "data.read(8) == session_id"
    )

    try:
        message = Message.read(data)
    except KeyError as e:
        if e.args[0] == 0:
            raise ConnectionError(
                "Received empty data. Check your internet connection."
            )

        left = data.read().hex()

        left = [left[i : i + 64] for i in range(0, len(left), 64)]
        left = [[left[i : i + 8] for i in range(0, len(left), 8)] for left in left]
        left = "\n".join(" ".join(x for x in left) for left in left)

        raise ValueError(
            f"The server sent an unknown constructor: {hex(e.args[0])}\n{left}"
        )

    SecurityCheckMismatch.check(
        msg_key == sha256(auth_key[96 : 96 + 32] + data.getvalue()).digest()[8:24],
        "msg_key == sha256(auth_key[96:96 + 32] + data.getvalue()).digest()[8:24]",
    )

    data.seek(32)
    payload = data.read()
    padding = payload[message.length :]
    SecurityCheckMismatch.check(
        12 <= len(padding) <= 1024, "12 <= len(padding) <= 1024"
    )
    SecurityCheckMismatch.check(len(payload) % 4 == 0, "len(payload) % 4 == 0")

    SecurityCheckMismatch.check(message.msg_id % 2 != 0, "message.msg_id % 2 != 0")

    if len(stored_msg_ids) > STORED_MSG_IDS_MAX_SIZE:
        del stored_msg_ids[: STORED_MSG_IDS_MAX_SIZE // 2]

    if stored_msg_ids:
        if message.msg_id < stored_msg_ids[0]:
            raise SecurityCheckMismatch

        if message.msg_id in stored_msg_ids:
            raise SecurityCheckMismatch

        time_diff = (message.msg_id - MsgId()) / 2**32

        if time_diff > 30:
            raise SecurityCheckMismatch

        if time_diff < -300:
            raise SecurityCheckMismatch

    bisect.insort(stored_msg_ids, message.msg_id)

    return message
