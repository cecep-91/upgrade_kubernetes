#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import time

def run_module():
    module_args = dict(
        kubeconfig=dict(type='str', required=True),
        pod_name_regex=dict(type='str', required=True),
        node_name=dict(type='str', required=True),
        timeout=dict(type='int', default=60)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    kubeconfig = module.params['kubeconfig']
    pod_name_regex = module.params['pod_name_regex']
    node_name = module.params['node_name']
    timeout = module.params['timeout']

    try:
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                check_pods_cmd = f"KUBECONFIG={kubeconfig} kubectl get pods -A -o wide | grep -P '{pod_name_regex}' | grep '{node_name}'"
                all_pods = subprocess.Popen(check_pods_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                skip = False
            except:
                skip = True
            if not skip:
                stdout, _ = all_pods.communicate()
                pods = stdout.decode().strip().splitlines()
                running_pods = [pod for pod in pods if "Running" in pod.split()]
                if running_pods:
                    result['message'] = f"Pod(s) matching '{pod_name_regex}' on node '{node_name}' are in Running state."
                    break
            else:
                result['message'] = f"No pods matching '{pod_name_regex}' found on node '{node_name}'. Considering as Running."
                break
            time.sleep(5)

        else:
            module.fail_json(msg=f"Timeout exceeded: Pod(s) matching '{pod_name_regex}' on node '{node_name}' are not in Running state.", **result)

    except Exception as e:
        module.fail_json(msg=f"Failed to get pod status: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
