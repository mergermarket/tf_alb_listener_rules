import unittest
import os
from subprocess import check_call, check_output

cwd = os.getcwd()


class TestTFALBListenerRules(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'get', 'test/infra'])

    def test_create_alb_listener_rule(self):
        # Given
        alb_listener_arn = (
            "arn:aws:elasticloadbalancing:us-east-1:123456789012:listener/app/"
            "my-load-balancer/50dc6c495c0c9188/f2f7dc8efc522ab2"
        )
        target_group_arn = (
            "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/"
            "my-targets/73e2d6bc24d8a067"
        )

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'alb_listener_arn={}'.format(alb_listener_arn),
            '-var', 'target_group_arn={}'.format(target_group_arn),
            '-no-color',
            '-target=module.alb_listener_rule',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.alb_listener_rule.aws_alb_listener_rule.rule
    action.#:                  "1"
    action.0.target_group_arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-targets/73e2d6bc24d8a067"
    action.0.type:             "forward"
    arn:                       "<computed>"
    condition.#:               "2"
    condition.0.field:         "host-header"
    condition.0.values.#:      "1"
    condition.0.values.0:      "*.*"
    condition.1.field:         "path-pattern"
    condition.1.values.#:      "1"
    condition.1.values.0:      "*"
    listener_arn:              "arn:aws:elasticloadbalancing:us-east-1:123456789012:listener/app/my-load-balancer/50dc6c495c0c9188/f2f7dc8efc522ab2"
    priority:                  "50"
        """.strip() in output # noqa

    def test_create_alb_listener_rule_custom_starting_priority(self):
        # Given
        priority = 16

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'alb_listener_arn=foobar',
            '-var', 'target_group_arn=foobar',
            '-var', 'starting_priority={}'.format(priority),
            '-no-color',
            '-target=module.alb_listener_rule_custom_starting_priority',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.alb_listener_rule_custom_starting_priority.aws_alb_listener_rule.rule
    action.#:                  "1"
    action.0.target_group_arn: "foobar"
    action.0.type:             "forward"
    arn:                       "<computed>"
    condition.#:               "2"
    condition.0.field:         "host-header"
    condition.0.values.#:      "1"
    condition.0.values.0:      "*.*"
    condition.1.field:         "path-pattern"
    condition.1.values.#:      "1"
    condition.1.values.0:      "*"
    listener_arn:              "foobar"
    priority:                  "16"
        """.strip() in output # noqa

    def test_create_alb_listener_rule_host_condition(self):
        # Given
        host_condition = "domain.com"

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'alb_listener_arn=foobar',
            '-var', 'target_group_arn=foobar',
            '-var', 'host_condition={}'.format(host_condition),
            '-no-color',
            '-target=module.alb_listener_rule_host_condition',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.alb_listener_rule_host_condition.aws_alb_listener_rule.rule
    action.#:                  "1"
    action.0.target_group_arn: "foobar"
    action.0.type:             "forward"
    arn:                       "<computed>"
    condition.#:               "2"
    condition.0.field:         "host-header"
    condition.0.values.#:      "1"
    condition.0.values.0:      "domain.com"
    condition.1.field:         "path-pattern"
    condition.1.values.#:      "1"
    condition.1.values.0:      "*"
    listener_arn:              "foobar"
    priority:                  "50"
        """.strip() in output # noqa

    def test_create_alb_listener_rule_two_paths(self):
        # Given
        path_conditions = "[\"/search\", \"/search/*\"]"

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'alb_listener_arn=foobar',
            '-var', 'target_group_arn=foobar',
            '-var', 'path_conditions={}'.format(path_conditions),
            '-no-color',
            '-target=module.alb_listener_rule_two_paths',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.alb_listener_rule_two_paths.aws_alb_listener_rule.rule.0
    action.#:                  "1"
    action.0.target_group_arn: "foobar"
    action.0.type:             "forward"
    arn:                       "<computed>"
    condition.#:               "2"
    condition.0.field:         "host-header"
    condition.0.values.#:      "1"
    condition.0.values.0:      "*.*"
    condition.1.field:         "path-pattern"
    condition.1.values.#:      "1"
    condition.1.values.0:      "/search"
    listener_arn:              "foobar"
    priority:                  "50"

+ module.alb_listener_rule_two_paths.aws_alb_listener_rule.rule.1
    action.#:                  "1"
    action.0.target_group_arn: "foobar"
    action.0.type:             "forward"
    arn:                       "<computed>"
    condition.#:               "2"
    condition.0.field:         "host-header"
    condition.0.values.#:      "1"
    condition.0.values.0:      "*.*"
    condition.1.field:         "path-pattern"
    condition.1.values.#:      "1"
    condition.1.values.0:      "/search/*"
    listener_arn:              "foobar"
    priority:                  "51"
        """.strip() in output # noqa
