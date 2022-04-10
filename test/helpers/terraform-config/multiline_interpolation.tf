locals {
  multiline = "${
    max(
      ceil(
        log((local.instance_memory * 1024) / 21474836480, 2) * 600
      ),
      200
    )
  }"

  multiline_2 = "${max(
      ceil(
        log((local.instance_memory * 1024) / 21474836480, 2) * 600
      ),
      200
  )}"
}
