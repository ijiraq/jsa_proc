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

from collections import OrderedDict

from jsa_proc.action.error_filter import JSAProcErrorFilter
from jsa_proc.state import JSAProcState
from jsa_proc.web.util import url_for


def prepare_error_summary(db, redirect_url, filtering=None, chosentask=None,
                          extrafilter=None, state_prev=None, error_state=None,
                          filter_done=True):
    """
    Prepare a summary of all jobs in error state.


    options:

    filter parameter will be applied to the latest log
    message for each job, and will only return the job if
    it matches the filter

    General options:
        * network: return errors containing

    """

    locations = ['JAC']

    # Check state_prev parameter
    if state_prev == '':
        state_prev = None

    # Check error_state parameter
    if error_state == '' or error_state is None:
        error_state = JSAProcState.ERROR

    # Fixup the extrafilter parameter.
    if extrafilter is None or extrafilter == '':
        extrafilter = None

    # Prepare a filter based on last error message for each ID.  Include
    # the "state_prev" constraint if not looking for jobs currently in the
    # error state.
    error_filter = JSAProcErrorFilter(
        filtering, extrafilter=extrafilter,
        state_prev=(None if error_state == JSAProcState.ERROR else state_prev))

    if chosentask is None or chosentask == '':
        chosentask = None
    tasks = db.get_tasks()

    # Dictionary to hold output. Keys are location, items are ordered dict
    error_dict = OrderedDict()
    if filter_done:
        for l in locations:
            # Find jobs in the desired "error" state, leaving state_prev
            # filtering to the error filter if this state isn't ERROR.
            error_dict[l] = db.find_errors_logs(
                location=l, task=chosentask,
                state_prev=(state_prev if error_state == JSAProcState.ERROR
                            else None),
                error_state=error_state)

            error_filter(error_dict[l])

    if extrafilter is None:
        extrafilter = ''
    return {
        'title': 'Errors in JSA Processing Jobs',
        'job_summary_dict': error_dict,
        'states': JSAProcState.STATE_ALL,
        'error_states': JSAProcState.STATE_ERROR,
        'filtering': filtering,
        'filtering_options': JSAProcErrorFilter.filter_names,
        'tasks': tasks,
        'chosentask': chosentask,
        'extrafilter': extrafilter,
        'chosen_state_prev': state_prev,
        'chosen_error_state': error_state,
        'redirect_url': redirect_url,
    }
