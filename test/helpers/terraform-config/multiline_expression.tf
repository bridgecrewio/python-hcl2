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

  binary_operator_break_comment = (
    # comment 1
    # comment 2
    true &&
    # comment 3
    # comment 4
    true
    # comment 5
    # comment 6
  )
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

variable "some_var2" {
  description = "description"
  type        = string
  default     = cidrsubnets(
    # comment 1
    # comment 2
    "10.0.0.0/24",
    # comment 3
    # comment 4
    2,
    # comment 5
    # comment 6
    2
    # comment 7
    # comment 8
  )
}

resource "null_resource" "multiline_comment_multiline" {
    triggers = [
        /* "a",
        "b" */
    ]
}

resource "null_resource" "multiline_comment_single_line_before_closing_bracket" {
    triggers = [
        /* "a", "b" */ ]
}

resource "null_resource" "multiline_comment_single_line_between_brackets" {
    triggers = [
        /* "a", "b" */
    ]
}

resource "null_resource" "multiline_comment_single_line_after_opening_bracket" {
    triggers = [ /* "a", "b" */
    ]
}

locals {
  # comment 1
  # comment 2
  servers = [
    # comment 3
    # comment 4
    for serverkey in local.configjson.Servers : merge(
      # comment 5
      # comment 6
      { a = "b" }
      # comment 7
      # comment 8
    )
    # comment 9
    # comment 10
  ]
  # comment 11
  # comment 12
}

locals {
  # comment 1
  # comment 2
  transform = {
    # comment 3
    # comment 4
    for s in local.some_strings : s =>
    # comment 5
    # comment 6
    {
      # comment 7
      # comment 8
      name = upper(s)
      tag  = "test"
      # comment 9
      # comment 10
    }
    # comment 11
    # comment 12
  }
  # comment 13
  # comment 14
}

locals {
  test_1 = (
    # comment 1
    # comment 2
    var.used != null
    # comment 3
    # comment 4
    ? var.used
    # comment 5
    # comment 6
    : "not set"
    # comment 7
    # comment 8
  )
  test_2 = (
    # comment 1
    # comment 2
    var.used != null
    # comment 3
    # comment 4
    ?
    # comment 5
    # comment 6
    var.used
    # comment 7
    # comment 8
    :
    # comment 9
    # comment 10
    "not set"
    # comment 11
    # comment 12
  )
  test_3 = (
    # comment 1
    # comment 2
    "string"
    # comment 3
    # comment 4
  )
}
