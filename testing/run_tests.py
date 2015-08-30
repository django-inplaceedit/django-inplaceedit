#!/usr/bin/env python

# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 by Yaco Sistemas <goinnn@gmail.com>
#               2015 by Pablo Martín <goinnn@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.

import django
import os
import sys
from django.conf import ENVIRONMENT_VARIABLE
from django.core import management


if len(sys.argv) == 1:
    os.environ[ENVIRONMENT_VARIABLE] = 'testing.settings'
else:
    os.environ[ENVIRONMENT_VARIABLE] = sys.argv[1]

if hasattr(django, 'setup'):
    django.setup()

if django.VERSION[0] == 1 and django.VERSION[1] <= 5:
    management.call_command('test', 'unit_tests')
else:
    management.call_command('test', 'testing.unit_tests')
