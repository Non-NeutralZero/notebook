+++
title = ""
description = "VS Code Configuration & Set-up"
tags = [
    "git",
    "ssh",
    "development",
]
date = "2023-11-17"
categories = [
    "Development",
    "Tutorials",
]
menu = "main"
parent = "tutorials"
+++

# Configuration
## Remote SSH 
```shell
Host machine
    Hostname machine.com
    User user_name
    IdentityFile path/to/ssh/key
```

## Remote SSH - SSH Tunnel
```shell
Host tunnel_machine
    Hostname machine.com
    User user_name
    IdentityFile path/to/ssh/key

Host machine_after_tunnel
    Hostname machine_after_tunnel.com
    User user_name
    IdentityFile path/to/ssh/key
    ForwardAgent yes
    ProxyJump tunnel_machine
```

# Uses
## Extensions
- Remote Explorer
- Docker
