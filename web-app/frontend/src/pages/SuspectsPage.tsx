import { useEffect, useState, useCallback } from 'react'
import { Button, Descriptions, Drawer, Space, Table, Tabs, message } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'

interface Suspect {
  id: number
  document_number?: string
  suspect_name: string
  appointment_date?: string
  appointment_date_thai?: string
  status: string
  suspect_id_card?: string
  suspect_address?: string
  police_station?: string
  police_province?: string
  police_address?: string
  victim_name?: string
  case_id?: string
  notes?: string
}

export default function SuspectsPage() {
  const [data, setData] = useState<Suspect[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<Suspect | null>(null)

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

  const downloadDocument = useCallback(async (record: Suspect) => {
    try {
      const res = await api.get(`/documents/suspect-summons/${record.id}`, {
        responseType: 'blob',
      })
      const blob = new Blob([res.data], { type: res.headers['content-type'] || 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `suspect_summons_${record.document_number}.docx`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      message.error('ดาวน์โหลดเอกสารไม่สำเร็จ')
    }
  }, [])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const columns: ColumnsType<Suspect> = [
    { title: 'เลขที่เอกสาร', dataIndex: 'document_number', key: 'document_number' },
    { title: 'ชื่อ-นามสกุล', dataIndex: 'suspect_name', key: 'suspect_name' },
    { title: 'วันนัดหมาย', dataIndex: 'appointment_date_thai', key: 'appointment_date_thai' },
    { title: 'สถานะ', dataIndex: 'status', key: 'status' },
    {
      title: 'การทำงาน',
      key: 'actions',
      render: (_value: unknown, record: Suspect) => (
        <Space>
          <Button onClick={() => downloadDocument(record)}>ดาวน์โหลดเอกสาร</Button>
        </Space>
      ),
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
                key: 'suspect',
                label: 'ข้อมูลผู้ต้องหา',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="ชื่อผู้ต้องหา">{selected.suspect_name}</Descriptions.Item>
                    <Descriptions.Item label="เลขบัตรประชาชน">{selected.suspect_id_card || '-'}</Descriptions.Item>
                    <Descriptions.Item label="ที่อยู่">{selected.suspect_address || '-'}</Descriptions.Item>
                  </Descriptions>
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
              {
                key: 'case',
                label: 'ข้อมูลคดี',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="ผู้เสียหาย">{selected.victim_name || '-'}</Descriptions.Item>
                    <Descriptions.Item label="เลขเคสไอดี">{selected.case_id || '-'}</Descriptions.Item>
                  </Descriptions>
                ),
              },
              {
                key: 'appointment',
                label: 'ใบนัดหมาย',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="วันที่นัด">{selected.appointment_date_thai || selected.appointment_date || '-'}</Descriptions.Item>
                    <Descriptions.Item label="สถานะ">{selected.status}</Descriptions.Item>
                    <Descriptions.Item label="เลขเอกสาร">{selected.document_number || '-'}</Descriptions.Item>
                  </Descriptions>
                ),
              },
              {
                key: 'notes',
                label: 'หมายเหตุ',
                children: (
                  <Descriptions column={1} bordered size="small">
                    <Descriptions.Item label="หมายเหตุ">{selected.notes || '-'}</Descriptions.Item>
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