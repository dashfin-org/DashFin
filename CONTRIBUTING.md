# Contributing to dashfin-org

Thank you for your interest in contributing to the dashfin-org project! Please take a moment to read this document before submitting issues or pull requests to ensure a smooth collaboration.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)

   * [Reporting Bugs](#reporting-bugs)
   * [Suggesting Enhancements](#suggesting-enhancements)
   * [Submitting Pull Requests](#submitting-pull-requests)
3. [Development Setup](#development-setup)
4. [Branching Strategy](#branching-strategy)
5. [Code Style Guidelines](#code-style-guidelines)
6. [Commit Message Guidelines](#commit-message-guidelines)
7. [Testing](#testing)
8. [Documentation](#documentation)
9. [Security](#security)
10. [Contacts and Support](#contacts-and-support)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to abide by its terms. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

1. Confirm whether the bug exists on the latest `main` branch.
2. Open an issue under the issue tracker with the following details:

   * **Steps to reproduce**
   * **Expected behavior**
   * **Actual behavior**
   * **Environment** (OS, Node/Python/Go version, etc.)

### Suggesting Enhancements

1. Check existing issues and pull requests for similar ideas.
2. Open an issue and tag it as an enhancement.
3. Provide a clear use case and possible implementation approach.

### Submitting Pull Requests

1. Fork the repository and create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Write clear, atomic commits with meaningful messages.
3. Ensure all tests pass and adhere to code style (see below).
4. Submit a pull request targeting `main`.
5. Describe what your change does and why it's needed.
6. Link to any relevant issues.

---

## Development Setup

1. **Clone the repo:**

   ```bash
   git clone https://github.com/dashfin-org/project.git
   cd project
   ```
2. **Install dependencies:**

   * For **Node.js**:

     ```bash
     npm install
     ```
   * For **Python** (if applicable):

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
3. **Run locally:**

   ```bash
   npm start
   # or
   python main.py
   ```

---

## Branching Strategy

We use the [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) workflow:

* `main`: production-ready releases
* `develop`: integration branch for features
* `feature/*`: new feature branches off `develop`
* `release/*`: prep release branches off `develop`
* `hotfix/*`: urgent fixes off `main`

---

## Code Style Guidelines

* **Indentation:** 2 spaces (JS/TS), 4 spaces (Python)
* **Line length:** max 100 characters
* **Naming:** `camelCase` for JS/TS, `snake_case` for Python
* **Linting:** run `npm run lint` or `flake8 .`
* **Formatting:** use Prettier (JS/TS) or Black (Python).

---

## Commit Message Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

* **type:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
* **scope:** module or file affected.

Example:

```
feat(auth): add JWT refresh token endpoint
```

---

## Testing

1. Write tests alongside your code.
2. Run tests:

   ```bash
   npm test    # JS/TS projects
   pytest      # Python projects
   ```
3. Aim for >80% coverage. Use coverage tools (`nyc`, `coverage.py`).

---

## Documentation

* Update [README.md](README.md) with usage, examples, and configuration notes.
* Document public APIs using JSDoc/Docstrings.
* Generate HTML/docs as needed via `npm run docs` or Sphinx.

---

## Security

Report vulnerabilities via email to [security@dashfin.org](mailto:security@dashfin.org). Do not open public issues for security concerns.

---

## Contacts and Support

* **Maintainers:**

  * @alice ([alice@dashfin.org](mailto:alice@dashfin.org))
  * @bob ([bob@dashfin.org](mailto:bob@dashfin.org))
* **Slack channel:** `#dashfin-support`

## OpenAI GitHub Connector Agent Access

To ensure uninterrupted, full access for the OpenAI GitHub Connector Agent:

1. **Install and Configure GitHub App**

   * Verify that the **OpenAI GitHub Connector** GitHub App is installed in the dashfin-org organization with *All repositories* access.
   * Confirm that the App’s permissions include:

     * **Contents**: Read & write
     * **Pull requests**: Read & write
     * **Issues**: Read & write
     * **Metadata**: Read-only
2. **Personal Access Token (PAT)**

   * The agent requires a GitHub PAT scoped to:

     * `repo` (full control of private repositories)
     * `workflow` (update GitHub Actions workflows)
     * `read:org` (read org membership)
   * Store the PAT in GitHub Actions secrets under `OPENAI_GITHUB_TOKEN`.
3. **Environment Variables**

   * For local development, set the PAT on your machine:

     ```powershell
     $Env:OPENAI_GITHUB_TOKEN = "<your_token_here>"
     ```
4. **Validation**

   * After setup, run the agent’s self-check:

     ```bash
     npm run openai-github-check
     ```
   * The script will report any missing scopes or installation issues.

If you encounter any access disruptions with the OpenAI GitHub Connector Agent, please open an issue tagged `infra` immediately. We’ll coordinate with the security and DevOps teams to restore full access.

Thank you for ensuring the connector remains operational!
