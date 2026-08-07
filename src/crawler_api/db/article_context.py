from src.crawler_api.db.data_access_context import DataAccessContext
from src.crawler_api.repository.article_repository import ArticleRepository


class ArticleContext(DataAccessContext):
    def __init__(
        self,
        client,
        transaction: bool=False
    ):

        super().__init__(
            client,
            repository_factories={
                ArticleRepository: lambda session: ArticleRepository(session=session)
            },
            transaction=transaction
        )


    @property
    def articles(self) -> ArticleRepository:
        return self.get_repository(ArticleRepository)