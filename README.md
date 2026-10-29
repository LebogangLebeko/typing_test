# Typing Test and Onboarding Assessment App

## Overview

The **Typing Test and Onboarding Assessment App** is a web-based assessment platform designed to evaluate users during the onboarding process. It helps the business identify each user's strengths, development areas, and overall readiness for roles that require active listening, mathematical literacy, information security awareness, and accurate data capturing.

The application includes four assessments:

1. Audio Test
2. Math Test
3. POPIA Test
4. Typing Test

After completing the assessments, the user's results can be used to support onboarding decisions, identify training needs, and create targeted development plans.

## Purpose

The purpose of the application is to provide a consistent and measurable way to assess essential workplace skills. Instead of relying only on interviews or manual observation, the business can use assessment results to better understand a user's capabilities.

The application can help the business to:

- Identify users' strengths and areas for improvement.
- Measure job-related skills during onboarding.
- Highlight users who may require additional training or support.
- Improve the consistency of onboarding assessments.
- Support informed placement and development decisions.
- Track performance across the different assessment categories.

## Assessments

### 1. Audio Test

The Audio Test evaluates the user's ability to listen actively, remain attentive, and gather important information from an audio recording or simulated call.

It may assess:

- Active listening.
- Attention to detail.
- Information retention.
- Ability to identify key details.
- Speed and accuracy when capturing information from a conversation.

This assessment is useful for roles where users must listen to customers, understand requests, and capture information correctly while on a call.

### 2. Math Test

The Math Test evaluates the user's mathematical literacy and problem-solving skills.

It may assess:

- Basic arithmetic.
- Percentages and ratios.
- Numerical reasoning.
- Interpretation of figures.
- Practical workplace calculations.
- Problem-solving ability.

This assessment helps determine whether the user can confidently work with numbers and solve everyday business-related mathematical problems.

### 3. POPIA Test

The POPIA Test evaluates the user's understanding of the **Protection of Personal Information Act (POPIA)** and their awareness of responsible information-handling practices.

It may assess the user's understanding of:

- Personal information and sensitive information.
- Secure handling of customer and employee data.
- Confidentiality requirements.
- Safe storage and sharing of information.
- Password and access-control practices.
- Reporting suspected data breaches or security incidents.
- The user's responsibility when processing personal information.

This assessment helps promote data protection awareness and supports the company's efforts to protect personal information belonging to customers, employees, and other users.

> **Note:** This assessment is intended for onboarding and awareness purposes. It should be reviewed by the organisation's legal, compliance, or information security team before being treated as formal legal or compliance training.

### 4. Typing Test

The Typing Test evaluates the user's data-capturing ability by measuring typing speed and accuracy.

It may assess:

- Words per minute (WPM).
- Typing accuracy.
- Number of errors.
- Corrected and uncorrected mistakes.
- Completion time.
- Overall data-capturing efficiency.

This assessment is useful for roles that require frequent data entry, customer record updates, note-taking, or accurate information capturing.

## Key Features

- User-friendly web interface.
- Four separate onboarding assessments.
- Clear instructions before each test.
- Timed or untimed assessment options.
- Automatic score calculation.
- Typing speed and accuracy measurement.
- Immediate or administrator-controlled results.
- Strength and development-area identification.
- User progress tracking.
- Assessment history and reporting.
- Administrative dashboard for reviewing results.
- Role-based access for users and administrators.

## Results Summary

A completed assessment will show:

- Audio Test score.
- Math Test score.
- POPIA Test score.
- Typing speed in words per minute.
- Typing accuracy percentage.
- Overall assessment score.
- Strongest skill category.
- Areas requiring improvement.
- Suggested training or development actions.

## Suggested Performance Categories

The business can configure score ranges according to its requirements. An example classification is:

- **Strong:** The user meets or exceeds the required standard.
- **Competent:** The user demonstrates an acceptable level of ability.
- **Developing:** The user may require additional training or practice.
- **Support Required:** The user requires focused intervention before performing the related task independently.

Assessment thresholds should be approved by the relevant business, human resources, training, compliance, and operational teams.

## Recommended User Journey

1. The user signs in or receives a unique assessment link.
2. The user reads the instructions and assessment rules.
3. The user completes the Audio Test.
4. The user completes the Math Test.
5. The user completes the POPIA Test.
6. The user completes the Typing Test.
7. The application calculates and stores the results.
8. The user or administrator reviews the results summary.
9. The business identifies strengths, development areas, and recommended next steps.

## Data Protection and Security

Because the application may process personal information and assessment results, the system should apply appropriate security controls.

Recommended controls include:

- Collecting only information that is necessary for the assessment.
- Informing users why their information is being collected.
- Restricting access to authorised users.
- Encrypting sensitive information where appropriate.
- Using secure authentication and password practices.
- Keeping an audit trail of administrative activities.
- Defining how long assessment results will be retained.
- Providing a process for correcting or deleting information where applicable.
- Avoiding unnecessary exposure of individual results.
- Reviewing the application against the organisation's privacy and security policies.

## Getting Started

### Prerequisites

Before running the application, make sure the required development tools and dependencies for the selected technology stack are installed.

### Installation

```bash
# Clone the repository
git clone <https://github.com/LebogangLebeko/typing_test.git>

# Open the project directory
cd typing_test

# Install project dependencies
python3 -m pip install flask reportlab
winget install --id Git.Git -e --source winget

# Start the application
python3 app.py

Replace the placeholder values and commands with the correct details for the project.

## Configuration

Create the required environment configuration file and add the project's settings. Do not commit passwords, API keys, database credentials, or other secrets to the repository.

Example configuration placeholders:

```env
APP_NAME=Onboarding Assessment App
APP_ENV=development
DATABASE_URL=<database-connection>
SESSION_SECRET=<secure-secret>
```

## Testing

Run the project's automated tests using the command that applies to the selected technology stack:

```bash
<test-command>
```

Testing should cover:

- User authentication and authorisation.
- Assessment navigation.
- Timer behaviour.
- Score calculation.
- Typing speed and accuracy calculations.
- Result storage and retrieval.
- Accessibility and keyboard navigation.
- Privacy and security controls.

## Future Improvements

Possible future enhancements include:

- Custom assessment thresholds for different job roles.
- Training recommendations based on test results.
- Downloadable assessment reports.
- Management dashboards and performance trends.
- Multilingual assessment support.
- Accessibility improvements.
- Question randomisation.
- Automated retest scheduling.
- Integration with human resources or learning management systems.
- Email notifications for completed assessments.


## Licence

Add the licence that applies to this project.

## Contact

For questions, support, or access requests, contact:

- **Project Owner:** Lebogang Lebeko
- **Email:** leboshoroma@gmail.com
- **Department:** IT
