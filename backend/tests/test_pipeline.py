"""Pipeline tests for the FounderGPT demo."""

from __future__ import annotations

import unittest

from app.orchestration.war_room_pipeline import WarRoomService


class PipelineTests(unittest.TestCase):
    def test_pipeline_creates_complete_session(self) -> None:
        service = WarRoomService()
        request = service.create_demo_request()

        response = service.run_analysis(request)

        self.assertTrue(response.session_id.startswith("session_"))
        self.assertEqual(response.request.startup_name, "OnboardPilot")
        self.assertGreaterEqual(len(response.agent_findings), 11)
        self.assertGreaterEqual(len(response.debate), 5)
        self.assertGreaterEqual(len(response.citations), 4)
        self.assertEqual(response.recommendation.decision, "Build a tighter MVP and win design partners")
        self.assertIsNotNone(service.get_session(response.session_id))


if __name__ == "__main__":
    unittest.main()

