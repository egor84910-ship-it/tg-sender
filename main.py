import os
import ctypes
import logging
import time
import gc
import re
import subprocess
from datetime import datetime
from time import sleep
from typing import List
from telethon.errors import SessionPasswordNeededError
from telethon.errors.common import InvalidBufferError
from telethon.sync import TelegramClient, errors
from colorama import init, Fore, Style
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser
from telethon.tl.types import Chat, Channel

# ─── Globals ────────────────────────────────────────────────────────────────
session_folder = 'sessions'
debug_folder   = 'Debug'
log_file_path  = os.path.join(debug_folder, 'Debug.log')
info_file_path = 'info.txt'

info_text = (
    "Информация о софте:\n"
    "Название: PIRATE SMM 🏴\u200d☠️\n"
    "Текущая версия: 3.55\n"
    "Описание:\n"
    "Всем доброго времени суток!\n"
    "Софт написан на последних алгоритмах!\n"
    "Мой дискорд https://discord.gg/q4TKWwGhzZ\n"
    "Лучшая крипто-биржа с самыми низкими комиссиями + 15$ бонус на фьючерсы новичкам - \n"
    "Ссылка на биржу - https://www.mexc.com/ru-RU/register?inviteCode=mexc-129JkC\n\n"
    "Инструкция по работе:\n"
    "1. Нужны трастовые аккаунты, чем старше - тем лучше. Отлично заходят аккаунты из Киргизии, их можно приобрести на лолзе.\n"
    "2. Когда есть премиум, страница дольше живет и спамит, плюс сама снимает спам блок.\n"
    "3. Избегайте живых чатов, где идет активное общение, чтобы избежать бана страницы.\n"
    "4. Есть запрещенные слова, обходите их, если страницы сразу блокируют.\n"
    "5. Также продаю готовые папки с чатами на разные тематики (от криптовалюты до поиска работы и серых схем). В наличии 500+ папок с чатами, цена - 40$.\n"
    "6. Консультация и помощь по софту и работе - 20$ (для тех, кто приобрел обучение, пожизненно бесплатно).\n"
    "7. Мой дискорд: https://discord.gg/q4TKWwGhzZ\n"
    "Часто страницы в Telegram блокируют конкуренты, но дискорд вечен!\n\n"
    "8. У меня есть обучение, включающее несколько софтов, базу чатов (включая личную), все фишки и алгоритмы Telegram. \n"
    "Покажу и расскажу, как зарабатывать на рассылке 700$+ на пассиве. Цена - 250$. Писать в дискорде, там дам контакт на Telegram.\n"
)

with open(info_file_path, 'w', encoding='utf-8') as file:
    file.write(info_text)

if not os.path.exists(info_file_path):
    with open(info_file_path, 'w', encoding='utf-8') as file:
        file.write(info_text)

subprocess.Popen(['notepad.exe', info_file_path])

if not os.path.exists(session_folder):
    os.makedirs(session_folder)

if not os.path.exists(debug_folder):
    os.makedirs(debug_folder)

logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

api_id   = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'

logo = (
    "                              \n"
    " ____  ____  ____    __   ____  ____    ___  __  __  __  __   \n"
    "(  _ \\(_  _)(  _ \\  /__\\ (_  _)( ___)  / __)(  \\/  )(  \\/  )   \n"
    " )___/ _)(  )   / /(__)\\  )(   )__)   \\__ \\ )    (  )    (    \n"
    "(__) (____)(_)\\_)(__)(__)(__) (____)  (___/(_/\\/\\_)(_/\\/\\_)   \n\n"
    "Лучшая крипто-биржа с самыми низкими комиссиями + 15$ бонус на фьючерсы новичкам\n"
    "Биржа - https://www.mexc.com/ru-RU/register?inviteCode=mexc-129JkC"
    "                                                                                                                   \n"
)


# ─── Utility functions ───────────────────────────────────────────────────────

