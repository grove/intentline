# Apache-2.0; adapted/extracted from grove/proofline, copyright its contributors.
# Pinned original function; imports and InputGap below are offline test scaffolding.
import re

class InputGap(ValueError):
    pass


def criterion_ids(brief):
    ids = re.findall(r"^\|\s*([A-Z][A-Z0-9]*-[0-9]+|[A-Z][0-9]+)\s*\|\s*\S", brief, re.MULTILINE)
    if not ids or len(ids) != len(set(ids)):
        raise InputGap("The direct brief needs unique material criterion IDs in Markdown table rows, e.g. | D1 | Required outcome |")
    return ids
