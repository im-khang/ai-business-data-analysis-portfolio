# Repository roles

This repo split prevents showcase pages from overlapping with analysis proof code.

## Showcase repo: `im-khang/portfolio-site`

Purpose: recruiter-facing portfolio website.

Owns:
- `https://im-khang.com` production site
- Open Design HTML artifacts
- homepage, case landing pages, operating-system narrative
- Vercel deployment config and preview flow

Does not own:
- raw analysis code
- notebooks
- generated proof artifacts
- local Kaggle/raw-data workflows

## Proof repo: `im-khang/data-analytics-stuff`

Purpose: analytics proof lab.

Owns:
- SQL/Python/notebooks and tests
- case-study source documentation
- aggregate JSON exported from pipelines
- reproducibility notes, assumptions, caveats, and evidence trail
- source links used by showcase site

Does not own:
- primary recruiter-facing website
- Open Design showcase publication
- im-khang.com production deployment

## Publishing rule

Open Design patches go to `portfolio-site`.
Analysis artifacts and proof updates go to `data-analytics-stuff`.

## Naming

- `portfolio-site`: short, explicit website repo.
- `data-analytics-stuff`: broad proof workspace for analytics code, cases, and artifacts.
