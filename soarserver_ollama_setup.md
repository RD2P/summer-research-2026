# Ollama Setup Guide

This guide details how to manually install and run Ollama on the servers `soarserver-1` or `soarserver-2` and access it from a local machine.

Due to the lack of `sudo` privileges on the servers, a standard installation is not possible. We will use an SSH tunnel to forward the Ollama port from the server to your local machine for access.

## On `soarserver`

1.  **Manually install Ollama**
 
    Follow the official documentation at [https://docs.ollama.com/linux](https://docs.ollama.com/linux).
    
    Use the following command to download and extract Ollama to a specific directory
    ````shell
    curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.zst | tar x --zstd -C /u2/users/<nsid>/ollama
    ````
    You can choose where to extract ollama. Here I chose `/u2/users/<nsid>/ollama`.
    After extraction there should be `bin` and `lib` in this directory. Ollama can be invoked with `/u2/users/<nsid>/ollama/bin/ollama` (you'll add this to PATH in the next step).

2.  **Configure Environment Variables**
 
    Add the following lines to `~/dot.bashrc` file - so you don't need to set the environment variables for each shell session:
    ````shell
    export OLLAMA_HOST=localhost:4378 # choose a port no one is using
    export OLLAMA_MODELS=/u2/users/<nsid/models # or wherever you want to store your models in the server
    export PATH="/u2/users/<nsid>/ollama/bin:$PATH" # wherever you extracted the binary
    ````
    
    Source `dot.bashrc` or open a new terminal session for the changes to take effect.

3.  **Start the Ollama Server**

    Start a `tmux` session to run the server as a long-running process.

    Inside the `tmux` session, start ollama:
    ````shell
    ollama serve
    ````
    Now it's safe to detach from tmux `ctl+b d` and go back to your local machine. With ollama running, we can access this service through ssh.

## On Local Machine

1. **Connect to ollama server***

    ````shell
    ssh -L 4378:localhost:4378 <user>@<host>
    ````

    The ollama server can now be accessed locally on localhost:4378.
    Check to see "Ollama is running".
    In the next step you can configure ssh to automatically bind the ports when connecting to the ollama service.

2.  **Configure SSH**

    Add the following to `~/.ssh/config` file to simplify connecting and forwarding the port:
    ````ssh_config
    Host ollama-server
        HostName soarserver-1 # or soarserver-2
        User <nsid>
        LocalForward 4378 localhost:4378
    ````

3.  **Connect and Start Tunnel**

    Run the following command to connect to the server. This will also automatically create the SSH tunnel defined in your config.
    ````shell
    ssh ollama-server
    ````
    Ollama will now be accessible on your local machine at `localhost:4378`.
    