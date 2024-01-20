from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



#  INLINE
mine = InlineKeyboardMarkup()
mine.row(InlineKeyboardButton(text = "🌕", callback_data = "mine"))
