from sqlalchemy import func

from finance_portfolio import db
from finance_portfolio.model.nasdaq import Nasdaq


class NasdaqRepository:

    @staticmethod
    def search_name(query):
        # regex_pattern = f'.*{query}.*'
        # results = Nasdaq.query.filter(Nasdaq.name.op('REGEXP')(regex_pattern)).all()
        # return results
        # return Nasdaq.query.filter(Nasdaq.name.like(f'%{query}%')).all()

        results = (
            db.session.query(
                Nasdaq.name,
                Nasdaq.ticker,
                func.instr(Nasdaq.name, query).label('position')
            )
            .filter(Nasdaq.name.op('REGEXP')(f'.*{query}.*'))
            .order_by(
                func.instr(Nasdaq.name, query),  # Order by position of the search term
                Nasdaq.name  # Secondary sort to maintain consistent order
            )
            .limit(10)
            .all()
        )

        return results