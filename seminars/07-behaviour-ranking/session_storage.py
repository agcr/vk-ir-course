from pathlib import Path
from collections import Counter, defaultdict

from typing import List

import pandas as pd

from pyclick.utils.YandexRelPredChallengeParser import YandexRelPredChallengeParser
from pyclick.utils.Utils import Utils
from pyclick.search_session.SearchResult import SearchResult
from pyclick.search_session.SearchSession import SearchSession


class SessionStorage:
    """
    Простейшая обертка для хранения сессий.

    Наивно разбивает по session id на train/test:
        * train составляет N% всех сессий

        * test содержит те сессии из оставшихся (100-N)%,
        запрос в которых содержится в train части,
        т.е. объём <=(100-N)%

        * N = 75% по-умолчанию, для академических целей этого достаточно
    """

    def __init__(
        self, path: Path, parser=YandexRelPredChallengeParser(), ratio: float = 0.75
    ) -> None:
        self.path = path
        self.parser = parser

        self.sessions = self.parser.parse(self.path)

        self.train_test_split = int(len(self.sessions) * ratio)

        self.train_sessions = self.sessions[: self.train_test_split]
        self.train_queries = Utils.get_unique_queries(self.train_sessions)

        self.test_sessions = Utils.filter_sessions(
            self.sessions[self.train_test_split :], self.train_queries
        )
        self.test_queries = Utils.get_unique_queries(self.test_sessions)

    def get_train_sessions(self) -> List[SearchSession]:
        return self.train_sessions

    def get_train_queries(self) -> List[str]:
        return self.train_queries

    def get_test_sessions(self) -> List[SearchSession]:
        return self.test_sessions

    def get_test_queries(self) -> List[str]:
        return self.test_queries

    def get_document(self, query: str, is_clicked: bool) -> str:
        click = 1 if is_clicked else 0
        documents = Counter()

        for session in self.sessions:
            if session.query != query:
                continue

            for result in session.web_results:
                if result.click == click:
                    documents[result.id] += 1

        return documents.most_common(1)[0][0]

    def get_dataset(self) -> pd.DataFrame:
        # заполняем мапу: query -> {document -> clicks}
        docs_per_query = defaultdict(lambda: defaultdict(int))

        for session in self.sessions:
            for result in session.web_results:
                docs_per_query[session.query][result.id] += result.click

        queries = []
        doc_ids = []
        clicks = []

        for query, docs in docs_per_query.items():
            for doc_id, click in docs.items():
                queries.append(query)
                doc_ids.append(doc_id)
                clicks.append(click)

        df = pd.DataFrame.from_dict(
            {
                "query": queries,
                "document": doc_ids,
                "clicks": clicks,
            }
        )

        return df

    def get_test_dataset(self) -> pd.DataFrame:
        df = self.get_dataset()
        df = df[df["query"].isin(self.get_test_queries())]
        df["clicked"] = (df["clicks"] > 0).astype(int)
        df = df.drop(columns=["clicks"])
        return df.reset_index(drop=True)
