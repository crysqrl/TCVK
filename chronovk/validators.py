from chronovk.exceptions import WrongIdException


def id_validator(cid):
    """Validates over negative id and str id"""
    if not isinstance(cid, int) or cid < 0:
        raise WrongIdException("Wrong id")
    return True
