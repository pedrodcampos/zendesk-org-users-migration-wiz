# zendesk-org-users-migration-wiz

This tool will migrate all end-users from one organization to another.

### Usage:
#### create a config/config.json file with zendesk url and credentials for both development and production environment.

_see config.example.json in the same folder_

#### create a .env file.

_see .env.example in root directory_

#### run `python org_migration.py [source_id] [target_id]`
_source_id: Organization Id where users should be moved from_

_target_id: Organization Id where users should be moved to_

