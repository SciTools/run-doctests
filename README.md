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

## Relation to other ways of running doctests
Both Sphinx and PyTest provide facilities to run doctests, but both have some drawbacks
  * Sphinx
    * requires a complete docs-build, and then tests its *output* : so this is slow
    * it is possible, though somewhat awkward, to run doctests in a single file  (but still need a full build)
  * PyTest
    * expects to run alongside regular tests, which is not always desirable
    * running *just* doctests is possible but awkward, depends on cwd not containing any 'real' tests
    * not possible to run a single selected file

### Test setup and cleanup sections
Both Sphinx and PyTest also allow for setup and cleanup (or "teardown") sections, in both docs sources and api (dosctrings).  
  * this is potentially useful (reduces duplication), but they don't agree on the syntax.  
  * the Sphinx form omits all the ">>>", and can't support them, which means it is not compatible with the plain `doctests` module operation.  
  * for Sphinx, it is also of course important that these **don't _appear_ in the rendered output**.  

**run_doctests** takes the view that there is nothing "special" about teardown/cleanup sections.
  * being based on `doctest`, each file simply contains ">>> " marked sections, which are all run as code, and tested as-is, in file order
  * this doesn't allow for shared setup/teardown, but is at least simple
  * temporary file/directory creation and global variable changes must be explicitly handled
    * -- but neither PyTest or Sphinx provides anything special to do this anyway, beyond shareable cleanup code (see also [Isolation of test contexts](https://github.com/SciTools/run-doctests/edit/main/README.md#isolation-of-test-contexts) below) 

#### Hiding setup/cleanup in Sphinx output
In Sphinx, the intended use of ".. testsetup:" and ".. testcleanup::" sections is to contain indented Python code, with no ">>>" prefixes, like this:
```
.. testsetup:: [[<optional-section-name]]
    test_object = {'a': 1}

.. doctest:
    >>> print(test_object['a'])
    1

.. testcleanup::
    del test_object
```
**Note that:** the actual doctest has ">>>" prefixes, but the setup/cleanup do not.

As long as we **no longer use Sphinx to run doctests**, these can safely be converted to the ">>> " form, i.e.
```
.. testsetup:: [[<optional-section-name]]
    >>> test_object = {'a': 1}

.. doctest:
    >>> print(test_object['a'])
    1

.. testcleanup::
    >>> del test_object
```

In this form, the test code simply runs through end-to-end.  

However, there are no _actual_ setup/cleanup sections, as doctest doesn't support it.
So, if you need to share setup/cleanup operations between different tests, this must be done manually.

#### Isolation of test contexts
It is often important to ensure that some temporary global context changes/setup are removed after the test.
( That is, changes in the global variable space, and maybe in the file system ).

With Sphinx and PyTest, setup/cleanup operations can be used to do this.  
However, it is important to note that this must be delivered by user code -- there is no special 'magic' for it.

This is quite different from running ordinary tests in PyTest, where there are various mechanisms for making temporary changes within a limited context, 
for exmaple the use of fixtures, `pytest.raises` or `mocker.patch`.

Actually in practice, global changes *are* permitted and commonly used to simplify subsequent tests -- e.g. a package import, or a test object definition, which are re-used in subsequent doctests.

    
   
