# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by whufclee (info@totalrevolution.tv)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# IMPORTANT: If you choose to use the special noobsandnerds features which hook into their server
# please make sure you give approptiate credit in your add-on description (noobsandnerds.com)
# 
# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. If you're found to be in breach of this license
# then any affected add-ons will be blacklisted and will not be able to work on the same system
# as any other add-ons which use this code. Thank you for your cooperation.

import os
import re
import shutil
import sys
import time
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import inspect
try:
    import simplejson as json
except:
    import json

from addons         import *
from android        import *
from database       import *
from directory      import *
from filetools      import *
from guitools       import *
from router         import *
from systemtools    import *
from tutorials      import *
from video          import *
from vartools       import *
from web            import *

def converthex(url):
    """ internal command ~"""
    import binascii
    return binascii.unhexlify(url)

try:
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
except:
    ADDON_ID = Caller()

AddonVersion = xbmcaddon.Addon(id=ADDON_ID).getAddonInfo('version')

try:
    if sys.argv[1] == converthex('7465737466696c65'):
        ADDON_ID  =  ADDON_ID+'.test'
except:
    pass

if ADDON_ID.endswith(converthex('2e74657374')):
    ORIG_ID      =  ADDON_ID[:-5]
else:
    ORIG_ID      = ADDON_ID

TestID           =  ADDON_ID
if not ADDON_ID.endswith(converthex('2e74657374')):
    TestID       =  ADDON_ID+converthex('2e74657374')

MODULE_ID        =  'script.module.python.koding.aio'
ADDON            =  xbmcaddon.Addon(id=ADDON_ID)
THIS_MODULE      =  xbmcaddon.Addon(id=MODULE_ID)
USE_TEST         =  Addon_Setting(addon_id=ADDON_ID,setting=converthex('74657374766572'))
USERDATA         =  xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c65'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,converthex('6164646f6e5f64617461')))
ADDONS           =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e73'))
PACKAGES         =  os.path.join(ADDONS,converthex('7061636b61676573'))
UPDATE_ICON      =  os.path.join(ADDONS,MODULE_ID,converthex('7265736f7572636573'),converthex('7570646174652e706e67'))
COOKIE           =  os.path.join(ADDON_DATA,ORIG_ID,converthex('636f6f6b696573'),converthex('74656d70'))
RUNCODE          =  os.path.join(ADDON_DATA,ORIG_ID,converthex('636f6f6b696573'),converthex('6b6565706d65'))
DOWNLOAD_DST     =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e732f7061636b616765732f6370'))
LOGIN            =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('6c6f67696e'))
FORUM            =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('666f72756d'))
USERNAME         =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('757365726e616d65')).replace(' ','%20') if LOGIN == 'true' else ''
PASSWORD         =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('70617373776f7264')) if LOGIN == 'true' else ''
DEBUG            =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('6465627567'))
INSTALL_REPOS    =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('696e7374616c6c7265706f73'))
INSTALL_ADDONS   =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('696e7374616c6c6164646f6e73'))
SILENT_MODE      =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('73696c656e74'))
KODI_VER         =  int(float(xbmc.getInfoLabel("System.BuildVersion")[:2]))

dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()

launch           =  'launch.py'
main_counter     =  0

downloads        =  []
stddownloads     =  []
nologindownloads =  []

usernamelen      =  len(USERNAME)
if usernamelen > 14:
    usernamelen = 15

if FORUM == converthex('556e6f6666696369616c204b6f646920537570706f7274'):
    FORUM = 'k'
if FORUM == converthex('436f6d6d756e697479204275696c647320537570706f7274'):
    FORUM = 'c'

if not os.path.exists(os.path.join(ADDON_DATA,ORIG_ID,converthex('636f6f6b696573'))):
    os.makedirs(os.path.join(ADDON_DATA,ORIG_ID,converthex('636f6f6b696573')))
