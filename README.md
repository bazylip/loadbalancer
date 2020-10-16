# Instructions

 - Pull repository to your workspace
 - Change default DNS servers
     - `sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf`
 - Build docker images: 
     - `docker-compose build --no-cache`
 - Bring up the containers: 
     - `docker-compose up`
 - To test the connection:
     - `localhost:8080`
 - Run load generator:
     - `python3 tools/load_generator/load_generator.py -a NGROK_ADDRESS -n 5`
# Why shouldn't we set docker user with root privilage
At first, we should face the principle of least privilege, also known as the principle of minimal privilege, requiring that in a particular abstraction layer of a computing environment every module, such as docker container must be able to access only the information and resources that are necessary for its legitimate purpose. This is critical when designing a secure system.
We should remember that a process running in a container is no different from other processes running on Linux. Containers are not trust boundaries, so anything running in a container should be treated with the same consideration as anything running on the host itself. 
Let's take a closer look for example.
```bash
user@machine: ~$ sudo -s
root@machine: ~# echo "top secret" >> /tmp/secrets.txt 
root@machine: ~# chmod 0600 /tmp/secrets.txt
```
We've created a top secret file that might be read-only by root user. Now let's get back to normal user profile
```bash
root@machine: ~# exit
user@machine: ~$ cat /tmp/secrets.txt
cat: /tmp/secrets.txt: Permission denied
```
Now let's imagine our docker is badly configurated, create Dockerfile trying to read this secret file.
```
FROM debian:stretch
CMD ["cat", "/tmp/secrets.txt"]
```
Lets run it...
```bash
user@machine:~$ docker run -v /tmp/secrets.txt:/tmp/secrets.txt <img>
top secret
```
So after this short presentation, we can notice that as a user I've just accessed a file I shouldn't be able to 
