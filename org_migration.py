import argparse
import zendesk

parser = argparse.ArgumentParser(prog="Zendesk User's Orgs Migration", usage='%(prog)s [options]')
parser.add_argument('source_id', help='Source Organization ID')
parser.add_argument('target_id', help='Target Organizatio  ID')

args = parser.parse_args()

source_id = args.source_id
target_id = args.target_id

if type(source_id) != int or type(target_id) != int:
    print("Both source and target ids must be integer")
else:
    zendesk.orgs.migrate_users_org(source_id,target_id)



