# tests/fidelity/test_build.py
from scripts.fidelity.build import detect_problems, bundler

GOOD = """Configuration file: /x/_config.yml
            Source: /x
       Destination: /x/_site
      Generating...
                    done in 3.2 seconds.
"""

def test_clean_log_has_no_problems():
    assert detect_problems(GOOD) == []

def test_liquid_exception_is_a_problem():
    log = GOOD + "Liquid Exception: Liquid syntax error (line 3): Unknown tag\n"
    assert detect_problems(log)

def test_deprecation_is_a_problem():
    assert detect_problems("Deprecation: pagination is now a plugin\n")

def test_jekyll_error_prefix_is_a_problem():
    assert detect_problems("  Error: could not read file foo: bar\n")

def test_normal_generating_line_is_not_a_problem():
    assert detect_problems("      Generating... \n                    done.\n") == []

def test_jekyll_conflict_is_a_problem():
    log = "          Conflict: The following destination is shared by multiple files.\n"
    assert detect_problems(log)

def test_bundler_resolves_to_a_command():
    # Debian ships 'bundle3.3'; most machines/CI ship 'bundle'. Either is fine.
    assert bundler()
