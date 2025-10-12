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

interface NonBankAccountFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function NonBankAccountFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: NonBankAccountFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord && !editingRecord._is_new_from_cfr
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null)
  const isFromCfr = !!editingRecord && editingRecord._is_new_from_cfr
  const [nonBanks, setNonBanks] = useState<any[]>([])

  // ดึงรายชื่อผู้ให้บริการ
  useEffect(() => {
    const fetchNonBanks = async () => {
      try {
        const response = await api.get('/non-banks/')
        setNonBanks(response.data)
      } catch (error) {
        console.error('Error fetching non-banks:', error)
      }
    }
    if (visible) {
      fetchNonBanks()
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
        
        // ถ้ามีข้อมูล date range จาก CFR
        if (editingRecord._date_range_start && editingRecord._date_range_end) {
          const dateRangeValue: [dayjs.Dayjs, dayjs.Dayjs] = [
            editingRecord._date_range_start,
            editingRecord._date_range_end
          ]
          setDateRange(dateRangeValue)
        } else {
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
        await api.put(`/non-bank-accounts/${editingRecord.id}`, payload)
        message.success('แก้ไขบัญชีผู้ให้บริการสำเร็จ')
      } else {
        await api.post('/non-bank-accounts/', payload)
        message.success('เพิ่มบัญชีผู้ให้บริการสำเร็จ')
      }

      form.resetFields()
      onClose(true)
    } catch (err: any) {
      if (err.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        message.error(
          isEdit ? 'ไม่สามารถแก้ไขบัญชีผู้ให้บริการได้' : 'ไม่สามารถเพิ่มบัญชีผู้ให้บริการได้'
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
      title={isEdit ? 'แก้ไขบัญชีผู้ให้บริการ' : 'เพิ่มบัญชีผู้ให้บริการ'}
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
              ข้อมูลผู้ให้บริการ (บังคับ)
            </h4>
          </Col>

          <Col span={24}>
            <Form.Item
              label="ชื่อผู้ให้บริการ"
              name="provider_name"
              rules={[{ required: true, message: 'กรุณาเลือกผู้ให้บริการ' }]}
            >
              <Select
                placeholder="เลือกผู้ให้บริการ"
                showSearch
                filterOption={(input, option) =>
                  (option?.children?.toString() || '')
                    .toLowerCase()
                    .includes(input.toLowerCase())
                }
              >
                {nonBanks.map((nonBank) => (
                  <Option key={nonBank.id} value={nonBank.company_name}>
                    {nonBank.company_name}
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
              📍 หมายเหตุ: ที่อยู่จะดึงจากข้อมูลสำนักงานของผู้ให้บริการโดยอัตโนมัติ
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
