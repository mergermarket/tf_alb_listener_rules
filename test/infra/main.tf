module "alb_listener_rule" {
  source = "../.."

  # required
  alb_listener_arn = "${var.alb_listener_arn}"
  target_group_arn = "${var.target_group_arn}"
}

module "alb_listener_rule_host_condition" {
  source = "../.."

  # required
  alb_listener_arn = "${var.alb_listener_arn}"
  target_group_arn = "${var.target_group_arn}"
  host_condition   = "${var.host_condition}"
}

module "alb_listener_rule_two_paths" {
  source = "../.."

  # required
  alb_listener_arn = "${var.alb_listener_arn}"
  target_group_arn = "${var.target_group_arn}"
  path_conditions  = "${var.path_conditions}"
}

module "alb_listener_rule_custom_starting_priority" {
  source = "../.."

  # required
  alb_listener_arn  = "${var.alb_listener_arn}"
  target_group_arn  = "${var.target_group_arn}"
  starting_priority = "${var.starting_priority}"
}

# configure provider to not try too hard talking to AWS API
provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

# variables
variable "alb_listener_arn" {}

variable "target_group_arn" {}

variable "path_conditions" {
  default = []
}

variable "host_condition" {
  default = "*.*"
}

variable "starting_priority" {
  default = "50"
}
