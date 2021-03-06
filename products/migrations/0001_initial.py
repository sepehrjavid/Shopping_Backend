# Generated by Django 3.1.1 on 2020-10-16 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('amount', models.IntegerField()),
                ('rating', models.FloatField(default=0)),
                ('brand', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('C', 'Cloth'), ('S', 'Sport tool')], max_length=1)),
                ('color', models.ManyToManyField(to='products.Color')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MultiPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='SportTool',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('size', models.ManyToManyField(to='products.Size')),
            ],
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='Cloth',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('material', models.CharField(max_length=50)),
                ('size', models.ManyToManyField(to='products.Size')),
            ],
            bases=('products.product',),
        ),
    ]
