# Fianance Brain

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)

## Overview

Current Version: **0.0.1**

## Features

## Setup

**Setup - PyPi Install:**

To **install** the library, run the following command from the terminal.

```console
pip install finance-brain
```

**Setup - PyPi Upgrade:**

To **upgrade** the library, run the following command from the terminal.

```console
pip install --upgrade finance-brain
```

**Setup - Local Install:**

If you are planning to make modifications to this project or you would like to access it
before it has been indexed on `PyPi`. I would recommend you either install this project
in `editable` mode or do a `local install`. For those of you, who want to make modifications
to this project. I would recommend you install the library in `editable` mode.

If you want to install the library in `editable` mode, make sure to run the `setup.py`
file, so you can install any dependencies you may need. To run the `setup.py` file,
run the following command in your terminal.

```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

## Usage

Here is a simple example of using the `finbrain` library to load a directory of files.

```python
from configparser import ConfigParser

from finbrain.client import FinBrainAssistant

# Path to the configuration file.
config = ConfigParser()
config.read('configs/config.ini')
api_key = config['openai_keys']['openai_secret_key']

# Initialize the FinBrainAssistant object.
assistant = FinBrainAssistant(
    api_key=api_key,
    save_state=True,
    state_file="state.json"
)

# Grab the Save State attribute.
print(assistant.save_state)

# Grab the State File attribute.
print(assistant.state_file)

# Grab the State attribute.
print(assistant.state)

# Add some files to the assistant.
assistant.files.add(file_path="sec_docs/13567242.html")
```
