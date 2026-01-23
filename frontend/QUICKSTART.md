# 🚀 Quick Start Guide

## Setup Instructions

### Prerequisites
- Node.js 16+ and npm
- Backend running on `http://localhost:8000`
- Valid backend credentials

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

---

## 🔐 Authentication

### Demo Accounts

| Role   | Username | Password | Permissions                    |
|--------|----------|----------|--------------------------------|
| Admin  | admin    | password | All access + user management   |
| Editor | editor   | password | Create/edit articles & tests   |
| User   | user     | password | View only                      |

### Login Flow

1. **Navigate to Login Page**
   - Automatically redirected if not authenticated
   - URL: `http://localhost:5173/login`

2. **Enter Credentials**
   - Username/Email field
   - Password field

3. **Submit**
   - Automatic redirect to home page
   - User info displays in navbar

4. **Logout**
   - Click the logout button (🚪) in UserInfo component
   - Token cleared from storage
   - Redirected to login page

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── index.js           # Axios instance with interceptors
│   │   ├── service.js         # ALL API endpoints & utilities
│   │   └── module.js          # Module-specific API
│   ├── components/
│   │   ├── AppHeader.vue
│   │   ├── AppCard.vue
│   │   ├── UserInfo.vue       # NEW: User display component
│   │   └── ...
│   ├── router/
│   │   ├── index.js           # Updated with guards
│   │   └── guards.js          # NEW: Auth guards
│   ├── views/
│   │   ├── Login.vue          # Enhanced login form
│   │   ├── Main.vue           # Enhanced with role checks
│   │   ├── Article.vue
│   │   ├── Module.vue
│   │   └── Tests.vue
│   ├── App.vue                # Updated with navbar
│   └── main.js
├── IMPLEMENTATION.md          # Detailed documentation
└── package.json
```

---

## 💻 Common Tasks

### Use API Service in Component

```vue
<script>
import { articleService, isEditor } from '@/api/service'

export default {
  data() {
    return {
      articles: []
    }
  },

  computed: {
    canEdit() {
      return isEditor()
    }
  },

  async mounted() {
    try {
      const response = await articleService.getAll(10, 0)
      this.articles = response.data
    } catch (error) {
      console.error('Error:', error)
    }
  },

  methods: {
    async deleteArticle(id) {
      try {
        await articleService.delete(id)
        this.articles = this.articles.filter(a => a.id !== id)
      } catch (error) {
        alert('Error deleting article')
      }
    }
  }
}
</script>
```

### Check User Permissions

```javascript
import { isAdmin, isEditor, getUserRole } from '@/api/service'

// Check authentication status
if (!isAuthenticated()) {
  router.push('/login')
}

// Check admin access
if (isAdmin()) {
  // Show admin features
}

// Check editor access
if (isEditor()) {
  // Show editor features
}

// Get current role
const role = getUserRole() // Returns: 'admin', 'editor', or 'user'
```

### Protect a Route

```javascript
// In router/index.js
{
  path: '/admin-panel',
  component: AdminPanel,
  beforeEnter: requireAdmin  // Only admins can access
}
```

### Handle API Errors

```javascript
try {
  const response = await articleService.create({
    content: 'New article',
    test_pk: null
  })
  // Success
} catch (error) {
  if (error.response?.status === 401) {
    // Not authenticated
    router.push('/login')
  } else if (error.response?.status === 403) {
    // Not authorized
    alert('Permission denied')
  } else if (error.response?.status === 400) {
    // Validation error
    console.error(error.response.data.detail)
  } else {
    // Server error
    alert('Server error. Please try again.')
  }
}
```

---

## 🧪 Testing

### Test Authentication
1. Open DevTools → Application → Storage → Local Storage
2. Verify `token` and `user` are stored after login
3. Check token format (should be JWT with 3 parts)

### Test Authorization
1. Login as admin/editor/user
2. Try accessing protected routes
3. Verify redirects work correctly

### Test API Calls
1. Check Network tab in DevTools
2. Verify requests have `Authorization: Bearer {token}` header
3. Check response status codes

---

## 🐛 Debugging

### Enable Logging

```javascript
// In src/api/service.js or any component
console.log('Current user:', getStoredUser())
console.log('Is authenticated:', isAuthenticated())
console.log('Is admin:', isAdmin())
console.log('Token:', localStorage.getItem('token'))
```

### Check Token Validity

```javascript
import { decodeToken } from '@/api/service'

const token = localStorage.getItem('token')
const decoded = decodeToken(token)
console.log('Token expires:', new Date(decoded.exp * 1000))
```

### Network Issues

```bash
# Check if backend is running
curl http://localhost:8000/v1/health

# Check CORS
# Look for CORS errors in DevTools console
```

---

## 📦 Building for Production

```bash
# Build optimization
npm run build

# Preview production build locally
npm run preview

# Output files in dist/
```

---

## 🔄 Environment Configuration

Create `.env.local` for local overrides:

```
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

Or use `.env.production` for production:

```
VITE_API_BASE_URL=https://api.example.com
VITE_API_TIMEOUT=5000
```

---

## ⚠️ Common Issues & Solutions

### Issue: "Cannot read property 'user' of null"
**Solution:** User not logged in or localStorage cleared
```javascript
// Add null check
const user = getStoredUser()
if (!user) router.push('/login')
```

### Issue: API returns 401 Unauthorized
**Solution:** Token expired or invalid
```javascript
// Clear storage and re-login
localStorage.clear()
router.push('/login')
```

### Issue: CORS errors when calling API
**Solution:** Backend CORS not configured
```javascript
// Ensure backend has CORS enabled for http://localhost:5173
```

### Issue: Routes not protected
**Solution:** Guard not applied correctly
```javascript
// Verify guard is imported and used
import { requireAuth } from './guards'

{
  path: '/protected',
  component: Protected,
  beforeEnter: requireAuth  // ← Make sure this is here
}
```

---

## 📚 API Quick Reference

### Authentication
```javascript
await authService.login({ username, password })
await authService.register({ username, email, password })
await authService.logout()
```

### Articles
```javascript
await articleService.getAll(limit, offset)
await articleService.getById(id)
await articleService.create({ content, test_pk })
await articleService.update(id, { content, test_pk })
await articleService.delete(id)
```

### Tests
```javascript
await testService.getAll(limit, offset)
await testService.getById(id)
await testService.create({ title, questions })
await testService.update(id, data)
await testService.delete(id)
```

### Test Sessions
```javascript
await testSessionService.start(testId, questionsCount)
await testSessionService.submitAnswer(token, questionId, answer)
await testSessionService.finishSession(token)
await testSessionService.getResults(token)
```

### Modules
```javascript
await moduleService.getAll(limit, offset)
await moduleService.create({ title, items })
await moduleService.addItem(moduleId, { title, article_id })
```

### Users (Admin only)
```javascript
await userService.getAll(limit, offset)
await userService.changeRole(id, role)
await userService.delete(id)
```

---

## 🆘 Need Help?

1. Check [IMPLEMENTATION.md](./IMPLEMENTATION.md) for detailed docs
2. Review component examples in the codebase
3. Check DevTools Network tab for API responses
4. Verify backend is running and accessible

---

**Happy Coding! 🚀**
