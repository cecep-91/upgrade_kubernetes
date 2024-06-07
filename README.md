# Upgrade Kubernetes version 1.21 up to version 1.30 
## (docker to cri-dockerd)

This is ansible playbook i made for upgrading kubernetes cluster.
This is how it works:
![Untitled Diagram drawio](https://github.com/cecep-91/upgrade_kubernetes/assets/148958846/dcfab26c-79b4-4762-8f2e-d029fcc5a48f)


- **target_minor_version**     : It's the minor version the kubernetes will be upgraded to. Can be changed in **hosts** file
- **ansible_managed_hosts**    : All the server in **hosts** file
- **kubeadm_version**          : Minor version kubeadm version of the server
- **kubelet_version**          : Minor version kulet version of the server
- **current_target_version**   : Minor version the kubernetes now being upgraded to

How to use it:
1. Download ansible
2. Change the hosts in **hosts** file, the hosts separated to 3 groups:
   - **first_master**  : the kubernetes master node that do the 'kubeadm init'
   - **other_master**  : other kubernetes master nodes
   - **worker**        : worker nodes
3. Change **target_minor_version** to the minor version your kubernetes cluster want to upgraded to
4. Change directory to the root dir of this repository
5. run **ansible-playbook setup upgrade_kubernetes.yaml**

The upgrade will be executed sequentially, so the cluster will not go all the way down, just one node will go down at a time. However, the download of images needed to upgrade to the **current_target_version** will be done in parallel, so it won't take much time waiting for each node to download the necessary images. The repository sucks too, not even 1MB/s here.
