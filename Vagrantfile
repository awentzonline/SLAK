# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Store the current version of Vagrant for use in conditionals when dealing
  # with possible backward compatible issues.
  vagrant_version = Vagrant::VERSION.sub(/^v/, '')

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "wheezy"

  config.vm.hostname = "gws"
  config.vm.network "forwarded_port", guest: 80, host: 8089

  config.vm.provider :vmware_fusion do |v, override|
    override.vm.box_url = "http://onionwebtech.s3.amazonaws.com/vagrant/wheezy-fusion.box"
  end

  config.vm.provider :virtualbox do |v, override|
    override.vm.box_url = "http://onionwebtech.s3.amazonaws.com/vagrant/wheezy-vbox.box"

    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  config.vm.network "private_network", type: :dhcp
  config.vm.synced_folder ".", "/www/gws", owner: "www-data", group: "www-data", mount_options: ["dmode=755,fmode=755"]

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "ansible/ansible.yml"
  end

  config.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end
end