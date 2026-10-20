import pipeline_probe


def test_pipeline_stops_on_rejected_sql(monkeypatch):

    def fake_generate_sql():
        return "DELETE FROM contact_events;"

    monkeypatch.setattr(
        pipeline_probe,
        "generate_sql",
        fake_generate_sql
    )

    result = pipeline_probe.run_pipeline_probe()

    assert result is False
