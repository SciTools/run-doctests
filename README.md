# run-doctests
Self-contained doctest checker using standard-library 'doctests' package.

The util itself is implemented in a single sourcefile, which can be templated in [`SciTools/.github/tree/main/templates`]([url](https://github.com/SciTools/.github/tree/main/templates)).  
So, the 'definitive' code for `run_doctests.py` lives there and **not** in this repo
   * .. but .. this repo is templated to that central version
   * .. and this repo is the home of **tests** for the doctest runner, and CI to check against any dependency change
