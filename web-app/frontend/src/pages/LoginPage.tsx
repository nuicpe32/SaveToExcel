import { useState } from 'react'
import { Card, Form, Input, Button, message, Space } from 'antd'
import { UserOutlined, LockOutlined, SunOutlined, MoonOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { useTheme } from '../contexts/ThemeContext'
import api from '../services/api'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()
  const { isDark, toggleTheme } = useTheme()
  const [loading, setLoading] = useState(false)

  const onFinish = async (values: any) => {
    setLoading(true)
    try {
      const body = new URLSearchParams()
      body.set('username', values.username)
      body.set('password', values.password)

      const { data: tokenData } = await api.post('/auth/login', body, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })

      const { data: userData } = await api.get('/auth/me', {
        headers: { Authorization: `Bearer ${tokenData.access_token}` },
      })

      setAuth(tokenData.access_token, userData)
      message.success('เข้าสู่ระบบสำเร็จ')
      navigate('/')
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'เข้าสู่ระบบไม่สำเร็จ')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
      <div style={{ position: 'absolute', top: '20px', right: '20px' }}>
        <Button
          type="text"
          icon={isDark ? <SunOutlined /> : <MoonOutlined />}
          onClick={toggleTheme}
          style={{ fontSize: '18px', width: 48, height: 48 }}
          title={isDark ? 'โหมดสว่าง' : 'โหมดมืด'}
        />
      </div>
      <Card 
        className="login-card"
        title="เข้าสู่ระบบจัดการคดีอาญา" 
        style={{ width: 400 }}
        extra={
          <Space>
            <Button
              type="text"
              icon={isDark ? <SunOutlined /> : <MoonOutlined />}
              onClick={toggleTheme}
              size="small"
              title={isDark ? 'โหมดสว่าง' : 'โหมดมืด'}
            />
          </Space>
        }
      >
        <Form onFinish={onFinish} layout="vertical">
          <Form.Item name="username" rules={[{ required: true, message: 'กรุณากรอกชื่อผู้ใช้' }]}>
            <Input prefix={<UserOutlined />} placeholder="ชื่อผู้ใช้" size="large" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: 'กรุณากรอกรหัสผ่าน' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="รหัสผ่าน" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large" loading={loading}>
              เข้าสู่ระบบ
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}