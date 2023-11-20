+++
title = "VS Code Configuration & Set-up"
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
```powershell
Host machine
    Hostname machine.com
    User user_name
    IdentityFile path/to/ssh/key
```

## Remote SSH - SSH Tunnel
```powershell
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

# PC Configuration
Authorize your local machine to connect to remote machine.

```powershell
$USER_AT_HOST="your-user-name-on-host@hostname"
$PUBKEYPATH="$HOME\.ssh\id_ed25519.pub"

$pubKey=(Get-Content "$PUBKEYPATH" | Out-String); ssh "$USER_AT_HOST" "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '${pubKey}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```
Verify that the ***authorized_keys*** file in the ***.ssh*** folder for your remote user on the SSH host is owned by you and no other user has permission to access it.

# Uses
## Extensions
- Remote Explorer
- Docker
