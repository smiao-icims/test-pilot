# CI/CD OPTIMIZED: Single-stage headless mode (hCaptcha disabled for test account)
poetry run python tests/exploratory/test_pilot_simple.py \
  --test-suite docs/icims-ats-demo-simple.md \
  --provider github_copilot \
  --model gpt-4.1

# DEVELOPMENT: Single-stage headed mode (visual debugging)
# poetry run python tests/exploratory/test_pilot_simple.py \
#   --test-suite docs/icims-ats-demo-simple.md \
#   --provider github_copilot \
#   --model gpt-4.1 \
#   --headed-mode

# EXPERIMENTAL: Two-stage mode (Playwright MCP storage state has limitations)
# poetry run python tests/exploratory/test_pilot_simple.py \
#   --test-suite docs/icims-ats-demo-simple.md \
#   --provider github_copilot \
#   --model gpt-4.1 \
#   --two-stage-mode \
#   --storage-file browser_storage.json  

