import React, { useState, useEffect, useCallback } from 'react'
import { 
  Table, 
  Button, 
  Space, 
  message, 
  Modal, 
  Tag, 
  Popconfirm, 
  Typography,
  Card,
  Row,
  Col,
  Statistic,
  Tabs
} from 'antd'
import { 
  CheckOutlined, 
  CloseOutlined, 
  UnlockOutlined, 
  UserOutlined,
  LockOutlined,
  EyeOutlined
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'
import dayjs from 'dayjs'

const { Title } = Typography

interface User {
  id: number
  username: string
  email: string
  full_name: string
  position?: string
  phone_number?: string
  line_id?: string
  is_active: boolean
  is_approved: boolean
  failed_login_attempts: number
  locked_until?: string
  created_at: string
  approved_at?: string
  rank?: {
    id: number
    rank_short: string
    rank_full: string
  }
  role?: {
    id: number
    role_name: string
    role_display: string
  }
  role_mappings?: Array<{
    id: number
    role_name: string
    role_display: string
    role_description?: string
  }>
}

interface UserStats {
  total: number
  pending: number
  approved: number
  locked: number
  inactive: number
}

export default function AdminUsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [pendingUsers, setPendingUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState<UserStats>({
    total: 0,
    pending: 0,
    approved: 0,
    locked: 0,
    inactive: 0
  })

  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const [allUsersRes, pendingUsersRes] = await Promise.all([
        api.get('/admin/all-users'),
        api.get('/admin/pending-users')
      ])
      
      setUsers(allUsersRes.data)
      setPendingUsers(pendingUsersRes.data)
      
      // Calculate stats
      const allUsers = allUsersRes.data
      const stats = {
        total: allUsers.length,
        pending: allUsers.filter((u: User) => !u.is_approved).length,
        approved: allUsers.filter((u: User) => u.is_approved).length,
        locked: allUsers.filter((u: User) => u.locked_until && dayjs(u.locked_until).isAfter(dayjs())).length,
        inactive: allUsers.filter((u: User) => !u.is_active).length
      }
      setStats(stats)
    } catch (error) {
      message.error('ไม่สามารถดึงข้อมูลผู้ใช้ได้')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  const handleApproveUser = async (userId: number) => {
    try {
      await api.post(`/admin/approve-user/${userId}`)
      message.success('อนุมัติผู้ใช้เรียบร้อยแล้ว')
      fetchUsers()
    } catch (error) {
      message.error('ไม่สามารถอนุมัติผู้ใช้ได้')
    }
  }

  const handleRejectUser = async (userId: number) => {
    try {
      await api.post(`/admin/reject-user/${userId}`)
      message.success('ปฏิเสธการสมัครสมาชิกเรียบร้อยแล้ว')
      fetchUsers()
    } catch (error) {
      message.error('ไม่สามารถปฏิเสธผู้ใช้ได้')
    }
  }

  const handleUnlockUser = async (userId: number) => {
    try {
      await api.post(`/admin/unlock-user/${userId}`)
      message.success('ปลดล็อคผู้ใช้เรียบร้อยแล้ว')
      fetchUsers()
    } catch (error) {
      message.error('ไม่สามารถปลดล็อคผู้ใช้ได้')
    }
  }

  const handleActivateUser = async (userId: number) => {
    try {
      await api.post(`/admin/activate-user/${userId}`)
      message.success('เปิดใช้งานผู้ใช้เรียบร้อยแล้ว')
      fetchUsers()
    } catch (error) {
      message.error('ไม่สามารถเปิดใช้งานผู้ใช้ได้')
    }
  }

  const handleDeactivateUser = async (userId: number) => {
    try {
      await api.post(`/admin/deactivate-user/${userId}`)
      message.success('ปิดใช้งานผู้ใช้เรียบร้อยแล้ว')
      fetchUsers()
    } catch (error) {
      message.error('ไม่สามารถปิดใช้งานผู้ใช้ได้')
    }
  }

  const isUserLocked = (user: User) => {
    return user.locked_until && dayjs(user.locked_until).isAfter(dayjs())
  }

  const getStatusTag = (user: User) => {
    if (!user.is_approved) {
      return <Tag color="orange">รออนุมัติ</Tag>
    }
    if (isUserLocked(user)) {
      return <Tag color="red">ถูกล็อค</Tag>
    }
    if (!user.is_active) {
      return <Tag color="gray">ปิดใช้งาน</Tag>
    }
    return <Tag color="green">ใช้งานได้</Tag>
  }

  const pendingColumns: ColumnsType<User> = [
    {
      title: 'ชื่อผู้ใช้',
      dataIndex: 'username',
      key: 'username',
      render: (text, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{text}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>{record.email}</div>
        </div>
      )
    },
    {
      title: 'ข้อมูลส่วนตัว',
      key: 'personal_info',
      render: (_, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>
            {record.rank?.rank_short} {record.full_name}
          </div>
          {record.position && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              ตำแหน่ง: {record.position}
            </div>
          )}
          {record.phone_number && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              โทร: {record.phone_number}
            </div>
          )}
        </div>
      )
    },
    {
      title: 'สิทธิ์ที่ขอ',
      key: 'requested_roles',
      render: (_, record) => (
        <div>
          {record.role_mappings && record.role_mappings.length > 0 ? (
            <div>
              {record.role_mappings.map((role, index) => (
                <Tag key={role.id} color="blue" style={{ marginBottom: '2px' }}>
                  {role.role_display}
                </Tag>
              ))}
            </div>
          ) : (
            <Tag color="orange">{record.role?.role_display || 'ไม่ระบุ'}</Tag>
          )}
        </div>
      )
    },
    {
      title: 'วันที่สมัคร',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => dayjs(date).format('DD/MM/YYYY HH:mm')
    },
    {
      title: 'การดำเนินการ',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Popconfirm
            title="อนุมัติผู้ใช้นี้?"
            onConfirm={() => handleApproveUser(record.id)}
            okText="อนุมัติ"
            cancelText="ยกเลิก"
          >
            <Button type="primary" size="small" icon={<CheckOutlined />}>
              อนุมัติ
            </Button>
          </Popconfirm>
          <Popconfirm
            title="ปฏิเสธการสมัครสมาชิก?"
            onConfirm={() => handleRejectUser(record.id)}
            okText="ปฏิเสธ"
            cancelText="ยกเลิก"
            okType="danger"
          >
            <Button danger size="small" icon={<CloseOutlined />}>
              ปฏิเสธ
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  const allUsersColumns: ColumnsType<User> = [
    {
      title: 'ชื่อผู้ใช้',
      dataIndex: 'username',
      key: 'username',
      render: (text, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{text}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>{record.email}</div>
        </div>
      )
    },
    {
      title: 'ข้อมูลส่วนตัว',
      key: 'personal_info',
      render: (_, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>
            {record.rank?.rank_short} {record.full_name}
          </div>
          {record.position && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              ตำแหน่ง: {record.position}
            </div>
          )}
          {record.phone_number && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              โทร: {record.phone_number}
            </div>
          )}
        </div>
      )
    },
    {
      title: 'สิทธิ์ปัจจุบัน',
      key: 'current_role',
      render: (_, record) => (
        <div>
          <Tag color="green">{record.role?.role_display || 'ไม่ระบุ'}</Tag>
          {record.role_mappings && record.role_mappings.length > 1 && (
            <div style={{ marginTop: '4px' }}>
              <div style={{ fontSize: '12px', color: '#666' }}>สิทธิ์เพิ่มเติม:</div>
              {record.role_mappings
                .filter(role => role.id !== record.role?.id)
                .map((role) => (
                  <Tag key={role.id} color="blue" size="small" style={{ marginBottom: '2px' }}>
                    {role.role_display}
                  </Tag>
                ))}
            </div>
          )}
        </div>
      )
    },
    {
      title: 'สถานะ',
      key: 'status',
      render: (_, record) => getStatusTag(record)
    },
    {
      title: 'วันที่สมัคร',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => dayjs(date).format('DD/MM/YYYY HH:mm')
    },
    {
      title: 'การดำเนินการ',
      key: 'actions',
      render: (_, record) => (
        <Space>
          {isUserLocked(record) && (
            <Popconfirm
              title="ปลดล็อคผู้ใช้นี้?"
              onConfirm={() => handleUnlockUser(record.id)}
              okText="ปลดล็อค"
              cancelText="ยกเลิก"
            >
              <Button type="primary" size="small" icon={<UnlockOutlined />}>
                ปลดล็อค
              </Button>
            </Popconfirm>
          )}
          {record.is_active ? (
            <Popconfirm
              title="ปิดใช้งานผู้ใช้นี้?"
              onConfirm={() => handleDeactivateUser(record.id)}
              okText="ปิดใช้งาน"
              cancelText="ยกเลิก"
              okType="danger"
            >
              <Button danger size="small" icon={<LockOutlined />}>
                ปิดใช้งาน
              </Button>
            </Popconfirm>
          ) : (
            <Popconfirm
              title="เปิดใช้งานผู้ใช้นี้?"
              onConfirm={() => handleActivateUser(record.id)}
              okText="เปิดใช้งาน"
              cancelText="ยกเลิก"
            >
              <Button type="primary" size="small" icon={<UserOutlined />}>
                เปิดใช้งาน
              </Button>
            </Popconfirm>
          )}
        </Space>
      )
    }
  ]

  const tabItems = [
    {
      key: 'pending',
      label: `รออนุมัติ (${stats.pending})`,
      children: (
        <Table
          columns={pendingColumns}
          dataSource={pendingUsers}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      )
    },
    {
      key: 'all',
      label: `ผู้ใช้ทั้งหมด (${stats.total})`,
      children: (
        <Table
          columns={allUsersColumns}
          dataSource={users}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      )
    }
  ]

  return (
    <div style={{ padding: '20px' }}>
      <Title level={2}>จัดการผู้ใช้</Title>
      
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="ผู้ใช้ทั้งหมด"
              value={stats.total}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="รออนุมัติ"
              value={stats.pending}
              valueStyle={{ color: '#fa8c16' }}
              prefix={<EyeOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="อนุมัติแล้ว"
              value={stats.approved}
              valueStyle={{ color: '#52c41a' }}
              prefix={<CheckOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="ถูกล็อค"
              value={stats.locked}
              valueStyle={{ color: '#f5222d' }}
              prefix={<LockOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Users Table */}
      <Card>
        <Tabs items={tabItems} />
      </Card>
    </div>
  )
}
