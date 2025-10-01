import React, { useState, useEffect } from 'react'
import { Form, Input, DatePicker, Select, Button, Card, message, Row, Col } from 'antd'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import dayjs from 'dayjs'

const { Option } = Select

interface CriminalCaseForm {
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  complaint_date: string
  case_type?: string
}

interface CaseTypesResponse {
  case_types: string[]
}

const AddCriminalCasePage: React.FC = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [caseTypes, setCaseTypes] = useState<string[]>([])
  const navigate = useNavigate()

  const statusOptions = [
    { value: 'ระหว่างสอบสวน', label: 'ระหว่างสอบสวน' },
    { value: 'ส่งอัยการ', label: 'ส่งอัยการ' },
    { value: 'ส่งศาล', label: 'ส่งศาล' },
    { value: 'เสร็จสิ้น', label: 'เสร็จสิ้น' },
    { value: 'จำหน่าย', label: 'จำหน่าย' }
  ]

  useEffect(() => {
    const fetchCaseTypes = async () => {
      try {
        const response = await api.get<CaseTypesResponse>('/case-types')
        setCaseTypes(response.data.case_types)
      } catch (error) {
        console.error('Error fetching case types:', error)
        message.error('ไม่สามารถโหลดรายการประเภทคดีได้')
      }
    }

    fetchCaseTypes()
  }, [])

  const onFinish = async (values: CriminalCaseForm) => {
    try {
      setLoading(true)

      // Format date for API
      const formattedValues = {
        ...values,
        // Remove empty case_number to trigger auto-generation
        case_number: values.case_number?.trim() || undefined,
        complaint_date: values.complaint_date ? dayjs(values.complaint_date).format('YYYY-MM-DD') : undefined
      }

      const response = await api.post('/criminal-cases/', formattedValues)

      // Show success message with generated case number
      if (response.data.case_number) {
        message.success(`เพิ่มข้อมูลคดีอาญาสำเร็จ - เลขที่คดี: ${response.data.case_number}`)
      } else {
        message.success('เพิ่มข้อมูลคดีอาญาสำเร็จ')
      }

      // Use setTimeout to ensure message is shown before navigation
      setTimeout(() => {
        navigate('/', { replace: true })
      }, 800)
    } catch (error: any) {
      console.error('Error creating criminal case:', error)
      if (error.response?.data?.detail) {
        message.error(error.response.data.detail)
      } else {
        message.error('เกิดข้อผิดพลาดในการเพิ่มข้อมูลคดีอาญา')
      }
      setLoading(false)
    }
  }

  const onCancel = () => {
    navigate('/', { replace: true })
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card title="เพิ่มข้อมูลคดีอาญาในความรับผิดชอบ" style={{ maxWidth: 800, margin: '0 auto' }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            status: 'ระหว่างสอบสวน'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="เลขที่คดี (Auto-generate)"
                name="case_number"
                help="เว้นว่างไว้เพื่อสร้างเลขที่คดีอัตโนมัติ หรือระบุเอง เช่น 1385/2568"
              >
                <Input placeholder="เว้นว่างเพื่อสร้างอัตโนมัติ" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="CaseID"
                name="case_id"
              >
                <Input placeholder="เช่น 1) นาย โสภณ พรหมแก้ว" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="สถานะคดี"
                name="status"
                rules={[{ required: true, message: 'กรุณาเลือกสถานะคดี' }]}
              >
                <Select placeholder="เลือกสถานะคดี">
                  {statusOptions.map(option => (
                    <Option key={option.value} value={option.value}>
                      {option.label}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="ประเภทคดี"
                name="case_type"
              >
                <Select placeholder="เลือกประเภทคดี" allowClear>
                  {caseTypes.map(caseType => (
                    <Option key={caseType} value={caseType}>
                      {caseType}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            label="ผู้ร้องทุกข์"
            name="complainant"
            rules={[{ required: true, message: 'กรุณาระบุชื่อผู้ร้องทุกข์' }]}
          >
            <Input placeholder="เช่น นาย โสภณ พรหมแก้ว" />
          </Form.Item>

          <Form.Item
            label="วันที่/เวลา รับคำร้องทุกข์"
            name="complaint_date"
            rules={[{ required: true, message: 'กรุณาเลือกวันที่รับคำร้องทุกข์' }]}
          >
            <DatePicker 
              style={{ width: '100%' }} 
              format="YYYY-MM-DD"
              placeholder="เลือกวันที่รับคำร้องทุกข์"
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Button onClick={onCancel} style={{ marginRight: 8 }}>
              ยกเลิก
            </Button>
            <Button type="primary" htmlType="submit" loading={loading}>
              บันทึก
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default AddCriminalCasePage
