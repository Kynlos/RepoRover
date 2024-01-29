# RepoRover - GitHub Repository Automation Companion 🚀

## Overview

Welcome to RepoRover, your indispensable companion for seamlessly navigating the expansive realm of GitHub repositories! 🌌 This Python script, aptly named RepoRover (reporover.py), brings a touch of sophistication to your repository-related tasks, making automation both enjoyable and efficient.

## Features

- **Commit Exploration**: Embark on an insightful journey through commit history, unraveling the details of each SHA, message, author, and date.
- **Real-time Console Updates**: Stay informed with dynamic updates in the console as RepoRover diligently explores the GitHub cosmos.
- **Tailored Log Files**: Craft individual log files for each repository, capturing changes with the precision of a seasoned explorer.
- **Consolidated Log Hub**: Assemble all logs into a unified hub for a comprehensive view of your GitHub ventures.
- **HTML Data Maps**: Generate HTML logs for a polished and organized representation, enhancing your journey through repositories.
- **Configuration Mastery**: Harness the power of RepoRover's customizable behavior through the `config.ini` file, offering flexibility and control.
- **Database Integration Excellence**: Store repository data in an SQLite database, creating a robust archive of historical changes.

## Usage

1. Plot your course by configuring repository URLs in the `config.ini` file under the `[GitHubRepos]` section.
2. Tailor your journey with preferences, scheduling, HTML logs, and database options in the `config.ini` file.
3. Launch RepoRover using the command: `python reporover.py`, and witness its automatic navigation through the GitHub galaxy, uncovering the intricacies of each repository.

## Configuration Options

- **GitHub Token**: Secure your GitHub token in the `config.ini` file under the `[GitHub]` section.
- **Log Preferences**: Choose the specific information to log, such as stars, forks, popularity comparisons, and latest releases.
- **Scheduling Mastery**: Set the time interval for RepoRover to embark on its automatic explorations.
- **HTML Logging Elegance**: Toggle HTML log generation for visually appealing representations of your GitHub expeditions.
- **Database Integration Wisdom**: Decide whether to store repository data in a robust database and specify the database file.

## Getting Started

1. Ensure you have Python installed and are ready for a productive coding session.
2. Configure your `config.ini` file with repository URLs and preferences.
3. Install required packages by running: `pip install beautifulsoup4 github3.py tqdm`.
4. Launch RepoRover using the command: `python reporover.py`.

**Note**: If you haven't set a GitHub token, RepoRover will prompt you during its exploration.

Embark on your GitHub journey with RepoRover, and may your code explorations be both enriching and enjoyable! 🌟🚀 If you have any questions or wish to share your experiences, feel free to reach out. Happy coding! 🌌✨

## Known Issues

`HTML Output` and `Combined Outputs` are not currently filling with data.  Will be fixed in a future update.
