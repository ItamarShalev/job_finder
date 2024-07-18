import { setupWorker } from 'msw';
import { handlers } from './handlers';

// זה יגדיר את ה-Mock Service Worker
export const worker = setupWorker(...handlers);
