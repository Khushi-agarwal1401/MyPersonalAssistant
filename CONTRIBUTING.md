# Contributing to JUGNU 💜

Thank you for your interest in contributing to **JUGNU**! We are excited to participate in **Winter of Code Social (WOCS) 2026** ❄️.

Whether you are a seasoned open-source contributor or submitting your very first pull request, we are happy to welcome you!

---

## ❄️ Winter of Code Social (WOCS) 2026 Guidelines

### Eligibility & Leaderboard Tracking
- Make sure you are registered for WOCS at [woc.codesocial.tech](https://woc.codesocial.tech).
- Merged pull requests count towards contributor points on the [WOCS Leaderboard](https://woc.codesocial.tech/leaderboard).

### Difficulty Levels & Point System
Every eligible PR will be reviewed and assigned difficulty labels by the Project Admin or Mentors:
- **wocs** + **level 1** = **2 points** (Beginner-friendly, bug fixes, UI tweaks, documentation improvements)
- **wocs** + **level 2** = **5 points** (Moderate features, enhancements, refactoring, new UI options)
- **wocs** + **level 3** = **11 points** (Substantial features, architectural upgrades, model handling, voice integration)

> [!IMPORTANT]
> The **wocs** label and a difficulty level (**level 1**, **level 2**, or **level 3**) must be added to your PR **before** it is merged to ensure points are tracked automatically. Once merged, level assignment is final.

---

## 🤖 AI Usage Policy

In accordance with WOCS guidelines, here is our project AI policy:
- **AI-Assisted Contributions**: You are welcome to use AI tools (e.g. GitHub Copilot, ChatGPT) as assistants for brainstorming, learning, or syntax help.
- **Guidelines**:
  - You must understand every line of code you submit and be able to explain your changes during PR reviews.
  - Blindly copy-pasting unverified AI-generated code without testing or understanding is strictly prohibited.
  - Always run and test your changes locally before submitting a PR.
  - Submitting unverified or hallucinated AI code may lead to PR closure and reporting to Team Code Social.

---

## 🚀 How to Contribute (Step-by-Step)

### 1. Claim or Create an Issue
- Browse open issues in the [Issues tab](https://github.com/kismatkumari56/MyPersonalAssistant/issues).
- Look for good first issue, level 1, level 2, or level 3 tags.
- Comment on the issue asking to be assigned. Please wait for assignment before starting work to avoid duplicate effort.
- Have a new feature idea or found a bug? Open a new issue first to discuss it with maintainers.

### 2. Fork & Clone
1. Fork this repository to your GitHub account.
2. Clone your fork locally:
   `ash
   git clone https://github.com/<your-username>/MyPersonalAssistant.git
   cd MyPersonalAssistant
   `
3. Add the upstream remote:
   `ash
   git remote add upstream https://github.com/kismatkumari56/MyPersonalAssistant.git
   `

### 3. Create a Branch
`ash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
`

### 4. Setup & Test Locally
- Follow the setup guide in [README.md](README.md).
- Install dependencies (pip install requests).
- If working with Ollama, ensure ollama run llama3.2:3b is accessible.
- Test your changes:
  `ash
  python desktop_app.py
  `

### 5. Commit & Push
- Write clear commit messages:
  `ash
  git commit -m "feat: add clear chat confirmation dialog"
  `
- Push to your fork:
  `ash
  git push origin feature/your-feature-name
  `

### 6. Submit a Pull Request
- Open a PR against the main branch of kismatkumari56/MyPersonalAssistant.
- In the PR description:
  - Mention the related issue (e.g., Fixes #1).
  - Describe the changes made and include screenshots/videos if UI changes were introduced.
  - Request review from maintainers/mentors.

---

## 📋 Code Guidelines
- Write readable, clean Python code following PEP 8 conventions.
- Never commit secrets, API keys, passwords, or personal credentials.
- Be respectful, supportive, and beginner-friendly in all discussions.

---

## 💬 Need Help?
- Ask questions in issue discussions or PR comments.
- For WOCS program queries, reach out in the Code Social Discord #wocs-help channel.

Happy Contributing! 🚀