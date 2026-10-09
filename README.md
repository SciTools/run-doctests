# run-doctests
Self-contained doctest checker using standard-library 'doctests' package.

The util itself is implemented in a single sourcefile, which can be templated in [`SciTools/.github/tree/main/templates`]([url](https://github.com/SciTools/.github/tree/main/templates)).  
So, the 'definitive' code for `run_doctests.py` lives there and **not** in this repo, 
but this repo ...
   * is templated to that central version
   * provides some documentation
   * is where [tests](https://github.com/SciTools/run-doctests/tree/main/tests) live, and CI to regularly [test against latest dependencies](https://github.com/SciTools/run-doctests/blob/main/.github/workflows/ci-tests.yml#L19-L20)
   * is not a package, or installable

## Features
* doesn't need a Sphinx build, so **runs much faster**
  * (it runs on the original source files, for both docs and api docstrings)
* uses the `doctest` module to implement a 'standard' syntax
  * (from the Python standard library)
* makes it easy to test specific sourcefiles

* example help text (including simple usage examples):
```
$ ./tools/run_doctests.py
usage: run_doctests [-h] [-m] [-r] [-p] [-e EXCLUDE] [-o [OPTIONS]] [-v] [-d] [-f] [paths ...]

Run doctests in docs files, or docstrings in packages.

positional arguments:
  paths                 docs filepaths, or module paths (not both).

options:
  -h, --help            show this help message and exit
  -m, --module          paths are module paths (xx.yy.zz), instead of filepaths.
  -r, --recurse         include submodules (only applies with -m).
  -p, --publiconly      exclude module names beginning '_' (only applies with -m and -r)
  -e, --exclude EXCLUDE
                        exclude paths containing substring (may appear multiple times).
  -o, --options [OPTIONS]
                        kwargs (Python) for doctest call, e.g. "raise_on_error=True,optionflags=8".
  -v, --verbose         show details of each operation.
  -d, --dryrun          only print names of modules/files which *would* be tested.
  -f, --stop-on-fail    stop at the first path with an error (else continue to test all).

Notes:
  * file paths support glob patterns '* ? [] **'  (** to include subdirectories)
      * N.B. use ** to include subdirectories
      * N.B. usually requires quotes, to avoid shell expansion
  * module paths do *not* support globs
      * but --recurse includes all submodules
  * "--exclude" patterns are a simple substring to match (not a glob/regexp)

Examples:
  $ run_doctests "docs/**/*.rst"                      # test all document sources
  $ run_doctests "docs/user*/**/*.rst" -e detail      # skip filepaths containing key string
  $ run_doctests -mr mymod                            # test module + all submodules
  $ run_doctests -mr mymod.util -e maths -e fun.err   # skip module paths with substrings
  $ run_doctests -mr mymod -o verbose=true            # make doctest print each test

```
