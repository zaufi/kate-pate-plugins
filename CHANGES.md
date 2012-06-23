Version 0.5.2 (2012-06-23)
==========================

* comment paragraph shrink/extend plugin (Meta+[, Meta+])
* some of existed plugins refactored to be faster
  (also to use new text processing facilities)
* if selection on the only line, extend it to whole line before do commenting
  (to avoid garbage in result)
* add sw(expr[, case1[, ..., caseN]]) expansion to generate switch statements

Version 0.5.1 (2012-06-14)
==========================

* color chooser plugin


Version 0.5.0 (2012-06-10)
==========================

* use cmake to install package files
* fix cursor positioning after expansion (waiting for movingInterface
  support in next versions of PyKDE4). '\1' replaces with '%{cursor}'
  keyword in expansion text
* fixed pate's argument parser for expansions to support variable number
  of parameters and named parameters
* improvements in C++ expansions
* add passive popups w/ native look and feel (as for me it's better than
  custom popups in Pate, which is looks ugly w/ my color scheme)
* use decorators to disable (show popup w/ alert) actions by various constraints,
  for example commenting text block w/ `#if 0' have sense only for C/C++
  documents
* make some comment manipulation actions to work w/ other than C/C++ source code
  (CMake, Python, Perl, Bash)


Version 0.4.0 (2012-06-04)
==========================

* boost-like functions/templates parameters list (un)formatter
