import { Layout, Menu, Button, Space } from 'antd'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import {
  DashboardOutlined,
  BankOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  SunOutlined,
  MoonOutlined,
  SettingOutlined,
  ApartmentOutlined,
  DatabaseOutlined,
} from '@ant-design/icons'
import { useAuthStore } from '../stores/authStore'
import { useTheme } from '../contexts/ThemeContext'

const { Header, Sider, Content } = Layout

export default function MainLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const { toggleTheme, isDark } = useTheme()
  const [collapsed, setCollapsed] = useState(() => {
    const saved = localStorage.getItem('sidebar-collapsed')
    return saved ? JSON.parse(saved) : false
  })

  const menuItems = [
    {
      key: 'criminal-cases',
      icon: <DashboardOutlined />,
      label: 'คดีอาญาในความรับผิดชอบ',
      children: [
        { key: '/', icon: <DashboardOutlined />, label: 'ภาพรวมคดี' },
        { key: '/bank-accounts', icon: <BankOutlined />, label: 'บัญชีธนาคาร' },
        { key: '/suspects', icon: <UserOutlined />, label: 'หมายเรียกผู้ต้องหา' }
      ]
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: 'โปรไฟล์ส่วนตัว'
    },
    ...(user?.role?.role_name === 'admin' ? [
      {
        key: 'admin',
        icon: <SettingOutlined />,
        label: 'ระบบผู้ดูแล',
        children: [
          { key: '/admin/users', icon: <UserOutlined />, label: 'จัดการผู้ใช้' },
          { key: '/admin/organizations', icon: <ApartmentOutlined />, label: 'จัดการหน่วยงาน' },
          { key: '/admin/master-data', icon: <DatabaseOutlined />, label: 'จัดการฐานข้อมูล' }
        ]
      }
    ] : [])
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const toggleCollapsed = () => {
    const newCollapsed = !collapsed
    setCollapsed(newCollapsed)
    localStorage.setItem('sidebar-collapsed', JSON.stringify(newCollapsed))
  }

  // Auto-collapse on mobile screens
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setCollapsed(true)
        localStorage.setItem('sidebar-collapsed', 'true')
      }
    }

    handleResize() // Check on mount
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        width={250} 
        collapsedWidth={80}
        collapsed={collapsed}
        theme="dark"
        trigger={null}
        collapsible
        breakpoint="md"
        onBreakpoint={(broken) => {
          if (broken) {
            setCollapsed(true)
            localStorage.setItem('sidebar-collapsed', 'true')
          }
        }}
      >
        <div style={{ 
          padding: '20px', 
          color: 'white', 
          textAlign: 'center', 
          fontSize: collapsed ? '14px' : '18px', 
          fontWeight: 'bold',
          whiteSpace: 'nowrap',
          overflow: 'hidden'
        }}>
          {collapsed ? 'ระบบคดี' : 'ระบบจัดการคดีอาญา'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          inlineCollapsed={collapsed}
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={toggleCollapsed}
              style={{ fontSize: '16px', width: 40, height: 40 }}
              title={collapsed ? 'ขยายเมนู' : 'ย่อเมนู'}
            />
            <div style={{ fontSize: '16px' }}>สวัสดี, {user?.full_name || user?.username}</div>
          </div>
          <Space>
            <Button
              type="text"
              icon={isDark ? <SunOutlined /> : <MoonOutlined />}
              onClick={toggleTheme}
              style={{ fontSize: '16px', width: 40, height: 40 }}
              title={isDark ? 'โหมดสว่าง' : 'โหมดมืด'}
            />
            <div style={{ cursor: 'pointer' }} onClick={handleLogout}>
              <LogoutOutlined /> ออกจากระบบ
            </div>
          </Space>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}