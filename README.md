# instagram-story-offer-posting-bot

This is a in-progress, hobby-study-like project.

A bot that:
- [x] parses offer urls from an input.txt file (currently, only from amazon.com.br);
- [x] scrapes offer data (currently: a title/description, a thumbnail, a "before" price, a "now" price, and the discount rate);
- [x] creates offer images with 720 by 1080 pixels resolution;
- [x] connects do a physical, debug ready Android phone (I'm using a POCO X3 NFC) using pure-python-adb (ppadb);
- [x] pushes offer images to the phone's SD card; and
- [x] launches phone's Instagram app and posts offer images (with url stickers with offer urls in them).
