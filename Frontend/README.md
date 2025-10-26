# Frontend (Vue 3 + Vite + Bootstrap)

Vue 3 SPA for the Vehicle Parking Management System.

## Prerequisites

- Node 18+ (or 20+)
- pnpm (or npm/yarn)

## Setup

```sh
pnpm install
```

## Run Dev Server

```sh
pnpm dev
```

Open http://localhost:5173.

## Build for Production

```sh
pnpm build
```

## Lint

```sh
pnpm lint
```

## Configuration

- API base URL is set to `http://localhost:5000` in `src/stores/auth.js` and axios usage; adjust if backend runs elsewhere.
- Bootstrap 5 is loaded via CDN in `index.html`.

## Auth Flow

- On successful login, access/refresh tokens and user info are stored in `localStorage`.
- Navigation is role-aware (admin/user) via Vue Router guards.

## Structure

- `src/components/admin/*` — admin modals and UI
- `src/components/user/*` — booking, release, history
- `src/components/auth/*` — login/register views
- `src/views/*` — pages (admin and user dashboards)
- `src/stores/*` — Pinia stores (auth)
- `src/router/*` — routes and guards

For full API details, see `../Backend/api_routes.yaml`.
