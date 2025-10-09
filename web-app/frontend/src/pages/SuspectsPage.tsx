import { useEffect, useState, useCallback } from 'react'
import { Descriptions, Drawer, Table, Tabs, message, Tag, Divider, Typography } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'
import dayjs from 'dayjs'

const { Title } = Typography

interface CriminalCase {
  id: number
  case_id?: string
  case_number?: string
  victim_name?: string
  complainant?: string
  damage_amount?: string
}

interface Suspect {
  id: number
  document_number?: string
  document_date?: string
  suspect_name: string
  appointment_date?: string
  appointment_date_thai?: string
  status: string
  reply_status?: boolean
  suspect_id_card?: string
  suspect_address?: string
  police_station?: string
  police_province?: string
  police_address?: string
  victim_name?: string
  case_id?: string
  notes?: string
  criminal_case?: CriminalCase
}

export default function SuspectsPage() {
  const [data, setData] = useState<Suspect[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<Suspect | null>(null)

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

  // ฟังก์ชันคำนวณจำนวนวันที่ส่งไปแล้ว (ใช้ document_date)
  const calculateDaysSinceDocument = (documentDate: string | undefined): number => {
    if (!documentDate) return 0
    const docDate = dayjs(documentDate)
    const today = dayjs()
    return today.diff(docDate, 'day')
  }

  // ฟังก์ชันแสดงสถานะตอบกลับ
  const renderReplyStatus = (record: Suspect) => {
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

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      const res = await api.get<Suspect[]>('/suspects/')
      setData(res.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลหมายเรียกได้')
    } finally {
      setLoading(false)
    }
  }, [])


  useEffect(() => {
    fetchData()
  }, [fetchData])

  const columns: ColumnsType<Suspect> = [
    { 
      title: 'เลขที่หนังสือ', 
      dataIndex: 'document_number', 
      key: 'document_number',
      align: 'center',
      render: (value: string) => (
        <span style={{ color: '#1890ff', fontWeight: 'bold', cursor: 'pointer' }}>
          {value}
        </span>
      )
    },
    { 
      title: 'ลงวันที่', 
      dataIndex: 'document_date', 
      key: 'document_date',
      align: 'center',
      render: (value: string) => formatThaiDate(value)
    },
    { 
      title: 'ชื่อ-นามสกุล', 
      dataIndex: 'suspect_name', 
      key: 'suspect_name',
      align: 'left'
    },
    { 
      title: 'ที่อยู่ ผตห.', 
      dataIndex: 'suspect_address', 
      key: 'suspect_address',
      align: 'left'
    },
    { 
      title: 'พื้นที่ สภ./สน.', 
      dataIndex: 'police_station', 
      key: 'police_station',
      align: 'center'
    },
    { 
      title: 'สถานะ', 
      dataIndex: 'reply_status', 
      key: 'reply_status',
      align: 'center',
      render: (_value: unknown, record: Suspect) => renderReplyStatus(record)
    },
  ]

  return (
    <div>
      <h1>จัดการหมายเรียกผู้ต้องหา</h1>
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
        title={selected ? `รายละเอียดหมายเรียก: ${selected.document_number || '-'}` : 'รายละเอียด'}
        placement="right"
        width={520}
        onClose={() => setOpen(false)}
        open={open}
        extra={selected ? renderReplyStatus(selected) : null}
      >
        {selected && (
          <Tabs
            items={[
              {
                key: 'case',
                label: 'ข้อมูลคดี',
                children: (
                  <div>
                    {/* ส่วนข้อมูลผู้ต้องหา */}
                    <Title level={5} style={{ marginBottom: 16, color: '#1890ff' }}>
                      ข้อมูลผู้ต้องหา
                    </Title>
                    <Descriptions column={1} bordered size="small" style={{ marginBottom: 24 }}>
                      <Descriptions.Item label="ชื่อผู้ต้องหา">{selected.suspect_name}</Descriptions.Item>
                      <Descriptions.Item label="เลขบัตรประชาชน">{selected.suspect_id_card || '-'}</Descriptions.Item>
                      <Descriptions.Item label="ที่อยู่">{selected.suspect_address || '-'}</Descriptions.Item>
                      <Descriptions.Item label="วันที่นัดหมาย">
                        {selected.appointment_date ? formatThaiDate(selected.appointment_date) : '-'}
                      </Descriptions.Item>
                    </Descriptions>

                    <Divider />

                    {/* ส่วนข้อมูลผู้เสียหาย/คดี */}
                    <Title level={5} style={{ marginBottom: 16, color: '#52c41a' }}>
                      ข้อมูลผู้เสียหาย/คดี
                    </Title>
                    <Descriptions column={1} bordered size="small">
                      <Descriptions.Item label="ผู้ร้องทุกข์/ผู้เสียหาย">
                        {selected.criminal_case?.complainant || '-'}
                      </Descriptions.Item>
                      <Descriptions.Item label="เลขเคสไอดี">
                        {selected.criminal_case?.case_id || selected.case_id || '-'}
                      </Descriptions.Item>
                    </Descriptions>
                  </div>
                ),
              },
              {
                key: 'police',
                label: 'หน่วยรับผิดชอบ',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="สภ.">{selected.police_station || '-'}</Descriptions.Item>
                    <Descriptions.Item label="จังหวัด">{selected.police_province || '-'}</Descriptions.Item>
                    <Descriptions.Item label="ที่อยู่ สภ.">{selected.police_address || '-'}</Descriptions.Item>
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