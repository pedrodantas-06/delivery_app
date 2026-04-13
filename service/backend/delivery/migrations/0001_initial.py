from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='DelivererModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=30)),
                ('region', models.CharField(max_length=80)),
                ('status', models.CharField(max_length=20)),
            ],
            options={'db_table': 'deliverers'},
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=80)),
                ('status', models.CharField(max_length=20)),
                ('assigned_deliverer_id', models.UUIDField(blank=True, null=True)),
            ],
            options={'db_table': 'orders'},
        ),
    ]
