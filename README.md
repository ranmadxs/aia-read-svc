---
runme:
  id: 01HJQE75SKBTCT1QQK59F1AVR6
  version: v2.0
---

# aia-read-svc

AIA Read Service

```console {"id":"01HJQE75SKBTCT1QQK57A0T1JR"}
poetry run daemon

git ls-remote --get-url origin 
git remote set-url origin git@github_ranmadxs:ranmadxs/aia-read-svc.git
```

## Docker

```console {"id":"01HJQ7F9RXZBJJ4YEQAAH1BXHZ"}
#build
docker build . --platform linux/arm64/v8 -t keitarodxs/aia:aia-read-svc_0.1.0

#push
docker push keitarodxs/aia:aia-read-svc_0.1.0

#go into docker container
sudo docker exec -ti aia_read_svc bash

```

### Install Img

```console {"id":"01HJQ7F9RXZBJJ4YEQAAX4XA1Y"}

#pull
docker pull keitarodxs/aia:aia-read-svc_0.1.0

#run
docker run -d --rm -e TZ=America/Santiago -v /home/ranmadxs/aia/aia-read-svc/target:/app/target --net=bridge --name aia_read_svc --env-file .env keitarodxs/aia:aia-read-svc_0.1.0


#other commands
docker save -o aia-read-svc_0.1.0.tar keitarodxs/aia:aia-read-svc_0.1.0

docker load -i aia-read-svc_0.1.0.tar
```

