# Automatic LinkedIn news: prepared, not connected

The News page works now with three sourced editorial updates. It is **not currently receiving new LinkedIn posts automatically**. No LinkedIn read credential was available in this session. No GitHub workflow has been installed or activated in the live repository.

The package includes a working import and static-rendering pipeline. Once authorized and deployed, it reads public posts every six hours, updates the news snapshot and redeploys the static site. This is polling, not an immediate webhook.

## Access needed

LinkedIn's official personal-post read permission is `r_member_social`, which is restricted. Ordinary sign-in or the `w_member_social` sharing permission does not grant read access. Creating a developer application alone does not guarantee approval.

Documentation: [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-06), [API access](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access).

If you have approved personal-post API access, configure repository secrets `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_AUTHOR_URN`, and the repository variable `LINKEDIN_API_VERSION` with a currently supported version from LinkedIn's official API documentation. Do not put credentials in HTML, JavaScript, Git history or a public JSON file. Tokens expire and must be renewed when required by the provider.

Enable the repository variable `LINKEDIN_NEWS_ENABLED=true` only after a successful manual import. Without these inputs the scheduled import remains gated off. A missing credential or failed provider request fails without deleting previous news.

## Deployment

The workflow in `.github/workflows/linkedin-news.yml` is for **the standalone static-site migration** with this package at repository root. It publishes its own updated artifact directly so a commit made with `GITHUB_TOKEN` does not need to trigger another workflow. Preserve/disable conflicting old al-folio deployment jobs during migration. It does not apply unchanged to the old Jekyll source tree.

The checked-out repository contains no private proposal/CV sources. The workflow stages only this public site. GitHub Pages must be configured to use GitHub Actions. Token and API access setup requires the account owner; this package does not create a paid third-party service or request new LinkedIn permissions.

## Run locally

With approved credentials in the environment, run `python scripts/sync_linkedin.py`. It retrieves all pages (up to a safety cap), validates author, PUBLIC visibility, PUBLISHED state and MAIN_FEED distribution, ignores unpublished/targeted posts, reconciles edits and deletions, and regenerates `news.html` and the home page's latest-news list. It never posts to LinkedIn.

Imported post text remains in its original language. DE/EN controls switch surrounding navigation and editorial translations; they do not silently machine-translate your LinkedIn posts.

If approved access is unavailable, a separately chosen authorized feed service is an alternative, but would require an account/provider decision. The package does not pretend that a LinkedIn profile link or a single embedded post automatically discovers future posts.
