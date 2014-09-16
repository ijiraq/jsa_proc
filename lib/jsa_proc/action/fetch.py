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

import logging

from jsa_proc.action.decorators import ErrorDecorator
from jsa_proc.action.datafile_handling \
    import assemble_input_data_for_job
from jsa_proc.config import get_database
from jsa_proc.state import JSAProcState
from jsa_proc.error import JSAProcError, NoRowsError

logger = logging.getLogger(__name__)


def fetch(job_id=None, db=None, force=False):
    """
    Assemble the files required to process a job.

    If it is not given a job_id, it will take the next JAC job
    with the highest priority and a state of MISSING.

    Optionally allows a database object to be given for testing purposes.
    Otherwise uses usual database from config file.

    This will raise an error if job is not in MISSING state to start with.
    This will advance the state of the job to WAITING on completion.
    Any error's raised in the process will be logged to the job log.

    """

    # Get the database.
    if not db:
        db = get_database()

    # Get next job if a job_id is not specified.
    if not job_id:
        force = False

        logger.debug('Looking for a job for which to fetch data')

        jobs = db.find_jobs(state=JSAProcState.MISSING, location='JAC',
                            prioritize=True, number=1, sort=True)

        if jobs:
            job_id = jobs[0].id

        else:
            logger.warning('Did not find a job to fetch!')
            return

    fetch_a_job(job_id, db=db, force=force)


@ErrorDecorator
def fetch_a_job(job_id, db=None, force=False):
    """
    Assemble the files required to process a job.

    Requires an integer job_id.

    Optionally allows a db to be given, for testing purposes. Otherwise
    uses usual database from config file.

    This will raise an error if job is not in MISSING state to start with.
    This will advance the state of the job to WAITING on completion.
    """

    if not db:
        # Get link to database
        db = get_database()

    logger.info('About to fetch data for job %i', job_id)

    try:
        # Change status of job to 'Fetching', raise error if not in MISSING
        db.change_state(job_id, JSAProcState.FETCHING,
                        'Data is being assembled',
                        state_prev=(None if force else JSAProcState.MISSING))

    except NoRowsError:
        # If the job was not in the MISSING state, it is likely that another
        # process is also trying to fetch it.  Trap the error so that the
        # ErrorDecorator does not put the job into the ERROR state as that
        # will cause the other process to fail to set the job to WAITING.
        logger.error('Job %i cannot be fetched because it is not missing',
                     job_id)
        return

    # Get the list of files.
    input_files = db.get_input_files(job_id)

    # Assemble the data.
    input_file_list = assemble_input_data_for_job(job_id, input_files)

    # Advance the state of the job to 'Waiting'.
    db.change_state(
        job_id, JSAProcState.WAITING,
        'Data has been assembled for job and job can now be executed',
        state_prev=JSAProcState.FETCHING)

    logger.info('Done fetching data for job %i', job_id)

    return job_id