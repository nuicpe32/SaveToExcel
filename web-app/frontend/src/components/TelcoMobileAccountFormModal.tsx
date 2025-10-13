import { useEffect, useState } from 'react'
import { Modal, Form, Input, DatePicker, Select, Switch, Row, Col, message } from 'antd'
import dayjs from 'dayjs'
import 'dayjs/locale/th'
import api from '../services/api'

const { TextArea } = Input
const { Option } = Select
const { RangePicker } = DatePicker

// ฟังก์ชันแปลงเดือนเป็นภาษาไทยแบบย่อ
const formatThaiMonth = (month: number): string => {
  const thaiMonths = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 
                      'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
  return thaiMonths[month]
}

// ฟังก์ชันแปลงเดือนไทยกลับเป็นตัวเลข
const parseThaiMonth = (monthStr: string): number => {
  const thaiMonths = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 
                      'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
  return thaiMonths.indexOf(monthStr)
}

// ฟังก์ชันแปลง date range เป็น text ไทย
const formatDateRangeToThai = (dates: [dayjs.Dayjs, dayjs.Dayjs] | null): string => {
  if (!dates || !dates[0] || !dates[1]) return ''
  
  const startDate = dates[0]
  const endDate = dates[1]
  
  // แปลงเป็น พ.ศ.
  const startDay = startDate.date()
  const startMonth = formatThaiMonth(startDate.month())
  const startYear = (startDate.year() + 543).toString().slice(-2) // เอา 2 หลักหลัง
  
  const endDay = endDate.date()
  const endMonth = formatThaiMonth(endDate.month())
  const endYear = (endDate.year() + 543).toString().slice(-2)
  
  return `${startDay} ${startMonth} ${startYear} - ${endDay} ${endMonth} ${endYear}`
}

// ฟังก์ชันแปลง text ไทยกลับเป็น date range objects
const parseThaiDateRange = (thaiDateRange: string): [dayjs.Dayjs, dayjs.Dayjs] | null => {
  if (!thaiDateRange) return null
  
  try {
    const parts = thaiDateRange.split(' - ')
    if (parts.length !== 2) return null
    
    // Parse start date
    const startParts = parts[0].trim().split(' ')
    if (startParts.length !== 3) return null
    const startDay = parseInt(startParts[0])
    const startMonth = parseThaiMonth(startParts[1])
    const startYear = parseInt(startParts[2]) + 2500 - 543 // แปลง พ.ศ. 2 หลัก → ค.ศ. 4 หลัก
    
    // Parse end date
    const endParts = parts[1].trim().split(' ')
    if (endParts.length !== 3) return null
    const endDay = parseInt(endParts[0])
    const endMonth = parseThaiMonth(endParts[1])
    const endYear = parseInt(endParts[2]) + 2500 - 543 // แปลง พ.ศ. 2 หลัก → ค.ศ. 4 หลัก
    
    // ตรวจสอบว่าค่าที่ parse ได้ถูกต้อง
    if (startMonth === -1 || endMonth === -1) return null
    
    // สร้าง dayjs objects
    const startDate = dayjs().year(startYear).month(startMonth).date(startDay)
    const endDate = dayjs().year(endYear).month(endMonth).date(endDay)
    
    if (!startDate.isValid() || !endDate.isValid()) return null
    
    return [startDate, endDate]
  } catch (error) {
    console.error('Error parsing Thai date range:', error)
    return null
  }
}

