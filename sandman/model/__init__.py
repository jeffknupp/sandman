"""The model module is responsible exposes the :class:`sandman.model.Model` class,
from which user models should derive. It also makes the :func:`register`
function available, which maps endpoints to their associated classes."""

from sandman.model.utils import register, activate, Model
