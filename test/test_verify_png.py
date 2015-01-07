# Copyright (C) 2015 Science and Technology Facilities Council.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from jsa_proc.action.verify_png import valid_png


class ValidFITSTestCase(TestCase):
    def test_valid_fits(self):
        self.assertTrue(valid_png('test/data/validpng.png'))
        self.assertFalse(valid_png('test/data/invalidpng.png'))
