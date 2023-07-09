# Program to watch new manga releases for Panini Manga
Wrote this for my GF so she won't miss any new releases and (hopefully) get notified the next day that the release happens.

# Usage
## Requirements
Create a file called "gmailSecrets.py" and in there put the following:
```python
gmailSender = "<sender_email_address>"
gmailPassword = "<application_password_for_sender_email_address>"
```
Read more about application passwords [here](https://support.google.com/accounts/answer/185833).

## Running
```bash
python3 PaniniMangaReleaseWatcher.py <email_that_you_want_the_notification_to_be_sent_to>
```
### Example:
```bash
python3 PaniniMangaReleaseWatcher.py test@example.com
```

## Set up cronjob
The script is meant to be run every day at 10:00 AM. To do this, you can set up a cronjob. To do this, run the following command:
```bash
crontab -e
```
And write the following line:
```bash
0 10 * * * cd /path/to/the/script && python3 /path/to/PaniniMangaReleaseWatcher.py <email_that_you_want_the_notification_to_be_sent_to>
```

## Add more mangas to track
To add more mangas to track, simply add the manga name to the list in the "mangas.json" file. For example, if you want to track "Dragon Ball Super", you would add the following line to the file:
```json
{"mangas": [{"name": "sasaki to miyano", "items": 5}, {"name": "DEMON SLAYER CUADERNO PARA COLOREAR", "items": 3}, {"name": "Dragon Ball Super", "items": 0}]}
```
The safest bet is to set the items to 0. You will get an email the first time for the manga you added but after the first time it will update the JSON file with the latest releases amount and you will only get an email when the releases amount changes.

# Limitations
- This script only works for Panini Manga.
- It only checks the number of items returned for the search query, so it will not work correctly if:
 1. Records are removed from the search results.
 2. A record is added and another one is removed (items would remain the same and the program would not detect the change).

The last limitation can be fixed by also checking the names for the records returned, but I don't think it's worth the effort right now. If you want to do it, feel free to do so and open a PR :) .