import ansible_runner

playbook = "playbook.yml"
private_data_dir = "/home/bakvivas/Documents/Projects/ansible-role-3x-ui"
inventory = "/home/bakvivas/Documents/Projects/ansible-role-3x-ui/hosts.ini"
extravars = {"action": "delete_image",
             "vpn_id_user": "1bakvivas"
            }
limit = "server1"

result = ansible_runner.run(
    private_data_dir=private_data_dir,
    inventory=inventory,
    playbook=playbook,
    extravars=extravars,
    limit=limit
)

print(f"Статус: {result.status}")
print(f"RC: {result.rc}")

# Вывод stdout для каждого события
for event in result.events:
    if 'stdout' in event:
        print(event['stdout'])