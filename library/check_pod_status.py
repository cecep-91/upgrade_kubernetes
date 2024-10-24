from ansible.module_utils.basic import AnsibleModule
import subprocess
import time
import sys

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

try:
    import six
except ImportError:
    six = None

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
                check_pods_cmd = "KUBECONFIG={} kubectl get pods -A -o wide | grep -P '{}' | grep '{}'".format(kubeconfig, pod_name_regex, node_name)
                all_pods = subprocess.Popen(check_pods_cmd, shell=True, stdout=subprocess.PIPE, stderr=DEVNULL)
                skip = False
            except:
                skip = True
            if not skip:
                stdout, _ = all_pods.communicate()

                if sys.version_info[0] == 3:
                    pods = stdout.decode().strip().splitlines()
                else:
                    pods = stdout.strip().splitlines()

                running_pods = [pod for pod in pods if "Running" in pod.split()]
                if running_pods:
                    result['message'] = "Pod(s) matching '{}' on node '{}' are in Running state.".format(pod_name_regex, node_name)
                    break
            else:
                result['message'] = "No pods matching '{}' found on node '{}'. Considering as Running.".format(pod_name_regex, node_name)
                break
            time.sleep(5)

        else:
            module.fail_json(msg="Timeout exceeded: Pod(s) matching '{}' on node '{}' are not in Running state.".format(pod_name_regex, node_name), **result)

    except Exception as e:
        module.fail_json(msg="Failed to get pod status: {}".format(str(e)), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
