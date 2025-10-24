from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='sports.sport')),
            ],
            options={
                'verbose_name': 'Sport Position',
                'verbose_name_plural': 'Sport Positions',
                'ordering': ['sport', 'name'],
                'unique_together': {('sport', 'code')},
            },
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=100),
        ),
    ]