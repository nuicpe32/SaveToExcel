import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Button,
  Card,
  Descriptions,
  Space,
  Table,
  Tabs,
  message,
  Spin,
  Typography,
  Tag,
  Popconfirm
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  BankOutlined,
  UserOutlined,
  FileTextOutlined,
  ArrowLeftOutlined,
  PrinterOutlined
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'
import BankAccountFormModal from '../components/BankAccountFormModal'
import SuspectFormModal from '../components/SuspectFormModal'

const { Title } = Typography
const { TabPane } = Tabs

interface CriminalCase {
  id: number
  case_number: string
  case_id: string
  status: string
  complainant: string
  victim_name?: string
  suspect?: string
  charge?: string
  case_scene?: string
  damage_amount?: string
  complaint_date?: string
  incident_date?: string
  court_name?: string
  prosecutor_name?: string
  officer_in_charge?: string
  notes?: string
  bank_accounts_count?: string
  suspects_count?: string
}

interface BankAccount {
  id: number
  document_number: string
  document_date?: string
  bank_name: string
  account_number: string
  account_name: string
  reply_status: boolean
  response_date?: string
  status: string
  notes?: string
}

interface Suspect {
  id: number
  document_number?: string
  document_date?: string
  suspect_name: string
  suspect_id_card?: string
  police_station?: string
  appointment_date?: string
  reply_status: boolean
  status: string
  notes?: string
}

