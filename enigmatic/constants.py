#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of enigmatic.

    enigmatic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    enigmatic is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with enigmatic.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppAttributes:
    application_name = "enigmatic"
    application_id = "com.github.hezral.enigmatic"
    application_description = " Safe keep your secrets and passwords by splitting it to family and friends and recover it with just a few of the parts"
    application_version = '1.0'
    about_authors = ["hezral@gmail.com"]
    about_comments = application_description
    about_license_type = Gtk.License.GPL_3_0
    about_logo_icon_name = "com.github.hezral.enigmatic"
    about_program_name = application_name
    about_version = application_version
    about_website = "https://github.com/hezral/enigmatic"
    about_website_label = "Feedback/Report Bugs at Github"
    about_copyright = "Copyright © 2020 Adi Hezral"