def set_console_title(new_title):
    ctypes.windll.kernel32.SetConsoleTitleW(new_title)


def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_startup_message():
    clear_console()
    print("Starting...")
    
    print("Проверяю обновление...")
   
    print("Разработчик: Дискорд - https://discord.gg/q4TKWwGhzZ")
   
    print("Лучшая крипто-биржа с самыми низкими комиссиями + 15$ бонус на фьючерсы новичкам")
    print("Биржа - https://www.mexc.com/ru-RU/register?inviteCode=mexc-129JkC ")
    
    current_time = datetime.now().strftime('%H:%M:%S')
    print()
    print(f"[{current_time}]  Текущая версия: 3.55")
    print()
    for i in range(1, 21):
        progress = ("█" * i).ljust(20)
        print(f"\r{progress} {i * 5}%", end="", flush=True)
    
    print()


# ─── Session management ──────────────────────────────────────────────────────

def find_session_files(api_id, api_hash):
    device_model = 'Samsung S24 Ultra'
    app_version  = '12.5.1'

    while True:
        try:
            print("Выбери, какой аккаунт хочешь Подключить:")
            print("[1] Подключить Session:")
            print("[2] Подключить Новый:")
            choice = input("Выбери вариант:")

            if choice == '1':
                choice = 'y'
            elif choice == '2':
                choice = 'n'
            else:
                print("Неверный выбор введи 1 или 2.")
                continue

            clear_console()
            print(logo)

            if choice.lower() == 'n':
                name         = input("Введи название для аккаунта [любое]: ")
                session_path = os.path.join(session_folder, name)

            elif choice.lower() == 'y':
                session_files = [f for f in os.listdir(session_folder) if f.endswith('.session')]
                print("Выбери аккаунт, который хочешь использовать:")
                for i, file in enumerate(session_files):
                    print(f"{i + 1}. {file}")

                file_index = input("Введи номер аккаунта для подключения: ")
                if file_index.isdigit():
                    file_index = int(file_index) - 1
                    if 0 <= file_index < len(session_files):
                        name         = session_files[file_index].replace('.session', '')
                        session_path = os.path.join(session_folder, name)
                        clear_console()
                        print(logo)
                    else:
                        print("Неверный номер файла.")
                        continue
                else:
                    print("Неверный ввод.")
                    continue
            else:
                print(f"Неверный ввод: {choice}")
                continue

            logging.info(f"Attempting to start TelegramClient with session: {session_path}")
            client = TelegramClient(
                session_path, api_id, api_hash,
                device_model="Desktop",
                system_version="Windows 11 x64",
                app_version="6.0.2 x64",
                system_lang_code="tdesktop",
                lang_code="jabka"

            )
            client.start()
            logging.info(f"Successfully started TelegramClient with session: {session_path}")
            me = client.get_me()
            clear_console()
            print(logo)
            return client

        except SessionPasswordNeededError:
            password = input("Введите пароль 2FA: ")
            client.start(password=password)
            continue

        except Exception as e:
            logging.error(f"Ошибка при входе в сессию: {e}", exc_info=True)
            print(f"Ошибка при входе в сессию: {e}")
            continue


# ─── SpamBot interaction (auto spam-block removal) ───────────────────────────

