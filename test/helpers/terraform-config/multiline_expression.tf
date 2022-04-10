locals {
  ternary_single_line = var.test == "" ? 0 : 1

  ternary_question_mark_break = var.test == "" ?
  0 : 1

  ternary_colon_break = var.test == "" ? 0 :
  1

  ternary_multi_line = var.test == "" ?
  0 :
  1

  ternary_pre_question_mark_break = var.test == ""
  ? 0 : 1

  ternary_pre_colon_break = var.test == "" ? 0
  : 1

  ternary_pre_multi_line = var.test == ""
  ? 0
  : 1

  binary_single_line = (false || true)

  binary_operator_break = (false ||
  true)

  binary_pre_operator_break = (false
  || true)

}

variable "some_var" {
  description = "description"
  type        = string
  # comment 1
  # comment 2
  validation {
    # comment 3
    # comment 4
    condition = alltrue(
      # comment 5
      # comment 6
      [
        # comment 7
        # comment 8
        length(regexall("^st", var.some_var)) == 0,
        # comment 9
        # comment 10
      ]
      # comment 11
      # comment 12
    )
    # comment 13
    # comment 14
    error_message = "error"
  }
  # comment 15
  # comment 16
}
