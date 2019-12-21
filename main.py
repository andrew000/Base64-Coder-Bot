import base64
import logging
import uuid
import binascii
import secrets

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

    available = "b16, b32, b64, b85, crc32, uuid1, uuid3, uuid4, uuid5, bsecret, hsecret, usecret"

    enter_a_text = [InlineQueryResultArticle(id=uuid.uuid4(),
                                             title="Enter some text",
                                             input_message_content=InputTextMessageContent("Example: b** some text"),
                                             description="Example: b64 some text")]

    if len(query.query.split()) < 1 or query.query == '':
        make_a_choice = [InlineQueryResultArticle(id=uuid.uuid4(),
                                                  title="Make a choice",
                                                  input_message_content=InputTextMessageContent(
                                                      f"Available: {available}"),
                                                  description=f"Available: {available}")]
        update.inline_query.answer(make_a_choice, cache_time=1, is_personal=True)
        return

    if query.query.split()[0] == 'b16':
        if len(query.query.split()) < 2:
            update.inline_query.answer(enter_a_text, cache_time=1, is_personal=True)
            return
        string = " ".join(query.query.split()[1:])
        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="BASE16 Encode",
                                            input_message_content=InputTextMessageContent(
                                                base64.b16encode(bytes(string, 'utf8')).decode()),
                                            description=base64.b16encode(bytes(string, 'utf8')).decode())]

        try:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE16 Decode",
                                                    input_message_content=InputTextMessageContent(
                                                        base64.b16decode(string).decode()),
                                                    description=base64.b16decode(string).decode()))

        except Exception as exc:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE16 Decode",
                                                    input_message_content=InputTextMessageContent("Not a BASE16"),
                                                    description=str(exc)))

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'b32':
        if len(query.query.split()) < 2:
            update.inline_query.answer(enter_a_text, cache_time=1, is_personal=True)
            return
        string = " ".join(query.query.split()[1:])
        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="BASE32 Encode",
                                            input_message_content=InputTextMessageContent(
                                                base64.b32encode(bytes(string, 'utf8')).decode()),
                                            description=base64.b32encode(bytes(string, 'utf8')).decode())]

        try:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE32 Decode",
                                                    input_message_content=InputTextMessageContent(
                                                        base64.b32decode(string).decode()),
                                                    description=base64.b32decode(string).decode()))

        except Exception as exc:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE32 Decode",
                                                    input_message_content=InputTextMessageContent("Not a BASE32"),
                                                    description=str(exc)))

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'b64':
        if len(query.query.split()) < 2:
            update.inline_query.answer(enter_a_text, cache_time=1, is_personal=True)
            return
        string = " ".join(query.query.split()[1:])
        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="BASE64 Encode",
                                            input_message_content=InputTextMessageContent(
                                                base64.b64encode(bytes(string, 'utf8')).decode()),
                                            description=base64.b64encode(bytes(string, 'utf8')).decode())]

        try:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE64 Decode",
                                                    input_message_content=InputTextMessageContent(
                                                        base64.b64decode(string).decode()),
                                                    description=base64.b64decode(string).decode()))

        except Exception as exc:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE64 Decode",
                                                    input_message_content=InputTextMessageContent("Not a BASE64"),
                                                    description=str(exc)))

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'b85':
        if len(query.query.split()) < 2:
            update.inline_query.answer(enter_a_text, cache_time=1, is_personal=True)
            return
        string = " ".join(query.query.split()[1:])
        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="BASE85 Encode",
                                            input_message_content=InputTextMessageContent(
                                                base64.b85encode(bytes(string, 'utf8')).decode()),
                                            description=base64.b85encode(bytes(string, 'utf8')).decode())]

        try:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE85 Decode",
                                                    input_message_content=InputTextMessageContent(
                                                        base64.b85decode(string).decode()),
                                                    description=base64.b85decode(string).decode()))

        except Exception as exc:
            results.append(InlineQueryResultArticle(id=uuid.uuid4(),
                                                    title="BASE85 Decode",
                                                    input_message_content=InputTextMessageContent("Not a BASE85"),
                                                    description=str(exc)))

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'crc32':
        if len(query.query.split()) < 2:
            update.inline_query.answer(enter_a_text, cache_time=1, is_personal=True)
            return
        generated = f"CRC32: `{binascii.crc32(bytes(' '.join(query.query.split()[1:]), 'utf8'))}`"
        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="CRC32",
                                            input_message_content=InputTextMessageContent(generated, ParseMode.MARKDOWN),
                                            description=generated)]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'uuid1':

        generated = f"UUID1: `{str(uuid.uuid1())}`"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="UUID1",
                                            input_message_content=InputTextMessageContent(generated,
                                                                                          ParseMode.MARKDOWN),
                                            description=generated)]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'uuid3':

        generated = f"UUID3: `{str(uuid.uuid3(uuid.uuid4(), update.inline_query.from_user.name))}`"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="UUID3",
                                            input_message_content=InputTextMessageContent(generated,
                                                                                          ParseMode.MARKDOWN),
                                            description=generated)]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'uuid4':
        generated = f"UUID4: `{str(uuid.uuid4())}`"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="UUID4",
                                            input_message_content=InputTextMessageContent(generated,
                                                                                          ParseMode.MARKDOWN),
                                            description=generated)]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'uuid5':

        generated = f"UUID5: `{str(uuid.uuid5(uuid.uuid4(), update.inline_query.from_user.name))}`"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="UUID5",
                                            input_message_content=InputTextMessageContent(generated,
                                                                                          ParseMode.MARKDOWN),
                                            description=generated)]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'hsecret':

        generated = f"HEX SECRET: <code>{secrets.token_hex()}</code>"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="Secret is to secret show this)",
                                            input_message_content=InputTextMessageContent(generated, ParseMode.HTML))]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'bsecret':

        generated = f"BYTE SECRET: <code>{secrets.token_bytes().decode('l1')}</code>"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="Secret is to secret show this)",
                                            input_message_content=InputTextMessageContent(generated, ParseMode.HTML))]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    elif query.query.split()[0] == 'usecret':

        generated = f"URL SAFE SECRET: <code>{secrets.token_urlsafe()}</code>"

        results = [InlineQueryResultArticle(id=uuid.uuid4(),
                                            title="Secret is to secret show this)",
                                            input_message_content=InputTextMessageContent(generated, ParseMode.HTML))]

        update.inline_query.answer(results, cache_time=1, is_personal=True)

    else:
        return


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)  # Place your token in config.py
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('b64e', b64encode))
    dp.add_handler(CommandHandler('b64d', b64decode))

    dp.add_handler(InlineQueryHandler(inline_query))

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
