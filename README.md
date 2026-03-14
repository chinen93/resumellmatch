# ResumeLLMatch

## Development

### Database Migrations Alembic

#### Generate a Migration Script

```sh
alembic revision --autogenerate -m "Add a description of your change"
```

#### Review and Apply Migrations

```sh
alembic upgrade head
```

Downgrade if needed
```sh
alembic downgrade -1
```