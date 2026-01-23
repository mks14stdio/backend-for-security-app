# Frontend Implementation Guide

## 📋 Overview

This document describes the complete implementation of axios HTTP logic, authentication guards, role-based access control (RBAC), and user information components.

## 🏗️ Architecture

### 1. **API Service Layer** (`src/api/service.js`)

Comprehensive centralized service with methods for all backend endpoints:

#### Auth Service
```javascript
authService.login(credentials)          // POST /v1/auth/login
authService.register(userData)          // POST /v1/auth/register
authService.logout()                    // Clears local storage
authService.refreshToken(refreshToken)  // POST /v1/auth/refresh
authService.getCurrentUser()            // GET /v1/auth/me
```

#### Article Service
```javascript
articleService.getAll(limit, offset)    // GET /v1/article/
articleService.getById(id)              // GET /v1/article/{id}
articleService.create(data)             // POST /v1/article/
articleService.update(id, data)         // PATCH /v1/article/{id}
articleService.delete(id)               // DELETE /v1/article/{id}
```

#### Test Service
```javascript
testService.getAll(limit, offset)       // GET /v1/test/
testService.getById(id)                 // GET /v1/test/{id}
testService.create(data)                // POST /v1/test/
testService.update(id, data)            // PATCH /v1/test/{id}
testService.delete(id)                  // DELETE /v1/test/{id}
```

#### Test Session Service
```javascript
testSessionService.start(testId, count)           // POST /v1/test-session/{testId}/start
testSessionService.getSession(token)              // GET /v1/test-session/current
testSessionService.submitAnswer(token, q, answer) // POST /v1/test-session/answer
testSessionService.finishSession(token)           // POST /v1/test-session/finish
testSessionService.getResults(token)              // GET /v1/test-session/results
```

#### Module Service
```javascript
moduleService.getAll(limit, offset)             // GET /v1/module/
moduleService.getById(id)                       // GET /v1/module/{id}
moduleService.create(data)                      // POST /v1/module/
moduleService.update(id, data)                  // PATCH /v1/module/{id}
moduleService.delete(id)                        // DELETE /v1/module/{id}
moduleService.getItems(moduleId)                // GET /v1/module/{moduleId}/items
moduleService.addItem(moduleId, itemData)       // POST /v1/module/{moduleId}/items
moduleService.updateItem(moduleId, itemId, data) // PATCH /v1/module/{moduleId}/items/{itemId}
moduleService.deleteItem(moduleId, itemId)      // DELETE /v1/module/{moduleId}/items/{itemId}
```

#### Question Service
```javascript
questionService.getAll(testId, limit, offset)          // GET /v1/test/{testId}/questions
questionService.getById(testId, questionId)            // GET /v1/test/{testId}/questions/{questionId}
questionService.create(testId, data)                   // POST /v1/test/{testId}/questions
questionService.update(testId, questionId, data)       // PATCH /v1/test/{testId}/questions/{questionId}
questionService.delete(testId, questionId)             // DELETE /v1/test/{testId}/questions/{questionId}
```

#### User Service (Admin only)
```javascript
userService.getAll(limit, offset)              // GET /v1/user/
userService.getById(id)                        // GET /v1/user/{id}
userService.create(data)                       // POST /v1/user/
userService.update(id, data)                   // PATCH /v1/user/{id}
userService.delete(id)                         // DELETE /v1/user/{id}
userService.changeRole(id, role)               // PATCH /v1/user/{id}/role
```

#### Utility Functions
```javascript
// JWT token handling
decodeToken(token)          // Decode JWT (without verification)
getStoredUser()            // Get user from localStorage
storeUser(user)            // Save user to localStorage
isAuthenticated()          // Check if user has token
isAdmin()                  // Check if user has admin role
isEditor()                 // Check if user has editor role
getUserRole()              // Get current user role
```

### 2. **Authentication Guards** (`src/router/guards.js`)

Role-based route guards:

```javascript
requireAuth      // Check if user is authenticated → redirect to /login if not
requireAdmin     // Check if user has admin role → redirect to /login if not
requireEditor    // Check if user has editor role (or admin) → redirect if not
requireUser      // Check if user is regular user (not admin)
requireGuest     // Only allow unauthenticated users → redirect to / if logged in
```

### 3. **Router Configuration** (`src/router/index.js`)

Routes with guard integration:

```javascript
/login     → Login (requireGuest)
/          → Main (requireAuth)
/article   → Article Editor (requireEditor)
/module    → Module Editor (requireEditor)
/tests     → Test Editor (requireEditor)
```

Global navigation guard ensures token validation on all route changes.

### 4. **User Info Component** (`src/components/UserInfo.vue`)

Displays authenticated user information with:
- User avatar with initial
- Username and email
- Role badge (color-coded)
- Copy user info button
- Logout button
- Account stats (for admins)

