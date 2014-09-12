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
import glob
import os
import re

from jsa_proc.error import NoRowsError
from jsa_proc.job_run.directories import get_log_dir
from jsa_proc.state import JSAProcState
from jsa_proc.qastate import JSAQAState
from jsa_proc.web.util import url_for, HTTPNotFound


def prepare_job_qa_info(db, job_id):
    # Fetch job and qa information from the database.
    try:
        job = db.get_job(job_id)
    except NoRowsError:
        raise HTTPNotFound()

    # Convert the information to a dictionary so that we can augment it.
    info = job._asdict()
    if info['foreign_id'] is not None:
        if info['location'] == 'CADC':
            info['foreign_url'] = \
                'http://beta.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/' \
                'dp/recipe/{0}'.format(info['foreign_id'])
        else:
            info['foreign_url'] = None

    try:
        input_files = db.get_input_files(job_id)
    except NoRowsError:
        input_files = ['in', 'in']


    previews1024 = []
    try:
        output_files = db.get_output_files(job.id)
        for i in output_files:
            if re.search('preview_1024.png', i) and (re.search('_reduced-', i) or re.search('_healpix-', i)):
                previews1024.append(i)

    except NoRowsError:
        output_files = []

    obs_info = db.get_obs_info(job.id)

    if obs_info:
        obs_info = [o._asdict() for o in obs_info]

    else:
        obs_info = None

    if previews1024:
        previews1024 = [url_for('job_preview', job_id=job.id, preview=i)
                        for i in previews1024]



    # Get the log files on disk (if any)
    logdir = get_log_dir(job_id)
    orac_logfiles = sorted(glob.glob(os.path.join(logdir, 'oracdr*.html')),
                           reverse=True)
    orac_logfiles = [os.path.split(i)[1] for i in orac_logfiles]
    orac_logfiles = [url_for('job_log_html', job_id=job.id, log=i)
                     for i in orac_logfiles]

    wrapdr_logfiles = sorted(glob.glob(os.path.join(logdir, 'jsawrapdr*.log')),
                             reverse=True)
    wrapdr_logfiles = [os.path.split(i)[1] for i in wrapdr_logfiles]
    wrapdr_logfiles = [url_for('job_log_text', job_id=job.id, log=i)
                       for i in wrapdr_logfiles]

    # QA log (f any)
    qalog = db.get_qas(job_id)
    qalog.reverse()

    return {
        'title': 'Job {}'.format(job_id),
        'info': info,
        'qalog': qalog,
        'output_files': output_files,
        'orac_logs': orac_logfiles,
        'wrapdr_logs': wrapdr_logfiles,
        'previews': zip(previews1024,previews1024),
        'states': JSAProcState.STATE_ALL,
        'obsinfo': obs_info,
        'qastates':JSAQAState.STATE_ALL,
    }
