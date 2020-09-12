import json
import time
import datetime
from defines import getCreds, makeApiCall


class StateHandler(object):
    
    def __init__(self, init=False):
        
        if init:
            self.config = dict()
            self.config['Page_Number'] = 1
            self.config['Search_Index'] = 0
            self.config['Next_Page_URL'] = ""
            self.config['Started_Search'] = False
            self.config['Finished'] = False
            with open('config.txt', 'w') as outfile:
                json.dump(self.config, outfile)
            
            self.data = dict()
            self.data['metadata'] = dict()
            with open('data.txt', 'w') as outfile:
                json.dump(self.data, outfile)
                
        else:
            with open('config.txt') as json_file:
                self.config = json.load(json_file)
            with open('data.txt') as json_file:
                self.data = json.load(json_file)
    
    def save(self):
        with open('config.txt', 'w') as outfile:
            json.dump(self.config, outfile)
        with open('data.txt', 'w') as outfile:
            json.dump(self.data, outfile)
    
    def update_data(self, data):
        self.data = data
        
    def update_config(self, config):
        self.config = config
        
    def get_data(self):
        return self.data
    
    def get_config(self):
        return self.config
    
class DataRetriever(object):
    
    def __init__(self):
        
        self.State = StateHandler()
        self.Data = self.State.get_data()
        self.Config = self.State.get_config()
        
        self.Creds = getCreds()
        self.Halt = False
        
    def get_state(self):
        return self.State
        
    def safe_exit(self):
        self.State.update_data(self.Data)
        self.State.update_config(self.Config)
        self.State.save()
            
    def main(self, Search):
        start_index = self.Config['Search_Index']
        for i in range(start_index, len(Search)):
            print("Hashtag >> " + str(Search[i]))
            response = self.getHashtagID(Search[i])
            
            if not self.Halt:
                hashtag_id = response['json_data']['data'][0]['id']
            else:
                break
            
            if not self.Config['Started_Search']:
                self.Data[str(hashtag_id)] = dict()
                self.Data[str(hashtag_id)]['Name'] = Search[i]
                self.setData(hashtag_id)
            else:
                self.setData(hashtag_id, cont=True)
            
            if self.Halt:
                break
        
        if not self.Halt:
            self.Config['Finished'] = True
                    
        self.safe_exit()
    
    def getHashtagsInString(self, text):
    
        """
        Gets all of the hashtags in a post's caption
        
        Parameters:
            captions: The caption in a string format
        
        Returns:
            hashtag_list: A list of all hashtags present in the caption
        """
        
        hashtag_list = []
        hashtag = ""
        reading = False
        for char in text:
            
            if (char == ' ' or char == '\n' or char == '\r' or char == '\t') and reading:
                reading = False
                hashtag_list.append(hashtag)
                hashtag = ""
                continue
            
            if char == '#' and not reading:
                reading = True
                continue
            
            if char == '#' and reading:
                hashtag_list.append(hashtag)
                hashtag = ""
                continue
            
            if reading:
                hashtag = hashtag + char
                
        if reading:
            hashtag_list.append(hashtag)
            
        return hashtag_list
    
    def getHashtagID(self, hashtag, debug=False):
    
        """
        Get Hashtag ID
        
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?
            user_id={user-id}&
            q={q}&
            fields={fields}&
            access_token={your-access-token}
            
        Returns:
            object: data from the endpoint
        
        """
        if not self.Halt:
        
            endpointParams = dict()
            endpointParams['user_id'] = self.Creds['instagram_account_id']
            endpointParams['q'] = str(hashtag)
            endpointParams['access_token'] = self.Creds['access_token']
            endpointParams['fields'] = 'id,name'
            
            url = self.Creds['endpoint_base'] + 'ig_hashtag_search?'
            
            response = makeApiCall(url, endpointParams=endpointParams, debug=debug)
            
            try:
                data = response['json_data']['data']
            except:
                print(response['json_data_pretty'])
                self.Halt = True
        
        else:
            response = None
        
        return response

    def setData(self, hashtag_id, fields=None, debug=False, pages=PAGES, cont=False):
    
        """
        Get Hashtag ID
        
        API Endpoint:
            graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?
            user_id={user-id}&
            fields={fields}&
            access_token={your-access-token}
            
        Fields (separated by a comma):
            - caption
            - children  (Album IG Media)
            - comments_count
            - id
            - like_count
            - media_type
            - media_url  (Album IG Media)
            - permalink
            - timestamp  (v7.0+)
            
        Returns:
            object: data from the endpoint
        
        """
        if not self.Halt:
            if not cont:
                if fields == None:
                    fields = 'caption,children,comments_count,id,like_count,media_type,media_url,permalink,timestamp'
                endpointParams = dict()
                endpointParams['user_id'] = self.Creds['instagram_account_id']
                endpointParams['fields'] = fields
                endpointParams['access_token'] = self.Creds['access_token']
                
                url = self.Creds['endpoint_base'] + str(hashtag_id) + '/top_media?'
                
                response = makeApiCall(url, endpointParams=endpointParams, debug=debug)
                try:
                    data = response['json_data']['data']
                except:
                    print(response['json_data_pretty'])
                    self.Halt = True
                if not self.Halt:
                    self.Data[str(hashtag_id)]['1'] = response['json_data']
                    self.Config['Started_Search'] = True
                    try:
                        url = response['json_data']['paging']['next']
                    except:
                        print(response['json_data_pretty'])
                        self.Halt = True
                    if not self.Halt:
                        for page in range(2, pages+1):
                            print("Page " + str(page) + " / " + str(pages))
                            response = makeApiCall(url)
                            try:
                                data = response['json_data']['data']
                            except:
                                self.Halt = True
                                self.Config['Page_Number'] = page
                                self.Config['Next_Page_URL'] = url
                                print(response['json_data_pretty'])
                                break
                            if not self.Halt:
                                self.Data[str(hashtag_id)][str(page)] = response['json_data']
                        if not self.Halt:
                            self.Config['Started_Search'] = False
            else: ## cont==True
                start = self.Config['Page_Number']
                url = self.Config['Next_Page_URL']
                for page in range(start, pages+1):
                    print("Page " + str(page) + " / " + str(pages))
                    response = makeApiCall(url, debug=debug)
                    try:
                        data = response['json_data']['data']
                    except:
                        self.Halt = True
                        self.Config['Page_Number'] = page
                        self.Config['Next_Page_URL'] = url
                        print(response['json_data_pretty'])
                        break
                    if not self.Halt:
                        self.Data[str(hashtag_id)][str(page)] = response['json_data']
                if not self.Halt:
                    self.Config['Started_Search'] = False
            
   
Initialise = False
BUFFER = 300
PAGES = 2000

if Initialise:
    state = StateHandler(init=True)
else:
    Search = ['FarFetch']
    DataEngine = DataRetriever()
    State = DataEngine.get_state()
    state_config = State.get_config()
    while not state_config['Finished']:
        DataEngine = DataRetriever()
        DataEngine.main(Search)
        State = DataEngine.get_state()
        state_config = State.get_config()
        if not state_config['Finished']:
            start_time = datetime.datetime.now() + datetime.timedelta(0, BUFFER)
            print("Waiting...")
            print("Resuming at >> ", start_time)
            time.sleep(BUFFER)
    


































