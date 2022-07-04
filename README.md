# Launchctl-Py

🚀 Quickly create _super basic_ background services (i.e., launchctl agents) for macOS in Python.

[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.7-blue.svg?logo=python)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg?logo=python)](https://www.python.org/dev/peps/pep-0008/) ![platform](https://img.shields.io/badge/Platform-macOS-green.svg?logo=apple)


## Requirements
- 🐍 [python>=3.7](https://www.python.org/downloads/)

## ⬇️ Installation

```sh
pip install launchctl-py
```

## ⌨️ Usage

```
usage: lpy [-h] [-c] [-s]

optional arguments:
  -h, --help    show this help message and exit
  -c, --create  Create a new launchctl agent
  -s, --status  Get the status of the agents you created
```


## 💡 Misc.

Optional: if you want the domain name of your agents to be something other than `local` (default), run:
```sh
launchctl setenv DEFAULT_DOMAIN "ReplaceMe"
echo 'setenv DEFAULT_DOMAIN ReplaceMe' >> ~/.conf.launchd
```

---

...\
**👷 Additional features are under development...**\
...
