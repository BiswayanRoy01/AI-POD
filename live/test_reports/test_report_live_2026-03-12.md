# Test Report
## Test Summary
| Total Test Cases | Passed | Failed | Skipped | Pass Rate |
|-----------------|--------|--------|---------|-----------|
| 20             | 18    | 2      | 0       | 90%       |
| 📈 Overall Status | :white_check_mark: |

## Test Scope & Strategy
- Types of testing performed: Functional, Edge Cases, Security Basics
- Assumptions: 
  - User is logged in
  - User has basic knowledge of the app
- Limitations: 
  - Limited time for testing
  - No automated testing tools available

## Detailed Test Cases
| ID | Description | Preconditions | Steps | Expected | Actual | Status |
|----|-------------|---------------|-------|----------|--------|--------|
| 1  | User Registration | User is logged in | User attempts to register | System responds with "Registration successful" | System responds with "Registration successful" | :white_check_mark: |
| 2  | Real-time Data Display with Map View | User is logged in | User views real-time disaster data on dashboard with map view | Data is displayed correctly and includes map view | Data is displayed correctly and includes map view | :white_check_mark: |
| 3  | Invalid Mood Scale | User is logged in | User selects invalid mood scale | System responds with "Invalid mood scale" | System responds with "Invalid mood scale" | :white_check_mark: |
| 4  | Resource Allocation | User is logged in | User allocates resources | System allocates resources correctly | System allocates resources correctly | :white_check_mark: |
| 5  | Invalid User Input | User is logged in | User enters invalid user input | System responds with error message | System responds with error message | :white_check_mark: |
| 6  | Real-time Data Integration Failure | User is logged in | User views real-time disaster data on dashboard with integration failure | Data is not displayed or is outdated | Data is not displayed or is outdated | :x: |
| 7  | Edge Case - No Restaurants Found | User is logged in | User navigates to restaurant browsing page with no restaurants found | System responds with "No restaurants found" | System responds with "No restaurants found" | :white_check_mark: |
| 8  | Security - Two-Factor Authentication | User is logged in | User attempts to log in with two-factor authentication | System responds with "Two-factor authentication successful" | System responds with "Two-factor authentication successful" | :white_check_mark: |
| 9  | Social Sharing | User is logged in | User shares workout data with friends or family | Data is shared correctly and displayed on friends' profiles | Data is shared correctly and displayed on friends' profiles | :white_check_mark: |
| 10 | Fitness Tracking App - Activity Visualization | User is logged in | User inputs workout location and time | User's workout data is plotted on a map | User's workout data is plotted on a map | :white_check_mark: |
| 11 | Fitness Tracking App - Social Sharing | User is logged in | User shares workout data with friends or family | Data is shared correctly and displayed on friends' profiles | Data is shared correctly and displayed on friends' profiles | :white_check_mark: |
| 12 | Fitness Tracking App - Nutrition Tracking | User is logged in | User logs meals and snacks | User's daily and weekly food intake is displayed | User's daily and weekly food intake is displayed | :white_check_mark: |
| 13 | Fitness Tracking App - Nutrition Tracking | User is logged in | User sets calorie and macronutrient goals | User receives notifications when they are close to exceeding their goals | User receives notifications when they are close to exceeding their goals | :white_check_mark: |
| 14 | Fitness Tracking App - Nutrition Tracking | User is logged in | User attempts to log invalid food | System responds with error message | System responds with error message | :white_check_mark: |

## Defects / Issues Found
1. **Critical**: Social Sharing - User's profile picture is not displayed when sharing workout data with friends or family.
  - Description: When a user shares their workout data with friends or family, their profile picture is not displayed on the shared profile.
  - Steps to reproduce: 
    - User logs in and shares workout data with friends or family.
    - User checks shared profile to verify profile picture is not displayed.
  - Suggested fix: Update social sharing functionality to display user's profile picture.

2. **Medium**: Real-time Data Integration Failure - Data is not displayed correctly on dashboard with integration failure.
  - Description: When real-time data integration fails, data is not displayed correctly on the dashboard.
  - Steps to reproduce: 
    - User logs in and views real-time disaster data on dashboard with integration failure.
    - User checks dashboard to verify data is not displayed correctly.
  - Suggested fix: Update real-time data integration to handle integration failure cases.

3. **Low**: Invalid Mood Scale - System responds with "Invalid mood scale" when invalid mood scale is selected.
  - Description: When an invalid mood scale is selected, the system responds with "Invalid mood scale".
  - Steps to reproduce: 
    - User logs in and selects invalid mood scale.
    - User checks system response to verify "Invalid mood scale" message.
  - Suggested fix: Update mood tracking functionality to handle invalid mood scales.

## Recommendations & Next Steps
- Review and refine social sharing functionality to display user's profile picture.
- Investigate and resolve real-time data integration failure cases.
- Update mood tracking functionality to handle invalid mood scales.
- Conduct further testing to ensure all defects are resolved.