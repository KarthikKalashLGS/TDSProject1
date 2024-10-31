# TDSProject1
# GitHub Repository Data Scraping and Analysis

- Data from GitHub profiles and repositories in Tokyo was scraped to uncover trends in developer preferences, follower count, and language usage.
- The most surprising insight was the strong link between complete profiles (bio, contact info) and higher follower counts, emphasizing profile optimization.
- Developers should prioritize popular languages like JavaScript, Python, and Java and ensure detailed profiles for maximum visibility.

## Data Scraping

This project involved collecting comprehensive GitHub user and repository data through the GitHub API, focusing on users in Tokyo with over 200 followers. Several sequential steps ensured both thorough data collection and adherence to API limitations:

1. **User Data Collection**: We collected user profiles based on location (Tokyo) and a minimum follower threshold of 200, fetching each user's GitHub ID and username.

2. **Detailed Profile Retrieval**: Additional details for each user—such as bio, company, email, follower count, and public repositories—were scraped, with company names standardized for cleaner analysis. Data is saved in both JSON and CSV formats at each step to preserve raw data and avoid any data loss due to errors or interruptions.

3. **Repository Data Extraction**: Detailed repository information for each user was gathered, capturing programming language, star and watcher counts, and repository features like projects and wikis.

4. **Progress Tracking and Data Storage**: `tqdm` progress bars are used to provide visual feedback during lengthy processes. Each stage saves data in JSON and CSV formats, ensuring that raw data is preserved after each major scraping step. This allows the process to resume from saved data if interrupted.

Key libraries included `requests` for handling API requests, `tqdm` for tracking progress, and `pandas` for data processing and storage.

## Error Handling

1. **Rate Limiting and Request Timing**: To avoid hitting the GitHub API rate limit, a delay is added between requests. The code respects GitHub's guidelines, maintaining consistent time gaps, especially during bulk data collection.
   
2. **Network Resilience**: For robustness, error handling is implemented at all critical stages. Requests are wrapped in `try-except` blocks, logging errors and retrying for intermittent network issues. For example, failed requests during repository data collection are logged, ensuring the process continues for the remaining users.

3. **JSON Backups**: All collected data is incrementally saved in JSON format to safeguard the raw data and facilitate recovery in case of interruptions or errors. CSV files are created only after successful completion of each main stage, allowing the program to restart without data loss.

## Data Analysis

The analysis focuses on trends in language popularity, profile completeness, and engagement patterns. Key findings include:

1. **Programming Language Popularity**: JavaScript, Python, and Java emerged as the top three languages, indicating that developers in Tokyo gravitate towards these languages.
2. **Profile Completeness and Engagement**: Users with more complete profiles—bios, company names, and email addresses—showed higher follower counts, suggesting the importance of profile optimization.
3. **Hireability Insights**: The analysis provided engagement metrics for "hireable" users, offering insights for recruiters seeking active GitHub users.

## Recommendation for Developers

Developers looking to boost GitHub visibility should:
- **Focus on Popular Languages**: Concentrating on JavaScript, Python, and Java can enhance appeal and accessibility to a broader audience.
- **Complete Profile Details**: Adding a bio, email, and company name may positively impact engagement and follower counts.
- **Leverage Repository Features**: Features like projects and wikis showcase collaborative skills and enhance profile interactivity.

## Technical Summary

The main code steps include:

1. **Data Collection Functions**:
   - `search_users`: Queries users by location and follower count, with error handling for rate limits and network issues.
   - `get_user_details`: Fetches detailed profile data with retry functionality for network errors.
   - `get_repo_data`: Retrieves repository information with progress tracking and logging for errors.

2. **Data Processing and Saving**:
   - Standardization of company names and date parsing for time-based insights.
   - Storing data in both JSON and CSV formats for safe, intermediate backups.

3. **File Management**:
   - JSON files serve as primary backups for easy data recovery, while CSV files organize data for structured analysis.

By combining progress tracking, robust error handling, and consistent data backups, this approach maximizes data integrity and provides valuable insights for developers and recruiters on GitHub.
