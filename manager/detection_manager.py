import random

# from test_tool.temp_folder import temp_karel

def get_decicion(url: str):
    """
    0 - url is normal
    1 - url is malicious
    2 - url is not url
    :param url:
    :return:
    """
    decision = random.randint(0, 2)
    return decision


# temp_karel.print_func()