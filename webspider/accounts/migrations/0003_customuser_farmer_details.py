from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='current_season',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='customuser',
            name='land_area_acres',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='land_survey_numbers',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='soil_type',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]
