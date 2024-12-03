# Автоматическое развертывание панели 3x-ui на серверах в контейнере Docker

---
clone repo https://github.com/zeroking783/3x-ui-ansible.git
---

- Добавляем ip серверов в hosts.ini
- Запускаем ansible playbook командой *ansible-playbook -i hosts.ini playbook.yml -e "vpn_id_user=value vpn_username=value vpn_password=value vpn_port=value vpn_web_base_path=value"*
- Complete!

Чтобы зайти на панель управления переходим по http://ip_server:vpn_port/vpn_web_base_path и вводим в панели управления vpn_username и vpn_password.

В Ansible присутствуют 2 роли: docker и 3x_ui_container. 
Если на сервере нет Docker, ansible сам его установит, если он есть, то выведет версию. 
Роль 3x_ui_container обновляет Dockerfile для контейнера и запускает его. 
Dockerfile просто скачивает установочный скрипт в контейнер и запускает его там. 
Если нужно изменить все переменные, то нужно делать build заново 
(web_base_path почему-то не меняется внутри контейнера). Но мой скрипт каждый раз делает build заново и запускает контейнер.
На сервер можно добавлять любое количество этих контейнеров.
