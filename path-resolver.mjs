import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * The project root: the folder that holds cv.md, config/, templates/ and
 * output/. cv-studio is a single flat workspace, so this is always the
 * directory this file lives in.
 *
 * @returns {string} Absolute path to the project root
 */
export function getCareerOpsRoot() {
  return __dirname;
}
