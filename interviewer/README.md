# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

## Running with Docker

This project includes a Docker setup that serves the built app via Nginx inside the container.

- Build the image: `docker build -t interviewer .`
- Run with Docker Compose: `docker compose up --build`

By default, docker-compose maps the container's port 80 to host port 8080 to avoid conflicts with services already using port 80 on your machine.

- Access the app at: http://localhost:8080

To change the host port, edit docker-compose.yml and modify the ports section (left side is the host port):

```
ports:
  - "3000:80"  # exposes on http://localhost:3000
```

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is currently not compatible with SWC. See [this issue](https://github.com/vitejs/vite-plugin-react/issues/428) for tracking the progress.

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
