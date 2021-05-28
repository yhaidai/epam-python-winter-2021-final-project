"""
Base class for services that use different loading strategies for nested
fields, this module defines the following classes:

- `StrategizedService`, service that uses different loading strategies for
nested fields
"""

from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, \
    raiseload, noload


class StrategizedService:
    """
    Service that uses different loading strategies for nested fields
    """
    # pylint: disable=too-few-public-methods

    #: set of supported loading strategies
    strategies = {
        lazyload, joinedload, subqueryload, selectinload, raiseload, noload
    }

    @classmethod
    def _check_strategy(cls, strategy):
        """
        Checks whether given strategy is supported, raises ValueError if not

        :param strategy: loading strategy to be checked
        :raise ValueError: in case of given strategy being unsupported
        :return: None
        """
        if strategy not in cls.strategies:
            raise ValueError(
                f'Unsupported strategy. Only {cls.strategies} are allowed')
