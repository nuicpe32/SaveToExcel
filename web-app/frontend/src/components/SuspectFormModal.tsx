import { useEffect } from 'react'
import { Modal, Form, Input, DatePicker, Select, Switch, Row, Col, message } from 'antd'
import dayjs from 'dayjs'
import api from '../services/api'

const { TextArea } = Input
const { Option } = Select

interface SuspectFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function SuspectFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: SuspectFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord

  useEffect(() => {
    if (visible) {
      if (editingRecord) {
        // แก้ไข - ใส่ค่าเดิม
        form.setFieldsValue({
          ...editingRecord,
          document_date: editingRecord.document_date
            ? dayjs(editingRecord.document_date)
            : null,
          appointment_date: editingRecord.appointment_date
            ? dayjs(editingRecord.appointment_date)
            : null,
        })
      } else {
        // เพิ่มใหม่ - reset form
        form.resetFields()
        form.setFieldsValue({
          criminal_case_id: criminalCaseId,
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
        appointment_date: values.appointment_date
          ? values.appointment_date.format('YYYY-MM-DD')
          : null,
      }

      if (isEdit) {
        await api.put(`/suspects/${editingRecord.id}`, payload)
        message.success('แก้ไขผู้ต้องหาสำเร็จ')
      } else {
        await api.post('/suspects/', payload)
        message.success('เพิ่มผู้ต้องหาสำเร็จ')
      }

      form.resetFields()
      onClose(true)
    } catch (err: any) {
      if (err.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        message.error(
          isEdit ? 'ไม่สามารถแก้ไขผู้ต้องหาได้' : 'ไม่สามารถเพิ่มผู้ต้องหาได้'
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
      title={isEdit ? 'แก้ไขผู้ต้องหา' : 'เพิ่มผู้ต้องหา'}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      width={800}
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
              label="เลขที่เอกสาร"
              name="document_number"
              tooltip="ระบบจะสร้างอัตโนมัติถ้าไม่ระบุ"
            >
              <Input placeholder="เช่น SP-2568-0001" />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="วันที่เอกสาร" name="document_date">
              <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
            </Form.Item>
          </Col>

          {/* ข้อมูลผู้ต้องหา */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลผู้ต้องหา (บังคับ)
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item
              label="ชื่อผู้ต้องหา"
              name="suspect_name"
              rules={[{ required: true, message: 'กรุณาระบุชื่อผู้ต้องหา' }]}
            >
              <Input placeholder="ชื่อ-นามสกุล" />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="เลขบัตรประชาชน"
              name="suspect_id_card"
              rules={[
                {
                  pattern: /^[0-9]{13}$/,
                  message: 'เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก',
                },
              ]}
            >
              <Input placeholder="1234567890123" maxLength={13} />
            </Form.Item>
          </Col>

          <Col span={24}>
            <Form.Item label="ที่อยู่ผู้ต้องหา" name="suspect_address">
              <TextArea
                rows={3}
                placeholder="บ้านเลขที่ ถนน ตำบล อำเภอ จังหวัด รหัสไปรษณีย์"
              />
            </Form.Item>
          </Col>

          {/* ข้อมูลสถานีตำรวจ */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลสถานีตำรวจ
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item label="สถานีตำรวจ" name="police_station">
              <Input placeholder="เช่น สภ.ลุมพินี" />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="จังหวัด" name="police_province">
              <Input placeholder="เช่น กรุงเทพมหานคร" />
            </Form.Item>
          </Col>

          <Col span={24}>
            <Form.Item label="ที่อยู่สถานีตำรวจ" name="police_address">
              <TextArea rows={2} placeholder="ที่อยู่สถานีตำรวจ" />
            </Form.Item>
          </Col>

          {/* ประเภทคดี */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลคดี
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item label="ประเภทคดี" name="case_type">
              <Select placeholder="เลือกประเภทคดี">
                <Option value="ฉ้อโกง">ฉ้อโกง</Option>
                <Option value="โกงรายได้">โกงรายได้</Option>
                <Option value="ยักยอกทรัพย์">ยักยอกทรัพย์</Option>
                <Option value="ฟอกเงิน">ฟอกเงิน</Option>
                <Option value="อื่นๆ">อื่นๆ</Option>
              </Select>
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="มูลค่าความเสียหาย" name="damage_amount">
              <Input placeholder="จำนวนเงิน (บาท)" />
            </Form.Item>
          </Col>

          {/* วันนัดหมาย */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              การนัดหมาย
            </h4>
          </Col>

          <Col span={12}>
            <Form.Item label="วันนัดหมาย" name="appointment_date">
              <DatePicker
                style={{ width: '100%' }}
                format="DD/MM/YYYY"
                placeholder="เลือกวันนัดหมาย"
              />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="เวลานัดหมาย" name="appointment_time">
              <Input placeholder="เช่น 09:00" />
            </Form.Item>
          </Col>

          {/* สถานะ */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              สถานะ
            </h4>
          </Col>

          <Col span={8}>
            <Form.Item
              label="สถานะมาตามนัด"
              name="reply_status"
              valuePropName="checked"
            >
              <Switch checkedChildren="มาแล้ว" unCheckedChildren="ยังไม่มา" />
            </Form.Item>
          </Col>

          <Col span={8}>
            <Form.Item label="สถานะ" name="status">
              <Select>
                <Option value="pending">รอดำเนินการ</Option>
                <Option value="summoned">ออกหมายเรียกแล้ว</Option>
                <Option value="appeared">มาตามนัด</Option>
                <Option value="not_appeared">ไม่มาตามนัด</Option>
                <Option value="completed">เสร็จสิ้น</Option>
              </Select>
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
