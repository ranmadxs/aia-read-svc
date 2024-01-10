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

```sh {"id":"01HJV2GKHFHRCW2MAYBX6DWF7V"}
#set var entorno
export AIA_TAG_READ=aia-read-svc_0.2.0
```

```sh {"id":"01HJQ7F9RXZBJJ4YEQAAH1BXHZ"}
#build
docker build . --platform linux/arm64/v8 -t keitarodxs/aia:$AIA_TAG_READ

#push
docker push keitarodxs/aia:$AIA_TAG_READ

#go into docker container
sudo docker exec -ti aia_read_svc bash

#run
docker run -d --rm -e TZ=America/Santiago -v /home/ranmadxs/aia/aia-cortex-nlu/target:/app/target --net=bridge --name aia_read_svc --env-file .env keitarodxs/aia:$AIA_TAG_READ

```
```sh
#other commands
docker save -o $AIA_TAG_READ.tar keitarodxs/aia:$AIA_TAG_READ

docker load -i $AIA_TAG_READ.tar
```