export default function CriminalCaseDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(false)
  const [criminalCase, setCriminalCase] = useState<CriminalCase | null>(null)
  const [bankAccounts, setBankAccounts] = useState<BankAccount[]>([])
  const [suspects, setSuspects] = useState<Suspect[]>([])

  // Modal states
  const [bankModalVisible, setBankModalVisible] = useState(false)
  const [suspectModalVisible, setSuspectModalVisible] = useState(false)
  const [editingBank, setEditingBank] = useState<BankAccount | null>(null)
  const [editingSuspect, setEditingSuspect] = useState<Suspect | null>(null)

  const fetchCriminalCase = async () => {
    try {
      setLoading(true)
      const res = await api.get<CriminalCase>(`/criminal-cases/${id}`)
      setCriminalCase(res.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลคดีได้')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const fetchBankAccounts = async () => {
    try {
      const res = await api.get<BankAccount[]>(`/bank-accounts/?criminal_case_id=${id}`)
      setBankAccounts(res.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลบัญชีธนาคารได้')
    }
  }

  const fetchSuspects = async () => {
    try {
      const res = await api.get<Suspect[]>(`/suspects/?criminal_case_id=${id}`)
      setSuspects(res.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลผู้ต้องหาได้')
    }
  }

  useEffect(() => {
    if (id) {
      fetchCriminalCase()
      fetchBankAccounts()
      fetchSuspects()
    }
  }, [id])

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
      fetchBankAccounts()
      fetchCriminalCase() // Refresh counts
    } catch (err) {
      message.error('ไม่สามารถลบบัญชีธนาคารได้')
    }
  }

  const handleBankModalClose = (success?: boolean) => {
    setBankModalVisible(false)
    setEditingBank(null)
    if (success) {
      fetchBankAccounts()
      fetchCriminalCase() // Refresh counts
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
      fetchSuspects()
      fetchCriminalCase() // Refresh counts
    } catch (err) {
      message.error('ไม่สามารถลบผู้ต้องหาได้')
    }
  }

  const handleSuspectModalClose = (success?: boolean) => {
    setSuspectModalVisible(false)
    setEditingSuspect(null)
    if (success) {
      fetchSuspects()
      fetchCriminalCase() // Refresh counts
    }
  }

  // Print Bank Summons
  const handlePrintBankSummons = async (bankAccountId: number) => {
    try {
      const response = await api.get(`/documents/bank-summons/${bankAccountId}`, {
        responseType: 'blob'
      })
      
      // สร้าง Blob URL และเปิดหน้าต่างใหม่
      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')
      
      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }
      
      message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก')
    } catch (err) {
      message.error('ไม่สามารถสร้างหมายเรียกได้')
    }
  }

  // Print Bank Envelope
  const handlePrintBankEnvelope = async (bankAccountId: number) => {
    try {
      const response = await api.get(`/documents/bank-envelope/${bankAccountId}`, {
        responseType: 'blob'
      })
      
      // สร้าง Blob URL และเปิดหน้าต่างใหม่
      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')
      
      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }
      
      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียก')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียกได้')
    }
  }

  // Table Columns
  const bankColumns: ColumnsType<BankAccount> = [
    {
      title: 'เลขที่เอกสาร',
      dataIndex: 'document_number',
      key: 'document_number',
      width: 150,
      render: (text: string) => text || '-',
    },
    {
      title: 'ธนาคาร',
      dataIndex: 'bank_name',
      key: 'bank_name',
      width: 200,
    },
    {
      title: 'เลขที่บัญชี',
      dataIndex: 'account_number',
      key: 'account_number',
      width: 150,
    },
    {
      title: 'ชื่อบัญชี',
      dataIndex: 'account_name',
      key: 'account_name',
      width: 200,
    },
    {
      title: 'สถานะตอบกลับ',
      dataIndex: 'reply_status',
      key: 'reply_status',
      width: 120,
      render: (status: boolean) => (
        <Tag color={status ? 'green' : 'orange'}>
          {status ? 'ตอบแล้ว' : 'รอตอบกลับ'}
        </Tag>
      ),
    },
    {
      title: 'การดำเนินการ',
      key: 'action',
      width: 200,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small" direction="vertical" style={{ width: '100%' }}>
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
            onClick={() => handlePrintBankSummons(record.id)}
            block
          >
            ปริ้นหมายเรียก
          </Button>
          <Button
            size="small"
            icon={<PrinterOutlined />}
            onClick={() => handlePrintBankEnvelope(record.id)}
            block
          >
            ปริ้นซองหมายเรียก
          </Button>
        </Space>
      ),
    },
  ]

  const suspectColumns: ColumnsType<Suspect> = [
    {
      title: 'เลขที่เอกสาร',
      dataIndex: 'document_number',
      key: 'document_number',
      width: 150,
    },
    {
      title: 'ชื่อผู้ต้องหา',
      dataIndex: 'suspect_name',
      key: 'suspect_name',
      width: 200,
    },
    {
      title: 'เลขบัตรประชาชน',
      dataIndex: 'suspect_id_card',
      key: 'suspect_id_card',
      width: 150,
    },
    {
      title: 'สถานีตำรวจ',
      dataIndex: 'police_station',
      key: 'police_station',
      width: 200,
    },
    {
      title: 'วันนัดหมาย',
      dataIndex: 'appointment_date',
      key: 'appointment_date',
      width: 120,
    },
    {
      title: 'สถานะมาตามนัด',
      dataIndex: 'reply_status',
      key: 'reply_status',
      width: 120,
      render: (status: boolean) => (
        <Tag color={status ? 'green' : 'orange'}>
          {status ? 'มาแล้ว' : 'ยังไม่มา'}
        </Tag>
      ),
    },
    {
      title: 'การดำเนินการ',
      key: 'action',
      width: 150,
      fixed: 'right',
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
  ]

  if (loading || !criminalCase) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <Space style={{ marginBottom: 16 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/dashboard')}>
          กลับ
        </Button>
      </Space>

      <Card>
        <Title level={3}>
          <FileTextOutlined /> คดีหมายเลข {criminalCase.case_number}
        </Title>

        {/* Case Details */}
        <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
          <Descriptions.Item label="เลขคดี">{criminalCase.case_number}</Descriptions.Item>
          <Descriptions.Item label="Case ID">{criminalCase.case_id}</Descriptions.Item>
          <Descriptions.Item label="สถานะ">
            <Tag color="blue">{criminalCase.status}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="วันที่รับคำกล่าวหา">
            {criminalCase.complaint_date}
          </Descriptions.Item>
          <Descriptions.Item label="ผู้กล่าวหา" span={2}>
            {criminalCase.complainant}
          </Descriptions.Item>
          <Descriptions.Item label="ผู้เสียหาย">
            {criminalCase.victim_name || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="ผู้ต้องหา">
            {criminalCase.suspect || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="ข้อกล่าวหา" span={2}>
            {criminalCase.charge || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="มูลค่าความเสียหาย">
            {criminalCase.damage_amount || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="เจ้าหน้าที่รับผิดชอบ">
            {criminalCase.officer_in_charge || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="สถานที่เกิดเหตุ" span={2}>
            {criminalCase.case_scene || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="เขตอำนาจศาล" span={2}>
            {criminalCase.court_name || '-'}
          </Descriptions.Item>
          {criminalCase.notes && (
            <Descriptions.Item label="หมายเหตุ" span={2}>
              {criminalCase.notes}
            </Descriptions.Item>
          )}
        </Descriptions>

        {/* Tabs for Bank Accounts and Suspects */}
        <Tabs defaultActiveKey="banks">
          <TabPane
            tab={
              <span>
                <BankOutlined />
                บัญชีธนาคาร ({bankAccounts.length})
              </span>
            }
            key="banks"
          >
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
              columns={bankColumns}
              dataSource={bankAccounts}
              rowKey="id"
              scroll={{ x: 1200 }}
              pagination={{ pageSize: 10 }}
            />
          </TabPane>

          <TabPane
            tab={
              <span>
                <UserOutlined />
                ผู้ต้องหา ({suspects.length})
              </span>
            }
            key="suspects"
          >
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
              columns={suspectColumns}
              dataSource={suspects}
              rowKey="id"
              scroll={{ x: 1200 }}
              pagination={{ pageSize: 10 }}
            />
          </TabPane>
        </Tabs>
      </Card>

      {/* Modals */}
      <BankAccountFormModal
        visible={bankModalVisible}
        criminalCaseId={Number(id)}
        editingRecord={editingBank}
        onClose={handleBankModalClose}
      />

      <SuspectFormModal
        visible={suspectModalVisible}
        criminalCaseId={Number(id)}
        editingRecord={editingSuspect}
        onClose={handleSuspectModalClose}
      />
    </div>
  )
}
