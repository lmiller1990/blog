import { parallel } from 'gulp'
import { execa } from "execa";


function tailwind() {
  return execa({ stdout: ["pipe", "inherit"] })`npx tailwindcss -i templates/index.css -o ./static/output.css --watch`;
}

function fastapi() {
  return execa({ stdout: ["pipe", "inherit"] })`fastapi dev server.py`;
}

const dev = parallel(fastapi, tailwind);

export { dev }
