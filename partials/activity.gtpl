<!-- ============================================================ -->
<!--  ACTIVITY SECTION  (auto-updated by the bot)               -->
<!--  Uses readme-scribe Go templates — do NOT edit the         -->
<!--  {{ range ... }} blocks. Change counts if you want more.   -->
<!-- ============================================================ -->

## 🚀 Recent Activity

### 👷 What I'm Currently Working On

{{ range recentContributions 5 }}
- [**{{ .Repo.Name }}**]({{ .Repo.URL }}){{ if .Repo.Description }} — {{ .Repo.Description }}{{ end }}
{{- end }}

---

### 🌱 My Latest Projects

{{ range recentRepos 5 }}
- [**{{ .Name }}**]({{ .URL }}){{ if .Description }} — {{ .Description }}{{ end }}
{{- end }}

---

### 🔨 Recent Pull Requests

{{ range recentPullRequests 5 }}
- [{{ .Title }}]({{ .URL }}) → [{{ .Repo.Name }}]({{ .Repo.URL }})
{{- end }}

---

### ⭐ Recently Starred

{{ range recentStars 5 }}
- [**{{ .Repo.Name }}**]({{ .Repo.URL }}){{ if .Repo.Description }} — {{ .Repo.Description }}{{ end }}
{{- end }}
