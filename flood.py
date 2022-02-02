from telethon import TelegramClient
from telethon.errors import rpcerrorlist, FloodWaitError, ChatWriteForbiddenError
import time
import os
import progressbar
import colorama
from colorama import Fore, Back, Style
from rich.console import Console
from rich.progress import *

console = Console()


if os.path.isfile('spamer.txt'):
    with open('spamer.txt', 'r') as r:
        data = r.readlines()
    api_id = int(data[0])
    api_hash = data[1]

else:
    api_id = input('Введите api_id: ')
    api_hash = input('Введите api_hash: ')
    with open('spamer.txt', 'w') as a:
        a.write(api_id + '\n' + api_hash)

client = TelegramClient('spamer', api_id, api_hash)


async def main():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    global target
    console.print('''[bold blue]
   __   _                       _ 
  / _| | |   ___     ___     __| |
 | |_  | |  / _ \   / _ \   / _` |
 |  _| | | | (_) | | (_) | | (_| |
 |_|   |_|  \___/   \___/   \__,_|
                                                                                                         
    ''')

    print(Fore.RED +'Выбери чат'+Fore.WHITE +':')
    i = 0
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(i, ':', dialog.name, 'has ID', dialog.id)
        i = i + 1

    confirm = False
    max = len(dialogs) - 1

    while confirm == False:
        target_index = -1

        # Get target chat
        while target_index < 0 or target_index > max:
            print(Fore.BLUE +"Введи цифру от 0 до", max)
            target_index = int(input(Fore.GREEN +'spammer>> '))
            if target_index < 0 | target_index > max:
                print(Fore.RED +'Ошибка!')

        target = dialogs[target_index]
        print(Fore.MAGENTA +'Чат-', target.name, 'ID-', target.id)

        print(Fore.YELLOW +'Верно? (y/n)')
        reply = input(Fore.GREEN +'spammer>> ')[0]
        if reply == 'Y' or reply == 'y':
            confirm = True

    print(Fore.RED +"Введите сообщение:")
    message = input(Fore.GREEN +"spammer>> ")
    print(Fore.MAGENTA +"Сколько сообщений отправить?:")
    Several = int(input(Fore.GREEN +"spammer>> "))

    print(Fore.BLUE +'Спам начнется через 3 секунды...')
    time.sleep(3)
    print(Fore.WHITE +"Атака началась!")
    bar = progressbar.ProgressBar(
        widgets=[progressbar.SimpleProgress()],
        max_value=Several,
    ).start()
    try:
        for i in range(int(Several)):
            await client.send_message(target.id, message)
            bar.update(i + 1)
        bar.finish()
        print(Fore.GREEN +"Успешно!")
    except rpcerrorlist.ChatAdminRequiredError:
        print(Fore.RED +"[!]У тебя нет доступа чтобы писать в этом чате!")
    except ChatWriteForbiddenError:
        print("[!] Вы были ограничены в написании сообщений в этом чате...!")
    except FloodWaitError:
        print("[!] Повторите попытку через час!")



with client:
    client.loop.run_until_complete(main())
