from veritas.experiment import run
from veritas.cli import demo_protocol
from veritas.protocol import freeze


def test_experiment_reports_package_version():
    result = run(
        freeze(demo_protocol())["payload"],
        [{"x": 0.0, "y": 0}, {"x": 1.0, "y": 1}],
        seed=1,
    )
    assert result["environment"]["veritas"] == "0.1.1"
