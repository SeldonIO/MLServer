from .repository import ModelRepository, SchemalessModelRepository
from ..settings import Settings


class ModelRepositoryFactory:
    @staticmethod
    def resolve_model_repository(settings: Settings) -> ModelRepository:
        result: ModelRepository
        if not settings.model_repository_implementation:
            settings.model_repository_implementation = SchemalessModelRepository

        result = settings.model_repository_implementation(
            root=settings.model_repository_root,
            **settings.model_repository_implementation_args,
        )

        return result
