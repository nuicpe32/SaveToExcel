import { useEffect, useState, useCallback } from 'react'
import { Button, Descriptions, Drawer, Space, Table, Tabs, message, Tag, Input } from 'antd'
import type { ColumnsType, FilterDropdownProps } from 'antd/es/table'
import { SearchOutlined } from '@ant-design/icons'
import api from '../services/api'
import dayjs from 'dayjs'

interface CriminalCase {
  id: number
  case_id?: string
  case_number?: string
  victim_name?: string
  complainant?: string
  damage_amount?: string
}

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
  criminal_case?: CriminalCase
  // Note: Address fields removed - retrieved from banks table via bank_id
}

export default function BankAccountsPage() {
  const [data, setData] = useState<BankAccount[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<BankAccount | null>(null)
  
  // ฟังก์ชันแปลงวันที่เป็นรูปแบบไทย
  const formatThaiDate = (date: string | undefined): string => {
    if (!date) return '-'
    
    const thaiMonths = [
      'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
      'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
    ]
    
    const dayjsDate = dayjs(date)
    const day = dayjsDate.date()
    const month = thaiMonths[dayjsDate.month()]
    const year = (dayjsDate.year() + 543).toString().slice(-2) // แปลงเป็น พ.ศ. และย่อเป็น 2 หลัก
    
    return `${day} ${month} ${year}`
  }

  // Pagination state
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 50,
    total: 0,
    showSizeChanger: true,
    showQuickJumper: true,
    showTotal: (total: number, range: [number, number]) => 
      `${range[0]}-${range[1]} จาก ${total} รายการ`,
  })

  // ฟังก์ชันสำหรับ filter dropdown
  const getColumnSearchProps = (dataIndex: keyof BankAccount) => ({
    filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }: FilterDropdownProps) => (
      <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
        <Input
          placeholder={`ค้นหา ${dataIndex}`}
          value={selectedKeys[0]}
          onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
          onPressEnter={() => confirm()}
          style={{ marginBottom: 8, display: 'block' }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => confirm()}
            icon={<SearchOutlined />}
            size="small"
            style={{ width: 90 }}
          >
            ค้นหา
          </Button>
          <Button
            onClick={() => clearFilters && clearFilters()}
            size="small"
            style={{ width: 90 }}
          >
            รีเซ็ต
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered: boolean) => (
      <SearchOutlined style={{ color: filtered ? '#1677ff' : undefined }} />
    ),
    onFilter: (value: string | number | boolean, record: BankAccount) => {
      const cellValue = record[dataIndex]
      if (cellValue == null) return false
      return cellValue.toString().toLowerCase().includes(value.toString().toLowerCase())
    },
  })

  // ฟังก์ชันคำนวณจำนวนวันที่ส่งไปแล้ว (ใช้ document_date)
  const calculateDaysSinceDocument = (documentDate: string | undefined): number => {
    if (!documentDate) return 0
    const docDate = dayjs(documentDate)
    const today = dayjs()
    return today.diff(docDate, 'day')
  }

  // ฟังก์ชันแสดงสถานะตอบกลับ
  const renderReplyStatus = (record: BankAccount) => {
    if (record.reply_status) {
      return (
        <div style={{ textAlign: 'center' }}>
          <Tag color="green">ตอบกลับแล้ว</Tag>
        </div>
      )
    } else {
      const daysSince = calculateDaysSinceDocument(record.document_date)
      if (daysSince > 0) {
        return (
          <div style={{ textAlign: 'center' }}>
            <Tag color="red">ยังไม่ตอบกลับ</Tag>
            <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
              (ส่งไปแล้ว {daysSince} วัน)
            </div>
          </div>
        )
      } else {
        return (
          <div style={{ textAlign: 'center' }}>
            <Tag color="red">ยังไม่ตอบกลับ</Tag>
          </div>
        )
      }
    }
  }

  const fetchData = useCallback(async (page: number = 1, pageSize: number = 50) => {
    try {
      setLoading(true)
      const res = await api.get('/bank-accounts/', {
        params: {
          page,
          per_page: pageSize
        }
      })
      
      // ข้อมูลจาก API response ที่มี pagination
      const responseData = res.data
      setData(responseData.items)
      
      // อัปเดต pagination state
      setPagination(prev => ({
        ...prev,
        current: responseData.page,
        pageSize: responseData.per_page,
        total: responseData.total,
      }))
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลบัญชีธนาคารได้')
    } finally {
      setLoading(false)
    }
  }, [])


  useEffect(() => {
    fetchData(pagination.current, pagination.pageSize)
  }, [fetchData, pagination.current, pagination.pageSize])

  // Handler สำหรับ pagination
  const handleTableChange = (paginationInfo: any) => {
    const { current, pageSize } = paginationInfo
    fetchData(current, pageSize)
  }

  const columns: ColumnsType<BankAccount> = [
    { 
      title: 'เลขที่หนังสือ', 
      dataIndex: 'document_number', 
      key: 'document_number',
      align: 'center',
      ...getColumnSearchProps('document_number'),
      render: (text: string) => (
        <span style={{ color: '#1890ff', fontWeight: 'bold', cursor: 'pointer' }}>
          {text}
        </span>
      )
    },
    { 
      title: 'ลงวันที่', 
      dataIndex: 'document_date', 
      key: 'document_date',
      align: 'center',
      ...getColumnSearchProps('document_date'),
      render: (date: string) => {
        if (!date) return '-'
        
        const thaiMonths = [
          'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
          'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
        ]
        
        const dayjsDate = dayjs(date)
        const day = dayjsDate.date()
        const month = thaiMonths[dayjsDate.month()]
        const year = (dayjsDate.year() + 543).toString().slice(-2) // แปลงเป็น พ.ศ. และย่อเป็น 2 หลัก
        
        return `${day} ${month} ${year}`
      }
    },
    { 
      title: 'ธนาคาร', 
      dataIndex: 'bank_name', 
      key: 'bank_name',
      align: 'center',
      ...getColumnSearchProps('bank_name')
    },
    { 
      title: 'เลขที่บัญชี', 
      dataIndex: 'account_number', 
      key: 'account_number',
      align: 'center',
      ...getColumnSearchProps('account_number')
    },
    { 
      title: 'ชื่อบัญชี', 
      dataIndex: 'account_name', 
      key: 'account_name',
      align: 'center',
      ...getColumnSearchProps('account_name')
    },
    { 
      title: 'สถานะ', 
      dataIndex: 'reply_status', 
      key: 'reply_status',
      align: 'center',
      filters: [
        { text: 'ตอบกลับแล้ว', value: true },
        { text: 'ยังไม่ตอบกลับ', value: false },
      ],
      onFilter: (value: string | number | boolean, record: BankAccount) => {
        return record.reply_status === value
      },
      render: (_value: unknown, record: BankAccount) => renderReplyStatus(record)
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
        pagination={pagination}
        onChange={handleTableChange}
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
            {renderReplyStatus(selected)}
          </Space>
        ) : null}
      >
        {selected && (
          <Tabs
            items={[
              {
                key: 'account',
                label: 'ข้อมูลบัญชี',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="เลขที่หนังสือ">{selected.document_number}</Descriptions.Item>
                    <Descriptions.Item label="ลงวันที่">
                      {selected.document_date ? formatThaiDate(selected.document_date) : '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="ธนาคาร">{selected.bank_name}</Descriptions.Item>
                    <Descriptions.Item label="เลขที่บัญชี">{selected.account_number}</Descriptions.Item>
                    <Descriptions.Item label="ชื่อบัญชี">{selected.account_name}</Descriptions.Item>
                    <Descriptions.Item label="ช่วงเวลาที่ขอข้อมูล">{selected.time_period || '-'}</Descriptions.Item>
                  </Descriptions>
                ),
              },
              {
                key: 'case',
                label: 'ผู้เสียหาย/คดี',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="ผู้ร้องทุกข์/ผู้เสียหาย">
                      {selected.criminal_case?.complainant || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="เลขที่คดี">
                      {selected.criminal_case?.case_number || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="เคสไอดี">
                      {selected.criminal_case?.case_id || selected.case_id || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="จำนวนความเสียหาย">
                      {selected.criminal_case?.damage_amount ? `${selected.criminal_case.damage_amount} บาท` : '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="วันนัดส่ง">{selected.delivery_date || '-'}</Descriptions.Item>
                  </Descriptions>
                ),
              },
            ]}
          />
        )}
      </Drawer>
    </div>
  )
}