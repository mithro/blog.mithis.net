# tests/fidelity/test_wayback.py
import io, json
from scripts.fidelity.wayback import parse_availability, snapshot_url

def test_parse_returns_url_when_available():
    payload = {"archived_snapshots": {"closest": {
        "available": True, "url": "http://web.archive.org/web/2016/https://blog.mithis.net/"}}}
    assert parse_availability(payload).startswith("http://web.archive.org/web/")

def test_parse_returns_none_when_empty():
    assert parse_availability({"archived_snapshots": {}}) is None
    assert parse_availability({}) is None

def test_snapshot_url_uses_injected_opener():
    body = json.dumps({"archived_snapshots": {"closest": {
        "available": True, "url": "http://web.archive.org/web/x"}}}).encode()
    class Resp(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): return False
    captured = {}
    def fake_opener(url, timeout=0):
        captured["url"] = url
        return Resp(body)
    out = snapshot_url("https://blog.mithis.net/archives/tp/15-tp-protocol-overview",
                       "20120101", opener=fake_opener)
    assert out == "http://web.archive.org/web/x"
    assert "blog.mithis.net" in captured["url"] and "timestamp=20120101" in captured["url"]
