

# Analyse KI-basierter Scheduler

This repository contains the implementation of my bachelor thesis. This is an implementation of an AI scheduler. The implementation is based on the work of Pierre Tassel, Martin Gebser and Konstantin Schekotihin, so this is a fork of this [repository](https://github.com/prosysscience/RL-Job-Shop-Scheduling).

## Getting started

Build the Dockerfile using

``` bin

docker build . -t ddoge/rl-jobshop

```

Then you can start the container using the following command, just be sure to replace <path_to_this_repository> with the path to this repository.

``` bin

docker run --name rl-jobshop --gpus all -v <path_to_this_repository>:jobshop/ -it ddoge/rl-jobshop

```

  
When you exit the container, you might need to start it again:

``` bin

docker start rl-jobshop

```

  

And connect to it again:

``` bin

docker exec -it rl-jobshop /bin/bash

```

When you are inside the container, you can start main.py using:
``` bin

python3.7 main.py

```

 Important:
 Currently, the path to the instance has to be set manually in main.py (line 78)
 Your instance must follow [Taillard's specification](http://jobshop.jjvh.nl/explanation.php#taillard_def).

  

Project Organization

------------
```
  
├── Dockerfile <-  The Dockerfile used for the container.
├── README.md <- The top-level README for developers using this project.
└── JSS
    ├── dispatching_rules/ <- Contains the code to run the disptaching rule FIFO and MWTR.
    ├── instances/ <- All Taillard's instances + 5 Demirkol instances.
    ├── randomLoop/ <- A random loop with action mask, usefull to debug environment and
    | to check if our agent learn.
    ├── CP.py <- OR-Tool's cp model for the JSS problem.
    ├── CustomCallbacks.py <- A special RLLib's callback used to save the best solution found.
    ├── default_config.py <- default config used for the disptaching rules.
    ├── env_wrapper.py <- Envrionment wrapper to save the action's of the best solution found
    ├── main.py <- PPO approach, the main file to call to reproduce our approach.
    └── models.py <- Tensorflow model who mask logits of illegal actions.

```


## License

MIT License