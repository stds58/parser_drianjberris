

output "vm1_ip" {
  value = module.vm1.external_ip_address
}



output "ssh_connection_command" {
  value = <<EOT
    ssh -A -i ~/.ssh/terraform_20250320 ubuntu@${module.vm1.external_ip_address}
    ssh -i ~/.ssh/terraform_20250320 ubuntu@${module.vm1.external_ip_address}
  EOT
}

