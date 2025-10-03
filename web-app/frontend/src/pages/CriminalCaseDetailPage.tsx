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
  Tag,
  Spin,
  Popconfirm
} from 'antd'
import {
  EditOutlined,
  DeleteOutlined,
  BankOutlined,
  UserOutlined,
  ArrowLeftOutlined,
  PrinterOutlined
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'
import BankAccountFormModal from '../components/BankAccountFormModal'
import SuspectFormModal from '../components/SuspectFormModal'
import { CriminalCase, BankAccount, Suspect } from '../types'

const { TabPane } = Tabs

const CriminalCaseDetailPage = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [criminalCase, setCriminalCase] = useState<CriminalCase | null>(null)
  const [bankAccounts, setBankAccounts] = useState<BankAccount[]>([])
  const [suspects, setSuspects] = useState<Suspect[]>([])
  const [loading, setLoading] = useState(true)
  const [bankModalVisible, setBankModalVisible] = useState(false)
  const [suspectModalVisible, setSuspectModalVisible] = useState(false)
  const [editingBankAccount, setEditingBankAccount] = useState<BankAccount | null>(null)
  const [editingSuspect, setEditingSuspect] = useState<Suspect | null>(null)

  useEffect(() => {
    if (id) {
      fetchCriminalCase()
      fetchBankAccounts()
      fetchSuspects()
    }
  }, [id])

  const fetchCriminalCase = async () => {
    try {
      const response = await api.get(`/criminal-cases/${id}`)
      setCriminalCase(response.data)
    } catch (error) {
      message.error('ไม่สามารถโหลดข้อมูลคดีได้')
    }
  }

  const fetchBankAccounts = async () => {
    try {
      const response = await api.get(`/criminal-cases/${id}/bank-accounts`)
      setBankAccounts(response.data)
    } catch (error) {
      message.error('ไม่สามารถโหลดข้อมูลบัญชีธนาคารได้')
    }
  }

  const fetchSuspects = async () => {
    try {
      const response = await api.get(`/criminal-cases/${id}/suspects`)
      setSuspects(response.data)
    } catch (error) {
      message.error('ไม่สามารถโหลดข้อมูลผู้ต้องหาได้')
    } finally {
      setLoading(false)
    }
  }

  const handleAddBankAccount = () => {
    setEditingBankAccount(null)
    setBankModalVisible(true)
  }

  const handleEditBankAccount = (bankAccount: BankAccount) => {
    setEditingBankAccount(bankAccount)
    setBankModalVisible(true)
  }

  const handleDeleteBankAccount = async (bankAccountId: number) => {
    try {
      await api.delete(`/bank-accounts/${bankAccountId}`)
      message.success('ลบบัญชีธนาคารเรียบร้อยแล้ว')
      fetchBankAccounts()
      fetchCriminalCase() // Refresh counts
    } catch (error) {
      message.error('ไม่สามารถลบบัญชีธนาคารได้')
    }
  }

  const handleBankModalClose = (success?: boolean) => {
    setBankModalVisible(false)
    setEditingBankAccount(null)
    if (success) {
      fetchBankAccounts()
      fetchCriminalCase() // Refresh counts
    }
  }

  const handleAddSuspect = () => {
    setEditingSuspect(null)
    setSuspectModalVisible(true)
  }

  const handleEditSuspect = (suspect: Suspect) => {
    setEditingSuspect(suspect)
    setSuspectModalVisible(true)
  }

  const handleDeleteSuspect = async (suspectId: number) => {
    try {
      await api.delete(`/suspects/${suspectId}`)
      message.success('ลบผู้ต้องหาเรียบร้อยแล้ว')
      fetchSuspects()
      fetchCriminalCase() // Refresh counts
    } catch (error) {
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

  // Print Suspect Summons
  const handlePrintSuspectSummons = async (suspectId: number) => {
    try {
      const response = await api.get(`/documents/suspect-summons/${suspectId}`, {
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
      
      message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียกผู้ต้องหา')
    } catch (err) {
      message.error('ไม่สามารถสร้างหมายเรียกผู้ต้องหาได้')
    }
  }

  // Print Suspect Envelope
  const handlePrintSuspectEnvelope = async (suspectId: number) => {
    try {
      const response = await api.get(`/documents/suspect-envelope/${suspectId}`, {
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
      
      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียกผู้ต้องหา')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียกผู้ต้องหาได้')
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

  const bankColumns: ColumnsType<BankAccount> = [
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
      title: 'ธนาคาร',
      dataIndex: 'bank_name',
      key: 'bank_name',
      width: 150,
    },
    {
      title: 'สาขา',
      dataIndex: 'branch_name',
      key: 'branch_name',
      width: 150,
    },
    {
      title: 'ยอดเงิน',
      dataIndex: 'balance',
      key: 'balance',
      width: 120,
      render: (balance: number) => balance ? balance.toLocaleString() : '-',
    },
    {
      title: 'การดำเนินการ',
      key: 'action',
      width: 250,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small" direction="vertical">
          <Space size="small">
            <Button
              type="link"
              icon={<EditOutlined />}
              onClick={() => handleEditBankAccount(record)}
            >
              แก้ไข
            </Button>
            <Popconfirm
              title="คุณแน่ใจหรือไม่ที่จะลบบัญชีธนาคารนี้?"
              onConfirm={() => handleDeleteBankAccount(record.id)}
              okText="ใช่"
              cancelText="ไม่"
            >
              <Button type="link" danger icon={<DeleteOutlined />}>
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
      render: (value) => value || '-',
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
      title: 'สถานะผลหมายเรียก',
      dataIndex: 'reply_status',
      key: 'reply_status',
      width: 160,
      render: (status: boolean) => (
        <Tag color={status ? 'green' : 'orange'}>
          {status ? 'ตอบกลับแล้ว' : 'ยังไม่ตอบกลับ'}
        </Tag>
      ),
    },
    {
      title: 'การดำเนินการ',
      key: 'action',
      width: 250,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small" direction="vertical">
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
          <Button
            type="primary"
            size="small"
            icon={<PrinterOutlined />}
            onClick={() => handlePrintSuspectSummons(record.id)}
            block
          >
            ปริ้นหมายเรียก
          </Button>
          <Button
            size="small"
            icon={<PrinterOutlined />}
            onClick={() => handlePrintSuspectEnvelope(record.id)}
            block
          >
            ปริ้นซองหมายเรียก
          </Button>
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
      <Card>
        <Space style={{ marginBottom: '16px' }}>
          <Button
            icon={<ArrowLeftOutlined />}
            onClick={() => navigate('/dashboard')}
          >
            กลับ
          </Button>
        </Space>

        <Descriptions title="รายละเอียดคดี" bordered column={2}>
          <Descriptions.Item label="เลขที่คดี">
            {criminalCase.case_number}
          </Descriptions.Item>
          <Descriptions.Item label="สถานะคดี">
            <Tag color="blue">{criminalCase.status}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="ผู้ร้องทุกข์">
            {criminalCase.complainant}
          </Descriptions.Item>
          <Descriptions.Item label="ผู้เสียหาย">
            {criminalCase.victim_name}
          </Descriptions.Item>
          <Descriptions.Item label="วันที่ร้องทุกข์">
            {criminalCase.complaint_date_thai || criminalCase.complaint_date}
          </Descriptions.Item>
          <Descriptions.Item label="ศาล">
            {criminalCase.court_name}
          </Descriptions.Item>
          <Descriptions.Item label="จำนวนบัญชีธนาคาร">
            {criminalCase.bank_accounts_count || 0}
          </Descriptions.Item>
          <Descriptions.Item label="จำนวนผู้ต้องหา">
            {criminalCase.suspects_count || 0}
          </Descriptions.Item>
        </Descriptions>

        <Tabs defaultActiveKey="bank-accounts" style={{ marginTop: '24px' }}>
          <TabPane
            tab={
              <span>
                <BankOutlined />
                บัญชีธนาคาร ({bankAccounts.length})
              </span>
            }
            key="bank-accounts"
          >
            <div style={{ marginBottom: '16px' }}>
              <Button type="primary" onClick={handleAddBankAccount}>
                เพิ่มบัญชีธนาคาร
              </Button>
            </div>
            <Table
              columns={bankColumns}
              dataSource={bankAccounts}
              rowKey="id"
              scroll={{ x: 1000 }}
              pagination={false}
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
            <div style={{ marginBottom: '16px' }}>
              <Button type="primary" onClick={handleAddSuspect}>
                เพิ่มผู้ต้องหา
              </Button>
            </div>
            <Table
              columns={suspectColumns}
              dataSource={suspects}
              rowKey="id"
              scroll={{ x: 1000 }}
              pagination={false}
            />
          </TabPane>
        </Tabs>
      </Card>

      <BankAccountFormModal
        visible={bankModalVisible}
        onClose={handleBankModalClose}
        criminalCaseId={Number(id)}
        bankAccount={editingBankAccount}
      />

      <SuspectFormModal
        visible={suspectModalVisible}
        onClose={handleSuspectModalClose}
        criminalCaseId={Number(id)}
        suspect={editingSuspect}
      />
    </div>
  )
}

export default CriminalCaseDetailPage