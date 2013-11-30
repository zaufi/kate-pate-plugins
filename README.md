What is this?
=============

  All that u c here is a mine set of plugins for Kate/Pâté. 

  Previous list of plugins alerady in the kate.git repo. Moreover,
  after huge refactoring I've done in the `master` (after 4.12 release), all that plugins
  will not work anymore. So they are tagged and deleted from this repo.

  Some new (experemental) plugins are coming :) in a new format...


Requirements
============

  Of cause u need a Kate package with enabled Python plugins host.


How to install
==============

  To install Pâté plugins system-wide:

    $ cmake . && sudo make install

  or

    $ cmake -DINSTALL_TYPE=user . && make install

  to install into your home directory. Do not forget to enable the Pâté plugin
  in Kate settings.
