# CampNet Utility

A lightweight command-line utility for logging in to and logging out of the **BITS Goa CampNet** network on Linux.

Instead of opening the CampNet login webpage and entering your credentials manually, this utility lets you authenticate directly from the terminal:

```bash
campnet login
```

and log out with:

```bash
campnet logout
```

> **Disclaimer:** This is an unofficial, community-made utility. It is not affiliated with, endorsed by, or officially supported by BITS Pilani, BITS Goa, CampNet, or the developers of the CampNet captive portal.

---

## Features

* Login to BITS Goa CampNet from the command line
* Logout from CampNet from the command line
* No browser interaction required
* Credentials stored separately from the source code
* Simple Python implementation
* Uses the CampNet portal's HTTP login/logout interface

---

## Requirements

You will need:

* Linux
* Python 3
* Access to the BITS Goa network
* A valid BITS Goa CampNet username and password

The utility uses the Python [`requests`](https://requests.readthedocs.io/) package.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/campnet-utility.git
cd campnet-utility
```

Replace `<your-username>` with the GitHub username that owns the repository, or use the URL of your fork.

---

## 2. Create a virtual environment

A virtual environment keeps the project's Python dependencies separate from your system Python installation.

Run:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your terminal should now show `(.venv)` at the beginning of the prompt.

For example:

```text
(.venv) user@computer:~/campnet-utility$
```

---

## 3. Install the dependency

With the virtual environment activated:

```bash
python -m pip install requests
```

---

# Configuration

Before using the utility, you need to provide your CampNet credentials.

Your credentials are stored locally in a file named:

```text
credentials.txt
```

This file is intentionally excluded from Git and should never be uploaded to GitHub.

## 1. Create `credentials.txt`

From the project directory:

```bash
nano credentials.txt
```

Enter your credentials on **two separate lines**:

```text
YOUR_USERNAME
YOUR_PASSWORD
```

For example:

```text
f20240477
your-password-here
```

Do not include labels such as:

```text
username=f20240477
password=your-password-here
```

Do not add quotation marks.

---

## 2. Protect your credentials

Because `credentials.txt` contains your password, restrict access to your Linux user:

```bash
chmod 600 credentials.txt
```

Check the permissions:

```bash
ls -l credentials.txt
```

You should see something similar to:

```text
-rw------- 1 user user ... credentials.txt
```

This allows your user to read and modify the file while preventing other users from accessing it.

The Python program can still read the file because it runs as your user.

---

## 3. Make sure Git does not track your credentials

The repository's `.gitignore` should contain:

```text
credentials.txt
.venv/
__pycache__/
```

Check what Git is tracking:

```bash
git ls-files
```

`credentials.txt` and `.venv/` should not appear in the output.

### Important

Never commit your actual CampNet password to a public GitHub repository.

If a password is accidentally committed, deleting the file afterward does not remove it from Git history. Change the password immediately and remove the exposed secret from the repository history.

---

# Usage

Once `credentials.txt` has been configured, the program can be run directly with Python.

## Login

```bash
python campnet.py login
```

A successful login displays:

```text
Login successful.
```

If the login fails, the message returned by CampNet is displayed.

For example:

```text
Login failed.
Reason: Login failed. Invalid user name/password.
```

---

## Logout

```bash
python campnet.py logout
```

A successful logout displays:

```text
Logout successful.
```

---

# Optional: Use `campnet` as a Command

You can create a small launcher so that you can run:

```bash
campnet login
```

and:

```bash
campnet logout
```

from any directory without manually activating the virtual environment.

## 1. Create the local executable directory

```bash
mkdir -p ~/.local/bin
```

## 2. Create the launcher

Create the file:

```bash
nano ~/.local/bin/campnet
```

Add:

```bash
#!/bin/bash

PROJECT_DIR="$HOME/Documents/Projects/campnet"

exec "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/campnet.py" "$@"
```

If you cloned the repository somewhere else, change `PROJECT_DIR` to the location of your local repository.

For example:

```bash
PROJECT_DIR="$HOME/code/campnet"
```

## 3. Make the launcher executable

```bash
chmod +x ~/.local/bin/campnet
```

## 4. Make sure `~/.local/bin` is in your PATH

Check:

```bash
echo "$PATH"
```

You can also check whether the command is available:

```bash
which campnet
```

If `~/.local/bin` is not in your PATH, add it to your shell configuration.

For Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For Zsh:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

You can now use:

```bash
campnet login
```

or:

```bash
campnet logout
```

The virtual environment does not need to be manually activated when using the launcher.

---

# How It Works

The CampNet web portal provides an HTTP interface for authentication.

This utility reproduces the login and logout requests made by the web portal.

## Login

The login request is sent using HTTP `POST` to:

```text
https://campnet.bits-goa.ac.in:8090/login.xml
```

The request contains:

```text
mode=191
username=<username>
password=<password>
a=<current timestamp in milliseconds>
producttype=0
```

The `a` parameter is generated using the current Unix timestamp in milliseconds.

CampNet returns an XML response. A successful login contains:

```xml
<status>LIVE</status>
```

The utility parses this response and reports whether the login was successful.

## Logout

The logout request is sent using HTTP `POST` to:

```text
https://campnet.bits-goa.ac.in:8090/logout.xml
```

The request contains:

```text
mode=193
username=<username>
a=<current timestamp in milliseconds>
producttype=0
```

The password is not required for the logout request.

The utility examines CampNet's response to determine whether the user has been signed out.

---

# Project Structure

The project directory looks like this:

```text
campnet/
├── .gitignore
├── .venv/
├── campnet.py
├── credentials.txt
└── README.md
```

| File              | Purpose                                                 |
| ----------------- | ------------------------------------------------------- |
| `campnet.py`      | Main Python program                                     |
| `credentials.txt` | Local CampNet username and password                     |
| `.gitignore`      | Prevents sensitive and local files from being committed |
| `.venv/`          | Local Python virtual environment                        |
| `README.md`       | Project documentation                                   |

`credentials.txt` and `.venv/` are local files and should not be part of the public repository.

---

# Development

Clone the repository and enter the project directory:

```bash
git clone https://github.com/<your-username>/campnet-utility.git
cd campnet-utility
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependency:

```bash
python -m pip install requests
```

Run the program directly:

```bash
python campnet.py login
```

or:

```bash
python campnet.py logout
```

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'requests'`

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then install the dependency:

```bash
python -m pip install requests
```

---

## `credentials.txt` not found

Make sure `credentials.txt` exists in the same directory as `campnet.py`:

```bash
ls -l credentials.txt
```

---

## Login fails

Check that:

* You are connected to the BITS Goa network.
* Your CampNet username is correct.
* Your CampNet password is correct.
* The CampNet service is currently available.

You can also test the CampNet web portal manually:

```text
https://campnet.bits-goa.ac.in:8090/httpclient.html
```

If login also fails through the browser, the problem is likely with the account or CampNet service rather than this utility.

---

## `campnet: command not found`

Check that the launcher exists:

```bash
ls -l ~/.local/bin/campnet
```

Make sure it is executable:

```bash
chmod +x ~/.local/bin/campnet
```

Check your PATH:

```bash
echo "$PATH"
```

You can also test the program directly:

```bash
python campnet.py login
```

---

# Security

The utility requires your CampNet credentials to authenticate with the campus network.

Credentials are stored locally in `credentials.txt` rather than in the source code.

Keep the following private:

```text
credentials.txt
```

Do not:

* Commit `credentials.txt` to Git
* Publish your CampNet password
* Share your credentials with other users
* Include credentials in screenshots, bug reports, or issues

If your password is accidentally exposed, change it immediately.

---

# Limitations

This utility currently performs login and logout only when explicitly requested.

It does not currently:

* Automatically detect when CampNet authentication expires
* Automatically reconnect after Wi-Fi or network changes
* Run continuously in the background
* Implement its own CampNet session-monitoring mechanism
* Manage multiple CampNet accounts

After login, CampNet's own session management is responsible for maintaining the authenticated session.

---

# Disclaimer

This is an unofficial third-party utility.

It is not affiliated with, endorsed by, or officially supported by:

* BITS Pilani
* BITS Goa
* CampNet
* The CampNet software vendor

The software is provided as-is for educational and personal use.

Users are responsible for complying with applicable institutional, network, and information-security policies.

---

# License

This project is licensed under the [MIT License](LICENSE).
