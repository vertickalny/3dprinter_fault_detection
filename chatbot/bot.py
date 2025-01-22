import os
import telebot
import requests
from klippy_api.KlippyAPI import KlippyAPI

def main() -> None:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHAT_ID = int(os.environ.get('CHAT_ID'))
    bot = telebot.TeleBot(BOT_TOKEN)
        
    base_url = "http://192.168.31.100:7125"
    klippy = KlippyAPI(base_url)

    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        print(message.chat.id)
        print(os.environ.get('CHAT_ID'))
        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, "Howdy, how are you doing?")
        else:
            print("not equal")

    @bot.message_handler(commands=['info'])
    def get_info(message):
        print("info command is invoked")
        printer_info = klippy.get_printer_info()

        if(message.chat.id == CHAT_ID):   
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

        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, "Printer's response: " + response)
    
    @bot.message_handler(commands=['restart_firmware'])
    def restart_firmware(message):
        print("restart firmware command is invoked")
        response = klippy.firmware_restart()
        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, "Printer's response: " + response)

    @bot.message_handler(commands=['extruder'])
    def get_extruder(message):
        print("extruder firmware command is invoked")
        status = klippy.query_printer_object_status({"gcode_move": None, "toolhead": None, "extruder": "target,temperature"})

        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, "Printer status: " + status)

    @bot.message_handler(commands=['emergency_stop'])
    def emergency_stop(message):
        print("emergency stop command is invoked")
        response = klippy.emergency_stop()     

        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, "Printer's response: " + response)

    @bot.message_handler(commands=['pause'])
    def pause(message):
        print("Pausing print")
        response = klippy.pause()

        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, message.text)

    @bot.message_handler(commands=['resume'])
    def pause(message):
        print("Resuming printing")
        response = klippy.pause()
        if(message.chat.id == CHAT_ID):   
            bot.reply_to(message, message.text)


    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        bot.reply_to(message, message.text)
    
    #to launch bot
    bot.infinity_polling()

    
if __name__ == '__main__':
    main()
