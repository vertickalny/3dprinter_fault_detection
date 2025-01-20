import os
import telebot
import requests
from klippy_api.KlippyAPI import KlippyAPI

def main() -> None:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    bot = telebot.TeleBot(BOT_TOKEN)
    
    base_url = "http://192.168.31.100:7125"
    klippy = KlippyAPI(base_url)

    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        print(message.chat.id)
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(commands=['info'])
    def get_info(message):
        print("info command is invoked")
        printer_info = klippy.get_printer_info()
        bot.reply_to(message, printer_info)

    @bot.message_handler(commands=['list'])
    def list(message):
        print("list command is invoked")
        printer_objects = klippy.list_printer_objects()
        bot.reply_to(message, "Printer Objest:" + printer_objects)

    @bot.message_handler(commands=['restart_host'])
    def restart_host(message):
        print("restart host command is invoked")
        response = klippy.restart_host()
        bot.reply_to(message, "Printer's response: " + response)
    
    @bot.message_handler(commands=['restart_firmware'])
    def restart_firmware(message):
        print("restart firmware command is invoked")
        response = klippy.firmware_restart()
        bot.reply_to(message, "Printer's response: " + response)

    @bot.message_handler(commands=['extruder'])
    def get_extruder(message):
        print("extruder firmware command is invoked")
        status = klippy.query_printer_object_status({"gcode_move": None, "toolhead": None, "extruder": "target,temperature"})
        bot.reply_to(message, "Printer status: " + status)

    @bot.message_handler(commands=['stop'])
    def emergency_stop(message):
        print("emergency stop command is invoked")
        response = klippy.emergency_stop()     
        bot.reply_to(message, "Printer's response: " + response)

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        bot.reply_to(message, message.text)
    
    #to launch bot
    bot.infinity_polling()

    
if __name__ == '__main__':
    main()
