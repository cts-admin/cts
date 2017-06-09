from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from slackclient import SlackClient
import time


class Command(BaseCommand):
    help = 'Powers up the bot and gives it life.'

    def handle(self, *args, **options):
        client = SlackClient(settings.SLACK_BOT_TOKEN)
        if client.rtm_connect():
            while True:
                events = client.rtm_read()
                for event in events:
                    if 'type' not in event:
                        continue
                    elif event['type'] == 'message' and event['text'] == 'data form':
                        client.rtm_send_message(
                            event['channel'],
                            "You can find the SOS data form here: "
                            "https://www.blm.gov/sites/blm.gov/files/program_nativeplants_collection_homepage_SOS%20Data%20Form%20Word%20Doc.docx",
                        )
                time.sleep(1)
