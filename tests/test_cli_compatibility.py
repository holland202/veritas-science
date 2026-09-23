from veritas.cli import demo_protocol
from veritas.protocol import validate_protocol


def test_demo_protocol_is_valid():
    assert validate_protocol(demo_protocol()) == []
    assert demo_protocol()["predictions"][0]["refutes_claim"] is False
