# Generated by Django 2.1.15 on 2020-07-21 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_chat_id', models.CharField(db_index=True, max_length=100)),
                ('telegram_channel_id', models.CharField(max_length=100)),
                ('slack_team_id', models.CharField(blank=True, max_length=100, null=True)),
                ('slack_bot_token', models.CharField(blank=True, max_length=100, null=True)),
                ('slack_channel_name', models.CharField(blank=True, help_text='The Slack Channel the Bot will post to', max_length=100, null=True)),
            ],
        ),
    ]
