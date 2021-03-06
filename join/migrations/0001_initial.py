# Generated by Django 3.2.7 on 2021-09-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('nid', models.CharField(max_length=15, unique=True)),
                ('dept', models.CharField(max_length=20)),
                ('level', models.CharField(choices=[('B1', '大一'), ('B2', '大二'), ('B3', '大三'), ('B4', '大四'), ('M1', '碩一'), ('M2', '碩二')], default='B1', max_length=2)),
                ('phone', models.CharField(max_length=15, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('status', models.CharField(choices=[('NP', '未付款'), ('M', '已入社')], default='NP', max_length=2)),
                ('pay', models.CharField(choices=[('C', '現金'), ('R', '匯款')], default='C', max_length=2)),
                ('bankAccount', models.CharField(blank=True, max_length=5, null=True)),
                ('is_FCU', models.CharField(choices=[('Y', '逢甲大學'), ('N', '其他學校')], default='Y', max_length=5)),
                ('school', models.CharField(blank=True, max_length=50)),
                ('DiscordId', models.CharField(max_length=50, null=True)),
                ('clothes', models.CharField(choices=[('N', '不購買'), ('XXS', '尺寸 XXS'), ('XS', '尺寸 XS'), ('S', '尺寸 S'), ('M', '尺寸 M'), ('L', '尺寸 L'), ('XL', '尺寸 XL'), ('2XL', '尺寸 2XL')], default='N', max_length=4)),
                ('receiptNumber', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCUcount', models.IntegerField()),
                ('offFCUcount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='secret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('nid', models.CharField(max_length=15, unique=True)),
                ('phone', models.CharField(max_length=15, null=True, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
