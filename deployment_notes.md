# Notes on deployment using docker machine

## Requirements

- Docker (including docker-compose and docker-machine)
- Properly configured `.env.prod` file
- A virtual machine to deploy on

## Staging

Check which machines are available

```
docker-machine ls		# Identify available machines
docker-machine create --help	# Create a new machine
docker-machine use <name>	# Set up environment to directly use machine
```

Production docker-compose file

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

For testing, set $STAGING_ENVIRONMENT to find app

```
export STAGING_ENVIRONMENT=http://$(docker-machine ip <name>)
make test
```

When you are finish, you can perform the following cleanup steps

```
make clean
docker-machine stop
docker-machine rm
docker-machine use -u
```
