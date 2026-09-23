from veritas.adapters.hai import sentinel_hai_adapter


def test_hai_adapter_metadata_is_pinned():
    adapter = sentinel_hai_adapter()
    assert adapter.repository == "https://github.com/holland202/sentinel-hai-validation"
    assert adapter.commit == "1faf2e2e6f002f76c92d52e931842b6bd2634eaa"
    assert adapter.name == "sentinel_hai"
    assert adapter.limitations


def test_hai_protocol_name_remains_explicit():
    adapter = sentinel_hai_adapter()
    result = adapter.run()
    assert result.result["protocol_name"] == "sentinel_hai_validation"
