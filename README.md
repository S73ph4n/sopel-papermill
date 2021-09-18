# sopel-papermill

A plugin to run IPython/Jupyter notebooks from IRC by integrating Papermill with Sopel (IRC bot).
Allows you to execute notebooks from IRC and look at the result.

# Installation

```pip install git+https://github.com/S73ph4n/sopel-papermill```

# Configuration

Run ```sopel configure```. For more info on this, see the [Sopel documentation](https://sopel.chat/usage/installing/).

Among other things, you'll have to say in which directory this plugin should look for notebooks.

# Usage

Work like any other [Sopel](https://sopel.chat/) plugin. See the Sopel docs.

After [starting/configurating Sopel](https://sopel.chat/usage/installing/), you can execute a notebook by typing ```.pm-e NotebookName.ipynb``` in any channel where your Sopel bot is present.

For help, type ```.help```.
