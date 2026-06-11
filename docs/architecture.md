# Architecture

FounderGPT is planned as a three-part system:

- A FastAPI backend that owns orchestration, agent execution, retrieval, scoring, and report generation.
- A frontend dashboard that presents the founder input flow, agent debate, scores, simulations, and final recommendation.
- A grounded knowledge layer powered by Foundry IQ and local hackathon knowledge documents.

The MVP should keep each component modular so local mocks can later be replaced with Microsoft Foundry services.

