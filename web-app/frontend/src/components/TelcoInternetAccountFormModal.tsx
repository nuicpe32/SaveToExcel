import { useEffect, useState } from 'react'
import { Modal, Form, Input, DatePicker, Select, Switch, Row, Col, message, TimePicker } from 'antd'
import dayjs from 'dayjs'
import 'dayjs/locale/th'
import api from '../services/api'

const { TextArea } = Input
const { Option } = Select

interface TelcoInternetAccountFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function TelcoInternetAccountFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: TelcoInternetAccountFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord
  const [providers, setProviders] = useState<any[]>([])
  const [loadingProviders, setLoadingProviders] = useState(false)

  // โหลดรายชื่อผู้ให้บริการ
  useEffect(() => {
    const fetchProviders = async () => {
      try {
        setLoadingProviders(true)
        const response = await api.get('/telco-internet/')
        setProviders(response.data || [])
      } catch (error: any) {
        console.error('Error fetching telco internet providers:', error)
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
          datetime_used: editingRecord.datetime_used
            ? dayjs(editingRecord.datetime_used)
            : null,
        })
      } else {
        // เพิ่มใหม่ - reset form
        form.resetFields()
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

      // แปลง dates และ datetime เป็น ISO string
      const payload = {
        ...values,
        criminal_case_id: criminalCaseId,
        document_date: values.document_date
          ? values.document_date.format('YYYY-MM-DD')
          : null,
        delivery_date: values.delivery_date
          ? values.delivery_date.format('YYYY-MM-DD')
          : null,
        datetime_used: values.datetime_used
          ? values.datetime_used.toISOString()
          : null,
      }

      if (isEdit) {
        await api.put(`/telco-internet-accounts/${editingRecord.id}`, payload)
        message.success('แก้ไข IP Address สำเร็จ')
      } else {
        await api.post('/telco-internet-accounts/', payload)
        message.success('เพิ่ม IP Address สำเร็จ')
      }

      form.resetFields()
      onClose(true)
    } catch (err: any) {
      if (err.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        message.error(
          isEdit ? 'ไม่สามารถแก้ไข IP Address ได้' : 'ไม่สามารถเพิ่ม IP Address ได้'
        )
      }
    }
  }

  const handleCancel = () => {
    form.resetFields()
    onClose(false)
  }

  return (
    <Modal
      title={isEdit ? 'แก้ไข IP Address' : 'เพิ่มข้อมูล IP Address'}
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

          {/* ข้อมูล IP Address */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูล IP Address (บังคับ)
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
              label="IP Address"
              name="ip_address"
              rules={[{ required: true, message: 'กรุณากรอก IP Address' }]}
            >
              <Input placeholder="192.168.1.1" />
            </Form.Item>
          </Col>

          {/* วันเวลาที่ใช้งาน */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              วันเวลาที่ใช้งาน
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item
              label="วันที่"
              name="datetime_used"
            >
              <DatePicker
                style={{ width: '100%' }}
                format="DD/MM/YYYY HH:mm"
                showTime={{ format: 'HH:mm' }}
                placeholder="เลือกวันที่และเวลา"
              />
            </Form.Item>
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

