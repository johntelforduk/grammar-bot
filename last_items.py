
def last_n_items(parm_list: list, n: int) -> list:
    """Return the last n items of parm list in reverse order."""
    if len(parm_list) >= n:
        return parm_list[:len(parm_list) - (n + 1):-1]
    else:
        return parm_list[::-1]
