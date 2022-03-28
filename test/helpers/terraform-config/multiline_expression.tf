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
