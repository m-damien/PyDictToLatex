import numpy as np
from collections import Counter

def pround(value, decimals=3):
    """
    Round a number to the specificied decimals. Leading and trailing zeros are removed
    """
    val = round(value, decimals).__str__()
    return val.rstrip('0').rstrip('.') if '.' in val else val

def continuous_variables_to_dict(values, decimals=1, bins=None):
    """
    Generate a dictionnary for a list of continuous variables and add a bunch of useful metrics (mean, median, min, max, std, count, sum)
    """
    json = {"values": values, "min": int(np.min(values)), "max": int(np.max(values)), 
            "mean": pround(np.mean(values), decimals), "median": pround(np.median(values), decimals), "std": pround(np.std(values), decimals), 
            "count": len(values), "sum": int(np.sum(values))}
    if bins:
        # Compute distribution of values
        distribution = np.histogram(values, bins=bins, density=True)[0]
        json['distribution'] = ",".join(map(lambda v: str(pround(v, decimals)), distribution))

    return json

def categorical_variables_to_dict(values, decimals=1):
    """
    Generate a dictionary for a list if categorical variables (count the occurences of each elements, percentage, order)
    """
    dictionary = {}
    counter = Counter(values)
    sorted_count = counter.most_common()
    dictionary["unique"] = len(sorted_count)
    dictionary["count"] = len(values)
    dictionary["descending"] = {}
    dictionary["ascending"] = {}
    for idx, (element, count) in enumerate(sorted_count):
        dictionary[element] = {
            "count": count,
            "percent": pround((count/len(values))*100, decimals)
        }
        dictionary["descending"][str(idx+1)] = element
        dictionary["ascending"][str(len(sorted_count)-idx)] = element

    return dictionary