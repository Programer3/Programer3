# 🛠️ Setup Guide — Auto-Updating GitHub Profile README

Follow these steps once and the bot does the rest forever.

---

## Step 1 — Create the special profile repo

GitHub shows a special README on your profile if you have a **public repo
named exactly the same as your username**.

1. Go to https://github.com/new
2. Set the repository name to **`Programer3`** (your username)
3. Make it **Public**
4. **Don't** add a default README — you'll push yours
5. Click **Create repository**

---

## Step 2 — Push these files

```bash
git clone https://github.com/Programer3/Programer3
cd Programer3

# Copy all the files from this zip into the folder, then:
git add .
git commit -m "feat: initial profile README setup"
git push origin main
```

---

## Step 3 — Create a Personal Access Token (PAT) for metrics

The metrics workflow needs extra scopes that `GITHUB_TOKEN` doesn't have.

1. Go to https://github.com/settings/tokens/new
2. Give it a name like `METRICS_TOKEN`
3. Select these scopes:
   - `read:user`
   - `repo`
   - `read:packages`
4. Click **Generate token** and copy it

Then add it as a secret:

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `METRICS_TOKEN`
4. Value: paste the token you just copied
5. Click **Add secret**

> The `GITHUB_TOKEN` secret is added automatically — you don't need to do anything for it.

---

## Step 4 — Trigger the workflows once manually

1. Go to your repo → **Actions** tab
2. Click **"Update README"** → **Run workflow** → **Run workflow**
3. Click **"Generate Metrics SVG"** → **Run workflow** → **Run workflow**

After ~30 seconds, both workflows will commit back to your repo and your profile README will be live! 🎉

---

## Customizing your README

| File | What to edit |
|------|-------------|
| `partials/header.gtpl` | Banner title, tagline, typing animation text |
| `partials/about.gtpl` | Bio bullets, email, fun fact |
| `partials/tech-stack.gtpl` | Add/remove technology icons |
| `partials/activity.gtpl` | Change how many recent items show (the number in `range recentContributions 5`) |
| `partials/stats.gtpl` | Theme, card layout, which stats to show |
| `partials/footer.gtpl` | Social links |
| `.github/workflows/metrics.yml` | Which metric plugins to enable |

**Never edit `README.md` directly** — the bot overwrites it on every run.

---

## How it works

```
You edit README.gtpl or partials/*.gtpl
         ↓
GitHub Actions runs readme-scribe
         ↓
README.md is rendered and committed (auto)
         ↓
Metrics workflow generates github-metrics.svg (auto)
         ↓
Your GitHub profile shows the updated README ✓
```

Both workflows run on a schedule (daily / every 6 hours) and also fire
on every push to `main`, so changes go live immediately.
