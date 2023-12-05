from telebot import TeleBot
from telebot import types
bot = TeleBot(BOT_TOKEN, threaded=False)
hideBoard = types.ReplyKeyboardRemove()  

TEST                =    1

TEST_TOKEN      = 'TEST_TOKEN'
AROMA_TOKEN     = 'ORIGINAL_TOKEN'

TEST_GRUPPO     = -1001721979634
AROMA_GRUPPO    = -1001457029650

if TEST:
    BOT_TOKEN       = TEST_TOKEN
    GRUPPO_AROMA    = TEST_GRUPPO
else:
    BOT_TOKEN       = AROMA_TOKEN
    GRUPPO_AROMA    = AROMA_GRUPPO