"""Signal-to-noise ratio (SNR) calculator."""
import argparse
import math

import numpy as np


def snr(N0: float, d: float, P: float, fr: float) -> float:
    """Computes the SNR of the received signal.

    Args:
      N0: The power spectral density of the noise.
      d: The distance between the transmitter and receiver.
      P: The power of the transmitted signal.
      fr: The frequency of the signal.

    Returns:
      The SNR of the received signal in linear scale.
    """
    alpha = _alpha(d, fr)
    snr: float = (alpha * P * np.random.exponential(1)) / N0
    return snr


def snr_th(N0: float, d: float, P: float, fr: float) -> float:
    """Calculates the theoretical SNR of the received signal.

    Args:
      N0: The power spectral density of the noise.
      d: The distance between the transmitter and receiver.
      P: The power of the transmitted signal.
      fr: The frequency of the signal.

    Returns:
      The theoretical SNR of the received signal in linear scale.
    """
    alpha = _alpha(d, fr)
    snr_th: float = (alpha * P) / N0
    return snr_th


def _alpha(d: float, fr: float) -> float:
    """Calculates the path loss in linear scale.

    Args:
      d: The distance between the transmitter and receiver.

    Returns:
      The path loss in linear scale.
    """
    f = fr  # frequency of the signal
    C: float = 3 * (10**8)  # speed of light
    log_alpha: float = (20 * math.log10(d)) + (
        20 * math.log10((4 * f * math.pi) / C)
    )  # path loss in dB
    alpha: float = 1 / (10 ** ((log_alpha) / 10))  # path loss in linear scale
    return alpha


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate signal-to-noise ratio (SNR)."
    )
    parser.add_argument("-N0", type=float, help="Power spectral density of the noise")
    parser.add_argument(
        "-d",
        type=float,
        help="Distance between the transmitter and receiver",
    )
    parser.add_argument("-fr", type=float, help="Frequency of the signal")
    parser.add_argument("-P", type=float, help="Power of the transmitted signal")
    args = parser.parse_args()

    if args.N0 is not None and args.d is not None and args.P is not None:
        snr_val = snr(args.N0, args.d, args.P, args.fr)
        snr_th_val = snr_th(args.N0, args.d, args.P, args.fr)
        print(f"SNR: {snr_val}")
        print(f"Theoretical SNR: {snr_th_val}")
