<template>
  <div v-if="user" class="user-info-container">
    <!-- User Display Component -->
    <div class="user-card">
      <div class="user-avatar">
        <span class="avatar-initial">{{ userInitial }}</span>
      </div>
      
      <div class="user-details">
        <h3 class="user-name">{{ user.username }}</h3>
        <p class="user-email">{{ user.email }}</p>
        <div class="user-role">
          <span class="role-badge" :class="`role-${user.role.toLowerCase()}`">
            {{ formatRole(user.role) }}
          </span>
        </div>
      </div>

      <div class="user-actions">
        <button @click="copyUserInfo" class="action-btn info-btn" title="Copy user info">
          📋
        </button>
        <button @click="logout" class="action-btn logout-btn" title="Logout">
          🚪
        </button>
      </div>
    </div>

    <!-- User Stats (if admin) -->
    <div v-if="isAdminUser" class="user-stats">
      <div class="stat-item">
        <span class="stat-label">Account Status:</span>
        <span class="stat-value">{{ user.is_active ? 'Active' : 'Inactive' }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Created:</span>
        <span class="stat-value">{{ formatDate(user.created_at) }}</span>
      </div>
    </div>
  </div>
  <div v-else class="user-info-container empty-state">
    <p>Not authenticated</p>
  </div>
</template>

<script>
import { getStoredUser, isAdmin, authService } from '@/api/service'
import router from '@/router'

export default {
  name: 'UserInfo',
  
  data() {
    return {
      user: null,
    }
  },

  computed: {
    userInitial() {
      if (!this.user) return '?'
      return this.user.username?.[0]?.toUpperCase() || '?'
    },

    isAdminUser() {
      return this.user && isAdmin()
    }
  },

  methods: {
    loadUser() {
      this.user = getStoredUser()
    },

    formatRole(role) {
      const roleMap = {
        'admin': '👤 Admin',
        'ADMIN': '👤 Admin',
        'editor': '✏️ Editor',
        'EDITOR': '✏️ Editor',
        'user': '👥 User',
        'USER': '👥 User'
      }
      return roleMap[role] || role
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },

    copyUserInfo() {
      const info = `User: ${this.user.username}\nEmail: ${this.user.email}\nRole: ${this.user.role}`
      navigator.clipboard.writeText(info)
      alert('User info copied to clipboard!')
    },

    async logout() {
      if (confirm('Are you sure you want to logout?')) {
        try {
          await authService.logout()
          router.push('/login')
        } catch (error) {
          console.error('Logout error:', error)
          router.push('/login')
        }
      }
    }
  },

  mounted() {
    this.loadUser()
  }
}
</script>

<style scoped>
.user-info-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.user-info-container.empty-state {
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  color: #666;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: bold;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.user-details {
  flex: 1;
}

.user-name {
  margin: 0 0 0.25rem 0;
  font-size: 18px;
  font-weight: 600;
}

.user-email {
  margin: 0 0 0.5rem 0;
  font-size: 13px;
  opacity: 0.9;
}

.user-role {
  display: flex;
  gap: 0.5rem;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.role-admin {
  background: #ff6b6b;
  color: white;
}

.role-editor {
  background: #4ecdc4;
  color: white;
}

.role-user {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.logout-btn:hover {
  background: #ff6b6b;
}

.info-btn:hover {
  background: rgba(255, 255, 255, 0.4);
}

.user-stats {
  display: grid;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.stat-label {
  opacity: 0.9;
}

.stat-value {
  font-weight: 600;
}
</style>
