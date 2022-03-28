
# Create S3 bucket 

A Ansible Playbook ot create AWS S3 bucket.
Customization can be done using vars/customization.yml file

## Running this Playbook

```command
ansible-playbook -i [inventory file] --vault-password-file [vault-password-file] -u [remote user] create_s3.yaml
```
