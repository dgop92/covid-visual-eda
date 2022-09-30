from typing import List


def get_mean(data: List[float]) -> float:
    """Return the mean of a list of numbers"""
    return sum(data) / len(data)


def get_standard_deviation(data: List[float], mean: float) -> float:
    """Return the standard deviation of a list of numbers"""
    return (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5


def get_z_score(mean: float, standard_deviation: float, value: float) -> float:
    """Return the z-score of a value"""
    return (value - mean) / standard_deviation