#----------------------------------------------------------------
# TUTORIAL #
def dolog(string, my_debug=False, line_info=True):
    """
Print to the Kodi log but only if debugging is enabled in settings.xml

CODE: koding.dolog(string, [my_debug])

AVAILABLE PARAMS:

    (*) string  -  This is your text you want printed to log.

    my_debug  -  This is optional, if you set this to True you will print
    to the log regardless of what the debug setting is set at in add-on settings.

    line_info - By default this is set to True and will show the line number where
    the dolog command was called from along with the filepath it was called from.

EXAMPLE CODE:
koding.dolog(string='Quick test to see if this gets printed to the log', my_debug=True, line_info=True)
dialog.ok('[COLOR gold]CHECK LOGFILE 1[/COLOR]','If you check your log file you should be able to see a new test line we printed \
and immediately below that should be details of where it was called from.')
koding.dolog(string='This one should print without the line and file info', my_debug=True, line_info=False)
dialog.ok('[COLOR gold]CHECK LOGFILE 2[/COLOR]','If you check your log file again you should now be able to see a new line printed \
but without the file/line details.')
~"""
    import xbmc
    if DEBUG == 'true' or my_debug:
        xbmc.log('### %s (%s) : %s'%(ADDON_ID,AddonVersion,string), level=xbmc.LOGNOTICE)
    if line_info:
        from inspect import getframeinfo, stack
        caller = getframeinfo(stack()[1][0])
        xbmc.log('^ Line No. %s  |  File: %s'%(caller.lineno,caller.filename),level=xbmc.LOGNOTICE)
#----------------------------------------------------------------
def Check_Addons(addons):
    """ internal command ~"""
    if ',' in addons and INSTALL_ADDONS != '0':
        addon_array = addons.split(',')
        for addon in addon_array:
            Main('addoninstall|id:%s~version:%s~repo:%s~silent:%s~installtype:%s' % (addon,KODI_VER,INSTALL_REPOS,SILENT_MODE,INSTALL_ADDONS))
#----------------------------------------------------------------
def Check_Cookie(mode = ''):
    """ internal command ~"""
    if not os.path.exists(COOKIE):
        cookie_folder = os.path.join(ADDON_DATA,ORIG_ID,converthex('636f6f6b696573'))
        if not os.path.exists(cookie_folder):
            os.makedirs(cookie_folder)
        writefile = open(COOKIE,'w')
        writefile.close()

    readfile    = open(COOKIE,'r')
    content     = Encryption('d',readfile.read())
    readfile.close()

    loginmatch  = re.compile('w="(.+?)"').findall(content)
    basematch   = re.compile('b="(.+?)"').findall(content)
    datematch   = re.compile('d="(.+?)"').findall(content)
    addonsmatch = re.compile('a="(.+?)"').findall(content)
    basedomain  = basematch[0] if (len(basematch) > 0) else 'http://noobsandnerds.com'
    date        = datematch[0] if (len(datematch) > 0) else '0'
    welcometext = loginmatch[0] if (len(loginmatch) > 0) else ''
    addons      = addonsmatch[0] if (len(addonsmatch) > 0) else ''

    returns = ['register','PASSWORD','restricted','reactivate']
    LOGIN            =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('6c6f67696e'))
    USERNAME         =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('757365726e616d65')) if LOGIN == 'true' else ''
    PASSWORD         =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('70617373776f7264')) if LOGIN == 'true' else ''

    if welcometext not in returns and welcometext != USERNAME:
        run_cookie = True
    elif LOGIN == 'true' and welcometext == '':
        User_Info()
        return
    elif LOGIN == 'true' and welcometext != USERNAME:
        run_cookie = True
    elif LOGIN == 'false' and welcometext == USERNAME:
        run_cookie = True
    else:
        run_cookie = False

    if run_cookie:
        try:
            shutil.rmtree(COOKIE)
        except:
            pass

    if mode == 'base':
        if int(date)+1000000 < int(Timestamp()):
            User_Info('cookie_check')
        else:
            return basedomain

    else:
        if int(date)+1000000 < int(Timestamp()) or run_cookie:
            return False
        else:
            return True
#----------------------------------------------------------------
def Check_File_Date(url, datefile, localdate, dst):
    """ internal command ~"""
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)

        if int(last_modified) > int(localdate):
            dp.create(THIS_MODULE.getLocalizedString(30979),THIS_MODULE.getLocalizedString(30807))
            download.download(url,dst,dp)
            if converthex('74737463686b') in url:
                extract.all(dst,ADDONS,dp)
            else:
                extract.all(dst, ADDON_DATA, dp)
            writefile = open(datefile, 'w+')
            writefile.write(last_modified)
            writefile.close()
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except:
            pass
    except:
        pass
