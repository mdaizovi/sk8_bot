# Generated by Django 2.1.15 on 2020-10-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks_consumer', '0006_auto_20201019_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='botoutput',
            old_name='output_channel',
            new_name='output_telegram_channel',
        ),
        migrations.AddField(
            model_name='botoutput',
            name='output_slack_channel',
            field=models.CharField(blank=True, help_text='The Slack Channel the Bot will post to', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='botoutput',
            name='output_function',
            field=models.CharField(choices=[('doggo', 'doggo'), ('kitty', 'kitty'), ('fox', 'fox'), ('compliment', 'compliment'), ('insult', 'insult'), ('taco', 'taco'), ('broadcast_message', 'broadcast_message')], help_text='Function that gets text or image that will be sent somewhere', max_length=20),
        ),
    ]
