variable "names" {
  type    = list(string)
  default = ["a"]
  validation {
    condition = alltrue([
      for n in var.names :
      length(n) > 0
      && !contains(["host"], n)
      && n != "x"
    ])
    error_message = "bad name"
  }
}

locals {
  not_then_or = (
    !var.a
    || var.b
  )
  negative_then_plus = (
    -var.c
    + 2
  )
  not_with_comment = (
    !var.a
    # comment
    && var.b
  )
}