#----------------------------------------------------------------
def Check_Updates(url, datefile, dst):
    """ internal command ~"""
    if os.path.exists(datefile):
        readfile  = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)
#----------------------------------------------------------------    
def Encryption(mode='', message=''):
    """ internal command ~"""
    finaltext   = ''
    translated  = ''
    finalstring = ''
    offset      = 8
    if len(USERNAME) > 0 and LOGIN == 'true':
        offset = usernamelen
    if mode == 'e':
        for symbol in message:
            num = ord(symbol)+offset
            if len(str(num))==2:
                num = '0'+str(num)
            finalstring = str(finalstring)+str(num)
        return finalstring+finaltext

    else:
        messagearray = [message[i:i+3] for i in range(0, len(message), 3)]
        for item in messagearray:
            item = int(item)-offset
            item = str(unichr(item))
            finaltext = finaltext+item
        return finaltext
#----------------------------------------------------------------
def Get_IP():
    """ internal command ~"""
    link          = Open_URL(converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f6c6f67696e5f636f6f6b69652e706870'), 'post').replace('\r','').replace('\n','').replace('\t','')
    link          = Encryption(mode='d',message=link)
    ipmatch       = re.compile('i="(.+?)"').findall(link)
    ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else ''
    return ipfinal
#----------------------------------------------------------------
# TUTORIAL #
def Main(url='', post_type = 'get'):
    """
If you have web pages of your own then you can hook into them using
koding.Main(url) which will pull the return from the URL and attempt
to execute that code.

WARNING: Running code directly from a server is generally discouraged,
any add-ons using such code will certainly not be accepted on the official
kodi.tv forum as it is strictly against their rules. By having add-ons
capable of self updating and bypassing their highly vetted repository
system it would be a security breach for the foundation so their stance on
this is completely understandable. For third party development you are
presumably in control of your own repository so it really shouldn't make
much difference, however do note that running code directly from a server
is slower than running locally and you'll find it's discouraged by a number
of devs. Can certainly be useful for quick dynamic updates which need to
take place though.

CODE:   koding.Main(url,[post_type])
post_type is optional, by default it's set as 'get'

AVAILABLE VALUES:

    'get'  -  This is already the default so no real need to add this but this uses a standard query string
    
    'post' -  This will convert the query string into a post

EXAMPLE CODE:
koding.Main('http://noobsandnerds.com?id=test', post_type='get')~"""
    try:
        url = converthex(url)
    except:
        pass

    if url == 'run':
        runcode_date = 0
        if os.path.exists(RUNCODE):
            runcode_date = os.path.getmtime(RUNCODE)
            runcode_date = time.localtime(runcode_date)
            runcode_date = time.strftime('%Y%m%d%H%M%S', runcode_date)
        if int(runcode_date)+1000000 < int(Timestamp()):
            run_code = Open_URL(url, post_type)
            if run_code:
                writefile = open(RUNCODE, 'w')
                writefile.write(run_code)
                writefile.close()
        else:
            readfile = open(RUNCODE,'r')
            run_code = readfile.read()
            readfile.close()

    else:
        run_code = Open_URL(url=url, post_type=post_type)

    if run_code:
        try:
            my_code = Encryption('d',run_code)
            dolog('MY CODE: %s'%my_code)
            exec(my_code)
            dolog(converthex('232323205375636365737366756c6c792072756e20636f646520696e20656e6372797074696f6e206d6f6465'))
        except:
            dolog(converthex('232323204661696c656420746f2072756e20636f64652c20617474656d7074696e6720746f20757365207374616e64617264206d6f6465'))
            try:
                exec(run_code)
                dolog(converthex('232323205375636365737366756c6c792072756e20636f6465'))
            except:
                dolog(Last_Error())
                try:
                    exec(converthex(run_code))
                    dolog(converthex('232323205375636365737366756c6c792072756e20636f6465'))
                except:
                    if DEBUG == 'true':
                        dialog.ok(THIS_MODULE.getLocalizedString(30980),THIS_MODULE.getLocalizedString(30981)%ADDON_ID)
    else:
        dolog(run_code)
#-----------------------------------------------------------------------------
# TUTORIAL #
def User_Info(mode = ''):
    """
THIS MUST BE CALLED AT START OF CODE IF USING NOOBSANDNERDS FRAMEWORK.

This is only required for developers who want to use the special
noobsandnerds features, this will create a cookie file containing cached
details. It's important you do this somewhere at the start of your code as
it will initialise your variables on first run.~"""
    global main_counter

    if not Check_Cookie():
        LOGIN       =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('6c6f67696e'))
        USERNAME    =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('757365726e616d65')).replace(' ','%20') if LOGIN == 'true' else ''
        PASSWORD    =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('70617373776f7264')) if LOGIN == 'true' else ''
        link        =  Open_URL('', 'post').replace('\r','').replace('\n','').replace('\t','')
        if len(link) < 3:
            dialog.ok(THIS_MODULE.getLocalizedString(30833),THIS_MODULE.getLocalizedString(30834))
            return
        try:
            link      = Encryption('d',link)
        except:
            try:
                link  = converthex(link)
            except:
                dolog(converthex('556e61626c6520746f2072657472696576652076616c696420646174612066726f6d20736572766572'))
        welcomematch  = re.compile('l="(.+?)"').findall(link)
        welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
        ipmatch       = re.compile('i="(.+?)"').findall(link)
        ipclean       = ipmatch[0] if (len(ipmatch) > 0) else '0.0.0.0'
        domainmatch   = re.compile('d="(.+?)"').findall(link)
        domain        = domainmatch[0] if (len(domainmatch) > 0) else ''
        emailmatch    = re.compile('e="(.+?)"').findall(link)
        email         = emailmatch[0] if (len(emailmatch) > 0) else 'Unknown'
        postsmatch    = re.compile('p="(.+?)"').findall(link)
        posts         = postsmatch[0] if (len(postsmatch) > 0) else '0'
        unreadmatch   = re.compile('u="(.+?)"').findall(link)
        unread        = unreadmatch[0] if (len(unreadmatch) > 0) else '0'
        messagematch  = re.compile('m="(.+?)"').findall(link)
        messages      = messagematch[0] if (len(messagematch) > 0) else '0'
        donmatch      = re.compile('t="(.+?)"').findall(link)
        don           = donmatch[0] if (len(donmatch) > 0) else ''
        stdmatch      = re.compile('s="(.+?)"').findall(link)
        std           = stdmatch[0] if (len(stdmatch) > 0) else ''
        nologinmatch  = re.compile('n="(.+?)"').findall(link)
        nologin       = nologinmatch[0] if (len(nologinmatch) > 0) else ''
        reqaddonmatch = re.compile('r="(.+?)"').findall(link)
        reqaddons     = reqaddonmatch[0] if (len(reqaddonmatch) > 0) else ''

        dolog(converthex('7265717569726564206164646f6e733a'))

