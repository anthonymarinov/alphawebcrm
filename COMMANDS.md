# Useful Commands to Remember

Command to get into AWS instance (ubuntu):\
    `ssh -i <location/to/key.pem> ubuntu@3.146.34.38`

Make sure to run in alpha-mm-inc-crm directory by ```cd alpha-mm-inc-crm```

Git push local changes to github, git pull on ubuntu ec2 instance.\
Shut down container: ```docker-compose down```\
Rebuild container: ```docker-compose build```\
Run container: ```docker-compose up -d```  (-d runs container in background)

Check container status and id: ```docker-compose ps```\
Check logs:\
    ```docker-compose logs -f nginx```\
    ```docker-compose logs -f web```

Enter container's shell:\
    ```docker exec -it <container-name-or-id> /bin/bash``` or\
    ```docker-compose exec web bash``` for web sontainter, or\
    ```docker-compose exec nginx bash``` for nginx container\
To exit container shell or ubuntu ec2 instance: 
    ```exit```

Remove all unused container images:\
    ```docker image prune -a```\
Remove all unused container volumes:\
    ```docker volume prune -a```

Check storage: ```df -h```
