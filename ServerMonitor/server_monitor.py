import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('ip',port,'name','pw')
stdin,stdout,stder = ssh.exec_command('df -h')
result_list=stdout.read().decode(encoding="utf-8", errors="strict").split('\n')[1].split(' ')
b={}
b=b.fromkeys(result_list)
b.pop('')
a=list(b.keys())
print(a)
stdin,stdout,stder = ssh.exec_command('uptime')
result_list=stdout.read()
print('123')
print(result_list)
ssh.close()