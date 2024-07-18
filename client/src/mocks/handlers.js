import { rest } from 'msw';

export const handlers = [
  // Mock להעלאת קובץ
  rest.post('http://localhost:8000/upload', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ message: 'File uploaded successfully' }));
  }),
  // Mock לטעינת מידע (אם נדרש)
  rest.get('http://localhost:8000/some-endpoint', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ data: 'Sample data from server' }));
  }),
];
