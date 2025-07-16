# CI/CD Test Automation Setup Guide

## Optimal Solution: Disable hCaptcha for Test Account

### Why This Is The Best Approach

1. **Eliminates hCaptcha Issues**: No more authentication blocking in headless mode
2. **Reliable CI/CD**: Consistent test execution across all environments  
3. **Performance**: Faster test execution without captcha delays
4. **Maintainability**: No complex workarounds or session management
5. **Industry Standard**: Common practice in enterprise test automation

### Implementation Steps

#### 1. iCIMS Configuration (Recommended)
Contact your iCIMS administrator to:
- **Whitelist test account**: Disable hCaptcha for `automatedtesting@notanemail.com`
- **IP whitelist**: Add CI/CD server IPs to trusted list
- **Test environment**: Configure separate test instance without hCaptcha

#### 2. Test Script Configuration

**For CI/CD (Headless Mode):**
```bash
poetry run python tests/exploratory/test_pilot_simple.py \
  --test-suite docs/icims-ats-demo-simple.md \
  --provider github_copilot \
  --model gpt-4.1
```

**For Development (Visual Debugging):**
```bash
poetry run python tests/exploratory/test_pilot_simple.py \
  --test-suite docs/icims-ats-demo-simple.md \
  --provider github_copilot \
  --model gpt-4.1 \
  --headed-mode
```

### CI/CD Pipeline Integration

#### GitHub Actions Example
```yaml
name: iCIMS Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.11'
      
      - name: Install Dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run iCIMS Test Suite
        run: |
          cd test-pilot
          ./test-suite-runner.sh
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Upload Test Report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-report
          path: test-pilot/test_report.md
```

#### Jenkins Example
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh '''
                    cd test-pilot
                    poetry install
                    ./test-suite-runner.sh
                '''
            }
        }
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test-pilot',
                reportFiles: 'test_report.md',
                reportName: 'iCIMS Test Report'
            ])
        }
    }
}
```

### Alternative Solutions (If hCaptcha Can't Be Disabled)

#### Option 1: Test Environment Configuration
- Set up dedicated test environment without hCaptcha
- Use separate subdomain for automation testing
- Configure environment-specific authentication

#### Option 2: API-Based Testing
- Use iCIMS REST APIs for data validation
- Combine API tests with minimal UI verification
- Focus UI tests on critical user journeys only

#### Option 3: Captcha Bypass Services
- **2captcha**: Automated captcha solving service
- **Anti-Captcha**: Enterprise captcha solving
- **Death by Captcha**: Another solving service

**Implementation example:**
```python
# Add to test_pilot_simple.py if needed
async def handle_captcha_with_service(page):
    """Handle captcha using external solving service"""
    if await page.locator("iframe[src*='hcaptcha']").is_visible():
        # Use captcha solving service API
        captcha_solution = await solve_captcha_external()
        await page.fill("captcha-response", captcha_solution)
```

### Environment Variables

```bash
# .env file for CI/CD
ICIMS_TEST_URL=https://configrariet.icims.com
ICIMS_TEST_USERNAME=automatedtesting@notanemail.com  
ICIMS_TEST_PASSWORD=Ready2test!
GITHUB_TOKEN=your_github_token
CAPTCHA_DISABLED=true
```

### Benefits of This Approach

1. **99.9% Reliability**: No captcha-related failures
2. **Fast Execution**: Tests run at full speed
3. **Easy Maintenance**: Simple configuration
4. **Scalable**: Works across multiple CI/CD systems
5. **Cost Effective**: No external services needed

### Monitoring and Alerting

```bash
# Add to CI/CD pipeline
if [ $? -eq 0 ]; then
    echo "✅ iCIMS tests passed"
    # Send success notification
else
    echo "❌ iCIMS tests failed"
    # Send failure alert with test report
    curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"iCIMS Test Suite Failed - Check test report"}' \
        $SLACK_WEBHOOK_URL
fi
```

### Security Considerations

1. **Test Account Isolation**: Ensure test account has minimal permissions
2. **Environment Separation**: Keep test and production environments separate
3. **Credential Management**: Use CI/CD secrets for sensitive data
4. **Access Logging**: Monitor test account usage

## Implementation Priority

1. ✅ **Primary**: Disable hCaptcha for test account (recommended)
2. ⚠️ **Secondary**: Use dedicated test environment
3. 🔧 **Fallback**: Captcha solving services
4. 📊 **Alternative**: API-focused testing strategy

This approach provides the most reliable, maintainable, and cost-effective solution for automated testing in CI/CD environments.
