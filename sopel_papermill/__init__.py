# coding=utf8
"""sopel-papermill

A plugin to run IPython/Jupyter notebooks from IRC by integrating Papermill with Sopel.
"""
from __future__ import unicode_literals, absolute_import, division, print_function
from sopel import module
from sopel.config.types import StaticSection, ValidatedAttribute, BooleanAttribute
import papermill as pm
import json

class PapermillSection(StaticSection):
    nb_dir = ValidatedAttribute('nb_dir', str)
    prefix = ValidatedAttribute('prefix', str)
    show_last_line = BooleanAttribute('show_last_line')

def setup(bot):
    bot.config.define_section('papermill', PapermillSection)

def configure(config):
    config.define_section('papermill', PapermillSection, validate=False)
    config.papermill.configure_setting('nb_dir', 'What is the path to the notebooks directory?', default='/home/sopel/notebooks/')
    config.papermill.configure_setting('prefix', 'What prefix to use for the notebook output (leave blank to overwrite)?', default='')
    config.papermill.configure_setting('show_last_line', 'Should Sopel print the last line after executing a notebook?', default=False)

def paths(bot, nb_name):
    """Returns the paths of notebook to execute and to write."""
    nb_dir = bot.config.papermill.nb_dir #Notebook directory (from config)
    nb_dir = nb_dir if nb_dir.endswith('/') else nb_dir+'/' #append '/' if missing
    path_in = nb_dir + nb_name
    path_out = nb_dir + bot.config.papermill.prefix + nb_name
    return(path_in, path_out)

def cell_output(path, i_cell):
    """Returns the output of cell i_cell of notebook found at path."""
    with open(path, 'r') as f:
        nb_json = json.loads(f.read())
        outputs = nb_json['cells'][i_cell]['outputs']
        if outputs != []:
            return(outputs[0]['text'][0])
        else:
            return('No output.')

@module.commands('papermill-execute', 'pm')
@module.example('.pm TestNotebook.ipynb')
def papermill_execute(bot, trigger):
    """Execute the IPython/Jupyter notebook mentionned. It has to be in the directory defined in the config."""
    nb_name = trigger.group(2).split(' ')[0]
    if not nb_name.endswith(".ipynb") or len(trigger.group(2).split(' ')) != 1:
        bot.say('Please give a valid IPython/Jupyter notebook name.')
        return
    bot.say('Executing '+ nb_name + '...')
    path_in, path_out = paths(bot, nb_name)
    try :
        pm.execute_notebook(path_in, path_out)
    except FileNotFoundError:
        bot.reply('That notebook does not exist.')
        return
    bot.reply('Notebook ' + nb_name + ' execution ok.')
    if bot.config.papermill.show_last_line :
        bot.say('Last cell output:')
        bot.say(cell_output(path_in, -1))
    
@module.commands('papermill-show', 'pm-s')
@module.example('.pm-s TestNotebook.ipynb 2')
def papermill_show(bot, trigger):
    """Show the output of a cell from a IPython/Jupyter notebook."""
    msg = trigger.group(2).split(' ')
    if len(msg) == 2 and msg[0].endswith(".ipynb") and msg[1].isdigit():
        nb_name, i_cell = msg[0], int(msg[1])
    elif len(msg) == 1 and msg[0].endswith(".ipynb"):
        nb_name, i_cell = msg[0], -1
    else :
        bot.say('Please give a IPython/Jupyter notebook name, followed by a cell number (optionnal).')
        return
    path_in, path_out = paths(bot, nb_name)
    bot.say('Cell n°'+str(i_cell)+' output of notebook '+nb_name+' :')
    bot.say(cell_output(path_in, i_cell))
