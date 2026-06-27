import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(__dirname, '..');

const PORT = 7778;
const BASE_URL = `http://localhost:${PORT}`;

function waitForServer(url, timeout = 30000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const check = async () => {
      if (Date.now() - start > timeout) {
        reject(new Error('Server did not start within timeout'));
        return;
      }
      try {
        const response = await fetch(url);
        if (response.ok) resolve();
        else setTimeout(check, 1000);
      } catch {
        setTimeout(check, 1000);
      }
    };
    check();
  });
}

async function main() {
  console.log('Starting dev server...');
  const server = spawn(
    'uv',
    ['run', 'fastapi', 'dev', 'server.py', '--port', String(PORT)],
    { cwd: projectDir, stdio: 'pipe', env: { ...process.env } }
  );

  server.stderr.on('data', (d) => process.stderr.write(d));

  try {
    await waitForServer(BASE_URL);

    console.log('Launching browser...');
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    const page = await browser.newPage();

    await page.goto(`${BASE_URL}/resume`, { waitUntil: 'networkidle0' });

    // Remove site chrome: avatar, nav, header — keep only resume content
    await page.evaluate(() => {
      // Remove the header row entirely
      const header = document.querySelector('div.flex.justify-between');
      if (header) header.remove();

      // Add name as document title for the standalone resume
      const content = document.querySelector('.max-w-2xl');
      if (content) {
        content.classList.remove('max-w-2xl');
        content.style.maxWidth = '100%';

        const h1 = document.createElement('h1');
        h1.textContent = 'Lachlan Miller';
        h1.style.fontSize = '1.875rem';
        h1.style.fontWeight = '700';
        h1.style.marginBottom = '0.5rem';
        content.insertBefore(h1, content.firstChild);

        const tagline = document.createElement('p');
        tagline.textContent =
          'Engineering manager and software engineer with 10+ years of experience in healthcare technology and bioinformatics. Passionate about open source and building high-performing engineering teams.';
        tagline.style.fontSize = '0.95rem';
        tagline.style.color = '#4b5563';
        tagline.style.marginBottom = '1.5rem';
        tagline.style.lineHeight = '1.5';
        h1.insertAdjacentElement('afterend', tagline);
      }

      // Change details summary text for PDF
      const detailsSummary = document.querySelector('details summary');
      if (detailsSummary) {
        detailsSummary.textContent = 'Additional roles available upon request';
      }

      // Remove the body padding constraint for print
      document.body.classList.remove('justify-center');
      document.body.style.padding = '0';
    });

    // Add print-friendly CSS
    await page.addStyleTag({
      content: `
        @media print {
          body { padding: 0 !important; margin: 0 !important; }
          .p-6 { padding: 0 !important; }
          .md\\:mx-32 { margin-left: 0 !important; margin-right: 0 !important; }
          a { color: inherit !important; }
        }
      `,
    });

    const outputPath = path.join(projectDir, 'static', 'resume.pdf');
    await page.pdf({
      path: outputPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' },
    });

    console.log(`PDF generated: ${outputPath}`);
    await browser.close();
  } finally {
    server.kill();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
