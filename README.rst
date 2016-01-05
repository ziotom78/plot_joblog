Plotting time tables for jobs ran by GNU Parallel
=================================================

The program ``print_joblog`` produces a textual representation of the
time required by a sequence of jobs ran by GNU parallel
(http://www.gnu.org/software/parallel/).

To use it, call GNU Parallel with the ``--joblog`` option::

    $ parallel --joblog log.txt ...[all the other parameters]...

After the file ``log.txt`` has been created, run ``plot_joblog`` on it::

    $ plot_joblog log.txt

(You do not have to wait till ``parallel`` has exited to run
``plot_joblog``.)


Installing the program
----------------------

Move in the source directory and run the following command::

    $ python3 setup.py install


Example
-------

Here is an example of the output::

    $ plot_joblog -w 20 joblog_example.txt
     1: |####                |
     2: |####################|
     3: |########            |
     4: |###                 |
     5: |   ################ |
     6: |    ###########     |
    $

Output can be customized by means of the following parameters:

- ``--width`` specifies the overall width of each bar, in characters.
- ``--space`` allows to set up the character used to fill the
  background of the bar.
- ``--fill`` allows to specify the character to be used to fill the
  bars.

A nice choice for UTF-8 terminals is to use the character \u2588 (``█``)
for filling the bars::

    $ plot_joblog -w 20 --fill='█' joblog_example.txt
     1: |████                |
     2: |████████████████████|
     3: |████████            |
     4: |███                 |
     5: |   ████████████████ |
     6: |    ███████████     |
    $

Run ``plot_joblog --help`` to see all the options provided by the
program.


License
-------

This program is released under the MIT license.
