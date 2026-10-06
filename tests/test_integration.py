"""Actual test exercising
"""
from pathlib import Path
import subprocess

_RUN_PATH = Path(__file__).parent / "resources"
_SCRIPT_PATH = _RUN_PATH.parents[1] / "run_doctests.py"

def run_script(args):
    """Run the run_doctests.py script with given args, return rc and stdout+stderr.

    We also need to ensure that the test python is on PATH, and the test module
    on the PYTHONPATH.
    """
    import os
    pypth = os.environ.get("PYTHONPATH")
    modpth = str(_RUN_PATH)
    pypth = (pypth or "") + ":" + modpth
    os.environ["PYTHONPATH"] = pypth
    syspth = os.environ.get("PATH")
    binpth = Path(os.__file__).parents[2] / "bin"
    syspth = str(binpth) + ":" + syspth  # this one needs to go at the front
    os.environ["PATH"] = syspth
    result = subprocess.run(
        [_SCRIPT_PATH, *args],
        cwd=_RUN_PATH, check=False, capture_output=True
    )
    return result


def tolerant_compare(result_lines, expect_lines):
    """Compare lists of output strings with some special syntax.

    "..." represents an arbitrary start or end of line (not both).
    "item[s]" matches "item" or "items" -- an awkward change in doctests at Python 3.13.
    """
    for i_line, (line, expect_line) in enumerate(zip(result_lines, expect_lines)):
        new_line = None
        if expect_line.startswith("..."):
            # Trim the result line.
            new_line = line[-len(expect_line):]
            # Replace 3 chars with ellipsis to make it (potentially) match.
            new_line = "..." + new_line[3:]
        elif expect_line.endswith("..."):
            # Similar, other end
            new_line = line[:len(expect_line)]
            new_line = new_line[:-3] + "..."
        elif 'item[s]' in expect_line:
            # Just to cover a specific, slightly awkward output change in Python 3.13
            if "items" in line:
                new_line = line.replace('items', 'item[s]')
            else:
                new_line = line.replace('item', 'item[s]')
        if new_line is not None:
            result_lines[i_line] = new_line
    assert result_lines == expect_lines


def test_docstrings():
    result = run_script(['-m', 'sample_module'])
    assert result.returncode == 1
    result_lines = result.stdout.decode().split("\n")
    expect_lines = [
        # N.B. lines starting "..."  match only the tail end of the relevant result line.
        '**********************************************************************',
        '.../tests/resources/sample_module.py", '
        'line 24, in sample_module.function_bad',
        'Failed example:',
        '    print(1)',
        'Expected:',
        '    0',
        'Got:',
        '    1',
        '**********************************************************************',
        '.../tests/resources/sample_module.py", '
        'line 26, in sample_module.function_bad',
        'Failed example:',
        '    1 == 2',
        'Expected:',
        '    True',
        'Got:',
        '    False',
        '**********************************************************************',
        '1 item[s] had failures:',
        '   2 of   2 in sample_module.function_bad',
        '***Test Failed*** 2 failures.',
        '**ERRORS**',
        '1/3 OK, 2/3 FAILED in path: sample_module',
        '',
        '=====',
        'run_doctest: FINAL REPORT',
        '    paths tested    = 1',
        '    tests completed = 3',
        '    errors          = 2',
        '',
        'FAILED.',
        '',
    ]
    tolerant_compare(result_lines, expect_lines)

def test_doc_sources():
    result = run_script(['*.md'])
    assert result.returncode == 1
    result_lines = result.stdout.decode().split("\n")
    expect_lines = [
        '**********************************************************************',
        '.../tests/resources/sample_doc_source.md", line 16, in sample_doc_source.md',
        'Failed example:',
        '    print(None)',
        'Expected:',
        '    none found',
        'Got:',
        '    None',
        '**********************************************************************',
        '.../tests/resources/sample_doc_source.md", line 18, in sample_doc_source.md',
        'Failed example:',
        '    1',
        'Expected:',
        '    2',
        '... ```',
        'Got:',
        '    1',
        '**********************************************************************',
        '1 item[s] had failures:',
        '   2 of   4 in sample_doc_source.md',
        '***Test Failed*** 2 failures.',
        '**ERRORS**',
        '2/4 OK, 2/4 FAILED in path: ...',
        '',
        '=====',
        'run_doctest: FINAL REPORT',
        '    paths tested    = 1',
        '    tests completed = 4',
        '    errors          = 2',
        '',
        'FAILED.',
        '',
    ]
    tolerant_compare(result_lines, expect_lines)
