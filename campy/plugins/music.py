#
# Copyright (c) 2011 Matthew Behrens <askedrelic@gmail.com>
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
from appscript import *

from plugins import CampyPlugin
from campy import settings

class Music(CampyPlugin):
    def send_help(self, campfire, room, message, speaker):
        help_text = ("""%s: Here is your help for the music control plugin:
    music next -- next track
    music previous -- previous track
    music current -- current track info"""
        % speaker['user']['name'])
        room.paste(help_text)

    def handle_message(self, campfire, room, message, speaker):
        body = message['body']
        if not body or not body.startswith(settings.CAMPFIRE_BOT_NAME):
            return

        patt = '%s: music (?P<command>.*)$' % settings.CAMPFIRE_BOT_NAME
        m = re.match(patt, body)
        if m:
            try:
                command = m.groupdict().get('command')
                itunes = app('iTunes')
                spotify = app('Spotify')
                if itunes.player_state.get() == k.playing:
                    player = itunes
                elif spotify.player_state.get() == k.playing:
                    player = spotify
                else:
                    room.speak('Nothing is playing right now, sorry :(')
                    return

                if command == 'next':
                    player.next_track()
                elif command == 'previous':
                    player.previous_track()

                track_name = player.current_track.name.get()
                track_artist = player.current_track.artist.get()
                message = 'Now playing "%s" by "%s"' % (track_name, track_artist)
                room.speak(message)
            except (KeyError,):
                room.speak(traceback.format_exc())
