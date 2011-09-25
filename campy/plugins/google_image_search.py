#
# Copyright (c) 2011 Ben Belchak <ben@belchak.com>
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

import traceback
import re
import simplejson
import httplib2
import urllib
import random

from plugins import CampyPlugin
from campy import settings

class GoogleImage(CampyPlugin):
    def send_help(self, campfire, room, message, speaker):
        help_text = ("""%s: Here is your help for the Google Image Search plugin:
    gis term -- Returns the first Google Image search result ( gis cuddly bunny )
    gis r[andom] term -- Returns a random search result ( gis random bunny )"""
        % speaker['user']['name'])
        room.paste(help_text)

    def handle_message(self, campfire, room, message, speaker):
        body = message['body']
        if not body or not body.startswith(settings.CAMPFIRE_BOT_NAME):
            return

        patt = '%s: gis (?P<random_flag>r(andom)? )?(?P<search_string>.*)$' % settings.CAMPFIRE_BOT_NAME
        m = re.match(patt, body)
        if m:
            try:
                search_string = urllib.quote(m.groupdict().get('search_string'))
                random_flag   = m.groupdict().get('random_flag')
                headers, content = httplib2.Http().request(
                    "https://ajax.googleapis.com/ajax/services/search/images?safe=%s&v=1.0&q=%s" %
                    (settings.GOOGLE_IMAGE_SAFE, search_string))
                json = simplejson.loads(content)
                results = json['responseData']['results']
                result_pos = 0
                if random_flag:
                    result_pos = random.randint(1,len(results)-1)
                self.speak_image_url(room, results[result_pos]['unescapedUrl'])
            except (KeyError,):
                room.speak(traceback.format_exc())

    def speak_image_url(self, room, url):
        room.speak(unicode(url))
