import React, { useEffect, useState } from 'react'
import { Card, Table, Switch, message, Typography, Tag, Space, Collapse, Statistic, Row, Col } from 'antd'
import { TeamOutlined, BankOutlined, ApartmentOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Title } = Typography
const { Panel } = Collapse

interface Supervision {
  id: number
  division_id: number
  name_full: string
  name_short: string
  is_active: boolean
  user_count: number
}

interface Division {
  id: number
  bureau_id: number
  name_full: string
  name_short: string
  is_active: boolean
  supervisions: Supervision[]
  user_count: number
}

interface Bureau {
  id: number
  name_full: string
  name_short: string
  is_active: boolean
  divisions: Division[]
  user_count: number
}

interface OrganizationTree {
  bureaus: Bureau[]
  total_users: number
  active_organizations: number
  inactive_organizations: number
}

const OrganizationManagementPage: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [orgTree, setOrgTree] = useState<OrganizationTree | null>(null)

  useEffect(() => {
    fetchOrganizationTree()
  }, [])

  const fetchOrganizationTree = async () => {
    setLoading(true)
    try {
      const response = await api.get('/organizations/tree')
      setOrgTree(response.data)
    } catch (error) {
      message.error('ไม่สามารถโหลดข้อมูลหน่วยงานได้')
    } finally {
      setLoading(false)
    }
  }

  const handleToggleSupervision = async (supervisionId: number, currentStatus: boolean) => {
    try {
      await api.put(`/organizations/supervisions/${supervisionId}`, {
        is_active: !currentStatus
      })
      message.success('อัพเดตสิทธิ์หน่วยงานสำเร็จ')
      fetchOrganizationTree()
    } catch (error) {
      message.error('ไม่สามารถอัพเดตสิทธิ์ได้')
    }
  }

  const handleToggleDivision = async (divisionId: number, currentStatus: boolean) => {
    try {
      await api.put(`/organizations/divisions/${divisionId}`, {
        is_active: !currentStatus
      })
      message.success('อัพเดตสิทธิ์หน่วยงานสำเร็จ')
      fetchOrganizationTree()
    } catch (error) {
      message.error('ไม่สามารถอัพเดตสิทธิ์ได้')
    }
  }

  const supervisionColumns = [
    {
      title: 'ชื่อหน่วยงาน',
      dataIndex: 'name_full',
      key: 'name_full',
      width: '40%',
    },
    {
      title: 'ชื่อย่อ',
      dataIndex: 'name_short',
      key: 'name_short',
      width: '30%',
    },
    {
      title: 'จำนวนผู้ใช้',
      dataIndex: 'user_count',
      key: 'user_count',
      width: '15%',
      align: 'center' as const,
      render: (count: number) => (
        <Tag color={count > 0 ? 'blue' : 'default'}>{count} คน</Tag>
      ),
    },
    {
      title: 'สถานะ',
      dataIndex: 'is_active',
      key: 'is_active',
      width: '15%',
      align: 'center' as const,
      render: (isActive: boolean, record: Supervision) => (
        <Switch
          checked={isActive}
          onChange={() => handleToggleSupervision(record.id, isActive)}
          checkedChildren="เปิด"
          unCheckedChildren="ปิด"
        />
      ),
    },
  ]

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <ApartmentOutlined /> จัดการหน่วยงาน
      </Title>

      {/* Statistics */}
      {orgTree && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="จำนวนผู้ใช้ทั้งหมด"
                value={orgTree.total_users}
                prefix={<TeamOutlined />}
                suffix="คน"
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="หน่วยงานเปิดใช้งาน"
                value={orgTree.active_organizations}
                valueStyle={{ color: '#3f8600' }}
                suffix="หน่วย"
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="หน่วยงานปิดใช้งาน"
                value={orgTree.inactive_organizations}
                valueStyle={{ color: '#cf1322' }}
                suffix="หน่วย"
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="รวมหน่วยงานทั้งหมด"
                value={orgTree.active_organizations + orgTree.inactive_organizations}
                suffix="หน่วย"
              />
            </Card>
          </Col>
        </Row>
      )}

      {/* Organization Tree */}
      <Card loading={loading}>
        {orgTree?.bureaus.map((bureau) => (
          <div key={bureau.id} style={{ marginBottom: 24 }}>
            <div
              style={{
                background: '#001529',
                color: 'white',
                padding: '12px 16px',
                borderRadius: '4px',
                marginBottom: 16,
              }}
            >
              <Space>
                <BankOutlined style={{ fontSize: 20 }} />
                <span style={{ fontSize: 18, fontWeight: 'bold' }}>
                  {bureau.name_short}
                </span>
                <Tag color={bureau.is_active ? 'success' : 'error'}>
                  {bureau.is_active ? 'เปิดใช้งาน' : 'ปิดใช้งาน'}
                </Tag>
                <Tag color="blue">{bureau.user_count} คน</Tag>
              </Space>
            </div>

            <Collapse defaultActiveKey={['1', '2', '3', '4', '5']}>
              {bureau.divisions.map((division, index) => (
                <Panel
                  header={
                    <Space>
                      <strong>{division.name_short}</strong>
                      <Tag color={division.is_active ? 'success' : 'error'}>
                        {division.is_active ? 'เปิด' : 'ปิด'}
                      </Tag>
                      <Tag color="blue">{division.user_count} คน</Tag>
                      <Switch
                        size="small"
                        checked={division.is_active}
                        onChange={(checked) => handleToggleDivision(division.id, !checked)}
                        onClick={(_, e) => e.stopPropagation()}
                        checkedChildren="เปิด"
                        unCheckedChildren="ปิด"
                      />
                    </Space>
                  }
                  key={String(index + 1)}
                >
                  <Table
                    dataSource={division.supervisions}
                    columns={supervisionColumns}
                    rowKey="id"
                    pagination={false}
                    size="small"
                  />
                </Panel>
              ))}
            </Collapse>
          </div>
        ))}
      </Card>

      <Card style={{ marginTop: 16 }} type="inner">
        <Typography.Paragraph>
          <strong>คำอธิบาย:</strong>
          <ul>
            <li>เปิดสิทธิ์: หน่วยงานจะปรากฏในหน้าสมัครสมาชิกให้เลือกได้</li>
            <li>ปิดสิทธิ์: หน่วยงานจะไม่ปรากฏในหน้าสมัครสมาชิก (ผู้ใช้เดิมยังใช้งานได้ปกติ)</li>
            <li>จำนวนผู้ใช้: แสดงจำนวนผู้ใช้ที่สังกัดหน่วยงานนั้น</li>
          </ul>
        </Typography.Paragraph>
      </Card>
    </div>
  )
}

export default OrganizationManagementPage

