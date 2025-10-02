import { useCallback, useEffect, useState } from 'react'
import { Table, message, Tag, Space, Button, Descriptions, Drawer, Tabs, Popconfirm, Modal } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { EditOutlined, DeleteOutlined, PlusOutlined, PrinterOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuthStore } from '../stores/authStore'
import BankAccountFormModal from '../components/BankAccountFormModal'
import SuspectFormModal from '../components/SuspectFormModal'

interface BankAccount {
  id: number
  order_number?: number
  document_number?: string
  document_date?: string
  document_date_thai?: string
  bank_name: string
  account_number: string
  account_name: string
  account_owner?: string
  complainant?: string
  victim_name?: string
  case_id?: string
  time_period?: string
  delivery_date?: string
  delivery_month?: string
  delivery_time?: string
  reply_status: boolean
  status: string
  // Note: bank_branch and bank_address removed - use headquarters address from banks table
}

interface Suspect {
  id: number
  document_number?: string
  document_date?: string
  document_date_thai?: string
  suspect_name: string
  suspect_id_card?: string
  suspect_address?: string
  police_station?: string
  police_province?: string
  police_address?: string
  complainant?: string
  victim_name?: string
  case_id?: string
  appointment_date?: string
  appointment_date_thai?: string
  reply_status: boolean
  status: string
}

interface CriminalCase {
  id: number
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  case_type?: string
  complaint_date?: string
  complaint_date_thai?: string
  incident_date?: string
  incident_date_thai?: string
  damage_amount?: string
  case_age_months?: number
  case_age_days?: number
  bank_accounts_count?: string
  suspects_count?: string
  court_name?: string
  row_class?: string
  row_style?: Record<string, any>
}

