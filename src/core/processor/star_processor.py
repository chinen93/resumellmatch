from src.storage.models import StarMetadata


class StarMetadataProcessor:
    # Handle the connection with the repository

    def new_item(
        self, user_id, type, title, subtitle, location, start_date, end_date
    ) -> None:
        _ = StarMetadata(
            user_id=user_id,
            type=type,
            title=title,
            subtitle=subtitle,
            location=location,
            start_date=start_date,
            end_date=end_date,
        )
