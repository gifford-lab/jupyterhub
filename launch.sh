#!/bin/bash
# /cluster/zeng/cluster-management/passwd is a copy of /etc/passwd on a CSAIL Ubuntu 14.04 node
# We can't directly use /etc/passwd on 16.04 as it no longer has the user info stored
docker run -d \
    --name=jupyterhub \
    -p 443:8000 \
    --env-file /root/setup_oauth_tokens.list \
    -e NVIDIA_STATUS="$(nvidia-smi | grep -Fv failed)" \
    -v /opt/jupyterhub:/srv/jupyterhub \
	-v /cluster/zeng/cluster-management/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -v /root/${HOSTNAME}_all.pem:/root/server.key \
    -v /root/${HOSTNAME}_all_certs.pem:/root/server.crt \
    -v /var/run/docker.sock:/var/run/docker.sock \
	-v $(pwd)/jupyterhub_config.py:/root/jupyterhub_config.py \
    -v $(which docker):/bin/docker \
    giffordlab/jupyterhub jupyterhub \
    -f /root/jupyterhub_config.py