export default function DashboardPage() {
  const [data, setData] = useState<CriminalCase[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<CriminalCase | null>(null)
  const [bankAccounts, setBankAccounts] = useState<BankAccount[]>([])
  const [suspects, setSuspects] = useState<Suspect[]>([])
  const [loadingDetails, setLoadingDetails] = useState(false)
  const [suspectDetailOpen, setSuspectDetailOpen] = useState(false)
  const [selectedSuspect, setSelectedSuspect] = useState<Suspect | null>(null)
  const [bankModalVisible, setBankModalVisible] = useState(false)
  const [suspectModalVisible, setSuspectModalVisible] = useState(false)
  const [editingBank, setEditingBank] = useState<BankAccount | null>(null)
  const [editingSuspect, setEditingSuspect] = useState<Suspect | null>(null)
  const navigate = useNavigate()
  const { token, user } = useAuthStore()

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      console.log('🔍 Dashboard: Fetching data...', { token: !!token, user: !!user })
      
      const res = await api.get<CriminalCase[]>('/criminal-cases/')
      console.log('📊 Dashboard: Data received:', res.data.length, 'cases')
      
      // Sort by complaint_date descending (newest first)
      const sortedData = res.data.sort((a, b) => {
        if (!a.complaint_date && !b.complaint_date) return 0
        if (!a.complaint_date) return 1
        if (!b.complaint_date) return -1
        return new Date(b.complaint_date).getTime() - new Date(a.complaint_date).getTime()
      })
      setData(sortedData)
      console.log('✅ Dashboard: Data sorted and set:', sortedData.length, 'cases')
    } catch (err: any) {
      console.error('❌ Dashboard: Error fetching data:', err)
      console.error('❌ Dashboard: Error response:', err.response?.data)
      console.error('❌ Dashboard: Error status:', err.response?.status)
      message.error('ไม่สามารถดึงข้อมูลคดีอาญาได้')
    } finally {
      setLoading(false)
    }
  }, [token, user])

  useEffect(() => {
    console.log('🚀 Dashboard: Component mounted, token:', !!token, 'user:', !!user)
    if (!token || !user) {
      console.log('⚠️ Dashboard: No auth token or user, redirecting to login')
      navigate('/login')
      return
    }
    fetchData()
  }, [fetchData, navigate, token, user])

  const fetchCaseDetails = useCallback(async (caseId: number) => {
    try {
      setLoadingDetails(true)
      const [bankRes, suspectsRes] = await Promise.all([
        api.get<BankAccount[]>(`/criminal-cases/${caseId}/bank-accounts`),
        api.get<Suspect[]>(`/criminal-cases/${caseId}/suspects`)
      ])
      setBankAccounts(bankRes.data)
      setSuspects(suspectsRes.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลรายละเอียดคดีได้')
    } finally {
      setLoadingDetails(false)
    }
  }, [])

  const showDetails = (record: CriminalCase) => {
    setSelected(record)
    setOpen(true)
    fetchCaseDetails(record.id)
  }

  const showSuspectDetail = (suspect: Suspect) => {
    setSelectedSuspect(suspect)
    setSuspectDetailOpen(true)
  }

  const handleEdit = (record: CriminalCase) => {
    navigate(`/edit-criminal-case/${record.id}`)
  }

  const handleDelete = async (record: CriminalCase) => {
    try {
      await api.delete(`/criminal-cases/${record.id}`)
      message.success('ลบคดีอาญาสำเร็จ')
      fetchData() // Refresh data
    } catch (err) {
      message.error('ไม่สามารถลบคดีอาญาได้')
    }
  }

  const handleAddNew = () => {
    navigate('/add-criminal-case')
  }

  // Bank Account Handlers
  const handleAddBank = () => {
    setEditingBank(null)
    setBankModalVisible(true)
  }

  const handleEditBank = (record: BankAccount) => {
    setEditingBank(record)
    setBankModalVisible(true)
  }

  const handleDeleteBank = async (bankId: number) => {
    try {
      await api.delete(`/bank-accounts/${bankId}`)
      message.success('ลบบัญชีธนาคารสำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
        fetchData() // Refresh counts
      }
    } catch (err) {
      message.error('ไม่สามารถลบบัญชีธนาคารได้')
    }
  }

  const handleBankModalClose = (success?: boolean) => {
    setBankModalVisible(false)
    setEditingBank(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
      fetchData() // Refresh counts
    }
  }

  // Suspect Handlers
  const handleAddSuspect = () => {
    setEditingSuspect(null)
    setSuspectModalVisible(true)
  }

  const handleEditSuspect = (record: Suspect) => {
    setEditingSuspect(record)
    setSuspectModalVisible(true)
  }

  const handleDeleteSuspect = async (suspectId: number) => {
    try {
      await api.delete(`/suspects/${suspectId}`)
      message.success('ลบผู้ต้องหาสำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
        fetchData() // Refresh counts
      }
    } catch (err) {
      message.error('ไม่สามารถลบผู้ต้องหาได้')
    }
  }

  const handleSuspectModalClose = (success?: boolean) => {
    setSuspectModalVisible(false)
    setEditingSuspect(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
      fetchData() // Refresh counts
    }
  }

  const getStatusTextStyle = (status: string, complaintDate?: string) => {
    if (status === 'จำหน่าย') {
      return { color: 'green' }
    }
    
    if (status === 'อยู่ระหว่างสอบสวน' && complaintDate) {
      const complaintDateObj = new Date(complaintDate)
      const now = new Date()
      const diffTime = now.getTime() - complaintDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays > 180) { // 6 months = ~180 days
        return { color: 'red' }
      }
    }
    
    return {}
  }

  const getRowClassName = (record: CriminalCase) => {
    if (record.status === 'อยู่ระหว่างสอบสวน' && record.complaint_date) {
      const complaintDateObj = new Date(record.complaint_date)
      const now = new Date()
      const diffTime = now.getTime() - complaintDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays > 180) { // 6 months = ~180 days
        return 'row-red'
      }
    }
    return ''
  }

  const calculateCaseAge = (complaintDate?: string) => {
    if (!complaintDate) return '-'
    
    try {
      const complaintDateObj = new Date(complaintDate)
      const now = new Date()
      const diffTime = now.getTime() - complaintDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      const months = Math.floor(diffDays / 30)
      const remainingDays = diffDays % 30
      
      if (months > 0) {
        return `${months} เดือน ${remainingDays} วัน`
      } else {
        return `${remainingDays} วัน`
      }
    } catch {
      return '-'
    }
  }

  const calculateDaysSinceSent = (documentDate?: string) => {
    if (!documentDate) return '-'
    
    try {
      const documentDateObj = new Date(documentDate)
      const now = new Date()
      const diffTime = now.getTime() - documentDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      const months = Math.floor(diffDays / 30)
      const remainingDays = diffDays % 30
      
      if (months > 0) {
        return `${months} เดือน ${remainingDays} วัน`
      } else {
        return `${remainingDays} วัน`
      }
    } catch {
      return '-'
    }
  }

  const formatThaiDate = (dateStr?: string) => {
    if (!dateStr) return '-'
    
    try {
      const date = new Date(dateStr)
      const thaiMonths = [
        'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
        'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
      ]
      
      const day = date.getDate()
      const month = thaiMonths[date.getMonth()]
      const year = date.getFullYear() + 543 // Convert to Buddhist Era
      
      return `${day} ${month} ${year}`
    } catch {
      return '-'
    }
  }

  const columns: ColumnsType<CriminalCase> = [
    {
      title: 'เลขที่คดี',
      dataIndex: 'case_number',
      key: 'case_number',
      render: (_, record: CriminalCase) => (
        <Button type="link" onClick={() => showDetails(record)}>
          {record.case_number}
        </Button>
      ),
    },
    {
      title: 'CaseID',
      dataIndex: 'case_id',
      key: 'case_id',
    },
    {
      title: 'สถานะคดี',
      dataIndex: 'status',
      key: 'status',
      render: (status: string, record: CriminalCase) => {
        const textStyle = getStatusTextStyle(status, record.complaint_date)
        return <Tag color="blue" style={textStyle}>{status}</Tag>
      },
    },
    {
      title: 'ผู้ร้องทุกข์',
      dataIndex: 'complainant',
      key: 'complainant',
    },
    {
      title: 'วันที่/เวลา รับคำร้องทุกข์',
      dataIndex: 'complaint_date',
      key: 'complaint_date',
      render: (date: string) => formatThaiDate(date),
      sorter: (a, b) => {
        if (!a.complaint_date && !b.complaint_date) return 0
        if (!a.complaint_date) return 1
        if (!b.complaint_date) return -1
        return new Date(a.complaint_date).getTime() - new Date(b.complaint_date).getTime()
      },
      defaultSortOrder: 'descend',
    },
    {
      title: 'เขตอำนาจศาล',
      dataIndex: 'court_name',
      key: 'court_name',
      render: (courtName: string) => courtName || '-',
    },
    {
      title: 'อายุคดี',
      dataIndex: 'complaint_date',
      key: 'case_age',
      render: (date: string) => calculateCaseAge(date),
    },
    {
      title: 'จำนวนบัญชีธนาคาร',
      dataIndex: 'bank_accounts_count',
      key: 'bank_accounts_count',
    },
    {
      title: 'จำนวน ผู้ต้องหาที่เกี่ยวข้อง',
      dataIndex: 'suspects_count',
      key: 'suspects_count',
    },
    {
      title: 'จัดการ',
      key: 'actions',
      render: (_, record: CriminalCase) => (
        <Space>
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          />
          <Popconfirm
            title="คุณแน่ใจหรือไม่ที่จะลบคดีนี้?"
            onConfirm={() => handleDelete(record)}
            okText="ใช่"
            cancelText="ไม่"
          >
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
            />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  if (!token || !user) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>กำลังตรวจสอบการเข้าสู่ระบบ...</p>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>คดีอาญาในความรับผิดชอบ</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAddNew}>
          เพิ่มคดีใหม่
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={data}
        loading={loading}
        rowKey="id"
        rowClassName={getRowClassName}
        pagination={{
          pageSize: 20,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => `${range[0]}-${range[1]} จาก ${total} รายการ`,
        }}
      />

      <Drawer
        title={
          `รายละเอียดคดี ${selected?.case_number || ''}${selected?.case_id ? ` | CaseID: ${selected.case_id}` : ''} ${
            selected?.complainant
              ? `(${selected.complainant.replace(/^\d+\)\s*/, '')})`
              : ''
          }`
        }
        placement="right"
        width="70%"
        onClose={() => setOpen(false)}
        open={open}
      >
        {selected && (
          <Tabs defaultActiveKey="general">
            <Tabs.TabPane tab="ข้อมูลทั่วไป" key="general">
              <Descriptions column={2} bordered>
                <Descriptions.Item label="เลขที่คดี">{selected.case_number || '-'}</Descriptions.Item>
                <Descriptions.Item label="CaseID">{selected.case_id || '-'}</Descriptions.Item>
                <Descriptions.Item label="สถานะคดี">{selected.status}</Descriptions.Item>
                <Descriptions.Item label="ประเภทคดี">{selected.case_type || '-'}</Descriptions.Item>
                <Descriptions.Item label="ผู้ร้องทุกข์">{selected.complainant}</Descriptions.Item>
                <Descriptions.Item label="วันที่/เวลา รับคำร้องทุกข์">
                  {selected.complaint_date_thai || '-'}
                </Descriptions.Item>
                <Descriptions.Item label="อายุคดี">
                  {calculateCaseAge(selected.complaint_date)}
                </Descriptions.Item>
                <Descriptions.Item label="ความเสียหาย">
                  {selected.damage_amount || '-'}
                </Descriptions.Item>
                <Descriptions.Item label="สถานที่เกิดเหตุ">
                  -
                </Descriptions.Item>
              </Descriptions>
            </Tabs.TabPane>

            <Tabs.TabPane tab="บัญชีธนาคารที่เกี่ยวข้อง" key="bank-accounts">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddBank}
                >
                  เพิ่มบัญชีธนาคาร
                </Button>
              </Space>
              <Table
                dataSource={bankAccounts}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date_thai',
                    key: 'document_date_thai',
                    render: (date) => date || '-',
                  },
                  {
                    title: 'ชื่อธนาคาร',
                    dataIndex: 'bank_name',
                    key: 'bank_name',
                  },
                  {
                    title: 'เลขบัญชี',
                    dataIndex: 'account_number',
                    key: 'account_number',
                  },
                  {
                    title: 'ชื่อบัญชี',
                    dataIndex: 'account_name',
                    key: 'account_name',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: BankAccount) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การดำเนินการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            size="small"
                            icon={<EditOutlined />}
                            onClick={() => handleEditBank(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="คุณแน่ใจหรือไม่ที่จะลบบัญชีนี้?"
                            onConfirm={() => handleDeleteBank(record.id)}
                            okText="ใช่"
                            cancelText="ไม่"
                          >
                            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={async () => {
                            try {
                              const response = await api.get(`/documents/bank-summons/${record.id}`, {
                                responseType: 'blob'
                              })
                              const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
                              const url = window.URL.createObjectURL(blob)
                              const printWindow = window.open(url, '_blank')
                              if (printWindow) {
                                printWindow.onload = () => {
                                  setTimeout(() => printWindow.print(), 500)
                                }
                              }
                              message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก')
                            } catch (err) {
                              message.error('ไม่สามารถสร้างหมายเรียกได้')
                            }
                          }}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={async () => {
                            try {
                              const response = await api.get(`/documents/bank-envelope/${record.id}`, {
                                responseType: 'blob'
                              })
                              const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
                              const url = window.URL.createObjectURL(blob)
                              const printWindow = window.open(url, '_blank')
                              if (printWindow) {
                                printWindow.onload = () => {
                                  setTimeout(() => printWindow.print(), 500)
                                }
                              }
                              message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียก')
                            } catch (err) {
                              message.error('ไม่สามารถสร้างซองหมายเรียกได้')
                            }
                          }}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>

            <Tabs.TabPane tab="ผู้ต้องหาที่เกี่ยวข้อง" key="suspects">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddSuspect}
                >
                  เพิ่มผู้ต้องหา
                </Button>
              </Space>
              <Table
                dataSource={suspects}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value ? parseInt(value.toString()) : '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date_thai',
                    key: 'document_date_thai',
                    render: (date) => date || '-',
                  },
                  {
                    title: 'ชื่อผู้ต้องหา',
                    dataIndex: 'suspect_name',
                    key: 'suspect_name',
                    render: (name: string, record: Suspect) => (
                      <Button type="link" onClick={() => showSuspectDetail(record)}>
                        {name}
                      </Button>
                    ),
                  },
                  {
                    title: 'บัตรประชาชน',
                    dataIndex: 'suspect_id_card',
                    key: 'suspect_id_card',
                  },
                  {
                    title: 'ที่อยู่ผู้ต้องหา',
                    dataIndex: 'suspect_address',
                    key: 'suspect_address',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: Suspect) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การดำเนินการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small">
                        <Button
                          type="link"
                          icon={<EditOutlined />}
                          onClick={() => handleEditSuspect(record)}
                        >
                          แก้ไข
                        </Button>
                        <Popconfirm
                          title="คุณแน่ใจหรือไม่ที่จะลบผู้ต้องหานี้?"
                          onConfirm={() => handleDeleteSuspect(record.id)}
                          okText="ใช่"
                          cancelText="ไม่"
                        >
                          <Button type="link" danger icon={<DeleteOutlined />}>
                            ลบ
                          </Button>
                        </Popconfirm>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>
          </Tabs>
        )}
      </Drawer>

      <Modal
        title={`รายละเอียดหมายเรียกผู้ต้องหา - ${selectedSuspect?.suspect_name || ''}`}
        open={suspectDetailOpen}
        onCancel={() => setSuspectDetailOpen(false)}
        footer={[
          <Button key="close" onClick={() => setSuspectDetailOpen(false)}>
            ปิด
          </Button>
        ]}
        width={700}
      >
        {selectedSuspect && (
          <Descriptions column={1} bordered>
            <Descriptions.Item label="เลขหนังสือ">
              {selectedSuspect.document_number ? parseInt(selectedSuspect.document_number.toString()) : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ลงวันที่">
              {selectedSuspect.document_date_thai || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ชื่อผู้ต้องหา">
              {selectedSuspect.suspect_name}
            </Descriptions.Item>
            <Descriptions.Item label="บัตรประชาชน">
              {selectedSuspect.suspect_id_card || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ที่อยู่ผู้ต้องหา">
              {selectedSuspect.suspect_address || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="กำหนดให้มาพบ">
              {selectedSuspect.appointment_date_thai || selectedSuspect.appointment_date || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="สถานีตำรวจ">
              {selectedSuspect.police_station || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="จังหวัด">
              {selectedSuspect.police_province || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ที่อยู่สถานีตำรวจ">
              {selectedSuspect.police_address || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="สถานะตอบกลับ">
              {selectedSuspect.reply_status ? (
                <Tag color="green">ตอบกลับแล้ว</Tag>
              ) : (
                <Tag color="red">ยังไม่ตอบกลับ</Tag>
              )}
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>

      <BankAccountFormModal
        visible={bankModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingBank}
        onClose={handleBankModalClose}
      />

      <SuspectFormModal
        visible={suspectModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingSuspect}
        onClose={handleSuspectModalClose}
      />

      <style>{`
        .row-red {
          background-color: #fff2f0 !important;
        }
        .row-green {
          background-color: #f6ffed !important;
        }
      `}</style>
    </div>
  )
}