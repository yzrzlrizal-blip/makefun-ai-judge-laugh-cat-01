#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Cat review for make.fun's "Make the AI Judge Laugh: Cat Reviews Its Human".

The review itself lives in entry.txt next to this script. Running this
script checks the review against the competition gate (one line, between
1 and 200 characters, no control characters, not only whitespace) and
publishes it as entry.txt inside the output folder the grader provides
through MAKEFUN_OUTPUT_DIR, defaulting to /output.
"""

import os, sys

MAX_CHARS = 200
SOURCE_NAME = "entry.txt"


class BadReview(Exception):
    """Raised when the review in entry.txt breaks the gate."""


def load_review():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, SOURCE_NAME), "rb") as handle:
        raw = handle.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as problem:
        raise BadReview("entry.txt is not valid UTF-8: %s" % problem)
    return text


def check_review(text):
    stripped = text.strip()
    if not stripped:
        raise BadReview("entry.txt holds only whitespace")
    if "\n" in stripped or "\r" in stripped:
        raise BadReview("the review must be a single line")
    if len(stripped) > MAX_CHARS:
        raise BadReview(
            "the review is %d characters, over the %d limit"
            % (len(stripped), MAX_CHARS)
        )
    for char in stripped:
        if ord(char) < 32:
            raise BadReview("the review holds a control character")
    return stripped


def publish_review(text):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise BadReview("published entry.txt does not match the review")
    return target


def run():
    try:
        review = check_review(load_review())
        target = publish_review(review)
    except (OSError, BadReview) as problem:
        print("review rejected: %s" % problem, file=sys.stderr)
        return 1
    print("published %d characters to %s" % (len(review), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
