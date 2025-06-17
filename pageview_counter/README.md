# Pageview Counter

A lightweight serverless service to track and return pageview counts by site.

## Usage

**Endpoint:**

POST /.netlify/functions/visit?site=portfolio

**Query Parameters:**

- `site`: required string (`portfolio`, `blog`, etc.)

## Files

- `netlify/visit.js`: main Netlify function
- `data/visits.json`: JSON storage for counts

## Setup

1. Deploy to Netlify
2. Add `fetch()` call in frontend to the function URL