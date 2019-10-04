import requests
import json
import time

from config import global_config

ZENDESK_URL = global_config['zendesk_url']
ZENDESK_AUTH = (global_config['user'], global_config['password'])

ORG_USERS_ENDPOINT = '/api/v2/organizations/{}/users.json'
ORG_MEMEBERSHIPS_ENDPOINT = '/api/v2/organizations/{}/organization_memberships.json'
CREATE_ORG_MEMEBERSHIPS_ENDPOINT = '/api/v2/organization_memberships/create_many.json'


def zendesk_get(path, response_container=None):
    if ZENDESK_URL in path:
        next_url = path
    else:
        next_url = ZENDESK_URL + path
        
    items = []
    while next_url:
        r = requests.get(next_url, auth=ZENDESK_AUTH)
        if r.status_code == 200:
            result = r.json()
            next_url = result.get('next_page',None)
            data = result[response_container] if response_container else result

            if type(data) == list:
                items += data
            elif next_url is None and type(data) == dict and len(items) == 0:
                items = data
            else:
                items.append(data)

        if r.status_code == 429:
            wait_for = r.headers['Retry-After']
            time.sleep(wait_for)

    return items


def zendesk_post(path, json, response_container=None):
    url = ZENDESK_URL + path

    r = requests.post(url, auth=ZENDESK_AUTH, json=json)

    if r.status_code in [200, 201]:
        return r.json().get(response_container, None) if response_container else r
    return r

def zendesk_delete(path,response_container=None):
    url = ZENDESK_URL + path
    r = requests.delete(url, auth=ZENDESK_AUTH)

    return r.json().get(response_container, None) if response_container else r

def check_job_status(ref,response):
    job_status_url = response['url']
    status = response['status']
    print('Request enqueued')

    while status not in ['completed', 'failed']:
        print('Checking...')
        
        response = zendesk_get(job_status_url,'job_status')
        if response:
            results = response['results']
            status = response['status']
            for result in results:
                if result.get('error', None):
                    index = result['index']
                    print(f"{ref[index]['user_id']}\t::\t{result['details'] if result.get('details',None) else result.get('error',result)}")
            print(response['message'])