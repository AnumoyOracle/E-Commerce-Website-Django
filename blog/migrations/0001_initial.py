# Generated by Django 5.1 on 2024-09-07 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=200)),
                ('head0', models.CharField(default='', max_length=200)),
                ('chead0', models.CharField(default='', max_length=10000)),
                ('head1', models.CharField(default='', max_length=200)),
                ('chead1', models.CharField(default='', max_length=10000)),
                ('head2', models.CharField(default='', max_length=200)),
                ('chead2', models.CharField(default='', max_length=10000)),
                ('pub_date', models.DateField()),
                ('image', models.ImageField(default='', upload_to='blog/img')),
            ],
        ),
    ]