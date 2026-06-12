"""Scoring tests for the FounderGPT demo."""

from __future__ import annotations

import unittest

from app.engines.failure_prediction_engine import predict_failure_risks
from app.engines.readiness_engine import calculate_readiness_score
from app.orchestration.war_room_pipeline import WarRoomService


class ScoringTests(unittest.TestCase):
    def test_scoring_returns_consistent_shape(self) -> None:
        service = WarRoomService()
        request = service.create_demo_request()

        scorecard = calculate_readiness_score(request)
        risks = predict_failure_risks(request, scorecard)

        self.assertGreaterEqual(scorecard.overall, 50)
        self.assertLessEqual(scorecard.overall, 95)
        self.assertIn(
            scorecard.readiness_stage,
            {"Discovery", "Customer validation", "Focused MVP", "Pilot and fundraising prep"},
        )
        self.assertEqual(len(risks), 4)
        self.assertGreaterEqual(risks[0].probability, risks[-1].probability)


if __name__ == "__main__":
    unittest.main()

