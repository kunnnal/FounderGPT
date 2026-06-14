import type { WarRoomRequest } from "@/lib/types";

export const defaultWarRoomRequest: WarRoomRequest = {
  startup_name: "OnboardPilot",
  one_line_pitch:
    "Intelligent onboarding coach for B2B SaaS teams that cuts time-to-value and support load.",
  problem:
    "Mid-market B2B SaaS teams lose trial users and expansion revenue because onboarding is manual, implementation is slow, and customer success teams cannot personalize setup at scale.",
  solution:
    "A guided onboarding workspace that maps product setup steps, nudges users toward first value, and gives customer success teams a playbook to reduce drop-off during implementation.",
  target_customer:
    "Series A to C B2B SaaS companies with sales-assisted onboarding and lean customer success teams.",
  business_model:
    "SaaS subscription with pilot onboarding fee and recurring platform seats.",
  market_context:
    "PLG and hybrid sales-led SaaS companies are under pressure to improve activation, expansion, and support efficiency.",
  stage: "mvp",
  traction_summary:
    "Five design partners, two paying pilots, and an early 18 percent improvement in time-to-value.",
  monthly_revenue: 4500,
  monthly_burn: 18000,
  runway_months: 10,
  team_size: 3,
  founder: {
    name: "Aarav Mehta",
    role: "CEO and product lead",
    years_experience: 9,
    domain_expertise:
      "B2B SaaS onboarding, customer success, and product-led growth",
    previous_startup_exits: 0,
    technical_strength: 7,
    go_to_market_strength: 8,
  },
};
