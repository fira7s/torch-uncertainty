import torch
from einops import rearrange
from torch.distributions import Distribution, Laplace, Normal


def cat_dist(distributions: list[Distribution], dim: int) -> Distribution:
    r"""Concatenate a list of distributions into a single distribution.

    Args:
        distributions (list[Distribution]): The list of distributions.
        dim (int): The dimension to concatenate.

    Returns:
        Distribution: The concatenated distributions.
    """
    dist_type = type(distributions[0])
    if not all(
        isinstance(distribution, dist_type) for distribution in distributions
    ):
        raise ValueError("All distributions must have the same type.")

    if isinstance(distributions[0], Normal | Laplace):
        locs = torch.cat(
            [distribution.loc for distribution in distributions], dim=dim
        )
        scales = torch.cat(
            [distribution.scale for distribution in distributions], dim=dim
        )
        return dist_type(loc=locs, scale=scales)
    raise NotImplementedError(
        f"Concatenation of {dist_type} distributions is not supported."
        "Raise an issue if needed."
    )


def squeeze_dist(distribution: Distribution, dim: int) -> Distribution:
    """Squeeze the distribution along a given dimension.

    Args:
        distribution (Distribution): The distribution to squeeze.
        dim (int): The dimension to squeeze.

    Returns:
        Distribution: The squeezed distribution.
    """
    dist_type = type(distribution)
    if isinstance(distribution, Normal | Laplace):
        loc = distribution.loc.squeeze(dim)
        scale = distribution.scale.squeeze(dim)
        return dist_type(loc=loc, scale=scale)
    raise NotImplementedError(
        f"Squeezing of {dist_type} distributions is not supported."
        "Raise an issue if needed."
    )


def to_ensemble_dist(
    distribution: Distribution, num_estimators: int = 1
) -> Distribution:
    dist_type = type(distribution)
    if isinstance(distribution, Normal | Laplace):
        loc = rearrange(distribution.loc, "(n b) c -> b n c", n=num_estimators)
        scale = rearrange(
            distribution.scale, "(n b) c -> b n c", n=num_estimators
        )
        return dist_type(loc=loc, scale=scale)
    raise NotImplementedError(
        f"Ensemble distribution of {dist_type} is not supported."
        "Raise an issue if needed."
    )