# User required re-activation on the FORUM - old FORUM user from totalxbmc
        if converthex('72656163746976617465') in welcometext:
            xbmc.log(converthex('75736572696e666f202d2072656163746976617465'))
            try:
                dolog(converthex('726561637469766174696f6e207265717569726564202d20706c656173652076697369742074686520666f72756d206174207777772e6e6f6f6273616e646e657264732e636f6d2f737570706f727420616e64206c6f67696e2e204974206c6f6f6b732061732074686f75676820796f75206861766520616e206f6c64206163636f756e742066726f6d20546f74616c58424d432064617973207768696368206a75737420726571756972656420726561637469766174696f6e2e'))
                os.remove(COOKIE)
            except:
                pass
            dialog.ok(THIS_MODULE.getLocalizedString(30831),THIS_MODULE.getLocalizedString(30832))

# Currently restricted
        elif converthex('72657374726963746564') in welcometext:
            xbmc.log(converthex('75736572696e666f202d2072657374726963746564'))
            dolog(converthex('5741524e494e473a204163636f756e742063757272656e746c792072657374726963746564202d20746f6f206d616e79206c6f67696e732066726f6d206d756c7469706c65204950732e20496620796f75207468696e6b20796f75277665206163636964656e74616c6c79206c656674206c6f67696e20696e666f726d6174696f6e20696e2061206275696c64206f7220796f7572206c6f67696e20686173206265656e20636f6d70726f6d6973656420706c656173652075706461746520796f75722070617373776f7264206f6e20746865206e6f6f6273616e646e6572647320666f72756d20415341502121212054686973207265737472696374696f6e2077696c6c206265206175746f6d61746963616c6c79206c69667465642077697468696e20323420686f757273206275742077696c6c206265207265696e73746174656420617320736f6f6e206173206d756c7469706c6520495020636f6e6e656374696f6e73206172652064657465637465642e'))
            dialog.ok(THIS_MODULE.getLocalizedString(30829),THIS_MODULE.getLocalizedString(30830))

