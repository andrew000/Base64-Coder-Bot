import base64
import logging
import uuid

from telegram import *
from telegram.ext import *

from config import TOKEN

logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Commands:\n\n"
                                  "BASE64_Encode: /b64e <code>some_text</code>\n"
                                  "BASE64_Decode: /b64d <code>some_text</code>",
                             parse_mode=ParseMode.HTML)


def b64encode(update, context):
    if len(update.message.text.split()) == 1:
        update.message.reply_text("Use /b64e `some_text`", parse_mode=ParseMode.MARKDOWN)
        return
    string = base64.b64encode(bytes(" ".join(update.message.text.split()[1:]), 'utf8')).decode()
    update.message.reply_text(string)


def b64decode(update, context):
    if len(update.message.text.split()) == 1:
        update.message.reply_text("Use /b64d `some_text`", parse_mode=ParseMode.MARKDOWN)
        return

    try:
        string = base64.b64decode(" ".join(update.message.text.split()[1:])).decode()
        update.message.reply_text(string)
    except Exception as exc:
        update.message.reply_text(str(exc))


def inline_query(update, context):

    query = update.inline_query

    if query.query == '':
        return

    results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                        title="BASE64 Encode",
                                        input_message_content=InputTextMessageContent(base64.b64encode(bytes(query.query, 'utf8')).decode()),
                                        description=base64.b64encode(bytes(query.query, 'utf8')).decode())]

    try:
        results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                title="BASE64 Decode",
                                                input_message_content=InputTextMessageContent(base64.b64decode(query.query).decode()),
                                                description=base64.b64decode(query.query).decode()))

    except Exception as exc:
        results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                title="BASE64 Decode",
                                                input_message_content=InputTextMessageContent("Not a BASE64"),
                                                description=str(exc)))

    update.inline_query.answer(results, cache_time=1, is_personal=True)


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def test_main():
    updater = Updater(TOKEN, use_context=True)  # Place your token here
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('b64e', b64encode))
    dp.add_handler(CommandHandler('b64d', b64decode))

    dp.add_handler(InlineQueryHandler(inline_query))

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    test_main()
