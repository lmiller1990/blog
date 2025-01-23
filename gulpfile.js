import { parallel } from 'gulp'
import { execa } from "execa";


function tailwind() {
  return execa({ stdout: ["pipe", "inherit"] })`npx tailwindcss -i templates/index.css -o ./static/output.css --watch`;
}

async function fastapi() {
  await execa('poetry', ['run', 'fastapi', 'dev', 'server.py'], { stdio: 'inherit' });
}

const dev = parallel(fastapi, tailwind);

export { dev }
