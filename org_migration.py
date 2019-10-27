import argparse
import zendesk

parser = argparse.ArgumentParser(prog="Zendesk User's Orgs Migration", usage='%(prog)s [options]')
parser.add_argument('source_id', help='Source Organization ID')
parser.add_argument('target_id', help='Target Organizatio  ID')

args = parser.parse_args()
try:
    source_id = int(args.source_id)
    target_id = int(args.target_id)
except ValueError:
    print("Both source and target ids must be integer")
    exit(-1)

zendesk.orgs.migrate_users_org(source_id,target_id)
    



