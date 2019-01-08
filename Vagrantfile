# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "bionicy64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64-vagrant.box"
  config.vm.forward_port 8000, 8000
  config.vm.provision :shell, :path => 'provision.sh'
end
