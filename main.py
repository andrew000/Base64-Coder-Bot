from telegram import *
from telegram.ext import *
import logging
import base64
import uuid

logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='commands here')


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


def main():
    updater = Updater('932627043:AAECgjqokI0bnYAraHMcuK74vj9HoUWB-GM', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(InlineQueryHandler(inline_query))

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()