interface TelcoMobileAccountFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function TelcoMobileAccountFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: TelcoMobileAccountFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null)
  const [providers, setProviders] = useState<any[]>([])
  const [loadingProviders, setLoadingProviders] = useState(false)

  // โหลดรายชื่อผู้ให้บริการ
  useEffect(() => {
    const fetchProviders = async () => {
      try {
        setLoadingProviders(true)
        console.log('🔍 Fetching telco mobile providers...')
        const response = await api.get('/telco-mobile/')
        console.log('✅ Telco mobile providers response:', response.data)
        setProviders(response.data || [])
        console.log('📋 Providers set:', response.data?.length || 0, 'items')
      } catch (error: any) {
        console.error('❌ Error fetching telco mobile providers:', error)
        console.error('❌ Error response:', error.response?.data)
        console.error('❌ Error status:', error.response?.status)
        message.error('ไม่สามารถดึงรายชื่อผู้ให้บริการได้')
      } finally {
        setLoadingProviders(false)
      }
    }

    if (visible) {
      fetchProviders()
    }
  }, [visible])

  useEffect(() => {
    if (visible) {
      if (editingRecord) {
        // แก้ไข - ใส่ค่าเดิม
        form.setFieldsValue({
          ...editingRecord,
          document_date: editingRecord.document_date
            ? dayjs(editingRecord.document_date)
            : null,
          delivery_date: editingRecord.delivery_date
            ? dayjs(editingRecord.delivery_date)
            : null,
        })
        
        // แปลง time_period (text) กลับเป็น date range objects
        if (editingRecord.time_period) {
          const parsedDateRange = parseThaiDateRange(editingRecord.time_period)
          if (parsedDateRange) {
            setDateRange(parsedDateRange)
          } else {
            setDateRange(null)
          }
        } else {
          setDateRange(null)
        }
      } else {
        // เพิ่มใหม่ - reset form
        form.resetFields()
        setDateRange(null)
        const today = dayjs()
        const deliveryDate = today.add(14, 'day')
        form.setFieldsValue({
          criminal_case_id: criminalCaseId,
          document_date: today,           // ลงวันที่ = วันนี้
          delivery_date: deliveryDate,     // กำหนดส่ง = วันนี้ + 14 วัน
          reply_status: false,
          status: 'pending',
        })
      }
    }
  }, [visible, editingRecord, criminalCaseId, form])

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()

      // แปลง dates เป็น string
      const payload = {
        ...values,
        criminal_case_id: criminalCaseId,
        document_date: values.document_date
          ? values.document_date.format('YYYY-MM-DD')
          : null,
        delivery_date: values.delivery_date
          ? values.delivery_date.format('YYYY-MM-DD')
          : null,
        // แปลง date range เป็น text ไทย
        time_period: dateRange ? formatDateRangeToThai(dateRange) : values.time_period,
      }

      if (isEdit) {
        await api.put(`/telco-mobile-accounts/${editingRecord.id}`, payload)
        message.success('แก้ไขหมายเลขโทรศัพท์สำเร็จ')
      } else {
        await api.post('/telco-mobile-accounts/', payload)
        message.success('เพิ่มหมายเลขโทรศัพท์สำเร็จ')
      }

      form.resetFields()
      onClose(true)
    } catch (err: any) {
      if (err.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        message.error(
          isEdit ? 'ไม่สามารถแก้ไขหมายเลขโทรศัพท์ได้' : 'ไม่สามารถเพิ่มหมายเลขโทรศัพท์ได้'
        )
      }
    }
  }

  const handleCancel = () => {
    form.resetFields()
    setDateRange(null)
    onClose(false)
  }

  return (
    <Modal
      title={isEdit ? 'แก้ไขหมายเลขโทรศัพท์' : 'เพิ่มข้อมูลหมายเลขโทรศัพท์'}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      width={900}
      okText={isEdit ? 'บันทึก' : 'เพิ่ม'}
      cancelText="ยกเลิก"
    >
      <Form form={form} layout="vertical">
        <Row gutter={16}>
          {/* ข้อมูลเอกสาร */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลเอกสาร
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item
              label="เลขที่หนังสือ"
              name="document_number"
            >
              <Input placeholder="ตช.0039.52/.." />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="ลงวันที่" name="document_date">
              <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
            </Form.Item>
          </Col>

          {/* ข้อมูลหมายเลขโทรศัพท์ */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลหมายเลขโทรศัพท์ (บังคับ)
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item
              label="ชื่อผู้ให้บริการ"
              name="provider_name"
              rules={[{ required: true, message: 'กรุณาเลือกผู้ให้บริการ' }]}
            >
              <Select
                showSearch
                placeholder="เลือกผู้ให้บริการ"
                loading={loadingProviders}
                filterOption={(input, option) =>
                  (option?.children as string)?.toLowerCase().includes(input.toLowerCase())
                }
              >
                {providers.map((provider) => (
                  <Option key={provider.id} value={provider.company_name_short}>
                    {provider.company_name_short}
                  </Option>
                ))}
              </Select>
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="หมายเลขโทรศัพท์"
              name="phone_number"
              rules={[{ required: true, message: 'กรุณากรอกหมายเลขโทรศัพท์' }]}
            >
              <Input placeholder="0812345678" />
            </Form.Item>
          </Col>

          {/* ช่วงเวลาที่ขอข้อมูล */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ช่วงเวลาที่ขอข้อมูล
            </h4>
          </Col>

          <Col span={24}>
            <Form.Item
              label="ช่วงเวลา"
              name="time_period_range"
            >
              <RangePicker
                style={{ width: '100%' }}
                format="DD/MM/YYYY"
                value={dateRange}
                onChange={(dates) => {
                  setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs] | null)
                }}
                placeholder={['วันที่เริ่มต้น', 'วันที่สิ้นสุด']}
              />
            </Form.Item>
            {dateRange && (
              <div style={{ marginTop: -16, marginBottom: 16, color: '#666', fontSize: '12px' }}>
                ช่วงเวลา: {formatDateRangeToThai(dateRange)}
              </div>
            )}
          </Col>

          {/* ข้อมูลการส่งเอกสาร */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลการส่งเอกสาร
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item label="กำหนดให้ส่งเอกสาร" name="delivery_date">
              <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="สถานะการตอบกลับ" name="reply_status" valuePropName="checked">
              <Switch checkedChildren="ตอบกลับแล้ว" unCheckedChildren="ยังไม่ตอบกลับ" />
            </Form.Item>
          </Col>

          {/* หมายเหตุ */}
          <Col span={24}>
            <Form.Item label="หมายเหตุ" name="notes">
              <TextArea rows={3} placeholder="หมายเหตุเพิ่มเติม..." />
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </Modal>
  )
}

