from telegram import InputMediaPhoto
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram

TOKEN = "6511945562:AAG0r6cDFS8wgRwigtJZx6E9CC_quLQAefU"

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

admin_id = 1252047562  # Anton
# admin_id = 1442538115  # Uliana
password = "1111"


class MyException(Exception):
    pass


def reply_photo(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    context.bot.send_message(admin_id, f"Username: {update.message.from_user.full_name}")
    context.bot.send_photo(admin_id, update.message.photo[3].file_id)
    # update.message.reply_photo(i.file_id)
    # obj = context.bot.get_file(i.file_id)
    # obj.download()
    update.message.reply_text(f"Photos are successfully sent\n(Фото успешно отправлено)")


def reply_video(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    context.bot.send_message(admin_id, f"Username: {update.message.from_user.full_name}")
    context.bot.send_video(admin_id, update.message.video.file_id)
    # obj = context.bot.get_file(update.message.video.file_id)
    # obj.download()
    update.message.reply_text("Video successfully sent\n(Видео успешно отправлено)")


def reply_text(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    pass


def get_password(text, cnt=2):
    if len(text.split()) != cnt:
        raise MyException("Invalid number of arguments\n(Неверное количество аргументов)")
    if len(text.split()) == 3:
        new_password = text.split()[2]
        for i in new_password:
            if i not in "123567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm":
                raise MyException(
                    "Password can only consists of symbols A-Z, a-z and numbers.\n(Пароль может содержать только символы A-Z, a-z и цифры")
        if len(new_password) < 5:
            raise MyException(
                "Password is too short (less than 5 characters)\n(Пароль слишком короткий (меньше 5 символов))")
    text = text.split()[1]
    if text != password:
        raise MyException("Invalid password\n(Неверный пароль)")
    return True


def set_admin(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    try:
        attempt = get_password(update.message.text)
    except Exception as e:
        update.message.reply_text(str(e))
        return
    global admin_id
    admin_id = update.message.from_user.id
    update.message.reply_text(
        f"Administrator successfully changed.\n  Админ успешно изменен (id: {admin_id})\n\nТеперь все фото/видео будут присылаться вам")


def set_password(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    try:
        new_one = get_password(update.message.text, cnt=3)
    except Exception as e:
        update.message.reply_text(str(e))
        return
    global admin_id, password
    if admin_id != update.message.from_user:
        update.message.reply_text("You are not an administrator\n\nВы не администратор =(")
    else:
        password = new_one
        update.message.reply_text("Password successfully changed.\n\nПароль успешно изменен.")


def get_password(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    if update.message != "/get_password":
        update.message.reply_text("Invalid number of arguments\n(Неверное количество аргументов)")
        return
    if admin_id != update.message.from_user.id:
        update.message.reply_text("You are not an administrator\n\nВы не администратор =(")
        return
    update.message.reply_text(f"Password is: {password}")


def help(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    update.message.reply_text("Sorry, this part is not done yet.\n\nИзвините, эта часть бота пока не работает.")


def admin_help():
    pass


def main():
    bot = Updater(TOKEN)
    disp: telegram.ext.updater.Dispatcher = bot.dispatcher

    disp.add_handler(MessageHandler(Filters.photo, reply_photo))
    disp.add_handler(MessageHandler(Filters.video, reply_video))
    disp.add_handler(CommandHandler("set_admin", set_admin))
    disp.add_handler(CommandHandler("set_password", set_password))
    disp.add_handler(CommandHandler("get_password", get_password))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(MessageHandler(Filters.text, reply_text))

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
