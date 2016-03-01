# Configuration file for jupyterhub.

import os

# Grant admin users permission to access single-user servers.
c.JupyterHub.admin_access = True

c.JupyterHub.authenticator_class = 'mitoauthenticator.MITGroupOAuthenticator'

c.MITGroupOAuthenticator.required_group = "cgs"

c.MITOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
c.MITOAuthenticator.client_id = os.environ['OAUTH_CLIENT_ID']
c.MITOAuthenticator.client_secret = os.environ['OAUTH_CLIENT_SECRET']

# Whether to shutdown the proxy when the Hub shuts down.
# 
# Disable if you want to be able to teardown the Hub while leaving the proxy
# running.
# 
# If both this and cleanup_servers are False, sending SIGINT to the Hub will
# only shutdown the Hub, leaving everything else running.
# 
# The Hub should be able to resume from database state.
c.JupyterHub.cleanup_proxy = True

# Whether to shutdown single-user servers when the Hub shuts down.
# 
# Disable if you want to be able to teardown the Hub while leaving the single-
# user servers running.
# 
# If both this and cleanup_proxy are False, sending SIGINT to the Hub will only
# shutdown the Hub, leaving everything else running.
# 
# The Hub should be able to resume from database state.
c.JupyterHub.cleanup_servers = False

# Path to SSL certificate file for the public facing interface of the proxy
c.JupyterHub.ssl_cert = '/root/server.crt'

# Path to SSL key file for the public facing interface of the proxy
c.JupyterHub.ssl_key = '/root/server.key'

# set of usernames of admin users
# 
# If unspecified, only the user that launches the server will be admin.
c.Authenticator.admin_users = set(["matted", "zeng", "thashim"])

# Dictionary mapping authenticator usernames to JupyterHub users.
# 
# Can be used to map OAuth service names to local users, for instance.
# 
# Used in normalize_username.
c.Authenticator.username_map = {"haoyangz" : "zeng"}

# The class to use for spawning single-user servers.
c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.proxy_api_ip = '0.0.0.0'

c.DockerSpawner.hub_ip_connect = "jupyterhub"
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.links = {"jupyterhub" : "jupyterhub"}

c.SystemUserSpawner.container_image = 'giffordlab/jupyter-systemuser'

c.SystemUserSpawner.read_only_volumes = {"/cluster" : "/cluster",
                                         "/etc/passwd" : "/etc/passwd",
                                         "/etc/group" : "/etc/group"}

c.SystemUserSpawner.extra_host_config = {"devices" : ["/dev/nvidiactl", 
                                                      "/dev/nvidia-uvm",
                                                      "/dev/nvidia0",
                                                      "/dev/nvidia1",
                                                      "/dev/nvidia2"]}

# Hack that lets us signal that we're on a GPU machine, even if the
# hub is inside Docker and not GPU-enabled itself.
if len(os.environ.get("NVIDIA_STATUS", "")) <= 0:
    # Don't mount the GPU devices if we're not on a GPU system (we
    # have return code 0 for success).
    c.SystemUserSpawner.extra_host_config = {}

c.SystemUserSpawner.host_homedir_format_string = '/cluster/{username}'
c.SystemUserSpawner.image_homedir_format_string = '/cluster/{username}'
