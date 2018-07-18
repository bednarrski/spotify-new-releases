rm -f ~/Logs/spotiffy_news_log.older
mv ~/Logs/spotiffy_news_log.old ~/Logs/spotiffy_news_log.older
mv ~/Logs/spotiffy_news_log.txt ~/Logs/spotiffy_news_log.old
~/anaconda3/envs/py36/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases.py >> ~/Logs/spotiffy_news_log.txt 2>&1