# Wrong PASSWORD entered
        elif converthex('70617373776f7264') in welcometext:
            xbmc.log(converthex('75736572696e666f202d2077726f6e672070617373776f7264'))
            try:
                dolog(converthex('77726f6e672070617373776f7264202d20706c656173652072652d656e74657220616e642074727920616761696e'))
                os.remove(COOKIE)
            except:
                pass
            dialog.ok(THIS_MODULE.getLocalizedString(30825),THIS_MODULE.getLocalizedString(30826))
            Open_Settings()

# Not registered and LOGIN is true
        elif converthex('7265676973746572') in welcometext and LOGIN == 'true':
            xbmc.log(converthex('75736572696e666f202d206e6f742072656769737465726564'))
            try:
                dolog(converthex('4e6f742072656769737465726564202d20706c65617365207265676973746572206174207777772e6e6f6f6273616e646e657264732e636f6d2f737570706f7274'))
                os.remove(COOKIE)
            except:
                pass
            dialog.ok(THIS_MODULE.getLocalizedString(30827),THIS_MODULE.getLocalizedString(30828))
            Open_Settings()

# Login is true but not details are entered
        elif LOGIN == 'true' and USERNAME == '' and PASSWORD == '':
            xbmc.log(converthex('75736572696e666f202d206c6f67696e207472756520627574206e6f2064657461696c73'))
            dialog.ok(THIS_MODULE.getLocalizedString(30835),THIS_MODULE.getLocalizedString(30836))
            Open_Settings()

# All settings checks are fine, create the COOKIE file
        else:
            xbmc.log(converthex('75736572696e666f202d20616c6c2066696e65'))
            dolog(converthex('416c6c2073657474696e677320636865636b206f75742066696e65202d207570646174696e6720636f6f6b69652066696c65'))
            writefile = open(COOKIE, mode='w+')
            writefile.write(Encryption('e','d="'+str(Timestamp())+'"|b="'+domain+'"|w="'+welcometext+'"|i="'+ipclean+'"|e="'+email+'"|m="'+messages+'"|u="'+unread+'"|t="'+don+'"|s="'+std+'"|p="'+posts+'"'+'"|n="'+nologin+'"'+'"|a="'+reqaddons+'"'))
            writefile.close()
            main_counter += 1
            Check_Addons(reqaddons)

            if main_counter < 3:
                xbmc.log(converthex('23232320646f696e6720766572696679'))
                Verify()
            else:
                dialog.ok(THIS_MODULE.getLocalizedString(30833),THIS_MODULE.getLocalizedString(30834))
                return

# If this was called to recreate a COOKIE file just to return base url then we call that function again
    elif mode == 'cookie_check':
        Check_Cookie('base')

    else:
        Verify()
#----------------------------------------------------------------
def Verify(testmode = ''):
    """ internal command ~"""
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id') 
    try:
        if sys.argv[1] == converthex('7465737466696c65'):
            ADDON_ID  =  ADDON_ID+'.test'
    except:
        pass
# if LOGIN is true but no USERNAME and PASSWORD we open settings
    localfile          = open(COOKIE, mode='r')
    content            = localfile.read()
    content            = Encryption('d',content)
    localfile.close()
    nologinmatch       = re.compile('n="(.+?)"').findall(content)

