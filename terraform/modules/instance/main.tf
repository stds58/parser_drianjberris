
resource "yandex_compute_instance" "vm" {
  name        = var.instance_name
  platform_id = var.platform_id
  zone        = var.zone

  resources {
    cores         = var.cores
    memory        = var.memory
    core_fraction = var.core_fraction
  }

  boot_disk {
    initialize_params {
      image_id = var.image_id
      size     = var.disk_size
      type     = var.disk_type
    }
  }

  network_interface {
    subnet_id          = var.subnet_id
    nat                = var.nat
    security_group_ids = var.security_group_ids
  }

  metadata = var.metadata
  labels   = var.labels

}
