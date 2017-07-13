#!/usr/bin/python

import simplejson as json
import requests
import apprendaapipythonclient
from email.header import Header
from ansible.module_utils.basic import AnsibleModule
from apprendaapipythonclient.apprenda_account_client import ApprendaAccountClient
from apprendaapipythonclient.configuration import Configuration

def authenticate(url, user, password, tenant):
    auth_url = "{0}/authentication/api/v1/sessions/developer".format(url)
    auth_data = {
        'username': user,
        'password': password,
        'tenant': tenant
    }
    resp = requests.post(auth_url, verify=False, json=auth_data)
    resp_json = resp.json()
    return resp_json['apprendaSessionToken']

def getRoleIdByName(accountClient, roleName):
    print "Looking for role %s" % roleName
    role_items = accountClient.get_roles()

    results = [role.id for role in role_items if role.name == roleName]
    print "Found role id %s" % results[0]
    return results[0]

def getPlanIdByName(accountClient, planName, app_alias, version_alias):
    print "Looking for plan %s" % planName
    plan_items = accountClient.get_plans(app_alias, version_alias)

    results = [plan.id for plan in plan_items if plan.name == planName]
    print "Found plan id %s" % results[0]
    return results[0]

def get_client(apprenda_url, username, password):
    config = Configuration()
    config.host = apprenda_url
    config.username = username
    config.password = password
    return ApprendaAccountClient(config=config)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True, choices=[
                'get_applications',
                'get_subscriptions',
                'get_subscriptions_by_key',
                'get_plans',
                'get_roles',
                'create_role',
                'get_users',
                'create_user',
                'delete_user',
                'add_user_role',
                'remove_user_role',
                'create_subscriptions']),
            apprenda_url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            tenant=dict(type='str', required=True),
            app_alias=dict(required=False, type='str'),
            version_alias=dict(required=False, type='str'),
            roleName=dict(required=False, type='str'),
            roleDescription=dict(required=False, type='str'),
            email=dict(required=False, type='str'),
            firstName=dict(required=False, type='str'),
            lastName=dict(required=False, type='str'),
            planName=dict(required=False, type='str'),
            numberOfSubs=dict(required=False, type='str')
        )
    )
    action = module.params['action']
    apprenda_url = module.params['apprenda_url']
    username = module.params['username']
    password = module.params['password']
    tenant = module.params['tenant']
    
    app_alias = module.params['app_alias']
    version_alias = module.params['version_alias']
    roleName = module.params['roleName']
    roleDescription = module.params['roleDescription']
    email = module.params['email']
    firstName = module.params['firstName']
    lastName = module.params['lastName']

    planName = module.params['planName']
    numberOfSubs = module.params['numberOfSubs']

    accountClient = get_client(apprenda_url, username, password)

    rc = 1
    facts = {}

    if action == "get_applications":
        (out, rc, response) = "OK", 0, accountClient.get_applications()
        for entry in response:
            facts[entry.application_name] = entry.to_dict()

    if action == "get_subscriptions":
        (out, rc, response) = "OK", 0, accountClient.get_subscriptions(app_alias, version_alias)
        for entry in response:
            facts[entry.label] = entry.to_dict()

    if action == "get_subscriptions_by_key":
        app_version_key = "{0}-{1}".format(app_alias, version_alias)
        (out, rc, response) = "OK", 0, accountClient.get_subscriptions_by_key(app_version_key)
        for entry in response.items:
            facts[entry.label] = entry.to_dict()

    if action == "get_plans":
        (out, rc, response) = "OK", 0, accountClient.get_plans(app_alias, version_alias)
        for entry in response:
            facts[entry.name] = entry.to_dict()

    if action == "get_roles":
        (out, rc, response) = "OK", 0, accountClient.get_roles()
        for entry in response:
            facts[entry.name] = entry.to_dict()

    if action == "create_role":
        (out, rc, response) = "OK", 0, accountClient.create_role(roleName, roleDescription)
        facts[response.name] = response.to_dict()

    if action == "get_users":
        (out, rc, response) = "OK", 0, accountClient.get_users()
        for entry in response:
            facts[entry.identifier] = entry.to_dict()
    
    if action == "create_user":
        (out, rc, response) = "OK", 0, accountClient.create_user(firstName, lastName, email, email, True)
        facts[response.identifier] = response.to_dict()

    if action == "delete_user":
        (out, rc, response) = "OK", 0, accountClient.delete_user(email)

    if action == "add_user_role":
        roleId = getRoleIdByName(accountClient, roleName)
        (out, rc, response) = "OK", 0, accountClient.add_users_to_role(roleId, [email])

    if action == "remove_user_role":
        roleId = getRoleIdByName(accountClient, roleName)
        (out, rc, response) = "OK", 0, accountClient.remove_users_from_role(roleId, [email])

    if action == "create_subscriptions":
        planId = getPlanIdByName(accountClient, planName, app_alias, version_alias)
        planIdAndNumbers = {}
        planIdAndNumbers[planId] = numberOfSubs
        (out, rc, response) = "OK", 0, accountClient.create_subscriptions(app_alias, version_alias, planIdAndNumbers)


    if (rc != 0):
        module.fail_json(msg="failure", result=out, ansible_facts=facts)
    else:
        module.exit_json(msg="success", result=out, ansible_facts=facts)

if __name__ == '__main__':
    main()