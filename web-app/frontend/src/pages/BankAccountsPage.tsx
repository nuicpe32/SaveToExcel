import { useEffect, useState, useCallback } from 'react'
import { Button, Descriptions, Drawer, Space, Table, Tabs, message } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'

interface BankAccount {
  id: number
  document_number: string
  bank_name: string
  account_number: string
  account_name: string
  status: string
  document_date?: string
  account_owner?: string
  victim_name?: string
  case_id?: string
  time_period?: string
  delivery_date?: string
  delivery_month?: string
  delivery_time?: string
  reply_status?: boolean
  response_date?: string
  notes?: string
  // Note: Address fields removed - retrieved from banks table via bank_id
}

export default function BankAccountsPage() {
  const [data, setData] = useState<BankAccount[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<BankAccount | null>(null)

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      const res = await api.get<BankAccount[]>('/bank-accounts/')
      setData(res.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลบัญชีธนาคารได้')
    } finally {
      setLoading(false)
    }
  }, [])

  const downloadDocument = useCallback(async (record: BankAccount) => {
    try {
      const res = await api.get(`/documents/bank-account/${record.id}`, {
        responseType: 'blob',
      })
      const blob = new Blob([res.data], { type: res.headers['content-type'] || 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `bank_account_${record.document_number}.docx`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      message.error('ดาวน์โหลดเอกสารไม่สำเร็จ')
    }
  }, [])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const columns: ColumnsType<BankAccount> = [
    { title: 'เลขที่เอกสาร', dataIndex: 'document_number', key: 'document_number' },
    { title: 'ธนาคาร', dataIndex: 'bank_name', key: 'bank_name' },
    { title: 'เลขที่บัญชี', dataIndex: 'account_number', key: 'account_number' },
    { title: 'ชื่อบัญชี', dataIndex: 'account_name', key: 'account_name' },
    { title: 'สถานะ', dataIndex: 'status', key: 'status' },
    {
      title: 'การทำงาน',
      key: 'actions',
      render: (_value: unknown, record: BankAccount) => (
        <Space>
          <Button onClick={() => downloadDocument(record)}>ดาวน์โหลดเอกสาร</Button>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <h1>จัดการบัญชีธนาคาร</h1>
      <Table
        rowKey="id"
        columns={columns}
        dataSource={data}
        loading={loading}
        onRow={(record) => ({
          onClick: () => {
            setSelected(record)
            setOpen(true)
          },
        })}
      />

      <Drawer
        title={selected ? `รายละเอียดบัญชีธนาคาร: ${selected.document_number}` : 'รายละเอียด'}
        placement="right"
        width={520}
        onClose={() => setOpen(false)}
        open={open}
        extra={selected ? (
          <Space>
            <Button onClick={() => downloadDocument(selected)}>ดาวน์โหลดเอกสาร</Button>
          </Space>
        ) : null}
      >
        {selected && (
          <Tabs
            items={[
              {
                key: 'doc',
                label: 'เอกสาร',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="เลขที่เอกสาร">{selected.document_number}</Descriptions.Item>
                    <Descriptions.Item label="วันที่เอกสาร">{selected.document_date || '-'}</Descriptions.Item>
                    <Descriptions.Item label="สถานะ">{selected.status}</Descriptions.Item>
                    <Descriptions.Item label="หมายเหตุ">{selected.notes || '-'}</Descriptions.Item>
                  </Descriptions>
                ),
              },
              {
                key: 'bank',
                label: 'ข้อมูลธนาคาร',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="ธนาคาร">{selected.bank_name}</Descriptions.Item>
                    <Descriptions.Item label="เลขที่บัญชี">{selected.account_number}</Descriptions.Item>
                    <Descriptions.Item label="ชื่อบัญชี">{selected.account_name}</Descriptions.Item>
                    <Descriptions.Item label="ช่วงเวลา">{selected.time_period || '-'}</Descriptions.Item>
                    <Descriptions.Item label="หมายเหตุ">ที่อยู่จากสำนักงานใหญ่ (ดูในข้อมูลธนาคาร)</Descriptions.Item>
                  </Descriptions>
                ),
              },
              {
                key: 'case',
                label: 'ผู้เสียหาย/คดี',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="ผู้เสียหาย">{selected.victim_name || '-'}</Descriptions.Item>
                    <Descriptions.Item label="เคสไอดี">{selected.case_id || '-'}</Descriptions.Item>
                  </Descriptions>
                ),
              },
              {
                key: 'delivery',
                label: 'การส่งและตอบกลับ',
                children: (
                  <>
                    <Descriptions column={1} bordered size="small">
                      <Descriptions.Item label="วันนัดส่ง">{selected.delivery_date || '-'}</Descriptions.Item>
                      <Descriptions.Item label="เวลาส่ง">{selected.delivery_time || '-'}</Descriptions.Item>
                      <Descriptions.Item label="ตอบกลับแล้ว">{selected.reply_status ? '✓' : '—'}</Descriptions.Item>
                      <Descriptions.Item label="วันที่ตอบกลับ">{selected.response_date || '-'}</Descriptions.Item>
                      <Descriptions.Item label="หมายเหตุ">{selected.notes || '-'}</Descriptions.Item>
                    </Descriptions>
                    <p style={{ marginTop: 16, color: '#888', fontSize: '13px' }}>
                      📍 ที่อยู่ธนาคาร: ใช้ที่อยู่สำนักงานใหญ่จากระบบ (ดูจากข้อมูลธนาคาร)
                    </p>
                  </>
                ),
              },
            ]}
          />
        )}
      </Drawer>
    </div>
  )
}