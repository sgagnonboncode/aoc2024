def read_lines(path) -> list[str]:
    """Enumerate lines in a file.

    Args:
        path (str): path to file

    Returns:
        list[str]: list of lines in file
    """
    with open(path, "r") as f:
        return f.readlines()
