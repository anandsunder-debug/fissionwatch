import unittest
from fissionwatch.customer import (
    capacity_adjusted_sri, customer_experience_quality,
    customer_trust_index, reliability_adjusted_sri,
)


class CustomerMetricTests(unittest.TestCase):
    def test_capacity_adjusted_sri(self):
        self.assertAlmostEqual(capacity_adjusted_sri(.2, .5), .4)

    def test_rsri_is_bounded_by_base_factor_for_nonnegative_inputs(self):
        self.assertLessEqual(reliability_adjusted_sri(.2, .5, 1.0), .4)

    def test_ceq_is_bounded(self):
        value = customer_experience_quality(1.0, 0.0, 0.0)
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)

    def test_geometric_cti(self):
        self.assertAlmostEqual(customer_trust_index(1, 1, 1, 1), 1.0)


if __name__ == "__main__":
    unittest.main()
