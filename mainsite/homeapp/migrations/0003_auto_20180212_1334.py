# Generated by Django 2.0.1 on 2018-02-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0002_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdf',
            name='user',
        ),
        migrations.AddField(
            model_name='pdf',
            name='university',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='pdf',
            name='uploaders',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='pdfName',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='pdf_desc',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='pdf_title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='professor_name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='subjectName',
            field=models.TextField(blank=True),
        ),
    ]