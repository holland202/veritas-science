import unittest
from veritas.attacks import attack
from veritas.cli import demo_protocol
from veritas.core import verify_envelope
from veritas.experiment import check_prediction, run
from veritas.protocol import freeze, validate_protocol

class TestVeritas(unittest.TestCase):
    def setUp(self):
        self.protocol = demo_protocol()
        self.data = [{"x": i / 100, "y": int(i >= 50)} for i in range(100)]

    def test_protocol_is_valid_and_hashed(self):
        self.assertEqual(validate_protocol(self.protocol), [])
        self.assertTrue(verify_envelope(freeze(self.protocol)))

    def test_verifier_attack_suite_passes(self):
        report = attack(self.protocol)
        self.assertTrue(report["passed"], report)

    def test_degenerate_result_is_rejected(self):
        result = {"n": 100, "accuracy": 1.0, "effect": 1.0}
        check = check_prediction(self.protocol["predictions"][0], result)
        self.assertEqual(check["status"], "NOT_SUPPORTED")
        self.assertIn("degenerate", check["reason"])

    def test_reference_run_is_deterministic(self):
        self.assertEqual(run(self.protocol, self.data), run(self.protocol, self.data))

    def test_invalid_data_is_rejected(self):
        with self.assertRaises(ValueError):
            run(self.protocol, [{"x": float("nan"), "y": 0}])

if __name__ == "__main__":
    unittest.main()
