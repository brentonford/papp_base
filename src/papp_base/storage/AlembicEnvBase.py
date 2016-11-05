from alembic import context
from sqlalchemy import engine_from_config, pool

from rapui import LoggingSetup


class AlembicEnvBase:
    def __init__(self, targetMetadata):
        LoggingSetup.setup()

        self._config = context.config
        self._targetMetadata = targetMetadata
        self._schemaName = targetMetadata.schema

    def _includeObjectFilter(self, object, name, type_, reflected, compare_to):
        # If it's not in this schema, don't include it
        if hasattr(object, 'schema') and object.schema != self._schemaName:
            return False

        return True

    def run(self):
        """Run migrations in 'online' mode.
    
        In this scenario we need to create an Engine
        and associate a connection with the context.
    
        """
        connectable = engine_from_config(
            self._config.get_section(self._config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool)

        with connectable.connect() as connection:
            # Ensure the schema exists
            connection.execute('CREATE SCHEMA IF NOT EXISTS "%s" ' % self._schemaName)

            context.configure(
                connection=connection,
                targetMetadata=self._targetMetadata,
                include_object=self._includeObjectFilter,
                include_schemas=True,
                version_table_schema=self._schemaName
            )

            with context.begin_transaction():
                context.run_migrations()
