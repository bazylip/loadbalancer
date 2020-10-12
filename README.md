# Instructions

 - Pull repository to your workspace
 - Initialize npm: 
     - `cd dockerfiles/server && npm init -y`
 - Build server's docker image: 
     - `docker build -t nodeapp:001 .`
 - Run two server containers using image from previous step: 
     - `docker container run -p 5001:5000 --name server1 -d nodeapp:001`
     - `docker container run -p 5002:5000 --name server2 -d nodeapp:001`
 - Build loadbalancer's docker image: 
     - `cd ../loadbalancer && docker build -t nginxbalancer:001 .`
 - Run loadbalancer container using image from previous step:
     - `docker container run -p 5000:80 --name loadbalancer -d nginxbalancer:001` 
