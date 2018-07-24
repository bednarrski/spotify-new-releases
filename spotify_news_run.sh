rm -f ~/Logs/spotiffy_news_log.older
mv ~/Logs/spotiffy_news_log.old ~/Logs/spotiffy_news_log.older
mv ~/Logs/spotiffy_news_log.txt ~/Logs/spotiffy_news_log.old
if ~/anaconda3/envs/py36/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotiffy_news_log.txt 2>&1 ; then
    echo "SUCCESS!" >> ~/Logs/spotiffy_news_log.txt 2>&1
else
    if ~/anaconda3/envs/py36/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotiffy_news_log.txt 2>&1 ; then
        echo "SUCCESS (2nd RUN NEEDED)!" >> ~/Logs/spotiffy_news_log.txt 2>&1
    else
        if ~/anaconda3/envs/py36/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotiffy_news_log.txt 2>&1 ; then
            echo "SUCCESS (3rd RUN NEEDED)!" >> ~/Logs/spotiffy_news_log.txt 2>&1
        else
            echo "FAILED 3 TIMES!" >> ~/Logs/spotiffy_news_log.txt 2>&1
        fi
    fi
fi
echo $(date) >> ~/Logs/spotiffy_news_log.txt 2>&1