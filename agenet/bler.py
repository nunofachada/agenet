import math
import argparse

import scipy.special as sp

# this function claculate block error rate for the given snr, n, k
# this function is used in the maincom.py file
# n is the number of bits in the block
# k is the number of bits in the message
# snr is the signal to noise ratio


def qfunc(x):
    """
    The Q-function is a mathematical function that gives the tail probability of the standard normal distribution.

    Parameters:
    x (float): input value for Q-function.

    Returns:
    float: value of the Q-function evaluated at x.
    """
    if x < 0:
        return 1
    return 0.5 - 0.5 * sp.erf(
        x / math.sqrt(2)
    )  # this function is the q function # this function is the q function


# The Q-function is a mathematical function that gives the tail probability of the standard normal distribution.


# Calculate the BLER for the given SNR, n, k
def blercal(snr, n, k):
    """
    Calculate the Block Error Rate (BLER) for the given SNR, n, k.

    Parameters:
    snr (float): Signal-to-Noise Ratio (SNR).
    n (int): Number of bits in the block.
    k (int): Number of bits in the message.

    Returns:
    float: Block Error Rate (BLER) for the given SNR, n, k.
    """
    if snr < 0:
        raise ValueError(
            "SNR must be non-negative"
        )  # testing the snr value is non-negative
    if n <= 0:
        raise ValueError(
            "n must be greater than 0"
        )  # testing the n value is greater than 0
    if k <= 0:
        raise ValueError(
            "k must be greater than 0"
        )  # testing the k value is greater than 0
    if k > n:
        raise ValueError(
            "k must be less than or equal to n"
        )  # testing the k value is less than or equal to n
    c = math.log2(1 + snr)  # this is the capacity of the channel
    v = 0.5 * (1 - (1 / (1 + snr) ** 2)) * ((math.log2(math.exp(1))) ** 2)
    # this is the variance of the channel
    err = qfunc(
        ((n * c) - k) / math.sqrt(n * v)
    )  # this function calculates the block error rate
    # ref. On the Evaluation of the Polyanskiy-Poor-Verdu Converse Bound for Finite Blocklength Coding in AWGN
    # if err > 1:
    # err = 1
    return err  # return the block error rate


def blercal_th(snr, n, k):  # this function calculates the theoretical block error rate
    """
    Calculate the theoretical Block Error Rate (BLER) for the given SNR, n, k.

    Parameters:
    snr (float): Signal-to-Noise Ratio (SNR).
    n (int): Number of bits in the block.
    k (int): Number of bits in the message.

    Returns:
    float: Theoretical Block Error Rate (BLER) for the given SNR, n, k.
    """
    beta = 1 / (
        2 * math.pi * math.sqrt((2 ** (2 * k / n)) - 1)
    )  # this is the beta value
    sim_phi = (2 ** (k / n)) - 1  # this is the phi value
    phi_bas = sim_phi - (1 / (2 * beta * math.sqrt(n)))  # this is the phi value
    delta = sim_phi + (1 / (2 * beta * math.sqrt(n)))
    err_th = 1 - (
        (beta * math.sqrt(n) * snr)
        * (math.exp(-1 * phi_bas * (1 / snr)) - math.exp(-1 * delta * (1 / snr)))
    )
    return err_th
if __name__ == "__main__":
    """
    This is the main function that is called when the file is run directly.
    command line arguments are used to calculate the block error rate.
    """

    parser = argparse.ArgumentParser(description="Block Error Rate Calculation")
    parser.add_argument("--snr", type=float, help="Signal-to-Noise Ratio (SNR)")
    parser.add_argument("--n", type=int, help="Number of bits in the block")
    parser.add_argument("--k", type=int, help="Number of bits in the message")
    parser.add_argument(
        "--theory",
        action="store_true",
        help="Calculate theoretical Block Error Rate (BLER)",
    )

    args = parser.parse_args()

    snr = args.snr
    n = args.n
    k = args.k
    theory = args.theory

    if snr is None or n is None or k is None:
        parser.print_help()
    else:
        if theory:
            err_th = blercal_th(snr, n, k)
            print(f"Theoretical BLER: {err_th}") # this prints the theoretical block error rate
        else:
            err = blercal(snr, n, k)
            print(f"BLER: {err}") # this prints the block error rate simulated
