#!/usr/bin/env python

import os

from setuptools import find_packages, setup

VERSION = os.getenv("CI_COMMIT_TAG")
if not VERSION:
    VERSION = "0.0.1"

# --- >
setup(
    name="skill-interest-stories-tavrida",
    version=VERSION,
    package_dir={'skill_interest_stories_tavrida': 'src/skill_interest_stories_tavrida'},
    python_requires=">=3.6.8",
    packages=find_packages(where='src', include=['skill_interest_stories_tavrida']),
    url="https://gitlab.com/mailru-voice/external_skills/skill_interest_stories_tavrida",
    license="MIT",
    author="n.orgeev",
    author_email="n.orgeev@corp.mail.ru",
    description="skill-interest-stories-tavrida",
)

