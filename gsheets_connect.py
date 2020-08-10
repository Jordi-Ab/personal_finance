from settings import google_services_credentials
from oauth2client.client import OAuth2WebServerFlow, GoogleCredentials
import httplib2
from googleapiclient.discovery import build

# import libraries
from apiclient.http import MediaFileUpload
from mimetypes import MimeTypes
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep

google_services_info = {
    'google_analytics':{
        'scope': 'https://www.googleapis.com/auth/analytics',
        'url': 'https://accounts.google.com/o/oauth2/token',
        'version':'v4',
        'name':'analytics'
    },
    'google_drive':{
        'scope': 'https://www.googleapis.com/auth/drive',
        'url': 'https://accounts.google.com/oauth2/v3/token',
        'version':'v3',
        'name':'drive'
    },
    'google_sheets':{
        'scope': 'https://www.googleapis.com/auth/spreadsheets',
        'url': 'https://accounts.google.com/o/oauth2/token',
        'version':'v4',
        'name':'sheets'
    }
}

class Connect():

    def __init__(self, service):    
        
        if service not in google_services_info.keys():
            raise ValueError('"service" param must be one of: {0}'.format(google_services_info.keys()))
        
        self.service = service
        self.scope = google_services_info[service]['scope']
        self.client_id = google_services_credentials[service]['client_id']
        self.client_secret = google_services_credentials[service]['client_secret']
        self.redirect_uri = google_services_credentials[service]['redirect_uri']
        self.access_code = google_services_credentials[service]['access_code']
        self.access_token = google_services_credentials[service]['access_token']
        self.refresh_token = google_services_credentials[service]['refresh_token']


    def get_service(self):
        if self.access_code == '' or self.access_token == '' or self.refresh_token == '':
            self._start_connection()
        else:
            credentials = GoogleCredentials(
                self.access_token, 
                self.client_id, 
                self.client_secret, 
                self.refresh_token, 
                3920, 
                google_services_info[self.service]['url'], 
                'test'
            )
            http = httplib2.Http()
            http = credentials.authorize(http)
            service = build(
                google_services_info[self.service]['name'],
                google_services_info[self.service]['version'], 
                http=http
            )
            return service

    def _start_connection(self):
        # create connection based on project credentials
        flow = OAuth2WebServerFlow(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            redirect_uri=self.redirect_uri
        )

        # capture different states of connection
        if self.access_code == '':
            # first run prints oauth URL
            auth_uri = flow.step1_get_authorize_url()
            print('----------')
            print('Go to this url and give permissions to google: {0}'.format(auth_uri))
            print('----------')
            print('*Note: Connection not yet established')
        elif self.access_token == '' and self.refresh_token == '':
            # second run returns access and refresh token
            credentials = flow.step2_exchange(self.access_code)
            print('----------')
            print('Access Token: ')
            print(credentials.access_token)
            print('Refresh Token: ')
            print(credentials.refresh_token)
            print('----------')
            print('*Note: Connection not yet established')



class GoogleSheets():

    # ---------CONSTRUCTOR-------------
    def __init__(self):
        conn = Connect(service='google_sheets')
        self.service = conn.get_service()

    # ---------PUBLIC---------------
    def gsheet_to_df(self, spreadsheet_id, range_name, header_ix=0):
        """ Converts Google sheet data to a Pandas DataFrame.
        Note: This script assumes that your data contains a header file on the first row!
        Also note that the Google API returns 'none' from empty cells - in order for the code
        below to work, you'll need to make sure your sheet doesn't contain empty cells,
        or update the code to account for such instances.
        """
        
        # Call the Sheets API and get the response as dict
        gsheet = self.get_gsheet_response(spreadsheet_id, range_name)

        # Assumes first line is header
        header = gsheet.get('values', [])[header_ix] 

        # Everything else is data.
        raw_values = gsheet.get('values', [])[header_ix+1:]

        if not raw_values:
            print('No data found.')
            return pd.DataFrame(columns = header)
        
        values = self._values_list_to_array(raw_values, len(header)) 
        
        return pd.DataFrame(
            values, 
            columns = header
        ).replace(
            ['', None], np.nan
        )

    def values_to_gsheet(
        self, 
        spreadsheet_id,
        values_list, 
        range_name, 
        value_input_option='RAW'
    ):
        """
        Writes data to a google sheet, rowwise, starting from "range_name"
        Ex.[
            [col1, col2, col3],
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ]
        Params:
            spreadsheet_id: Id of the Google Sheet to write on
            values_list: two dimensional list [[]]
            range_name: 


        """
        if not isinstance(values_list, list):
            raise ValueError('"values_list" must be a list')
        
        data = [
            {
                'range': range_name,
                'values': values_list
            }
        ]
        body = {
            'valueInputOption': 'RAW',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, 
            body=body
        ).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def clear_values(self, spreadsheet_id, range_name):
        gsheet_response = self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, 
            range=range_name 
        ).execute()
        return gsheet_response

    def get_gsheet_response(self, spreadsheet_id, range_name):
        # Call the Sheets API
        gsheet_response = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, # <Your spreadsheet ID>
            range=range_name # <Your worksheet name>
        ).execute()
        return gsheet_response

    # ---------PRIVATE-------------
    def _values_list_to_array(self, values_list, n_cols):
        """
        Transforms a list of lists, with not necesarily the
        same length, to a numpy array.
        """
        lengths = [len(l) for l in values_list]
        arr = np.empty((len(values_list),n_cols),dtype=object)
        mask = np.arange(n_cols) < np.array(lengths)[:,None]
        arr[mask] = np.concatenate(values_list)
        return arr