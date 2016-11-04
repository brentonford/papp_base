from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from rapui import LoggingSetup

global config
config = context.config

LoggingSetup.setup()

target_metadata = None


def include_object(object, name, type_, reflected, compare_to):
    # If it's not in this schema, don't include it
    if hasattr(object, 'schema') and object.schema != target_metadata.schema:
        return False

    return True


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        # Ensure the schema exists
        connection.execute('CREATE SCHEMA IF NOT EXISTS "%s" ' % target_metadata.schema)

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            include_schemas=True,
            version_table_schema=target_metadata.schema
        )

        with context.begin_transaction():
            context.run_migrations()
