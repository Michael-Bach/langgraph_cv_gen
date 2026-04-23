from apply.graph import build_graph, should_revise


def test_graph_builds_without_error():
    g = build_graph()
    assert g is not None


def test_graph_has_expected_nodes():
    g = build_graph()
    node_names = set(g.nodes.keys())
    expected = {
        "fetch_job", "parse_job", "evaluate_fit", "human_approval",
        "draft_cv", "draft_cover_letter", "review", "revise", "compile_latex",
    }
    assert expected.issubset(node_names)


def test_should_revise_when_needed_and_count_below_2():
    state = {"review_critique": {"needs_revision": True}, "revision_count": 0}
    assert should_revise(state) == "revise"


def test_should_compile_when_max_revisions_reached():
    state = {"review_critique": {"needs_revision": True}, "revision_count": 2}
    assert should_revise(state) == "compile"


def test_should_compile_when_no_revision_needed():
    state = {"review_critique": {"needs_revision": False}, "revision_count": 0}
    assert should_revise(state) == "compile"


def test_should_compile_when_critique_missing():
    state = {"revision_count": 0}
    assert should_revise(state) == "compile"
