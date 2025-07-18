# iCIMS ATS Platform Complete Test Suite

## Overview

This test suite covers the complete user journey in the iCIMS platform:
- **Authentication**: Login and session management
- **Job Management**: Search, view, and navigate job requisitions
- **Candidate Management**: Review candidates and handle attachments
- **File Operations**: Upload and download attachments
- **Session Management**: Proper logout and session termination

## Prerequisites

Before running this test:
1. **Environment Setup**: 
2. **Access Rights**: Ensure test account has appropriate permissions
3. **Network Access**: Verify connectivity to iCIMS platform
4. **MCP Tool**: Confirm MCP Playwright tool is configured in VS Code

## Global Configuration

```
Browser: Chrome (recommended for this demo)
Website: https://configrariet.icims.com
Network: Standard timeout settings
```

---

## Automatic Test Execution Instructions

Complete the ATS testing workflow automatically.
**Do not ask for confirmation. Complete all steps in the test suite automatically. If you encounter ambiguity, make a best guess and continue**


## Manual Test Execution Instructions

For step-by-step manual execution, copy and paste the following sections to execute the test suite using MCP Playwright tool:


### Phase 1: Authentication and Login

```
Please use the MCP Playwright tool to execute this complete iCIMS ATS login sequence:

1. **Initial Navigation**:
   - Navigate to https://configrariet.icims.com
   - Take an accessibility snapshot to assess page state

2. **Authentication Check**:
   - Look for "Logged in as..." text to check existing session
   - If already logged in, click the home icon to go to dashboard
   - If not logged in, proceed with login flow

3. **Login Process**:
   - Locate the "Username or email address" input field
   - Enter username: automatedtesting@notanemail.com
   - if you see a reCaptcha screen, check "I am a human"
   - Hit Enter or Click "Continue" button to proceed to password screen
   - Wait for password page to load completely
   - Locate the "Password" input field
   - Enter password: Ready2test!
   - if you see a reCaptcha screen, check "I am a human"
   - Hit Enter or Click the "LOG IN" button

4. **Two-Factor Authentication Handling**:
   - If "two-step verification" prompt appears:
     - Look for "No, just a password" or "Skip for now" options
     - Click the appropriate option to bypass 2FA

5. **Login Verification**:
   - Wait for dashboard to load completely
   - Take accessibility snapshot of dashboard
   - Verify presence of "Logged in as..." text when mouse over Profile picture
   - Confirm platform URL contains "/platform"
   - Report login success status

Expected Results: Successful authentication and access to iCIMS dashboard
```

### Phase 2: Job Search and Navigation

```
Continue with job search testing using MCP Playwright tool:

1. **Navigate to Job Search**:
   - From the main dashboard, locate the "Search" menu button in main navigation toolbar
   - **Method 1 - Hover then Click**:
     - First hover over the "Search" button to trigger the dropdown menu
     - Wait 1-2 seconds for dropdown to appear
     - Then click on "Job" option in the dropdown menu
   - **Method 2 - Keyboard Navigation** (if Method 1 fails):
     - Press Tab key repeatedly until "Search" button is focused (highlighted)
     - Press Enter or Space key to open the dropdown menu
     - Use Arrow Down key to navigate to "Job" option
     - Press Enter to select "Job" option
   - **Method 3 - Force Click Sequence** (if above methods fail):
     - Take accessibility snapshot to see current state
     - Try clicking on "Search" button multiple times with 1-second delays
     - Look for dropdown menu appearance in subsequent snapshots
     - Click on "Job" option when dropdown becomes visible
   - Wait for job search interface to load completely (may take 1-2 seconds)
   - Take snapshot of job search interface

2. **Execute Job Search**:
   - Locate the keyword search input field
   - Enter search term: "Computer Programmer"
   - Try one of these approaches in sequence:
     - Click search button to execute search
     - Press Enter key while in the search field
     - If neither works, try tabbing to the search button and pressing Enter
   - Wait for search results to load completely (at least 1 second)
   - Take accessibility snapshot of search results

3. **Analyze Search Results**:
   - Count and report number of jobs found
   - Note job titles and requisition IDs displayed
   - Verify search results are relevant to keyword

4. **Access Job Details**:
   - Click on the first job/requisition in results (look for job ID link)
   - Wait for job details page to load (at least 1 second)
   - Verify job information, tabs, and navigation options are visible

5. **View Job Details**
   - Navigate "Details" tab if available 
   - Note Compensation details
   - Verify compensation details

6. **View Description**
   - Navigate "Description" tab if available
   - Note Job Description, Responsibilities and Qualifications
   - Verify the description

Expected Results: Successful job search with relevant results and accessible job details
```

### Phase 3: Candidate Management

```
Continue with candidate management testing:

1. **Navigate to Candidates**:
   - From the job details page, locate and click the "Candidates" tab
   - Wait for candidates list to load completely
   - Take accessibility snapshot of candidates interface

2. **Review Candidate Information**:
   - Count and report number of candidates for this job
   - Note candidate names and status information
   - Select the candidate Anika West to view her profile (click on candidate name Anika West)

3. **Access Candidate Profile**:
   - Wait for candidate profile page to load
   - Look for tabs like "Person Attachments" or "Documents"

4. **Test File Attachment Operations**:
   - Click "More" tab downdrop if available
   - Navigate to "Person Attachments" tab if available
   - If no attachments exist:
     - Create a test file: test-attachment.txt with content "hello world"
     - Use "Add Attachment" button to upload the test file
     - Wait for upload completion and verify file appears
   - If attachments exist:
     - Locate download links or icons
     - Test download functionality by clicking first download option
     - Verify download initiates successfully

Expected Results: Access to candidate profiles and successful file operations
```

