sudo apt update -y
sudo apt install python3-pip -y

git clone https://github.com/searayeah/vk-telegram-bot.git /home/vk-telegram-bot
pip3 install -r ./home/vk-telegram-bot/requirements.txt
pip3 install https://github.com/searayeah/vkbottle/archive/refs/tags/4.11.11.zip

python3 -m /home/vk-telegram-bot/bot
