---
metadata:
  name: "react-app-setup"
  version: "1.0.0"
  description: "Set up a modern React application with TypeScript, Tailwind CSS, and best practices"
  category: "web-development"
  tags: ["react", "typescript", "tailwind", "frontend", "vite"]
  author: "skillhub"
  created: "2024-01-15"
  updated: "2024-01-15"

requirements:
  os: ["linux", "macos", "windows"]
  node: ">=18.0.0"
  packages:
    - npm>=9.0.0
  hardware:
    - ram: ">=4GB"
    - disk_space: ">=2GB"

estimated_time: "15-20 minutes"
difficulty: "beginner"
---

# React App Setup

## Overview
This skill sets up a modern React application with TypeScript, Tailwind CSS, ESLint, Prettier, and React Router. Includes project structure, best practices, and a sample component to get you started quickly.

## Task Description
Complete React application setup:
1. Initialize Vite project with React and TypeScript
2. Install and configure Tailwind CSS
3. Set up ESLint and Prettier for code quality
4. Install React Router for navigation
5. Create project folder structure
6. Build sample components and pages
7. Configure development and build scripts

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Basic understanding of React
- Code editor (VS Code recommended)

## Steps

### 1. Initialize Vite Project
```bash
# Create new Vite project with React and TypeScript
npm create vite@latest my-react-app -- --template react-ts

cd my-react-app

# Install dependencies
npm install
```

### 2. Install Tailwind CSS
```bash
# Install Tailwind CSS and its dependencies
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind config
npx tailwindcss init -p
```

### 3. Configure Tailwind
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles */
body {
  @apply bg-gray-50 text-gray-900;
}
```

### 4. Install Additional Dependencies
```bash
# React Router for navigation
npm install react-router-dom

# Useful utilities
npm install clsx

# Development tools
npm install -D @types/node
npm install -D eslint-plugin-react-hooks
```

### 5. Configure ESLint and Prettier
```json
// .eslintrc.cjs
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
```

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "arrowParens": "avoid"
}
```

### 6. Create Project Structure
```bash
# Create folder structure
mkdir -p src/{components,pages,hooks,utils,types,layouts}
mkdir -p src/components/{common,features}
```

### 7. Create Layout Component
```typescript
// src/layouts/MainLayout.tsx
import { Outlet, Link } from 'react-router-dom';

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex-shrink-0">
              <Link to="/" className="text-2xl font-bold text-blue-600">
                MyApp
              </Link>
            </div>
            <div className="flex space-x-4">
              <Link
                to="/"
                className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Home
              </Link>
              <Link
                to="/about"
                className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                About
              </Link>
            </div>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 MyApp. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
```

### 8. Create Pages
```typescript
// src/pages/HomePage.tsx
export default function HomePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to MyApp
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          A modern React application with TypeScript and Tailwind CSS
        </p>
        <div className="flex justify-center space-x-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
            Get Started
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-6 rounded-lg transition-colors">
            Learn More
          </button>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
        <FeatureCard
          title="⚡ Fast"
          description="Built with Vite for lightning-fast development and optimized builds"
        />
        <FeatureCard
          title="🎨 Beautiful"
          description="Styled with Tailwind CSS for modern, responsive designs"
        />
        <FeatureCard
          title="🔒 Type-Safe"
          description="TypeScript ensures your code is reliable and maintainable"
        />
      </div>
    </div>
  );
}

// Feature Card Component
function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
```

```typescript
// src/pages/AboutPage.tsx
export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-6">About MyApp</h1>
      <div className="prose prose-lg">
        <p className="text-gray-600 mb-4">
          This is a modern React application built with the latest technologies
          and best practices.
        </p>
        <h2 className="text-2xl font-semibold mt-8 mb-4">Technology Stack</h2>
        <ul className="space-y-2">
          <li>⚛️ React 18 with TypeScript</li>
          <li>⚡ Vite for fast development</li>
          <li>🎨 Tailwind CSS for styling</li>
          <li>🚦 React Router for navigation</li>
          <li>✅ ESLint and Prettier for code quality</li>
        </ul>
      </div>
    </div>
  );
}
```

### 9. Set Up Router
```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<HomePage />} />
          <Route path="about" element={<AboutPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

### 10. Update Package Scripts
```json
// package.json (update scripts section)
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "type-check": "tsc --noEmit"
  }
}
```

### 11. Run the Application
```bash
# Start development server
npm run dev

# In another terminal, format code
npm run format

# Check types
npm run type-check

# Build for production
npm run build
```

## Expected Output
- Fully configured React application running on http://localhost:5173
- Two pages (Home and About) with navigation
- Tailwind CSS styling applied
- TypeScript type checking enabled
- ESLint and Prettier configured
- Production-ready build in `dist/` folder

## Troubleshooting

### Port Already in Use
```bash
# Vite will automatically try another port, or specify manually
npm run dev -- --port 3000
```

### TypeScript Errors
```bash
# Check TypeScript configuration
npm run type-check

# If errors persist, check tsconfig.json
cat tsconfig.json
```

### Tailwind Styles Not Applied
```bash
# Ensure Tailwind is imported in src/index.css
# Restart dev server
npm run dev
```

### Module Not Found Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Success Criteria
- [x] Development server runs without errors
- [x] Application loads in browser at localhost:5173
- [x] Navigation between Home and About pages works
- [x] Tailwind CSS styles are applied correctly
- [x] TypeScript compilation succeeds
- [x] ESLint shows no errors
- [x] Production build completes successfully

## Next Steps
- Add state management (Redux, Zustand, or Context API)
- Integrate API calls with React Query or SWR
- Add unit tests with Vitest and React Testing Library
- Set up CI/CD pipeline
- Add authentication and protected routes
- Implement dark mode toggle
- Add error boundaries and loading states

## Related Skills
- `setup-testing-react`
- `add-authentication`
- `deploy-vercel`
- `setup-state-management`

## References
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Router Documentation](https://reactrouter.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
