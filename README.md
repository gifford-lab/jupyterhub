# Gifford lab Jupyterhub server

This is an image and launching script for running a Jupyterhub
(master) server inside Docker, where it is able to launch user Jupyter
(client) notebook servers as separate Docker containers on the same
outer host machine.

It is based on the [compmodels Docker
setup](https://github.com/compmodels/jupyterhub) and the
[dockerspawner](https://github.com/jupyter/dockerspawner)
documentation.

Custom authentication using MIT accounts is provided by
[mit-oidc-authenticator](https://github.com/matted/mit-oidc-authenticator).

[This](https://github.com/gifford-lab/jupyter-docker-stacks/tree/master/systemuser)
is the client notebook server image that contains all the client-side
libraries, and it's based on [this
image](https://github.com/gifford-lab/jupyter-docker-stacks/tree/master/datascience-notebook).
It has many R and Python packages installed, as well as full CUDA
capability along with Theano and related libraries (which will work
only if the server is running on a GPU machine).  Each user only has
write access to `/cluster/$USERNAME` and read-only access to all of
`/cluster`.  There are automatic Docker builds with these names hooked
to the Github repository.

The overall goal is to have a very thin layer of extra code around the core
Jupyter functionality, so that we can stay up to date and not create
more headaches down the road.

### Setup 

Browsing through `jupyterhub_config.py` and `launch.sh` should give an
idea of what needs to be set up on the server before starting the hub:

* Docker installed and the client image
  `giffordlab/jupyter-systemuser` and the hub image
  `giffordlab/jupyterhub` pulled

* The file `/root/setup_oauth_tokens.list`, a Docker `env-file` that
  sets `OAUTH_CALLBACK_URL`, `OAUTH_CLIENT_ID`, and
  `OAUTH_CLIENT_SECRET`, which are all obtained by following the
  instructions
  [here](https://github.com/matted/mit-oidc-authenticator)

* Certificate files at `/root/${HOSTNAME}_all.pem` and
  `/root/${HOSTNAME}_all_certs.pem`, obtained by following the
  instructions
  [here](https://github.com/gifford-lab/ipython-docker-servers/)

### Using the hub

Run the script `launch.sh`.  Make sure the port and persistent storage
directory (mapped to `/srv/jupyterhub`) values are correct.

### Debugging

* Check the hub and client logs (via Docker) for any error messages.

* Double check which version of `python` or `pip` you're using, and
make sure libraries are installed for the correct location (and Python
version).  Everything inside the notebook should use the Conda
installation at `$CONDA_DIR`.

## Updating the notebook image

If you want more features or packages inside your notebook, you have
several choices:

1. Install a Python or R package with `pip`, `conda`, or `R`.  The
user's home directory inside the image is set to `/cluster/$USERNAME`,
so user-installed packages will go in subdirectories there and persist
across container restarts.  Note that the default versions of `python`
and `pip` in the container are for Python 3; to install Python 2
packages first run `source activate python2` or make sure to use
binaries in `$CONDA_DIR/envs/python2/bin`.

2. Log into the running container (it will be named
`jupyter-$USERNAME`) as root and install a system package.

3. File a pull request that updates the [source
image](https://github.com/gifford-lab/jupyter-docker-stacks/tree/master/datascience-notebook),
then pull a fresh `giffordlab/jupyter-systemuser` image on the hub
machine.  Manually stop and remove (`docker stop` and `docker rm`)
your running image so that when you log in again, a fresh container is
launched.  This option is slower but better for improvements that
should be shared.

## Notes

Inside the per-user container, `HOME` is set to `/cluster/$USERNAME`.
There is no AFS access in the container.

Access is currently restricted to the `cgs` group.  See the details at
[mit-oidc-authenticator](https://github.com/matted/mit-oidc-authenticator).
