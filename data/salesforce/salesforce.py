import os
import json
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import pandas as pd


def login():
    # find or prompt for credentials
    creds_path = 'data/salesforce/credentials.json'
    if os.path.isfile(creds_path):
        with open(creds_path, 'r') as creds_file:
            creds = json.load(creds_file)
            if 'username' not in creds:
                username = input('Enter your Salesforce email address: ')
                creds['username'] = username
            else:
                username = creds['username']
            if 'password' not in creds:
                password = input('Enter your Salesforce password: ')
                creds['password'] = password
            else:
                password = creds['password']
            if 'token' not in creds:
                token = input('Enter your security token (see https://help.salesforce.com/s/articleView?id=sf.user_security_token.htm&type=5 for more info): ')
                creds['token'] = token
            else:
                token = creds['token']
        with open(creds_path, 'w') as creds_file:
            json.dump(creds, creds_file)
    else:
        print('Input Salesforce credentials. They will be saved for future attempts.')
        username = input('Enter your Salesforce email address: ')
        password = input('Enter your Salesforce password: ')
        token = input('Enter your security token (see https://help.salesforce.com/s/articleView?id=sf.user_security_token.htm&type=5 for more info): ')
        with open(creds_path, 'w') as creds_file:
            creds = {
                'username': username,
                'password': password,
                'token': token
            }
            json.dump(creds, creds_file)
    sf_client = Salesforce(username=username, password=password, security_token=token)
    return sf_client


def extract():

    sf = login()
    # metadata_org = sf.describe()
    # df_sobjects = pd.DataFrame(metadata_org['sobjects'])
    # df_sobjects.to_csv('sf_metadata.csv', index=False)

    # protocol = sf.Protocol__c
    # protocol_metadata = protocol.describe()
    # df_protocol_metadata = pd.DataFrame(protocol_metadata.get('fields'))
    # df_protocol_metadata.to_csv('data/csv/protocol_metadata.csv',
    #                             index=False)

    fields = ['Github_ID__c', 'CreatedDate', 'Delivery_Date__c', 'TAT_days__c',
              'Category__c', 'Status__c', 'Assignee__c']
    fields_str = ','.join(fields)
    SOQL = f'SELECT {fields_str} FROM Protocol__c'
    data = sf.query(SOQL)

    df_dict = {field: [d[field] for d in data['records']] for field in fields}
    df = pd.DataFrame(df_dict)
    df_new = df.rename(
        columns={'Github_ID__c': 'id', 'CreatedDate': 'created',
                 'Delivery_Date__c': 'delivered', 'TAT_days__c': 'tat',
                 'Category__c': 'sf_category', 'Status__c': 'sf_status',
                 'Assignee__c': 'sf_assignee'})

    with open('data/salesforce/user_map.json') as user_map_file:
        user_map = json.load(user_map_file)
        df_new['sf_assignee'].replace(user_map, inplace=True)

    # df_new['delivered'] = pd.to_datetime(df_new['delivered'], format='%f')
    # df_new['created'] = pd.to_datetime(df_new['created'], format='%f')
    df_new.to_csv('data/csv/salesforce.csv')
    return df_new


if __name__ == '__main__':
    extract()
