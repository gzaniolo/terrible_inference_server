# Instructions

In case the DINO server goes down, this document should contain enough instructions to allow you to get it running again.


## Build containers

If you also delete all of the images, you will have to rebuild the container:
```
docker build -f Dockerfile_inf_server -t inf_server .
```

## Start container (First time)

```
cd inf_server
docker run -v $(pwd)/:/webserver -p 4000:80 -it --entrypoint /bin/bash --gpus all --name inf_server inf_server
```
Once in the container
```
nginx
gunicorn -c gunicorn.conf.py --workers 1 --bind 0.0.0.0:8000 myapp:app
```
The first time you run it, wait until the required things are installed before querying the server.

## Start container (Next times)

```
docker restart inf_server
docker exec -it inf_server /bin/bash
```
Once in the container
```
nginx
gunicorn -c gunicorn.conf.py --workers 1 --bind 0.0.0.0:8000 myapp:app
```

## Test if container is working

### Test from within WSL
```
curl -X GET http://localhost:4000/ 
```

### Test within windows machine
How to get WSL IP:
```
hostname -I
```
Test:
```
curl -X GET http://172.22.139.165:4000/
```

### Test from outside windows machine
How to get windows machine IP:
```
ipconfig
```
And then look for ipv4 under `Ethernet adapter Ethernet`

Test:
```
curl -X GET http://172.24.156.5:4000/
```

## Debugging

The first time USL was launched, you needed to map the Windows ports to the WSL ports. Here is a useful command:
```
netsh interface portproxy add v4tov4 listenaddress='windows ip' listenport=4000 connectaddress='wsl ip' connectport=4000
```
Additionally, some firewall rules needed to be enstated to allow requests to WSL. The commands for this scenario are currently undocumented.

## Additional Notes

The webserver is located in `/webserver`.\
All of the DINO code is located in `/mmdetection`

The `./inf_server/` directory is `-v` mapped into the docker container at `/webserver`

