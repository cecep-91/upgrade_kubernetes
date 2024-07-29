#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_module():
    module_args = dict(
        path=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        original_message='',
        message='',
        error=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    result['original_message'] = path

    try:
        # Install the .deb package
        install_command = ['dpkg', '-i', path]
        subprocess.run(install_command, check=True)

        # Fix broken dependencies
        fix_command = ['apt', '-f', 'install', '-y']
        subprocess.run(fix_command, check=True)

        result['changed'] = True
        result['message'] = 'Package installed and dependencies fixed successfully'
    except subprocess.CalledProcessError as e:
        result['error'] = str(e)
        module.fail_json(msg='Error installing package or fixing dependencies', **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
