import {spawnSync} from 'node:child_process';
import process from 'node:process';

const executable = process.platform === 'win32' ? 'awesome-lint.cmd' : 'awesome-lint';
const result = spawnSync(executable, [], {
  cwd: new URL('..', import.meta.url),
  encoding: 'utf8',
  shell: false,
  stdio: 'inherit',
});

if (result.error) {
  console.error(`Unable to run local awesome-lint: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
