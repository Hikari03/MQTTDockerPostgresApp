# Setup
 - `docker-compose up -d` 
 - `docker-compose exec mosquitto sh`
 - `chmod 0700 /mosquitto/config/pwfile`
 - `chown root /mosquitto/config/pwfile`
 - `mosquitto_passwd -c /mosquitto/config/pwfile <USERNAME>`
 - `exit`
 - `docker-compose restart mosquitto`
