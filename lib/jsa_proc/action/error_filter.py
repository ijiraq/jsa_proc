# Copyright (C) 2014 Science and Technology Facilities Council.
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

from __future__ import absolute_import, division

import operator

from jsa_proc.error import JSAProcError


class JSAProcErrorFilter():
    """Class to assist in filtering jobs which are in error, based on their
    last log message.
    """

    filters = {
        'unauthorized': [
            '401 Client Error',
            ],
        'network': [
            '503 Server Error',
            'fails hds validation',
            ],
        'running': [
            'jsawrapdr exited with non zero status',
            ],
    }

    filter_names = sorted(filters.keys()) + ['uncategorized']

    def __init__(self, filter_name):
        """Create error filter object.

        Parameters:
            filter_name: the name of the filter.  Must be one of the values
            of the JSAProcErrorFilter.filter_names list.
        """

        if filter_name == 'uncategorized':
            self.search = sum(self.filters.values(), [])
            self.condition = operator.not_
        else:
            try:
                self.search = self.filters[filter_name]
                self.condition = operator.truth
            except KeyError:
                raise JSAProcError(
                    'Unknown filtering option "{0}"'.format(filter_name))

    def __call__(self, job_logs):
        """Apply filter to a dictionary of jobs and their errors.

        The given dictionary (or OrderedDict) is modified in place to remove
        those jobs which do not match the filter.
        """

        # Iterate over a copy of the list of items because in Python 3 items
        # is an iterator, which we can't use while popping entries out of
        # the dictionary.
        for (job, log) in list(job_logs.items()):
            if self.condition(all(log[0].message.find(i) == -1
                                  for i in self.search)):
                job_logs.pop(job)