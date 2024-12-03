# Автоматическое развертывание панели 3x-ui на серверах в контейнере Docker

- Добавляем ip серверов в hosts.ini
- Запустить ansible playbook командой ~ansible-playbook -i hosts.ini playbook.yml -e "vpn_id_user=<id> vpn_username=<panel_login> vpn_password=<panel_password> vpn_port=<port> vpn_web_base_path=<additional_path>"
- Complete!

В Ansible присутствуют 2 роли: docker и 3x_ui_container. Если на сервере нет Docker, ansible сам его установит, если он есть, то выведет версию. Роль 3x_ui_container обновляет Dockerfile для контейнера и запускает его. Dockerfile просто скачивает установочный скрипт в контейнер и запускает его там. Если нужно изменить все переменные, то нужно делать build заново (web_base_path почему-то не меняется внутри контейнера). 