def send_start_message(client):
    global stopped, spam_block_removed

    if stopped:
        return

    try:
        for _ in range(2):
            client.send_message('@SpamBot', '/start')
            time.sleep(3)

        history = client(GetHistoryRequest(
            peer=PeerUser(user_id=client.get_entity('@SpamBot').id),
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        if history and history.messages:
            last_message = history.messages[0].message

            if ('Ваш аккаунт свободен от каких-либо ограничений.' in last_message or
                    "Good news, no limits are currently applied to your account. You're free as a bird!" in last_message):
                if not spam_block_removed:
                    print(f"{Fore.GREEN}🟢 SpamBlok Успешно Снят{Style.RESET_ALL}")
                    print(f"{Fore.MAGENTA}🟣 Продолжаю Рассылать{Style.RESET_ALL}")
                    spam_block_removed = True

            elif re.search(
                "Здравствуйте|очень жаль|пока действуют ограничения|Hello|I'm very sorry|While the account is limited",
                last_message
            ):
                print(f"{Fore.RED}🔴 Аккаунт получил вечный SpamBlok:{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}🟢 Рассылка остановлена:{Style.RESET_ALL}")
                stopped = True
                while True:
                    sleep(99999999)

    except errors.FloodError as e:
        logging.error(f"Flood error: {e.message}")
    except Exception as exc:
        logging.error(f"Произошла непредвиденная ошибка: {exc}")


# ─── Get list of groups/megagroups ───────────────────────────────────────────

def create_groups_list(client: TelegramClient) -> List:
    groups = []
    for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, Chat) or (
            isinstance(dialog.entity, Channel) and dialog.entity.megagroup
        ):
            groups.append(dialog)
    return groups


# ─── Main spammer loop ───────────────────────────────────────────────────────

def spammer(client: TelegramClient, send_start_message_enabled: bool, delay: int):
    total_messages_sent = 0

    with client:
        # Get last saved message from "me"
        for m in client.iter_messages('me', 1):
            msg = m

        while True:
            print("Рассылаю...")
            groups = create_groups_list(client)

            for g in groups[:1000]:
                try:
                    client.forward_messages(g, msg, 'me')
                    total_messages_sent += 1

                except errors.ChatWriteForbiddenError as chat_write_error:
                    logging.error(f"Невозможно отправить сообщение в чат: {chat_write_error}")
                    continue

                except errors.ForbiddenError as o:
                    logging.error(f"Не удалось отправить сообщение в чат: {o}")
                    continue

                except errors.FloodError as e:
                    if e.seconds > 120:
                        continue
                    logging.error(f"Flood: {e.message} Требуется ожидание {e.seconds} секунд")
                    sleep(e.seconds)
                    continue

                except errors.UserNotParticipantError as user_not_participant_error:
                    logging.error(f"UserNotParticipantError: {user_not_participant_error}")
                    continue

                except errors.MessageTooLongError:
                    logging.error(f"Message was too long ==> {g.name}")
                    continue

                except errors.BadRequestError as i:
                    logging.error(f"Flood: {i.message}")
                    if i.message == 'BAD_REQUEST' and send_start_message_enabled:
                        send_start_message(client)
                    continue

                except errors.RPCError as rpc_error:
                    logging.error(f"RPCError: {rpc_error}")
                    continue

                except InvalidBufferError:
                    logging.error("Ошибка при обработке буфера: InvalidBufferError")
                    continue

                except Exception as exc:
                    logging.error(f"Произошла непредвиденная ошибка: {exc}")
                    continue

            gc.collect()
            groups.clear()
            clear_console()
            print(logo)

            account_name = client.get_me().first_name
            print(f"{Fore.GREEN}Аккаунт: {account_name}{Style.RESET_ALL}")
            print("Отправлено сообщений:", total_messages_sent)
            print(f"Ушел в сон на {delay} секунд...")
            sleep(delay)


# ─── Helper ──────────────────────────────────────────────────────────────────

def ask_user_confirmation(message: str) -> bool:
    response = input(f"{message} [да/нет]: ").lower()
    return response == 'да'


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    new_title = 'PIRATE SMM 🏴\u200d☠️'
    set_console_title(new_title)
    print(logo)

    show_startup_message()
    clear_console()
    print(logo)

    client       = find_session_files(api_id, api_hash)
    account_name = client.get_me().first_name
    print_success(f"Аккаунт: {account_name}")

    delay = int(input("Введите значение таймера в секундах: "))

    stopped                   = False
    send_start_message_enabled = False
    spam_block_removed         = False

    send_start_message_enabled = ask_user_confirmation("Включить / Выключить: Авто Снятие SpamBlok")
    spammer(client, send_start_message_enabled, delay)
