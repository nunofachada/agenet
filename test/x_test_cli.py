"""Tests for the CLI module."""

from unittest.mock import MagicMock, patch

import pytest

from agenet.cli import _main


# Helper function to setup mock args
def setup_mock_args(**kwargs):
    """Setup mock args for testing."""
    default_args = {
        "num_nodes_const": 2,
        "active_prob_const": 0.5,
        "n_const": 150,
        "k_const": 100,
        "P_const": 2 * (10**-3),
        "d_const": 700,
        "N0_const": 1 * (10**-13),
        "fr_const": 6 * (10**9),
        "numevnts": 500,
        "numruns": 100,
        "quiet": False,
        "plots": False,
        "plots_folder": None,
        "blockerror": False,
        "snr": False,
        "csv_location": None,
        "num_nodes_vals": [1, 2, 3, 4, 5],
        "active_prob_vals": [0.1, 0.15, 0.2, 0.25],
        "n_vals": [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250],
        "k_vals": [50, 60, 70, 80, 90, 95, 100],
        "P_vals": [2 * (10**-3), 4 * (10**-3), 6 * (10**-3), 8 * (10**-3)],
        "seed": None,  # Add seed parameter with default value None
    }
    default_args.update(kwargs)
    mock_args = MagicMock(**default_args)
    return mock_args


@pytest.fixture()
def mock_dependencies():
    """Fixture for mocking dependencies."""
    with patch(
        "agenet.cli.argparse.ArgumentParser.parse_args"
    ) as mock_parse_args, patch("agenet.cli.plot") as mock_plot, patch(
        "agenet.cli.generate_table"
    ) as mock_generate_table, patch(
        "agenet.cli.snr_th"
    ) as mock_snr_th, patch(
        "agenet.cli.blercal_th"
    ) as mock_blercal_th:
        yield {
            "mock_parse_args": mock_parse_args,
            "mock_plot": mock_plot,
            "mock_generate_table": mock_generate_table,
            "mock_snr_th": mock_snr_th,
            "mock_blercal_th": mock_blercal_th,
        }


# Test default behavior without specific flags
def test_main_default_behavior(mock_dependencies):
    """Test the default behavior of the main function."""
    mock_args = setup_mock_args()
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_generate_table"].assert_called_once()
    mock_dependencies["mock_plot"].assert_not_called()
    mock_dependencies["mock_snr_th"].assert_not_called()
    mock_dependencies["mock_blercal_th"].assert_not_called()


# Test behavior with --plots flag
def test_main_with_plots(mock_dependencies):
    """Test the behavior of the main function with the --plots flag."""
    mock_args = setup_mock_args(plots=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_plot"].assert_called_once()
    # Check if plot was called with the correct seed (None in this case)
    args, kwargs = mock_dependencies["mock_plot"].call_args
    assert "seed" in kwargs
    assert kwargs["seed"] is None


# Test behavior with --snr flag
def test_main_with_snr(mock_dependencies):
    """Test the behavior of the main function with the --snr flag."""
    mock_args = setup_mock_args(snr=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_snr_th"].assert_called_once()


# Test behavior with --blockerror flag
def test_main_with_blockerror(mock_dependencies):
    """Test the behavior of the main function with the --blockerror flag."""
    mock_args = setup_mock_args(blockerror=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_blercal_th"].assert_called_once()


# New test to check behavior with seed
def test_main_with_seed(mock_dependencies):
    """Test the behavior of the main function with a specified seed."""
    mock_args = setup_mock_args(seed=42)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    # Check if generate_table was called with the correct seed
    mock_dependencies["mock_generate_table"].assert_called_once()
    _, kwargs = mock_dependencies["mock_generate_table"].call_args
    assert kwargs.get("seed") == 42


# New test to check seed handling with plots
def test_main_with_plots_and_seed(mock_dependencies):
    """Test the behavior of the main function with plots and a specified seed."""
    mock_args = setup_mock_args(plots=True, seed=42)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_plot"].assert_called_once()
    # Check if plot was called with the correct seed
    args, kwargs = mock_dependencies["mock_plot"].call_args
    assert "seed" in kwargs
    assert kwargs["seed"] == 42


# New test to check reproducibility with the same seed
def test_main_reproducibility(mock_dependencies):
    """Test that the main function produces the same results with the same seed."""
    mock_args = setup_mock_args(seed=42)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()
    first_call_args = mock_dependencies["mock_generate_table"].call_args

    mock_dependencies["mock_generate_table"].reset_mock()

    _main()
    second_call_args = mock_dependencies["mock_generate_table"].call_args

    assert (
        first_call_args == second_call_args
    ), "Results are not reproducible with the same seed"


# New test to check different results with different seeds
def test_main_different_seeds(mock_dependencies):
    """Test that the main function produces different results with different seeds."""
    mock_args1 = setup_mock_args(seed=42)
    mock_args2 = setup_mock_args(seed=123)

    mock_dependencies["mock_parse_args"].side_effect = [mock_args1, mock_args2]

    _main()
    first_call_args = mock_dependencies["mock_generate_table"].call_args

    mock_dependencies["mock_generate_table"].reset_mock()

    _main()
    second_call_args = mock_dependencies["mock_generate_table"].call_args

    assert (
        first_call_args != second_call_args
    ), "Results are identical with different seeds"
    assert first_call_args[1]["seed"] == 42
    assert second_call_args[1]["seed"] == 123
