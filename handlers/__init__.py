from .genders import gender_labeler
from .age import age_labeler
from .names import names_labeler
from .misc_handlers import misc_labeler


labelers = [gender_labeler, age_labeler, names_labeler, misc_labeler]

__all__ = ('labelers', )