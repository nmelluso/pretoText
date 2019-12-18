import math

__all__ = ["cosine_similarity"]


def cosine_similarity(v1, v2):
    """
    Compute cosine similarity of v1 to v2 as: 

    .. math::

        \\frac{(v1 \\cdot v2)}{{||v1||*||v2||}}
    
    """
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    if sumxx == 0.0 or sumyy == 0.0:
        return 0.0
    return sumxy / math.sqrt(sumxx * sumyy)
