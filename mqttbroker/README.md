# Setup
 - `docker-compose up -d` 
 - `docker-compose exec mosquitto sh`
 - `mosquitto_passwd -c /mosquitto/config/pwfile <USERNAME>`
 - `exit`
 - `docker-compose restart mosquitto`
