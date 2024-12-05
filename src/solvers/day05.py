from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel


class PageOrderingRule(BaseModel):
    before: int
    after: int


class SafetyManualUpdate(BaseModel):
    pages: list[int]

    def get_middle_page(self) -> int:
        return self.pages[len(self.pages) // 2]


class SafetyManualValidator:
    def __init__(self):
        self.rules: list[PageOrderingRule] = []

    def add_rule(self, rule: PageOrderingRule):
        self.rules.append(rule)

    def validate(self, manual: SafetyManualUpdate) -> bool:
        for rule in self.rules:
            if rule.before not in manual.pages or rule.after not in manual.pages:
                # this rule does not apply
                continue

            # test rule
            before_index = manual.pages.index(rule.before)
            after_index = manual.pages.index(rule.after)

            if before_index > after_index:
                return False

        return True

    def fix_manual(self, manual: SafetyManualUpdate) -> SafetyManualUpdate:
        rules_of_interest = [
            r
            for r in self.rules
            if r.before in manual.pages and r.after in manual.pages
        ]

        manual = self.swap_pages(manual, rules_of_interest)
        while not self.validate(manual):
            manual = self.swap_pages(manual, rules_of_interest)

        return manual

    def swap_pages(
        self, manual: SafetyManualUpdate, rules: list[PageOrderingRule]
    ) -> SafetyManualUpdate:
        for rule in rules:
            before_index = manual.pages.index(rule.before)
            after_index = manual.pages.index(rule.after)

            if before_index > after_index:
                # swap
                manual.pages[before_index], manual.pages[after_index] = (
                    manual.pages[after_index],
                    manual.pages[before_index],
                )

        return manual


def parse_input(
    lines: list[str],
) -> Tuple[SafetyManualValidator, list[SafetyManualUpdate]]:
    validator = SafetyManualValidator()
    manuals = []

    # rules, then input
    for line in lines:
        if "|" in line:
            # rule
            numbers = re.findall(r"\d+", line)
            if len(numbers) != 2:
                raise ValueError("Invalid rule")

            rule = PageOrderingRule(before=int(numbers[0]), after=int(numbers[1]))
            validator.add_rule(rule)

        elif "," in line:
            # manual
            numbers = re.findall(r"\d+", line)
            manuals.append(SafetyManualUpdate(pages=[int(n) for n in numbers]))

    return (validator, manuals)


def solve_part1() -> int:
    # lines = read_lines("input/day05/example.txt")
    lines = read_lines("input/day05/part1.txt")

    validator, manuals = parse_input(lines)

    total = 0
    for manual in manuals:
        if not validator.validate(manual):
            continue

        total += manual.get_middle_page()

    return total


def solve_part2() -> int:
    # lines = read_lines("input/day05/example.txt")
    lines = read_lines("input/day05/part1.txt")

    validator, manuals = parse_input(lines)
    invalid_manuals = [m for m in manuals if not validator.validate(m)]

    total = 0
    for manual in invalid_manuals:
        fixed_manual = validator.fix_manual(manual)
        total += fixed_manual.get_middle_page()

    return total
