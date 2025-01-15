import telebot
import platform
import os  # To interact with the filesystem

bot = telebot.TeleBot('7726476744:AAHJAopdXu4WSOAP_6u0rhKMHZhA6LHhZ_0')  # Replace with your bot token

@bot.message_handler(commands=['start'])
def main(message):
    os_type = platform.system()  # Get the OS type
    bot.send_message(message.chat.id, f"Immediately. The 3D printer is working with a defect. It will be stopped. OS: {os_type}")

@bot.message_handler(commands=['image'])
def send_images(message):
    folder_path = '/home/zhan/3dprinter_camera_capture/detections'  # Replace with the absolute path to your folder
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            bot.send_message(message.chat.id, "The specified folder does not exist. Please check the path.")
            return

        # List all files in the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            bot.send_message(message.chat.id, "No images found in the folder.")
            return

        # Send each image
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=f"Image: {file_name}")

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

bot.polling(none_stop=True)
