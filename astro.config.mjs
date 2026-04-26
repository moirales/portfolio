import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite'; // <--- Esta es la línea que daba error

export default defineConfig({
  vite: {
    plugins: [tailwind()],
  },
});