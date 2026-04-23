from apply.profile import load_profile


def test_load_profile_returns_all_keys():
    profile = load_profile()
    expected_keys = {
        "candidate_profile",
        "behavioral_profile",
        "writing_style",
        "job_evaluation",
        "cv_templates",
        "cover_letter_templates",
    }
    assert expected_keys == set(profile.keys())


def test_load_profile_values_are_nonempty_strings():
    profile = load_profile()
    for key, value in profile.items():
        assert isinstance(value, str), f"{key} is not a string"
        assert len(value) > 0, f"{key} is empty"
