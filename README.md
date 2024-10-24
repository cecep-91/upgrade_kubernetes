# Ansible Playbook to Upgrade Kubernetes Version 1.21 Up to Version 1.30 
## CRI: (docker to cri-dockerd)

This is ansible playbook i made for upgrading kubernetes cluster. Only tested on Ubuntu 22 and CentOS 7 servers.
**Note: Even though this playbook supports both Ubuntu 22 and CentOS 7, you can't use it for both OSes at the same time. This is because CentOS only has Python 2.7 installed, so it needs a different Ansible version. You’ll need to use conda (or another Python version manager) to switch between Ansible with Python 2 and 3.

How to use it:
1. Download ansible
2. Clone this repo
   ```sh
   git clone https://github.com/cecep-91/upgrade_kubernetes.git
   ```
3. Change directory to this repository
   ```sh
   cd upgrade_kubernetes
   ```
4. Open **hosts** file and change the hosts there. The hosts separated to 3 groups:
   - **first_master**  : the kubernetes master node that do the 'kubeadm init'
   - **other_master**  : other kubernetes master nodes
   - **worker**        : worker nodes
5. Open **group_vars/all** and edit parameter you want to change, especially **kubernetes.target_minor_version**
6. run **ansible-playbook upgrade_kubernetes.yaml**

The upgrade will be executed sequentially, so the cluster will not go all the way down, just one node will go down at a time. However, the download of images needed to upgrade to the **current_target_version** will be done in parallel, so it won't take much time waiting for each node to download the necessary images.
