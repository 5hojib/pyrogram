from .copy_media_group import CopyMediaGroup
from .copy_message import CopyMessage
from .delete_messages import DeleteMessages
from .download_media import DownloadMedia
from .edit_inline_caption import EditInlineCaption
from .edit_inline_media import EditInlineMedia
from .edit_inline_reply_markup import EditInlineReplyMarkup
from .edit_inline_text import EditInlineText
from .edit_message_caption import EditMessageCaption
from .edit_message_media import EditMessageMedia
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_text import EditMessageText
from .forward_messages import ForwardMessages
from .get_available_effects import GetAvailableEffects
from .get_chat_history import GetChatHistory
from .get_chat_history_count import GetChatHistoryCount
from .get_custom_emoji_stickers import GetCustomEmojiStickers
from .get_discussion_message import GetDiscussionMessage
from .get_discussion_replies import GetDiscussionReplies
from .get_discussion_replies_count import GetDiscussionRepliesCount
from .get_media_group import GetMediaGroup
from .get_messages import GetMessages
from .read_chat_history import ReadChatHistory
from .search_global import SearchGlobal
from .search_global_count import SearchGlobalCount
from .search_messages import SearchMessages
from .search_messages_count import SearchMessagesCount
from .send_animation import SendAnimation
from .send_audio import SendAudio
from .send_cached_media import SendCachedMedia
from .send_chat_action import SendChatAction
from .send_contact import SendContact
from .send_document import SendDocument
from .send_media_group import SendMediaGroup
from .send_message import SendMessage
from .send_photo import SendPhoto
from .send_reaction import SendReaction
from .send_sticker import SendSticker
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice
from .send_web_page import SendWebPage
from .stream_media import StreamMedia


class Messages(
    DeleteMessages,
    EditMessageCaption,
    EditMessageReplyMarkup,
    EditMessageMedia,
    EditMessageText,
    ForwardMessages,
    GetAvailableEffects,
    GetMediaGroup,
    GetMessages,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDocument,
    SendAnimation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendSticker,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SendWebPage,
    DownloadMedia,
    GetChatHistory,
    SendCachedMedia,
    GetChatHistoryCount,
    ReadChatHistory,
    EditInlineText,
    EditInlineCaption,
    EditInlineMedia,
    EditInlineReplyMarkup,
    SearchMessages,
    SearchGlobal,
    CopyMessage,
    CopyMediaGroup,
    SearchMessagesCount,
    SearchGlobalCount,
    GetDiscussionMessage,
    SendReaction,
    GetDiscussionReplies,
    GetDiscussionRepliesCount,
    StreamMedia,
    GetCustomEmojiStickers
):
    pass
