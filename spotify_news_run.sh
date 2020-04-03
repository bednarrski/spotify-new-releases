#!/bin/bash

filename='/Users/bednar/Logs/spotify_news_log.txt'

if [[ $(find "$filename" -mmin +$((2*24*60)) -print) ]]; then
	echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1
	if [ $? -eq 0 ]; then

		rm -f ~/Logs/spotify_news_log.older
		mv ~/Logs/spotify_news_log.old ~/Logs/spotify_news_log.older
		mv ~/Logs/spotify_news_log.txt ~/Logs/spotify_news_log.old

		if /Users/bednar/opt/anaconda3/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotify_news_log.txt 2>&1 ; then
		    echo "SUCCESS!" >> ~/Logs/spotify_news_log.txt 2>&1
		else
		    if /Users/bednar/opt/anaconda3/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotify_news_log.txt 2>&1 ; then
		        echo "SUCCESS (2nd RUN NEEDED)!" >> ~/Logs/spotify_news_log.txt 2>&1
		    else
		        if /Users/bednar/opt/anaconda3/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotify_news_log.txt 2>&1 ; then
		            echo "SUCCESS (3rd RUN NEEDED)!" >> ~/Logs/spotify_news_log.txt 2>&1
		        else
			        if /Users/bednar/opt/anaconda3/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotify_news_log.txt 2>&1 ; then
			            echo "SUCCESS (4th RUN NEEDED)!" >> ~/Logs/spotify_news_log.txt 2>&1
			        else
				        if /Users/bednar/opt/anaconda3/bin/python ~/Repositories/spotify-new-releases/spotify-new-releases2.py >> ~/Logs/spotify_news_log.txt 2>&1 ; then
				            echo "SUCCESS (5th RUN NEEDED)!" >> ~/Logs/spotify_news_log.txt 2>&1
				        else
				            echo "FAILED 5 TIMES!" >> ~/Logs/spotify_news_log.txt 2>&1
				        fi
			        fi
		        fi
		    fi
		fi
		echo $(date) >> ~/Logs/spotify_news_log.txt 2>&1
	    break
	else
	    echo "COMPUTER IS OFFLINE $(date)" >> ~/Logs/spotify_news_log.txt 2>&1
	fi
else
    echo "LOG TOO FRESH $(date)" >> ~/Logs/spotify_news_log.txt 2>&1
fi
