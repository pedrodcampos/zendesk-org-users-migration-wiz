import json
from zendesk.request import zendesk_get, zendesk_post, zendesk_delete, check_job_status

ORG_USERS_ENDPOINT = '/api/v2/organizations/{}/users.json'
ORG_MEMEBERSHIPS_ENDPOINT = '/api/v2/organizations/{}/organization_memberships.json'
CREATE_ORG_MEMEBERSHIPS_ENDPOINT = '/api/v2/organization_memberships/create_many.json'
DELETE_ORG_MEMBERSHIPS_ENDPOINT ='/api/v2/organization_memberships/destroy_many.json?ids={}'

def get_org_end_users(org_id):
    path = ORG_USERS_ENDPOINT.format(org_id)
    users = zendesk_get(path, 'users')
    users = [user for user in users if user['role'] == 'end-user']

    return users

def add_users_to_org(user_ids, org_id):
    payload = [{'user_id': user_id, 'organization_id': org_id}
               for user_id in user_ids]

    for i in range(1, 1 + round(len(payload)/100+0.5)):
        payload_slice = payload[(i-1)*100:i*100]
        org_membership_payload = {"organization_memberships": payload_slice}
        
        response = zendesk_post(CREATE_ORG_MEMEBERSHIPS_ENDPOINT,org_membership_payload,'job_status')
        check_job_status(payload_slice,response)
        
def get_users_membership_id(user_ids, org_id):
    path = ORG_MEMEBERSHIPS_ENDPOINT.format(org_id)
    memberships = zendesk_get(path, 'organization_memberships')
    membership_ids = [membership['id'] for membership in memberships if membership['user_id'] in user_ids]

    return membership_ids

def delete_memberships(membership_ids):
    if len(membership_ids)>0:
        path = DELETE_ORG_MEMBERSHIPS_ENDPOINT.format(','.join(map(str,membership_ids)))
        response = zendesk_delete(path,'job_status')
        check_job_status(membership_ids,response)

def migrate_users_org(source_org_id, target_org_id):
    end_users = get_org_end_users(source_org_id)
    end_user_ids = [end_user['id'] for end_user in end_users]
    
    add_users_to_org(end_user_ids,target_org_id)

    memberships = get_users_membership_id(end_user_ids,source_org_id)
    delete_memberships(memberships)

    print('Done')
