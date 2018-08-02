from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from app.models import Image, ImageClass

import urllib.request


class Parser:
    def __init__(self, srcfile):
        self.soup = BeautifulSoup(srcfile, "html.parser")

    def parse_record(self, node):
        return Image(
            image_id=node['data-mark-id'],
            description=node.h3.text)

    def parse_classes(self, node):
        return [int(ch.text) for ch in node.children]

    def parse(self):
        body = self.soup.find("body")
        images = []
        for ch in body.children:
            if ch.name != u'div':
                raise CommandError("Unexpected tag {} instead of 'div'." % ch.name)
            images.append((self.parse_record(ch), self.parse_classes(ch.ul)))
        return images


class Command(BaseCommand):
    help = 'Get signs with classes and fill up Image table.'

    def handle(self, *args, **options):
        print("Retrieving data from remote {}...".format(settings.GETDATA_URL))
        f = urllib.request.urlopen(settings.GETDATA_URL)
        # TODO: handle IO error
        print("Parsing the obtained file...")
        images = Parser(f).parse()
        print("Deleting old objects...")
        Image.objects.all().delete()

        print("Saving new {} objects.".format(len(images)))
        image_classes = []
        for img, class_numbers in images:
            img.save()
            image_classes.extend(ImageClass(image=img, class_number=cls) for cls in class_numbers)
        ImageClass.objects.bulk_create(image_classes)
        print("{} objects saved".format(len(images)))
