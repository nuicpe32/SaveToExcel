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
    console.log('Parsing Thai date range:', thaiDateRange)
    
    // รูปแบบ: "4 ส.ค. 68 - 6 ส.ค. 68"
    const parts = thaiDateRange.split(' - ')
    console.log('Parts:', parts)
    if (parts.length !== 2) {
      console.log('Invalid format: parts length is not 2')
      return null
    }
    
    // Parse start date
    const startParts = parts[0].trim().split(' ')
    console.log('Start parts:', startParts)
    if (startParts.length !== 3) {
      console.log('Invalid start date format')
      return null
    }
    const startDay = parseInt(startParts[0])
    const startMonth = parseThaiMonth(startParts[1])
    const startYear = parseInt(startParts[2]) + 2500 - 543 // แปลง พ.ศ. 2 หลัก → ค.ศ. 4 หลัก
    console.log('Start date parsed:', { startDay, startMonth, startYear })
    
    // Parse end date
    const endParts = parts[1].trim().split(' ')
    console.log('End parts:', endParts)
    if (endParts.length !== 3) {
      console.log('Invalid end date format')
      return null
    }
    const endDay = parseInt(endParts[0])
    const endMonth = parseThaiMonth(endParts[1])
    const endYear = parseInt(endParts[2]) + 2500 - 543 // แปลง พ.ศ. 2 หลัก → ค.ศ. 4 หลัก
    console.log('End date parsed:', { endDay, endMonth, endYear })
    
    // ตรวจสอบว่าค่าที่ parse ได้ถูกต้อง
    if (startMonth === -1 || endMonth === -1) {
      console.log('Invalid month name')
      return null
    }
    
    // สร้าง dayjs objects
    const startDate = dayjs().year(startYear).month(startMonth).date(startDay)
    const endDate = dayjs().year(endYear).month(endMonth).date(endDay)
    console.log('Created dayjs objects:', { 
      startDate: startDate.format('YYYY-MM-DD'), 
      endDate: endDate.format('YYYY-MM-DD'),
      startValid: startDate.isValid(),
      endValid: endDate.isValid()
    })
    
    if (!startDate.isValid() || !endDate.isValid()) {
      console.log('Invalid dayjs objects')
      return null
    }
    
    console.log('Successfully parsed date range')
    return [startDate, endDate]
  } catch (error) {
    console.error('Error parsing Thai date range:', error)
    return null
  }
}

interface BankAccountFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

// รายชื่อธนาคารไทย
const THAI_BANKS = [
  'ธนาคารกรุงเทพ',
  'ธนาคารกสิกรไทย',
  'ธนาคารไทยพาณิชย์',
  'ธนาคารกรุงไทย',
  'ธนาคารกรุงศรีอยุธยา',
  'ธนาคารทหารไทยธนชาต',
  'ธนาคารเกียรตินาคินภัทร',
  'ธนาคารซีไอเอ็มบีไทย',
  'ธนาคารทิสโก้',
  'ธนาคารยูโอบี',
  'ธนาคารธนชาต',
  'ธนาคารแลนด์ แอนด์ เฮ้าส์',
  'ธนาคารไอซีบีซี (ไทย)',
  'ธนาคารพัฒนาวิสาหกิจขนาดกลางและขนาดย่อมแห่งประเทศไทย',
  'ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร',
  'ธนาคารออมสิน',
  'ธนาคารอาคารสงเคราะห์',
  'ธนาคารอิสลามแห่งประเทศไทย',
]

