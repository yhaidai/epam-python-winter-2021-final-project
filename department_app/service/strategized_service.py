from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, \
    raiseload, noload


class StrategizedService:
    strategies = {
        lazyload, joinedload, subqueryload, selectinload, raiseload, noload
    }

    @classmethod
    def _check_strategy(cls, strategy):
        if strategy not in cls.strategies:
            raise ValueError(
                f'Unsupported strategy. Only {cls.strategies} are allowed')
