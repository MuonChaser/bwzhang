# Repository Guidelines

## Project Structure & Module Organization

This repository is a Hugo static site using the `PaperMod` theme. Site configuration lives in `hugo.toml` and legacy settings may also appear in `config.toml`. Blog content is stored under `content/posts/`, with section pages such as `content/archives.md` and `content/search.md`. Reusable Hugo layout overrides belong in `layouts/`, translations in `i18n/`, and archetypes in `archetypes/`. Source assets belong in `assets/`; files copied directly to the built site belong in `static/`, including `static/CNAME` and the standalone `static/homepage/`. The `public/` directory is generated output and should not be edited by hand. Theme code is vendored as a git submodule under `themes/PaperMod/`.

## Build, Test, and Development Commands

- `hugo server -D`: run the local development server, including draft content.
- `hugo --minify`: build the production site into `public/`.
- `hugo --gc --minify`: production build with cleanup of unused generated resources.
- `git submodule update --init --recursive`: fetch the PaperMod theme after cloning.
- `./auto_push.sh`: build and sync `public/` to the configured VPS with `rsync`; review changes before using.

GitHub Actions builds Pages on pushes to `main` with Hugo `0.152.2`.

## Coding Style & Naming Conventions

Use TOML for Hugo configuration and Markdown with front matter for posts. Keep content filenames descriptive; existing posts use lowercase English slugs such as `content/posts/math/kl.md` and Chinese titles where appropriate, such as `矩阵求导.md`. Prefer two-space indentation in TOML tables and YAML-like front matter. Keep custom CSS, JavaScript, and templates scoped to `assets/` or `layouts/` unless intentionally modifying the theme submodule.

## Testing Guidelines

There is no separate test suite. Validate changes by running `hugo --minify` before committing. For content edits, also preview with `hugo server -D` and check navigation, search pages, tags/categories, images, and code blocks. Treat Hugo warnings as issues to fix unless they are already known theme warnings.

## Commit & Pull Request Guidelines

Recent history uses short Chinese commit messages that describe the change, for example `更新个人主页的副标题和社交链接` or `切换主题为 PaperMod，更新配置`. Follow that concise imperative style and group related content/config changes together. Pull requests should include a brief summary, affected pages or paths, verification command output, and screenshots when visual layout changes.

## Security & Configuration Tips

Do not commit secrets, deployment keys, or local machine artifacts. Avoid committing `.DS_Store` files. Review `auto_push.sh` before deployment because it targets a specific remote host and uses `--delete` on the destination directory.
