from django.db import models
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now
from django.apps.registry import Apps


def override_db_table_django_migration(plataforma):
    """
    Função usada para adicionar prefixo na tabela de migrations, deve ser importada e colocada antes das declarações
    de urls em todas as plataformas com o prefixo específico para cada plataforma
    """

    class Migration(models.Model):
        app = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
        applied = models.DateTimeField(default=now)

        class Meta:
            apps = Apps()
            app_label = "migrations"
            db_table = f"{plataforma}_django_migrations"

        def __str__(self):
            return "Migration %s for %s" % (self.name, self.app)

    MigrationRecorder._migration_class = Migration
