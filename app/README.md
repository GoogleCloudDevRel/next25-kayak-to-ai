# google-advocacy-demo

This repo houses reusable Vue.js components and styles for the Google Advocacy demos

## Project Setup

Make sure you have NVM or a compatible version of Node.js installed.

```sh
nvm use
```

```sh
npm install
```

### Compile and Hot-Reload for Development + run Node.js WSS

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

### Run Node.js WSS 
```sh
npm run dev:server
```

## App Routes
  - `http://localhost:3000/!#/`: Tv 55"
  - `http://localhost:3000/!#/chromebook`: Chromebook

## queryParams
  - `?manual` to control of the navigation by clicking to go next
  - `?view` to start from a specific route

## Useful files
  - `app/src/utils/api.js` -> where mock API calls are placed
  - `app/src/store/index.js` -> the store definition
  - `app/src/views` -> main entrypoints for chromebook/tv routers
  - `app/src/routes` -> chromebook/tv screens
  - `app/server.js` -> WSS definition
