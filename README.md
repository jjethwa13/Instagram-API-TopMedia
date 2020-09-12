# Instagram-API-TopMedia
Automatically gathers data on top media by a hashtag search

DETAILED DESCRIPTION

The system will automatically collect data in paginations of the top media related to a given hashtag. You can specify the number of paginations you would like to collect up to.
Note the importance of this is because The Official Instagram API sets a 200 requests per hour limit which will disrupt most processes collecting large amounts of data from the
API. The program will collect data until it reaches an error (usually that the limit has been reached), upon reaching the error it will save the state of the application, wait
until the BUFFER time has elapsed, and continue where it left off. Because of the design, once the state has been saved, it is possible to close down the application and start 
it back up again at a later time.


INSTRUCTIONS

1. You will need to create a new defines.py file within the directory with the API-Key, Client-ID, Client-Secret, Instagram-ID etc
2. Run Gather_data.py initially with Initialise = True, then set back to False (This will set up the necessary files in the directory)
3. You can specify the hashtags to be searched via the list Search, you can change the buffer time between searches by adjusting BUFFER, you can change the number of pages in the
pagination that will be downloaded via PAGES
4. Then run the script, sit back and relax :)


DATA FORMAT

Data.txt >> (hashtag_id) >> Name, 1, 2, 3, ... 

Name >> (hashtag name)

1 >> (Return for 1st page in pagination)

2 >> (Return for 2nd page in pagination)

3 >> (Return for 3rd page in pagination)

.

.

.
                
                
FURTHER DETAILS

The structure of each post and details on the API endpoints etc can be found via https://developers.facebook.com/docs/instagram-api/
           
