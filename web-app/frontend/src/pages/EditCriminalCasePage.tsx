import React, { useState, useEffect } from 'react'
import { Form, Input, DatePicker, Select, Button, Card, message, Row, Col, Spin } from 'antd'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../services/api'
import dayjs from 'dayjs'

const { Option } = Select

interface CriminalCase {
  id: number
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  complaint_date: string
  case_type?: string
  court_name?: string
  damage_amount?: string
}

interface CriminalCaseForm {
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  complaint_date: string
  case_type?: string
  court_name?: string
  damage_amount?: string
}

interface CaseTypesResponse {
  case_types: string[]
}

interface Court {
  id: number
  court_name: string
  court_type: string
  region: string
  province: string
}

const EditCriminalCasePage: React.FC = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [criminalCase, setCriminalCase] = useState<CriminalCase | null>(null)
  const [caseTypes, setCaseTypes] = useState<string[]>([])
  const [courts, setCourts] = useState<Court[]>([])
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()

  const statusOptions = [
    { value: 'ระหว่างสอบสวน', label: 'ระหว่างสอบสวน' },
    { value: 'ส่งอัยการ', label: 'ส่งอัยการ' },
    { value: 'ส่งศาล', label: 'ส่งศาล' },
    { value: 'เสร็จสิ้น', label: 'เสร็จสิ้น' },
    { value: 'จำหน่าย', label: 'จำหน่าย' }
  ]

  useEffect(() => {
    const fetchCriminalCase = async () => {
      try {
        setFetching(true)
        const response = await api.get<CriminalCase>(`/criminal-cases/${id}`)
        setCriminalCase(response.data)
        
        // Fetch case types
        const caseTypesResponse = await api.get<CaseTypesResponse>('/case-types')
        setCaseTypes(caseTypesResponse.data.case_types)

        // Fetch courts
        const courtsResponse = await api.get('/courts/', {
          params: { limit: 300 }
        })
        setCourts(courtsResponse.data)

        // Set form values
        form.setFieldsValue({
          case_number: response.data.case_number,
          case_id: response.data.case_id,
          status: response.data.status,
          complainant: response.data.complainant,
          case_type: response.data.case_type,
          court_name: response.data.court_name,
          damage_amount: response.data.damage_amount,
          complaint_date: response.data.complaint_date ? dayjs(response.data.complaint_date) : undefined
        })
      } catch (error: any) {
        console.error('Error fetching criminal case:', error)
        message.error('ไม่สามารถดึงข้อมูลคดีอาญาได้')
        navigate('/', { replace: true })
      } finally {
        setFetching(false)
      }
    }

    if (id) {
      fetchCriminalCase()
    }
  }, [id, form, navigate])

  const onFinish = async (values: CriminalCaseForm) => {
    try {
      setLoading(true)

      // Validate that either case_number or case_id is provided
      if (!values.case_number && !values.case_id) {
        message.error('กรุณาระบุเลขที่คดีหรือ CaseID อย่างใดอย่างหนึ่ง')
        setLoading(false)
        return
      }

      // Format date for API
      const formattedValues = {
        ...values,
        complaint_date: values.complaint_date ? dayjs(values.complaint_date).format('YYYY-MM-DD') : undefined
      }

      await api.put(`/criminal-cases/${id}`, formattedValues)
      message.success('แก้ไขข้อมูลคดีอาญาสำเร็จ')

      // Use setTimeout to ensure message is shown before navigation
      setTimeout(() => {
        navigate('/', { replace: true })
      }, 500)
    } catch (error: any) {
      console.error('Error updating criminal case:', error)
      if (error.response?.data?.detail) {
        message.error(error.response.data.detail)
      } else {
        message.error('เกิดข้อผิดพลาดในการแก้ไขข้อมูลคดีอาญา')
      }
      setLoading(false)
    }
  }

  const onCancel = () => {
    navigate('/', { replace: true })
  }

  if (fetching) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Spin size="large" />
        <p>กำลังโหลดข้อมูล...</p>
      </div>
    )
  }

  if (!criminalCase) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <p>ไม่พบข้อมูลคดีอาญา</p>
        <Button onClick={() => navigate('/', { replace: true })}>กลับไปหน้าหลัก</Button>
      </div>
    )
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card title={`แก้ไขข้อมูลคดีอาญา - ${criminalCase.case_number || criminalCase.case_id}`} style={{ maxWidth: 800, margin: '0 auto' }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="เลขที่คดี"
                name="case_number"
                rules={[
                  {
                    validator: (_, value) => {
                      const caseId = form.getFieldValue('case_id')
                      if (!value && !caseId) {
                        return Promise.reject('กรุณาระบุเลขที่คดีหรือ CaseID อย่างใดอย่างหนึ่ง')
                      }
                      return Promise.resolve()
                    }
                  }
                ]}
              >
                <Input placeholder="เช่น 1385/2568" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="CaseID"
                name="case_id"
                rules={[
                  {
                    validator: (_, value) => {
                      const caseNumber = form.getFieldValue('case_number')
                      if (!value && !caseNumber) {
                        return Promise.reject('กรุณาระบุเลขที่คดีหรือ CaseID อย่างใดอย่างหนึ่ง')
                      }
                      return Promise.resolve()
                    }
                  }
                ]}
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

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="เขตอำนาจศาล"
                name="court_name"
              >
                <Select
                  placeholder="เลือกศาล"
                  showSearch
                  allowClear
                  optionFilterProp="children"
                  filterOption={(input, option) => {
                    const children = option?.children as any
                    if (typeof children === 'string') {
                      return children.toLowerCase().includes(input.toLowerCase())
                    }
                    if (Array.isArray(children)) {
                      return children.join('').toLowerCase().includes(input.toLowerCase())
                    }
                    return false
                  }}
                >
                  {courts.map(court => (
                    <Option key={court.id} value={court.court_name}>
                      {court.court_name} ({court.province})
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="ความเสียหาย (บาท)"
                name="damage_amount"
              >
                <Input placeholder="เช่น 500000" />
              </Form.Item>
            </Col>
          </Row>

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

export default EditCriminalCasePage
