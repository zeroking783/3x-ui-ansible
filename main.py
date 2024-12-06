import ansible_runner
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import random
import string
import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("BOT_API_TOKEN")
HOME_DIRECTORY = os.getenv("HOME_DIRECTORY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_server_ip(server_name, ini_file="hosts.ini"):
    with open(ini_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith(server_name):
            parts = line.split()
            for part in parts:
                if part.startswith("ansible_host="):
                    return part.split("=")[1]
    raise ValueError(f"Сервер '{server_name}' не найден в файле {ini_file}")

def run_ansible_playbook(extravars, limit):
    playbook = "playbook.yml"
    private_data_dir = f"{HOME_DIRECTORY}/ansible-role-3x-ui"
    inventory = f"{HOME_DIRECTORY}/hosts.ini"

    result = ansible_runner.run(
        private_data_dir=private_data_dir,
        inventory=inventory,
        playbook=playbook,
        extravars=extravars,
        limit=limit,
    )

    print(f"Статус: {result.status}")
    print(f"RC: {result.rc}")

    for event in result.events:
        if 'stdout' in event:
            print(event['stdout'])

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Чтобы развернуть новый контейнер с панелью 3x-ui, введи команду /new")

@dp.message(Command("new"))
async def cmd_start(message: Message):
    vpn_id_user = generate_random_string().lower()
    vpn_username = generate_random_string()
    vpn_password = generate_random_string()
    vpn_port = random.randint(60000, 65000)
    vpn_web_base_path = generate_random_string()

    server_name = "server1"
    ip = get_server_ip(server_name)

    extravars = {"action": "build_image",
                 "vpn_id_user": vpn_id_user,
                 "vpn_username": vpn_username,
                 "vpn_password": vpn_password,
                 "vpn_port": vpn_port,
                 "vpn_web_base_path": vpn_web_base_path}

    run_ansible_playbook(extravars, server_name)

    await message.answer("Вот твоя ссылка для входа в панель:")
    await message.answer(f"http://{ip}:{vpn_port}/{vpn_web_base_path}")
    await message.answer("Данные для входа:")
    await message.answer(f"login: {vpn_username}")
    await message.answer(f"password: {vpn_password}")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


