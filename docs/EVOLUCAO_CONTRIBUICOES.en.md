# Contribution Progress

Dashboard calculated using the GitHub REST API. The count includes closed Pull Requests with a populated merged_at field; rejected or closed PRs without a merge are excluded.

**Updated:** 2026-11-08 04:23 UTC  
**Repository:** [luisfvmartins/clean-my-android](https://github.com/luisfvmartins/clean-my-android)

## Indicators

- **Merged Pull Requests:** 31
- **Distinct authors with merged PRs:** 1
- **Cataloged devices:** 2
- **Represented manufacturers:** 1

## Merged Pull Requests by year

| Merge year | Pull Requests |
|---:|---:|
| 2026 | 31 |

## Scope and limitations

- Distinct authors are counted by the GitHub login associated with the author of a merged PR. This does not represent verified individuals or current active members.
- A PR represents an integrated contribution but may contain multiple files or devices.
- Device and manufacturer counts come from data/device_catalog.json; PR activity comes from the GitHub API.
- The dashboard does not measure quality, useful lines, device testing, or script approval.
- Data reflects the repository at the time of the update.

## Updates

The contribution dashboard workflow generates both Portuguese and English pages from the same GitHub API response. It runs after updates to the main branch, daily, and can also be started manually from the Actions tab. It uses the GITHUB_TOKEN provided by GitHub Actions; no personal token is stored in the repository.

Also see [project statistics](ESTATISTICAS.en.md) and the [audit catalog](../reports/README.md).
