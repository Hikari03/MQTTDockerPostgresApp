# Setup
 - `docker-compose up -d` 
 - `docker-compose exec mosquitto sh`
 - `sudo chown root /mosquitto/config/pwfile`
 - `mosquitto_passwd -c /mosquitto/config/pwfile <USERNAME>`
 - `exit`
 - `docker-compose restart mosquitto`
