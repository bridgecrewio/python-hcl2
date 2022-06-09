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

resource "aws_alb" "alb" {
  name                             = "foobar-nlb"
  load_balancer_type               = "network"
  enable_cross_zone_load_balancing = true


  tags = "${merge("${var.lbcustomtags}", tomap({
     Name = "foobar-nlb"
  }))}"
}
