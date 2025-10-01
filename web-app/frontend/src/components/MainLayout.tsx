import { Layout, Menu } from 'antd'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  DashboardOutlined,
  BankOutlined,
  UserOutlined,
  LogoutOutlined,
} from '@ant-design/icons'
import { useAuthStore } from '../stores/authStore'

const { Header, Sider, Content } = Layout

export default function MainLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()

  const menuItems = [
    { key: '/', icon: <DashboardOutlined />, label: 'แดชบอร์ด' },
    { key: '/bank-accounts', icon: <BankOutlined />, label: 'บัญชีธนาคาร' },
    { key: '/suspects', icon: <UserOutlined />, label: 'หมายเรียกผู้ต้องหา' },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={250} theme="dark">
        <div style={{ padding: '20px', color: 'white', textAlign: 'center', fontSize: '18px', fontWeight: 'bold' }}>
          ระบบจัดการคดีอาญา
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontSize: '16px' }}>สวัสดี, {user?.full_name || user?.username}</div>
          <div style={{ cursor: 'pointer' }} onClick={handleLogout}>
            <LogoutOutlined /> ออกจากระบบ
          </div>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}