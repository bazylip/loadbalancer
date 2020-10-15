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