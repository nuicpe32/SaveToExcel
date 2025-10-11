import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from 'antd'
import { useAuthStore } from './stores/authStore'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import BankAccountsPage from './pages/BankAccountsPage'
import SuspectsPage from './pages/SuspectsPage'
import AddCriminalCasePage from './pages/AddCriminalCasePage'
import EditCriminalCasePage from './pages/EditCriminalCasePage'
import CriminalCaseDetailPage from './pages/CriminalCaseDetailPage'
import AdminUsersPage from './pages/AdminUsersPage'
import OrganizationManagementPage from './pages/OrganizationManagementPage'
import MainLayout from './components/MainLayout'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuthStore()

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { token, user } = useAuthStore()

  if (!token) {
    return <Navigate to="/login" replace />
  }

  if (!user?.role || user.role.role_name !== 'admin') {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

function App() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="bank-accounts" element={<BankAccountsPage />} />
          <Route path="suspects" element={<SuspectsPage />} />
          <Route path="add-criminal-case" element={<AddCriminalCasePage />} />
          <Route path="edit-criminal-case/:id" element={<EditCriminalCasePage />} />
          <Route path="cases/:id" element={<CriminalCaseDetailPage />} />
          <Route 
            path="admin/users" 
            element={
              <AdminRoute>
                <AdminUsersPage />
              </AdminRoute>
            } 
          />
          <Route 
            path="admin/organizations" 
            element={
              <AdminRoute>
                <OrganizationManagementPage />
              </AdminRoute>
            } 
          />
        </Route>
      </Routes>
    </Layout>
  )
}

export default App