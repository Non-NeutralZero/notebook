+++
title = "Running PySpark & Jupyter With Docker"
description = "How to set up a development environment around pyspark and jupyter using docker"
tags = [
    "spark",
    "docker",
    "jupyter",
]
date = "2023-06-08"
categories = [
    "Development",
    "Tutorials",
]
menu = "main"
parent = "tutorials"
+++

Thanks to the Jupyter community, it's now much easier to run PySpark on Jupyter using Docker.
There are two ways you can do this : 1. the "direct" way and 2. the customized way.

## The "direct" way 
- verify your local settings are aligned with the pre-requisites to run this container, grosso modo
make sure docker is installed, of course !
{{< hint info >}}  
You have to have about 4 GB of free space 
{{< /hint >}}


- pull image from docker hub 
https://hub.docker.com/r/jupyter/pyspark-notebook

- run the downloaded image as a container - and do not forget to specify the volume to be used (to save and move the notebooks in and out the container) 
For more on the run command you can check the documentation
- you can now access Jupyter notebook via the token provided by the image
- now, your environment is ready for work !


Note that if you install docker desktop, you can start/access/stop your container directly from the containers tab.

## The customized way
The pyspark Jupyter image can also be used as a base image to build your own containers and run the environment that works best for your project.

You can check the Jupyter Docker stacks to select the image you might be interested in.

- write your Dockerfile
- build your container
- run your environement

I've been working with a customized image for quite some time now. You can find it on [my github](https://github.com/Non-NeutralZero/pyspark-jupyter-env).