# Set the standard logged in downloads array
    if len(nologinmatch)>0:
        nologindownloads = nologinmatch[0].split(',')

        for item in nologindownloads:
            if len(item)>3:
                download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+ORIG_ID+'/'+item+'.jpeg')
                Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+ORIG_ID+'/'+item), DOWNLOAD_DST)

# If LOGIN is true but they haven't entered details then open up settings
    if LOGIN == 'true' and (USERNAME == '' or PASSWORD == ''):
        dolog(converthex('6c6f67696e207472756520627574207573657220616e64207061737320626c616e6b'))
        dialog.ok(THIS_MODULE.getLocalizedString(30835),THIS_MODULE.getLocalizedString(30836))
        ADDON.openSettings()
        return

# if test version enabled but LOGIN isn't tell user they need to enter credentials
    elif USE_TEST == 'true' and LOGIN == 'false':
        dolog(converthex('747279696e6720746f2072756e20746573742076657273696f6e20627574206e6f206c6f67696e20696e666f'))
        dialog.ok(THIS_MODULE.getLocalizedString(30961),THIS_MODULE.getLocalizedString(30962))
        ADDON.openSettings()
        return

# else if LOGIN is true continue
    elif LOGIN == 'true':
        dolog(converthex('6c6f67696e20697320656e61626c6564'))

# if user not previously logged in call the user_info function
        if not os.path.exists(COOKIE):
            dolog(converthex('6c6f6767696e6720696e20666f722066697273742074696d65202d20636865636b696e672063726564656e7469616c73'))
            User_Info()

# if user previously logged in then read COOKIE file
        else:
            dolog(converthex('70726576696f75736c79206c6f6767656420696e2c20636865636b696e6720636f6f6b6965'))

            userdatematch       = re.compile('d="(.+?)"').findall(content)
            loginmatch          = re.compile('w="(.+?)"').findall(content)
            ipmatch             = re.compile('i="(.+?)"').findall(content)
            donmatch            = re.compile('t="(.+?)"').findall(content)
            stdmatch            = re.compile('s="(.+?)"').findall(content)
            basematch           = re.compile('b="(.+?)"').findall(content)
            addonsmatch         = re.compile('a="(.+?)"').findall(content)
            basedomain          = basematch[0] if (len(basematch) > 0) else ''
            updatecheck         = userdatematch[0] if (len(userdatematch) > 0) else '0'
            welcometext         = loginmatch[0] if (len(loginmatch) > 0) else ''
            addons              = addonsmatch[0] if (len(addonsmatch) > 0) else ''
            ipclean             = ipmatch[0] if (len(ipmatch) > 0) else '0.0.0.0'
            myip = Get_IP()

# Set the standard logged in downloads array
            if len(stdmatch)>0:
                stddownloads = stdmatch[0].split(',')

# if user has chosen to use test version check test version is avaialble and if not already installed install it then open the settings for new addon
            if USE_TEST == 'true':
                global launch
                testmatch           = donmatch[0].split('|')
                launch              = testmatch[0]
                downloads           = testmatch[1].split(',')

                if not ADDON_ID.endswith(converthex('2e74657374')):
                    TestADDON_ID = ADDON_ID+converthex('2e74657374')
                else:
                    TestADDON_ID = ADDON_ID
                    ADDON_ID     = ADDON_ID.replace(converthex('2e74657374'),'')

                if len(downloads)>0 and not os.path.exists(os.path.join(ADDONS,TestADDON_ID)):
                    try:
                        download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+ADDON_ID+'/'+downloads[0]+'.jpeg')
                        Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+ADDON_ID+'/'+downloads[0]), DOWNLOAD_DST)
                        xbmc.executebuiltin('UpdateLocalAddons')

# open settings for new addon, this is so the relevant settings can be opened
                        xbmc.sleep(2000)
                        xbmcaddon.Addon(id=TestADDON_ID).openSettings()
                        return
                    except:
                        dialog.ok(THIS_MODULE.getLocalizedString(30965),THIS_MODULE.getLocalizedString(30966))
                        return
                elif len(downloads)==0:
                    dialog.ok(THIS_MODULE.getLocalizedString(30963),THIS_MODULE.getLocalizedString(30964))
                    return

            xbmc.executebuiltin("XBMC.Notification("+THIS_MODULE.getLocalizedString(30807)+","+THIS_MODULE.getLocalizedString(30808)+",5000,"+UPDATE_ICON+")")

