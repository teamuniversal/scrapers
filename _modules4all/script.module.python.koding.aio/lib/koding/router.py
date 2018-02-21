# -*- coding: utf-8 -*-

"""
    router.py --- functions implementing a routing function
    Copyright (C) 2017, Midraal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import directory
import tutorials
import video
import xbmc
import xbmcgui

dialog       = xbmcgui.Dialog()
HOME         = xbmc.translatePath('special://home')
master_modes = {
# Required for certain koding functions to work
    "populate_list":    {'function': directory.Populate_List, 'args': ["url","start_point","end_point","separator","skip"]},
    "play_video":       {'function': video.Play_Video, 'args': ["url"]},
    "show_tutorial":    {'function': tutorials.Show_Tutorial, 'args': ["url"]},
    "tutorials":        {'function': tutorials.Grab_Tutorials, 'args': []},
}
#----------------------------------------------------------------
# TUTORIAL #
def route(mode, args=[]):
    """
Use this to set a function in your master_modes dictionary.
This is to be used for Add_Dir() items, see the example below.

CODE: route(mode, [args])

AVAILABLE PARAMS:
            
    (*) mode  -  This must be set, it needs to be a custom string.
    This is the string you'd use in your Add_Dir command to call
    the function.

    args  -  This is optional but if the function you're calling
    requires extra paramaters you can add them in here. Just add them
    as a list of strings. Example: args=['name','artwork','description']

BELOW IS AN EXAMPLE OF HOW TO CALL THE CODE IN YOUR MAIN ADDON PY FILE:

@route(mode="test", args=["name","description"])
def Test_Function(name,description):
    dialog.ok('This is a test function', name, description')

koding.Add_Dir(name='Test Dialog', url={"name":"My Test Function", "description" : "Its ALIVE!!!"}, mode='test')
koding.run()
~"""
    if mode not in master_modes:

        def _route(function):
            master_modes[mode] = {
                'function': function,
                'args': args
            }
            return function
        return _route
    else:
        dialog.ok('DUPLICATE MODE',
                            'The following mode already exists:',
                            '[COLOR=dodgerblue]%s[/COLOR]' % mode)
#----------------------------------------------------------------
# TUTORIAL #
def Run(default="main"):
    """
This needs to be called at the bottom of your code in the main default.py

This checks the modes called in Add_Dir and does all the clever stuff
in the background which assigns those modes to functions and sends
through the various params.

Just after this command you need to make
sure you set the endOfDirectory (as shown below).


CODE: run([default])
xbmcplugin.endOfDirectory(int(sys.argv[1]))

AVAILABLE PARAMS:
    
    default  -  This is the default mode you want the add-on to open
    into, it's set as "main" by default. If you have a different mode
    name you want to open into just edit accordingly.
~"""
    import urllib
    import urlparse
    import sys
    from __init__    import DEBUG
    from guitools    import Text_Box
    from systemtools import Last_Error

    params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
    mode = params.get("mode", default)
    if mode in master_modes:
        evaled_args = []

    # Grab the url and split up into a dictionary of args
        try:
            main_url = params["url"]
        # Convert back from special to physical path - useful for community shares
            if urllib.unquote_plus("special://home/") in main_url:
                main_url = main_url.replace('special://home/',HOME)
        except:
            main_url = ''
        try:
            my_args = eval(main_url)
        except:
            my_args = {"url":main_url}

        for arg in master_modes[mode]["args"]:
            try:
                evaled_args.append(my_args[arg])
            except:
                if DEBUG == 'true':
                    dialog.ok('ERROR IN CODE','Your Add_Dir function is expecting the [COLOR=gold][B]%s[/B][/COLOR] paramater to be sent through. This does not exist, please check your Add_Dir function.'%arg)
                    xbmc.log(Last_Error(),2)
                return
        try:
            master_modes[mode]["function"](*evaled_args)
        except:
            if DEBUG == 'true':
                Text_Box('ERROR IN CODE', Last_Error())
                xbmc.log(Last_Error(),2)
            else:
                pass
    else:
        dialog.ok('MODE DOES NOT EXIST',
                            'The following mode does not exist in your\
                            master_modes dictionary:',
                            '[COLOR=dodgerblue]%s[/COLOR]' % mode)
