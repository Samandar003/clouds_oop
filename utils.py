from main import CloudStorage
import time
import random
import string
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


class TelegramFileBot(CloudStorage):
    def __init__(self, token):
        self.token = token

    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Send me a file, and I will store it in sql db.')

    def handle_file(self, update: Update, context: CallbackContext):
        file_id = update.message.document.file_id
        file_unique_id = update.message.document.file_unique_id
        file_name = update.message.document.file_name

        file = context.bot.get_file(file_id)
        file_content = file.download_as_bytearray()

        timestamp = int(time.time())
        code=CloudStorage.generate_6_digit_id()
        conn = self.connection
        c = conn.cursor()
        c.execute(f"INSERT INTO {self.table} (file_name, file_id, content, timestamp) VALUES (?, ?, ?, ?)", (file_name, file_name, code, file_content, timestamp))
        conn.commit()
        conn.close()

        update.message.reply_text(f'File stored successfully! Use file_code {code} to retrieve the file.')

    def retrieve_file(self, update: Update, context: CallbackContext) -> None:
        code = update.message.text.strip()  # Presume that the user sends the code as text

        # Retrieve the file using the code from the database
        conn = self.connection
        c = conn.cursor()
        c.execute(f"SELECT file_id, file_name FROM {self.table} WHERE file_id=?", (code,))
        result = c.fetchone()
        conn.close()

        if result:
            file_unique_id, file_name = result
            context.bot.send_document(update.message.chat_id, document=file_unique_id, filename=file_name)
        else:
            update.message.reply_text('File not found with the provided code.')

    def run(self):
        updater = Updater(self.token)
        dispatcher = updater.dispatcher

        # Add handler
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(MessageHandler(Filters.document, self.handle_file))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.retrieve_file))

        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
    bot = TelegramFileBot("6841161241:AAGAavXXP9pf-lJrlptrNDmKo_Vp_0uNcQs")
    bot.run()