export default function BankAccountFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: BankAccountFormModalProps) {
  const [form] = Form.useForm()
  // ตรวจสอบว่าเป็นการแก้ไขจริงหรือเป็นการสร้างใหม่จาก CFR
  const isEdit = !!editingRecord && !editingRecord._is_new_from_cfr
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null)
  // ตรวจสอบว่ามาจาก CFR หรือไม่
  const isFromCfr = !!editingRecord && editingRecord._is_new_from_cfr

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
        
        // ถ้ามีข้อมูล date range จาก CFR
        if (editingRecord._date_range_start && editingRecord._date_range_end) {
          const dateRangeValue: [dayjs.Dayjs, dayjs.Dayjs] = [
            editingRecord._date_range_start,
            editingRecord._date_range_end
          ]
          setDateRange(dateRangeValue)
        } else if (editingRecord.time_period) {
          // แปลง time_period (text) กลับเป็น date range objects
          console.log('🔍 Attempting to parse time_period:', editingRecord.time_period)
          const parsedDateRange = parseThaiDateRange(editingRecord.time_period)
          console.log('📅 Parsed date range result:', parsedDateRange)
          if (parsedDateRange) {
            console.log('✅ Setting date range:', parsedDateRange)
            setDateRange(parsedDateRange)
          } else {
            console.log('❌ Failed to parse, setting null')
            setDateRange(null)
          }
        } else {
          console.log('ℹ️ No time_period found, setting null')
          setDateRange(null)
        }
      } else {
        // เพิ่มใหม่ - reset form
        form.resetFields()
        setDateRange(null) // reset date range
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
        await api.put(`/bank-accounts/${editingRecord.id}`, payload)
        message.success('แก้ไขบัญชีธนาคารสำเร็จ')
      } else {
        await api.post('/bank-accounts/', payload)
        message.success('เพิ่มบัญชีธนาคารสำเร็จ')
      }

      form.resetFields()
      onClose(true)
    } catch (err: any) {
      if (err.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        message.error(
          isEdit ? 'ไม่สามารถแก้ไขบัญชีธนาคารได้' : 'ไม่สามารถเพิ่มบัญชีธนาคารได้'
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
      title={isEdit ? 'แก้ไขบัญชีธนาคาร' : 'เพิ่มบัญชีธนาคาร'}
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

          {/* ข้อมูลธนาคาร */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลธนาคาร (บังคับ)
            </h4>
          </Col>

          <Col span={24}>
            <Form.Item
              label="ชื่อธนาคาร"
              name="bank_name"
              rules={[{ required: true, message: 'กรุณาเลือกธนาคาร' }]}
            >
              <Select
                placeholder="เลือกธนาคาร"
                showSearch
                filterOption={(input, option) =>
                  (option?.children?.toString() || '')
                    .toLowerCase()
                    .includes(input.toLowerCase())
                }
              >
                {THAI_BANKS.map((bank) => (
                  <Option key={bank} value={bank}>
                    {bank}
                  </Option>
                ))}
              </Select>
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="เลขที่บัญชี"
              name="account_number"
              rules={[{ required: true, message: 'กรุณาระบุเลขที่บัญชี' }]}
            >
              <Input placeholder="เช่น 1234567890" />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="ชื่อบัญชี"
              name="account_name"
              rules={[{ required: true, message: 'กรุณาระบุชื่อบัญชี' }]}
            >
              <Input placeholder="ชื่อเจ้าของบัญชี" />
            </Form.Item>
          </Col>

          <Col span={24}>
            <Form.Item label="ช่วงเวลาที่ทำธุรกรรม">
              <RangePicker
                style={{ width: '100%' }}
                format="DD/MM/YYYY"
                placeholder={['วันที่เริ่มต้น', 'วันที่สิ้นสุด']}
                value={dateRange}
                onChange={(dates) => {
                  setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs] | null)
                  if (dates) {
                    const formattedText = formatDateRangeToThai(dates as [dayjs.Dayjs, dayjs.Dayjs])
                    form.setFieldsValue({ time_period: formattedText })
                  } else {
                    form.setFieldsValue({ time_period: '' })
                  }
                }}
              />
              <Form.Item name="time_period" noStyle>
                <Input type="hidden" />
              </Form.Item>
              {dateRange && (
                <div style={{ marginTop: 8, color: isFromCfr ? '#ff4d4f' : '#1890ff', fontSize: '13px', fontWeight: isFromCfr ? 'bold' : 'normal' }}>
                  จะบันทึกเป็น: {formatDateRangeToThai(dateRange)}
                  {isFromCfr && <span style={{ marginLeft: 8 }}>(ตามข้อมูลจาก CFR)</span>}
                </div>
              )}
            </Form.Item>
          </Col>

          <Col span={24}>
            <p style={{ marginTop: 8, color: '#888', fontSize: '13px' }}>
              📍 หมายเหตุ: ที่อยู่จะดึงจากข้อมูลสำนักงานใหญ่ของธนาคารโดยอัตโนมัติ
            </p>
          </Col>

          {/* ข้อมูลการส่งเอกสาร */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              การส่งเอกสาร
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item label="กำหนดให้ส่งเอกสาร" name="delivery_date">
              <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="สถานะตอบกลับ"
              name="reply_status"
              valuePropName="checked"
            >
              <Switch checkedChildren="ตอบแล้ว" unCheckedChildren="รอตอบกลับ" />
            </Form.Item>
          </Col>

          {/* หมายเหตุ */}
          <Col span={24}>
            <Form.Item label="หมายเหตุ" name="notes">
              <TextArea rows={3} placeholder="บันทึกข้อมูลเพิ่มเติม..." />
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </Modal>
  )
}