### Phase 4: Person Search

1. **Navigate Person Search**
   - Locate the "Search" menu button in main navigation toolbar
   - **Method 1 - Hover then Click**:
     - First hover over the "Search" button to trigger the dropdown menu
     - Wait 1-2 seconds for dropdown to appear
     - Then click on "Person" option in the dropdown menu
     - Then click on "Person" (Search -> Person -> Person) Note click second Person will bring us to the Person search screen
   - **Method 2 - Keyboard Navigation** (if Method 1 fails):
     - Press Tab key repeatedly until "Search" button is focused (highlighted)
     - Press Enter or Space key to open the dropdown menu
     - Use Arrow Down key to navigate to "Person" option
     - Press Enter to select "Person" option
     - Click "Person" 
2. **Add Person Search:Filters**
   - Click "Show More" in "Person Search: Filters" panel if available
   - Click "Add Filter" button label with a plus icon
   - Wait for the "Add Filter" flyout to be displayed
   - Type "Marital Status" in "Narrow down results" search box and then hit Enter
   - Locate and select "Marital Status" under "DEI Tab"
   - Click "Add Selected"
   - Select "is" from the dropdown for "Marital Status" filter
   - Locate the "Search" button in "Add Filter" flyout page (at the bottom of the flyout, please do not confuse with Person Search button)
   - Wait for the search result 

3. **Verify Search Result**
   - Count and report number of people found 
   - Note Full Name, Email, etc. 

4. **Add additional Search:Filter**
   - Click "Add Filter" button label with a plus icon
   - Wait for the "Add Filter" flyout to be displayed
   - Type "City" in "Narrow down results" search box and then hit Enter
   - Locate and click "Profile & Experience Tab"
   - Locate and Select "City"
   - Click "Add Selected"
   - Select "is" from the dropdown 
   - Click "--Blank--" text box next to "is" operator
   - Type "London"
   - Locate and Click "Search" button with an icon

5. **Verify Search Result again**
   - Count and report number 
   - Note Full Name, Email, etc. 

6. **Export Search Result**
   - Locate and check "Select All" checkbox under "Person Search Result" title
   - Navigate to "Export" (you may need to click "More" dropdown and then click "Export")
   - Wait for Export Dialog screen 
   - Click "Export" button 
   - Wait for "Download File" to be displayed (at least 2 seconds)
   - Click "Download File" 
   - Click "Close" button after the file is downloaded

### Phase 5: Session Termination

```
Complete the test suite with proper logout:

1. **Logout Process**:
   - From any authenticated page, locate "Logged in as Automated Testing" button in header
   - Try one of these approaches in sequence:
     - Click on the user profile button to open user menu
     - If clicking fails, press Tab key multiple times until user profile button is focused, then press Enter
     - If both fail, try direct navigation to https://login.icims.com/logout

2. **Execute Logout**:
   - If user menu opened successfully:
     - Locate and click "Log out" option in user menu
     - Wait for logout process to complete
   - Allow page redirection to logout confirmation
   - If redirected to an error page, navigate directly to https://login.icims.com/logout

3. **Verify Logout Success**:
   - Take accessibility snapshot of logout page
   - Confirm page title shows "iCIMS Logout Successful"
   - Verify "You have been logged out successfully" message
   - Check that "Log In" button is available for re-authentication
   - Confirm no "Logged in as..." text remains visible

Expected Results: Complete session termination with logout confirmation
```

---

## Test Verification Checklist

Throughout test execution, verify:

✅ **Page Loading**:
- All pages load without errors
- Loading indicators appear and disappear appropriately
- No JavaScript console errors

✅ **Element Interaction**:
- All buttons and links are clickable
- Form inputs accept text correctly
- Navigation menus function properly

✅ **Data Integrity**:
- Search results match search criteria
- Candidate information displays correctly
- File uploads/downloads work properly

✅ **User Experience**:
- Pages respond within reasonable time
- Visual feedback for user actions
- Error messages are clear and actionable

✅ **Security & Session Management**:
- Login/logout processes work correctly
- Session state maintained during navigation
- Proper access control enforcement

## Troubleshooting Guide

### Common Issues:

1. **Login Failures**:
   - Verify credentials in .env file
   - Check for two-factor authentication prompts
   - Ensure network connectivity to iCIMS

2. **Navigation Issues**:
   - Wait for pages to load completely before next action
   - Take snapshots to verify page state
   - Check for dynamic content loading

3. **Element Not Found**:
   - Take accessibility snapshot to see current page state
   - Look for alternative element selectors
   - Verify page has loaded completely

4. **File Operation Issues**:
   - Ensure test files exist in correct location
   - Check browser download settings
   - Verify file permissions

5. **Click Interaction Failures**:
   - If clicking an element fails, try keyboard navigation (Tab key + Enter)
   - Try alternative direct URLs when possible
   - Check if elements are inside iframes that need to be focused first
   - Use explicit waits (5-10 seconds) before interactions with complex UI elements

### Recovery Steps:

1. If test gets stuck, take snapshot to assess state
2. Navigate back to known good state (dashboard)
3. Re-attempt failed operation with different approach
4. Clear browser state if necessary and restart
5. For persistent click issues, try these fallback strategies:
   - Use keyboard navigation (Tab/Shift+Tab to focus, Enter to click)
   - Try direct URL navigation if possible
   - Use browser refresh and retry the operation
   - Increase wait times before interactions