### 5. **Updated App.vue**

Main application component with:
- Sticky navigation bar (when authenticated)
- User info display
- Router outlet for views
- Global styling with CSS variables
- Responsive design

### 6. **Enhanced Login View** (`src/views/Login.vue`)

Modern login interface with:
- Input validation
- Error/success messages
- Loading state
- Demo credentials display
- Smooth animations

### 7. **Enhanced Main View** (`src/views/Main.vue`)

Home page with:
- Role-based card visibility
- Quick stats display
- User role information
- Access control indicators

## 🔐 Security Flow

### Authentication Flow
```
1. User enters credentials → Login.vue
2. POST /v1/auth/login
3. Receive access_token + user object
4. Store token in localStorage
5. Store user object in localStorage
6. Redirect to /
```

### Authorization Flow
```
1. User navigates to protected route
2. Router guard checks beforeEnter
3. Guard checks isAuthenticated() → localStorage.getItem('token')
4. If authenticated, check role requirements
5. If authorized, proceed to route
6. If not authorized, redirect to /login
```

### API Request Flow
```
1. Component calls service method (e.g., articleService.getById(1))
2. Service makes HTTP request via axios instance
3. Request interceptor adds Authorization header with JWT token
4. Request sent to backend
5. Response interceptor checks for 401 status
6. If 401, clear token and redirect to /login
7. Component receives data or error
```

## 📝 Usage Examples

### Login
```javascript
import { authService, storeUser } from '@/api/service'
import router from '@/router'

try {
  const response = await authService.login({ 
    username: 'admin', 
    password: 'password' 
  })
  const { access_token, user } = response.data
  localStorage.setItem('token', access_token)
  storeUser(user)
  router.push('/')
} catch (error) {
  console.error('Login failed:', error)
}
```

### Fetch Articles (protected route, editor only)
```javascript
import { articleService } from '@/api/service'

export default {
  async mounted() {
    try {
      const response = await articleService.getAll(10, 0)
      this.articles = response.data
    } catch (error) {
      console.error('Failed to fetch articles:', error)
    }
  }
}
```

### Create Article
```javascript
import { articleService } from '@/api/service'

async createArticle() {
  try {
    const response = await articleService.create({
      content: 'Article content here',
      test_pk: null
    })
    this.articles.push(response.data)
  } catch (error) {
    console.error('Failed to create article:', error)
  }
}
```

### Check User Permissions
```javascript
import { isAdmin, isEditor, getUserRole } from '@/api/service'

export default {
  computed: {
    canEdit() {
      return isEditor()
    },
    
    canManageUsers() {
      return isAdmin()
    }
  }
}
```

## 🌐 HTTP Interceptors

### Request Interceptor
- Automatically adds `Authorization: Bearer {token}` header
- Only adds if token exists in localStorage

### Response Interceptor
- Catches 401 Unauthorized responses
- Clears token from storage
- Redirects to /login

## 🎨 Styling Features

- **CSS Variables** for consistent theming
- **Gradient backgrounds** for modern look
- **Smooth animations** for UX
- **Responsive design** for mobile devices
- **Dark/Light contrast** for accessibility

## 🚀 Getting Started

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Run Development Server
```bash
npm run dev
```

### 3. Build for Production
```bash
npm run build
```

### 4. Test Login
- Go to http://localhost:5173/login
- Use demo credentials: `admin / password` or `editor / password`
- Verify redirect to home page
- Check user info in navbar

## 📱 Component Hierarchy

```
App.vue
├── AppNavbar
│   └── UserInfo.vue
├── router-view
│   ├── Login.vue (requireGuest)
│   ├── Main.vue (requireAuth)
│   │   └── AppCard.vue
│   ├── Article.vue (requireEditor)
│   ├── Module.vue (requireEditor)
│   ├── Tests.vue (requireEditor)
│   └── Users.vue (requireAdmin)
```

## 🔍 Troubleshooting

### Token not persisting
- Check browser's localStorage is enabled
- Verify token is being stored: `localStorage.getItem('token')`

### Routes not protecting
- Verify guards are correctly imported in router/index.js
- Check localStorage for token: `localStorage.getItem('token')`

### User info not showing
- Ensure `authService.getCurrentUser()` is being called in App.vue
- Check user object structure matches expected format

### API 401 errors
- Verify token is valid and not expired
- Check token is sent in Authorization header
- Clear localStorage and re-login if needed

## 📚 Environment Variables

Create `.env` file in frontend root:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

Update `src/api/index.js` to use environment variables:
```javascript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/',
  timeout: import.meta.env.VITE_API_TIMEOUT || 10000
})
```

---

**Last Updated:** December 2024
**Status:** Production Ready
