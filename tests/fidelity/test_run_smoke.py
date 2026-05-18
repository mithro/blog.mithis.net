# tests/fidelity/test_run_smoke.py
import importlib
def test_run_module_imports():
    m = importlib.import_module("scripts.fidelity.run")
    assert hasattr(m, "main")
