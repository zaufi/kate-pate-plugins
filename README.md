What is this?
=============

  All that u c here is a mine set of plugins for Pâté. Latter is a plugin
  for KDE's Kate editor which allows to write plugins using Python.

  Most of this plugins I wrote to help myself writing a C++ code and
  found them r quite usable. After feedback from my friends (C++ coders too :)
  I've decided to share them. Anyway if u'd like to make some improvements
  your changes r welcome... just please share it :)

  Also I'm not a Python guru yet, so any performance or other optimizations
  r welcome as well :) I've just found that writing plugins for Kate is easy
  enough using Python, so I'm just having fun... :)

  U may found a brief plugins description at top of particular .py file.

  In a expand/ subdir is a mine set of plugins for Pâté's example plugin
  called `expand' :) Latter is quite similar to standard snippets shipped
  with Kate, but thanx to Python is could be much more powerful...
  So, mostly, I prefer to use Pâté's expand (Ctrl-E).


Requirements
============

  Of cause u need a Pâté package installed before. Gentoo users may find it
  in a kde-testing overlay. Owners of other distros (I'm in doubt that corresponding
  packages exists) may download it from http://github.com/pag/pate.

  BTW, recently Pâté plugin was commited into playground/ of the Kate git repo.


How to install
==============

  To install Pâté plugins system-wide:

    $ cmake && sudo make install

  or

    $ cmake -DINSTALL_TYPE=user && make install

  to install into your home directory. Do not forget to enable the Pâté plugin
  in Kate settings.
