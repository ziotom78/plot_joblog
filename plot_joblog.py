#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2016 Maurizio Tomasi
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''Command-line utility to display the execution time of jobs run by GNU parallel'''

from collections import namedtuple
import click
import os.path
import re
import sys

__version__ = '1.0.0'
DEFAULT_SPACE = ' '
DEFAULT_FILL = '#'

JobInfo = namedtuple('JobInfo', 'seq starttime endtime runtime')


def read_jobs_from_file(input_file):
    # Discard the first line (header)
    input_file.readline()

    lines = [x.strip() for x in input_file.readlines()]
    field_re = re.compile('^([\\d]+)\\s+[\\S]+\\s+([\\d.]+)\\s+([\\d.]+)')
    jobs = []
    for cur_line in lines:
        match = field_re.match(cur_line)
        assert match

        seq = int(match.group(1))
        starttime = float(match.group(2))
        runtime = float(match.group(3))
        endtime = starttime + runtime

        jobs.append(JobInfo(seq=seq,
                            starttime=starttime,
                            runtime=runtime,
                            endtime=endtime))

    return jobs


def display_jobs(job_list, max_num_of_chars=80, space=' ', fill='*'):
    overall_start = min([x.starttime for x in job_list])
    overall_end = max([x.endtime for x in job_list])
    overall_span = overall_end - overall_start

    for cur_job in job_list:
        job_start_char, job_end_char = \
            [int((x - overall_start) / overall_span * max_num_of_chars)
             for x in (cur_job.starttime, cur_job.endtime)]

        s = '{0:6d}: |{1}{2}{3}|'.format(cur_job.seq,
                                         space * job_start_char,
                                         fill *
                                         (job_end_char - job_start_char),
            space * (max_num_of_chars - job_end_char))
        click.echo(s)


@click.command()
@click.version_option(version=__version__)
@click.argument('input_file', type=click.File('rt'))
@click.option('-w', '--width', default=80, type=int, metavar='NUM',
              help='Maximum number of characters to use for the bars',
              show_default=True)
@click.option('-s', '--sort', 'ordering', default='seq', metavar='FIELD',
              help='Specify how jobs should be ordered. Possible values '
              'are "seq", "starttime", "endtime", and "runtime"',
              show_default=True)
@click.option('--space', default=DEFAULT_SPACE, metavar='CHAR',
              help='Character to use for the plot background')
@click.option('--fill', default=DEFAULT_FILL, metavar='CHAR',
              help='Character to use for the plot bars',
              show_default=True)
def main(input_file, width, ordering, space, fill):

    sort_dict = {'seq': lambda x: x.seq,
                 'starttime': lambda x: x.starttime,
                 'endtime': lambda x: x.endtime,
                 'runtime': lambda x: x.runtime}

    if len(space) != 1:
        sys.stderr.write(
            'only one character is expected for --space, reverting to the default\n')
        space = DEFAULT_SPACE

    if len(fill) != 1:
        sys.stderr.write(
            'only one character is expected for --fill, reverting to the default\n')
        fill = DEFAULT_FILL

    jobs = sorted(read_jobs_from_file(input_file),
                  key=sort_dict[ordering])

    display_jobs(jobs, max_num_of_chars=width, space=space, fill=fill)
