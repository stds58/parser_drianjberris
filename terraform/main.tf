

module "network" {
  source = "./modules/network"

  network_name = "uc_network"
}

module "subnetwork" {
  source = "./modules/subnet"

  subnet_name    = "uc_subnetwork"
  zone           = "ru-central1-a"
  v4_cidr_blocks = ["192.168.10.0/24"]
  network_id     = module.network.network_id
}

module "security_groups_vm1" {
  source    = "./modules/security-groups"

  network_id          = module.network.network_id
  security_group_name = "sg-vm1"
  ingress_rules = [
    {
      protocol       = "tcp"
      port           = 22
      v4_cidr_blocks = ["0.0.0.0/0"] # Разрешаем SSH-доступ с любого IP
    }
  ]
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}


module "vm1" {
  source = "./modules/instance"

  instance_name      = "vm1"
  platform_id        = "standard-v3" # Intel Ice Lake
  zone               = "ru-central1-a"
  cores              = 2
  memory             = 4
  core_fraction      = 100
  image_id           = data.yandex_compute_image.ubuntu.id
  disk_size          = 30
  disk_type          = "network-ssd"
  subnet_id          = module.subnetwork.subnet_id
  nat                = true
  security_group_ids = [module.security_groups_vm1.security_group_id]
  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/terraform_20250320.pub")}"
  }

  labels = {
    environment = "vm1"
    terraform   = "true"
    role        = "vm1"
  }
}

