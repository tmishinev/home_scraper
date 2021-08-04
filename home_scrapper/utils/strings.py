# -*- coding: utf-8 -*-


def extract_digits(string: str):
    """Extracts digits from strings!"""
    return "".join(c for c in string if c.isdigit())


def strip_digits(string: str):
    """Extracts non digits from strings!"""
    return "".join(c for c in string if not c.isdigit()).strip()
