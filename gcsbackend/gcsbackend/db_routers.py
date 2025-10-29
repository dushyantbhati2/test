class MigrationRouter:
    """
    Route all migrations to the 'migrations' database (DIRECT_URL).
    All other queries go to 'default' (pooled).
    """

    def db_for_read(self, model, **hints):
        return "default"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Run migrations only on 'migrations' DB if defined
        return db == "migrations"
