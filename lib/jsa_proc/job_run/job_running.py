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

"""
Routines for running the perl-JSA script 'jsawrapdr' from the JAC
processing system.
"""

from datetime import datetime
import shutil
import signal
import subprocess
import tempfile
import os
import sys

from jsa_proc.config import get_config
from jsa_proc.job_run.directories \
    import get_scratch_dir, get_log_dir, get_output_dir
from jsa_proc.error import JSAProcError


def jsawrapdr_run(job_id, input_file_list, mode, drparameters,
                  cleanup='cadc', location='JAC', persist=False,
                  jsawrapdr=None,
                  debug=False):
    """Routine to execute jsawrapdr from python.

    Takes in a job_id, input_file_list, mode and drparameters..

    Calls jsawrapdr with following options
    jsawrapdr --outdir=configbase/scratch/$job_id
              --inputs=input_file_list
              --id = jac-$job_id
              --mode=$mode
              --drparameters=$drparameters
              --cleanup=$cleanup (cadc by default)
              --location=$location (JAC by default)

         if persist is True, then it adds the flag:
              -persist

    job_id, integer
    job identifier from jsaproc database

    input_file_list, string
    list of files (with extensions and full path).

    mode, string
    'night', 'obs', 'public' or 'project'.

    drparameters, string


    cleanup, optional, string |'cadc'|'none'|'all'

    The jsawrapdr clean option, default is 'cadc'.

    persist, boolean, defaults to False

    If persist is turned on, then dpCapture will copy acceptable
    products to the default output directory. Otherwise it won't (used
    for debugging purposes). The output directory is determined by
    jsa_proc.job_run.directories 'get_output_dir' for the given job_id.

    # Location is not currently implemented!
    location, string |'cadc'|'JAC'|

    The default is 'JAC', others probably never used?

    jsawrapdr, string, optional
    path to jsawrapdr, otherwise uses one in configured starlink

    debug, boolean, optional (default False)
    turn on jsawrapdr debugging if true

    Returns: logfilename, string

    Returns the filename (including path) of the logfile (string).

    """

    # Get config information.
    scratch_base_dir = get_scratch_dir(job_id)
    if not os.path.exists(scratch_base_dir):
        os.makedirs(scratch_base_dir)

    log_dir = get_log_dir(job_id)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get scratchdir and logfile name using timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    scratch_dir = os.path.join(scratch_base_dir, timestamp)
    if os.path.exists(scratch_dir):
        scratch_dir = tempfile.mkdtemp(prefix=scratch_dir)
    else:
        os.mkdir(scratch_dir)
    logfile = os.path.join(log_dir, 'jsawrapdr_'+timestamp+'.log')

    # Get output directory name
    out_dir = get_output_dir(job_id)

    # If output dir currently exists, delete the directory.
    if os.path.exists(out_dir):
        # This will leave the parent directory, so dpCapture can re-create
        # the "transfer" directory.
        shutil.rmtree(out_dir)
    else:
        # The parent directory may not exist, so we must make the "transfer"
        # directory because dpCapture will not do so in that case.
        os.makedirs(out_dir)

    # Find path to jsawrapdr and orac_dr
    config = get_config()
    starpath = config.get('job_run', 'starpath')
    if not jsawrapdr:
        jsawrapdr = os.path.join(starpath, 'Perl', 'bin', 'jsawrapdr')
    orac_dir = os.path.join(starpath, 'bin', 'oracdr', 'src')

    # jac recipe id
    jacid = 'jac-'+str(job_id)

    # jsawrapdr arguments.
    jsawrapdrcom = [jsawrapdr,
                    '--debugxfer',
                    '--outdir='+scratch_dir,
                    '--inputs='+input_file_list,
                    '--id='+jacid,
                    '--mode='+mode,
                    '--cleanup='+cleanup,
                    '--drparameters='+drparameters]
    if persist:
        jsawrapdrcom.append('-persist')
        jsawrapdrcom.append('--transdir='+out_dir)

    if debug:
        jsawrapdrcom.append('-debug')

    # environment
    jsa_env = os.environ.copy()
    jsa_env['STARLINK_DIR'] = starpath
    jsa_env['PATH'] = os.path.join(starpath, 'bin') + os.pathsep + \
        jsa_env['PATH']
    jsa_env['LD_LIBRARY_PATH'] = os.path.join(starpath, 'lib') + os.pathsep + \
        jsa_env['LD_LIBRARY_PATH']
    jsa_env['ORAC_DIR'] = orac_dir
    jsa_env['ORAC_LOGDIR'] = log_dir
    jsa_env['STAR_LOGIN'] = '1'
    jsa_env['CONVERT_DIR'] = os.path.join(starpath, 'bin', 'convert')
    # Remainder of oracdr required environmental variables are set
    # inside WrapDR.pm->run_pipeline

    # Set up logfile
    if os.path.exists(logfile):
        log = tempfile.NamedTemporaryFile(prefix='jsawrapdr_'+timestamp,
                                          dir=log_dir, suffix='.log',
                                          delete=False)
    else:
        log = open(logfile, 'w')

    # Run jsawrapdr
    retcode = subprocess.call(jsawrapdrcom, env=jsa_env, bufsize=1,
                              stdout=log, stderr=subprocess.STDOUT,
                              preexec_fn=restore_signals)

    log.close()

    if retcode != 0:
        raise JSAProcError('jsawrapdr exited with non zero status. '
                           'Retcode was %i; job_id is %i.'
                           'stdin/stderr are written in %s' %
                           (retcode, job_id, log.name),
                           retcode, job_id, log.name)
    # Need to return list of produced files in output directory?

    return log.name


def restore_signals():
    """Restore signals which Python otherwise ignores.

    For more information about this issue, please see:
    http://bugs.python.org/issue1652"""

    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGXFSZ, signal.SIG_DFL)
