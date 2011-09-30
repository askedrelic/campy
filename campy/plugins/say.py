#
# Copyright (c) 2011 Trey Doig <john@doig.me>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import re
import os

from plugins import CampyPlugin
from campy import settings

class Say(CampyPlugin):
    
    def send_help(self, campfire, room, message, speaker):
        help_text = ("""%s: Here is your help for the say plugin:
    say text -- pipe text to the Mac say command"""
        % speaker['user']['name'])
        room.paste(help_text)

    def handle_message(self, campfire, room, message, speaker):
        body = message['body']
        if not body or not body.startswith(settings.CAMPFIRE_BOT_NAME):
            return

        patt = '%s: say (?P<command>.*)$' % settings.CAMPFIRE_BOT_NAME
        m = re.match(patt, body)
        if m:
            command = m.groupdict().get('command')
            os.system("say %s" % command)
