block {
  for = "2m"
  in  = "place"
  if  = "condition"
}

resource "grafana_rule_group" "alerts" {
  rule {
    name          = "High Disk Usage"
    condition     = "B"
    for           = "2m"
    no_data_state = "NoData"
  }
}

locals {
  doubled = [for x in [1, 2, 3] : x * 2]
}
