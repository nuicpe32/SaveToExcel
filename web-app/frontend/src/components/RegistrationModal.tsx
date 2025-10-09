import React, { useState, useEffect } from 'react'
import { Modal, Form, Input, Select, Checkbox, Button, message, Space, Row, Col } from 'antd'
import { UserOutlined, MailOutlined, PhoneOutlined, IdcardOutlined } from '@ant-design/icons'
import api from '../services/api'

interface PoliceRank {
  id: number
  rank_full: string
  rank_short: string
  rank_english: string
}

interface UserRole {
  id: number
  role_name: string
  role_display: string
  role_description?: string
}

interface RegistrationFormData {
  rank_id: number
  full_name: string
  position?: string
  email: string
  phone_number?: string
  line_id?: string
  role_ids: number[]
  username: string
  password: string
  confirmPassword: string
}

interface RegistrationModalProps {
  open: boolean
  onClose: () => void
  onSuccess: () => void
}

const RegistrationModal: React.FC<RegistrationModalProps> = ({ open, onClose, onSuccess }) => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [ranks, setRanks] = useState<PoliceRank[]>([])
  const [roles, setRoles] = useState<UserRole[]>([])
  const [selectedRoles, setSelectedRoles] = useState<number[]>([])

  // ดึงข้อมูลยศตำรวจและสิทธิ์
  useEffect(() => {
    if (open) {
      fetchMasterData()
    }
  }, [open])

  const fetchMasterData = async () => {
    try {
      const [ranksRes, rolesRes] = await Promise.all([
        api.get('/registration/ranks'),
        api.get('/registration/roles')
      ])
      setRanks(ranksRes.data)
      setRoles(rolesRes.data)
    } catch (error) {
      message.error('ไม่สามารถดึงข้อมูลได้')
    }
  }

  const handleSubmit = async (values: RegistrationFormData) => {
    if (selectedRoles.length === 0) {
      message.error('กรุณาเลือกสิทธิ์อย่างน้อย 1 สิทธิ์')
      return
    }

    if (values.password !== values.confirmPassword) {
      message.error('รหัสผ่านไม่ตรงกัน')
      return
    }

    setLoading(true)
    try {
      const registrationData = {
        rank_id: values.rank_id,
        full_name: values.full_name,
        position: values.position,
        email: values.email,
        phone_number: values.phone_number,
        line_id: values.line_id,
        role_ids: selectedRoles,
        username: values.username,
        password: values.password
      }

      await api.post('/registration/register', registrationData)
      message.success('สมัครสมาชิกเรียบร้อยแล้ว รอการอนุมัติจากผู้ดูแลระบบ')
      form.resetFields()
      setSelectedRoles([])
      onSuccess()
      onClose()
    } catch (error: any) {
      if (error.response?.data?.detail) {
        message.error(error.response.data.detail)
      } else {
        message.error('เกิดข้อผิดพลาดในการสมัครสมาชิก')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleRoleChange = (checkedValues: number[]) => {
    setSelectedRoles(checkedValues)
  }

  const checkUsernameAvailability = async (username: string) => {
    if (username.length < 3) return
    try {
      const response = await api.get(`/registration/check-username/${username}`)
      if (!response.data.available) {
        throw new Error('ชื่อผู้ใช้นี้มีอยู่แล้ว')
      }
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'ชื่อผู้ใช้นี้มีอยู่แล้ว')
    }
  }

  const checkEmailAvailability = async (email: string) => {
    try {
      const response = await api.get(`/registration/check-email/${email}`)
      if (!response.data.available) {
        throw new Error('อีเมลนี้มีอยู่แล้ว')
      }
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'อีเมลนี้มีอยู่แล้ว')
    }
  }

  return (
    <Modal
      title="สมัครสมาชิก"
      open={open}
      onCancel={onClose}
      footer={null}
      width={800}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
      >
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="ยศ"
              name="rank_id"
              rules={[{ required: true, message: 'กรุณาเลือกยศ' }]}
            >
              <Select placeholder="เลือกยศ" showSearch optionFilterProp="children">
                {ranks.map(rank => (
                  <Select.Option key={rank.id} value={rank.id}>
                    {rank.rank_short}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="ชื่อ-นามสกุล"
              name="full_name"
              rules={[{ required: true, message: 'กรุณากรอกชื่อ-นามสกุล' }]}
            >
              <Input prefix={<UserOutlined />} placeholder="ชื่อ-นามสกุล" />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="ตำแหน่ง"
              name="position"
            >
              <Input placeholder="ตำแหน่ง" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="อีเมล"
              name="email"
              rules={[
                { required: true, message: 'กรุณากรอกอีเมล' },
                { type: 'email', message: 'รูปแบบอีเมลไม่ถูกต้อง' },
                { validator: (_, value) => checkEmailAvailability(value) }
              ]}
            >
              <Input prefix={<MailOutlined />} placeholder="อีเมล" />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="หมายเลขโทรศัพท์"
              name="phone_number"
            >
              <Input prefix={<PhoneOutlined />} placeholder="หมายเลขโทรศัพท์" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="ID Line"
              name="line_id"
            >
              <Input prefix={<IdcardOutlined />} placeholder="ID Line" />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item
          label="สิทธิ์"
          rules={[{ required: true, message: 'กรุณาเลือกสิทธิ์อย่างน้อย 1 สิทธิ์' }]}
        >
          <Checkbox.Group onChange={handleRoleChange} value={selectedRoles}>
            <Row>
              {roles.map(role => (
                <Col span={12} key={role.id}>
                  <Checkbox value={role.id}>
                    {role.role_display}
                    {role.role_description && (
                      <div style={{ fontSize: '12px', color: '#666', marginTop: '2px' }}>
                        {role.role_description}
                      </div>
                    )}
                  </Checkbox>
                </Col>
              ))}
            </Row>
          </Checkbox.Group>
        </Form.Item>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="ชื่อผู้ใช้"
              name="username"
              rules={[
                { required: true, message: 'กรุณากรอกชื่อผู้ใช้' },
                { min: 3, message: 'ชื่อผู้ใช้ต้องมีอย่างน้อย 3 ตัวอักษร' },
                { validator: (_, value) => checkUsernameAvailability(value) }
              ]}
            >
              <Input placeholder="ชื่อผู้ใช้" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="รหัสผ่าน"
              name="password"
              rules={[
                { required: true, message: 'กรุณากรอกรหัสผ่าน' },
                { min: 6, message: 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร' }
              ]}
            >
              <Input.Password placeholder="รหัสผ่าน" />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item
          label="ยืนยันรหัสผ่าน"
          name="confirmPassword"
          rules={[
            { required: true, message: 'กรุณายืนยันรหัสผ่าน' },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve()
                }
                return Promise.reject(new Error('รหัสผ่านไม่ตรงกัน'))
              },
            }),
          ]}
        >
          <Input.Password placeholder="ยืนยันรหัสผ่าน" />
        </Form.Item>

        <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
          <Space>
            <Button onClick={onClose}>
              ยกเลิก
            </Button>
            <Button type="primary" htmlType="submit" loading={loading}>
              สมัครสมาชิก
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Modal>
  )
}

export default RegistrationModal
