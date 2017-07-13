Apprenda Users
=========

This role enables management of Apprenda Platform Users through the Account Portal.

Requirements
------------

* Apprenda Cloud Platform v7.1 or higher
* Python requests library (`pip install requests`)
* Python apprendaapipythonclient Library (`pip install apprendaapipythonclient`)

Role Variables
--------------

`apprenda_url` - FQDN of your ACP instance (i.e, `https://apps.apprenda.com`) **Required**

`username` - Platform user to execute role actions under. **Required**

`password` - Password of the platform user. **Required**

`tenant` - Tenant Alias of the platform user. **Required**

`action` - The action to perform. This can be one of the following. Required parameters for each action are below the action. **Required**
- `create_user`: Creates a new platform user.
  - `email`: The email address of the user. This is the primary identifier and login username for a user in ACP.
  - `prefix`: A prefix for the user's full name.
  - `firstName`: The user's first name.
  - `middleName`: The user's middle name.
  - `lastName`: The user's last name.
  - `suffix`: A suffix for the user's full name.
- `delete_user`: Deletes an existing platform user.
  - `email`: The email address of the user.
- `add_user_role`: Add an existing role to a user.
  - `email`: The email address of the user.
  - `roleName`: The name of the role.
- `remove_user_role`: Remove an existing role from a user.
  - `email`: The email address of the user.
  - `roleName`: The name of the role.

Dependencies
------------


Example Playbook
----------------

This demonstrates how to create, delete, and modify user roles.

```
---
- hosts: localhost
  vars:
    apprenda_url: "https://apps.apprenda.bxcr"
    username: "bxcr@apprenda.com"
    password: "password"
    tenant: "developer"
  roles:
  - role: "apprenda_users"
    action: "create_user"
    email: "smitty@apprenda.com"
    prefix: "Mr."
    firstName: "Smitty"
    middleName: "G"
    lastName: "Danish"
    suffix: "Jr."
	
  - role: "apprenda_users"
    action: "delete_user"
    email: "smitty@apprenda.com"
	
  - role: "apprenda_users"
    action: "add_user_role"
    email: "smitty@apprenda.com"
    roleName: "TestRole"
	
  - role: "apprenda_users"
    action: "remove_user_role"
    email: "smitty@apprenda.com"
    roleName: "TestRole"

```

License
-------

MIT

Author Information
------------------

Please see http://www.apprenda.com for more information about the Apprenda Cloud Platform.