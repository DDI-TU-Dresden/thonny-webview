# Webview Plugin for the thonny IDE

## Warning

You can only start the webview once. If you try to start it another time, thonny and the webview will crash. This is especially annoying because unsaved work will be gone and cannot be recovered.

## Installation

- Install qt for your operating system. You can find information about that [here](https://pywebview.flowrl.com/guide/installation.html#dependencies).

- Install the python dependencies

```bash
pip install -r requirements.txt --user
```

## Start the plugin with thonny

```bash
cd /path/to/thonny/
PYTHONPATH=/path/to/thonny-webview/ python -m thonny
```