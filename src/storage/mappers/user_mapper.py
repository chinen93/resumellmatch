from src.core.models import User as UserModel
from src.storage.mappers.star_mapper import StarMetadataMapper
from src.storage.models import User


class UserMapper:
    @staticmethod
    def to_core_model(storage_model: User) -> UserModel:
        return UserModel(
            id=storage_model.id,
            name=storage_model.name,
            email=storage_model.email,
            star_metadatas=[
                StarMetadataMapper.to_core_model(meta)
                for meta in storage_model.star_metadatas
            ],
        )

    @staticmethod
    def to_storage_model(core_model: UserModel) -> User:
        return User(
            id=core_model.id,
            name=core_model.name,
            email=core_model.email,
            star_metadatas=[
                StarMetadataMapper.to_storage_model(meta)
                for meta in core_model.star_metadatas
            ],
        )

    @staticmethod
    def from_raw_fields(name: str, email: str) -> UserModel:
        """Builds the core model directly from raw input fields."""
        return UserModel(
            name=name,
            email=email,
        )