# if user needs to reactivate account remove COOKIE file and notify user they need to LOGIN at FORUM
            if converthex('72656163746976617465') in welcometext:
                dolog(converthex('23232320766572696679202d206163636f756e74206e6565647320726561637469766174696f6e'))
                try:
                    os.remove(COOKIE)
                except:
                    pass
                dialog.ok(THIS_MODULE.getLocalizedString(30831),THIS_MODULE.getLocalizedString(30832))

# if user is currently restricted they cannot continue
            elif converthex('63757272656e746c792072657374726963746564') in welcometext:
                dolog(converthex('23232320766572696679202d206163636f756e742069732072657374726963746564'))
                dialog.ok(THIS_MODULE.getLocalizedString(30829),THIS_MODULE.getLocalizedString(30830))

# if user enters wrong PASSWORD remove COOKIE and get them to re-enter details
            elif converthex('57726f6e672050617373776f726420456e7465726564') in welcometext:
                dolog(converthex('23232320766572696679202d2077726f6e672070617373776f72642c2072656d6f76696e6720636f6f6b6965'))
                try:
                    os.remove(COOKIE)
                except:
                    pass
                dialog.ok(THIS_MODULE.getLocalizedString(30825),THIS_MODULE.getLocalizedString(30826))
                ADDON.openSettings()

# if they aren't registered remove the COOKIE file and open settings
            elif converthex('524547495354455220464f522046524545') in welcometext:
                dolog('4449584945204445414e204953204120434f434b20474f42424c4552')
                try:
                    os.remove(COOKIE)
                except:
                    pass
                dialog.ok(THIS_MODULE.getLocalizedString(30827),THIS_MODULE.getLocalizedString(30828))
                ADDON.openSettings()

# if the date in COOKIE is not up and the ip matches the one in COOKIE we can continue
                dolog(Encryption('e', converthex('23232320766572696679202d206970636c65616e3a202573') % ipclean))
                dolog(Encryption('e', converthex('23232320766572696679202d206d7969703a202573') % myip))

            elif int(updatecheck)+1000000 > int(Timestamp()) and ipclean == myip:
                if USE_TEST == 'true':
                    dolog(converthex('23232320766572696679202d207465737476657273696f6e2069732074727565'))
                    for item in downloads:
                        dolog(Encryption('e',converthex('23232320766572696679202d20636865636b696e673a202573') % item))
                        download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+ADDON_ID+'/'+item+'.jpeg')
                        cleanitem = item.replace('test','')
                        if Addon_Setting(addon_id=TestID,setting=cleanitem) == 'true':
                            Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+TestID+'/'+item), DOWNLOAD_DST)
                for item in stddownloads:
                    dolog('4449584945204445414e204953204120434f434b20474f42424c4552')
                    download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+ORIG_ID+'/'+item+'.jpeg')
                    if Addon_Setting(addon_id=ADDON,setting=item) == 'true':
                        Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+ORIG_ID+'/'+item), DOWNLOAD_DST)
                xbmc.executebuiltin('Dialog.Close(busydialog)')
                Main('run')
            
            else:
                User_Info()
    elif LOGIN == 'false':
        dolog('232323206c6f67696e2064697361626c6564')
        Main('run')
#----------------------------------------------------------------
try:
    if sys.argv[1] == converthex('7465737466696c65') and LOGIN == 'true':
        if os.path.exists(os.path.join(ADDONS,ORIG_ID)) and os.path.exists(os.path.join(ADDONS,TestID)):
            dolog(converthex('2323232072756e6e696e67207665726966792822747275652229'))
            Verify('true')
    if sys.argv[1] == converthex('73657474696e6773'):
        if not os.path.exists(os.path.join(ADDONS,TestID)):
            dialog.ok(THIS_MODULE.getLocalizedString(30901),THIS_MODULE.getLocalizedString(30902))
        else:
            xbmcaddon.Addon(id=TestID).openSettings()
    if sys.argv[1] == converthex('636c6561725f64617461'):
        Clear_Data(ADDON_ID)
except:
    pass