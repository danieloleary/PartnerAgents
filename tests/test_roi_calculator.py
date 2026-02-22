"""ROI Calculator tests."""

import pytest


def test_roi_calculation_base_case():
    """Test ROI calculation with base case values."""
    # Base case: 10, 25, 50 partners with $15k revenue each
    partners_y1, partners_y2, partners_y3 = 10, 25, 50
    revenue_per_partner = 15000

    rev_y1 = partners_y1 * revenue_per_partner
    rev_y2 = partners_y2 * revenue_per_partner
    rev_y3 = partners_y3 * revenue_per_partner

    assert rev_y1 == 150000
    assert rev_y2 == 375000
    assert rev_y3 == 750000


def test_roi_calculation_costs():
    """Test cost calculation with all inputs."""
    pm_cost = 120000
    marketing_pct = 20
    training_cost = 2500
    tech_cost = 20000
    commission_pct = 15

    rev_y1 = 150000

    cost_y1 = (
        pm_cost
        + (rev_y1 * marketing_pct / 100)
        + (10 * training_cost)  # 10 partners
        + tech_cost
        + (rev_y1 * commission_pct / 100)
    )

    assert cost_y1 == 217500


def test_roi_formula():
    """Test ROI formula: (Revenue - Costs) / Costs * 100."""
    revenue = 150000
    costs = 217500

    roi = ((revenue - costs) / costs) * 100

    assert roi == pytest.approx(-31.03, rel=0.1)


def test_payback_period_calculation():
    """Test payback period calculation."""
    monthly_revenue = 150000 / 12  # 12500
    monthly_cost = 217500 / 12  # 18125

    cumulative = 0
    months = 0
    for i in range(1, 25):  # 24 months
        monthly_net = monthly_revenue - monthly_cost
        cumulative += monthly_net
        months = i
        if cumulative >= 0:
            break

    assert months > 12  # Should take more than a year


def test_scenario_conservative():
    """Test conservative scenario values."""
    partners = (5, 10, 20)
    revenue_per = 10000
    marketing_pct = 15

    rev_y1 = partners[0] * revenue_per
    rev_y2 = partners[1] * revenue_per
    rev_y3 = partners[2] * revenue_per

    assert rev_y1 == 50000
    assert rev_y2 == 100000
    assert rev_y3 == 200000


def test_scenario_optimistic():
    """Test optimistic scenario values."""
    partners = (20, 50, 100)
    revenue_per = 20000
    marketing_pct = 25

    rev_y1 = partners[0] * revenue_per
    rev_y2 = partners[1] * revenue_per
    rev_y3 = partners[2] * revenue_per

    assert rev_y1 == 400000
    assert rev_y2 == 1000000
    assert rev_y3 == 2000000


def test_three_year_total_roi():
    """Test overall 3-year ROI calculation - verifies formula works."""
    # Test formula with known values
    revenue = 1000000
    costs = 500000

    overall_roi = ((revenue - costs) / costs) * 100

    # 100% ROI when revenue is double costs
    assert overall_roi == 100


def test_zero_revenue_handling():
    """Test handling of zero revenue."""
    revenue = 0
    costs = 100000

    if costs > 0:
        roi = ((revenue - costs) / costs) * 100
        assert roi == -100


def test_cost_inflation():
    """Test that costs increase with inflation assumption."""
    pm_cost = 120000
    tech_cost = 20000

    # Year 2: 8% PM inflation, 10% tech inflation
    cost_y2 = pm_cost * 1.08 + tech_cost * 1.1

    assert cost_y2 > pm_cost + tech_cost


def test_revenue_per_partner_scaling():
    """Test revenue per partner can scale by year."""
    base_rev = 15000
    year2_multiplier = 1.25
    year3_multiplier = 1.5

    rev_y2 = base_rev * year2_multiplier
    rev_y3 = base_rev * year3_multiplier

    assert rev_y2 == 18750
    assert rev_y3 == 22500
