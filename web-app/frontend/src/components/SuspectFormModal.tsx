import { useEffect, useState } from 'react'
import { Modal, Form, Input, DatePicker, Switch, Row, Col, message, AutoComplete, Upload, Button } from 'antd'
import { UploadOutlined, FileTextOutlined, SearchOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import api from '../services/api'
import PoliceStationSearchModal from './PoliceStationSearchModal'

const { TextArea } = Input

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
  const [bankAccountNames, setBankAccountNames] = useState<string[]>([])
  const [uploading, setUploading] = useState(false)
  const [policeStationModalVisible, setPoliceStationModalVisible] = useState(false)
  const isEdit = !!editingRecord

  // ดึงข้อมูลชื่อเจ้าของบัญชีธนาคารจากคดีนี้
  const fetchBankAccountNames = async () => {
    try {
      const response = await api.get(`/criminal-cases/${criminalCaseId}/bank-accounts`)
      const accountNames = response.data
        .map((account: any) => account.account_name)
        .filter((name: string) => name && name.trim() !== '')
        .filter((name: string, index: number, arr: string[]) => arr.indexOf(name) === index) // remove duplicates
      setBankAccountNames(accountNames)
    } catch (error) {
      console.error('Error fetching bank account names:', error)
      setBankAccountNames([])
    }
  }

  // แกะข้อมูลจากไฟล์ PDF ทร.14
  const parsePDFData = async (file: File): Promise<{name: string, idCard: string, address: string, addressValid: boolean, message: string} | null> => {
    try {
      setUploading(true)
      
      // สร้าง FormData สำหรับส่งไฟล์
      const formData = new FormData()
      formData.append('file', file)
      
      // ส่งไฟล์ไปยัง backend เพื่อแกะข้อมูล
      const response = await api.post('/parse-pdf-thor14', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      
      if (response.data && response.data.success) {
        const data = response.data.data
        return {
          name: data?.name || '',
          idCard: data?.idCard || '',
          address: data?.address || '',
          addressValid: data?.addressValid !== false,
          message: response.data.message || 'แกะข้อมูลจากไฟล์ PDF สำเร็จ'
        }
      }
      
      return null
    } catch (error) {
      console.error('Error parsing PDF:', error)
      message.error('ไม่สามารถแกะข้อมูลจากไฟล์ PDF ได้')
      return null
    } finally {
      setUploading(false)
    }
  }

  // จัดการการอัปโหลดไฟล์ PDF
  const handlePDFUpload = async (file: File) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      message.error('กรุณาเลือกไฟล์ PDF เท่านั้น')
      return false
    }

    const pdfData = await parsePDFData(file)
    
    if (pdfData) {
      // เติมข้อมูลลงในฟอร์ม
      const formData = {
        suspect_name: pdfData.name,
        suspect_id_card: pdfData.idCard,
        // ถ้าที่อยู่ไม่ถูกต้อง ให้ปล่อยเป็นค่าว่าง
        suspect_address: pdfData.addressValid ? pdfData.address : ''
      }
      
      form.setFieldsValue(formData)
      
      // แสดงข้อความแจ้งเตือนตามสถานะ
      if (pdfData.addressValid) {
        message.success(pdfData.message)
      } else {
        message.warning(pdfData.message)
      }
    } else {
      message.warning('ไม่พบข้อมูลในไฟล์ PDF')
    }
    
    return false // ป้องกันการอัปโหลดไฟล์จริง
  }

  // จัดการการเลือกสถานีตำรวจ
  const handleSelectPoliceStation = (station: any) => {
    // กรอกข้อมูลสถานีตำรวจลงในฟอร์ม
    form.setFieldsValue({
      police_station_name: station.name,
      police_station_address: station.address,
    })
    
    message.success(`เลือกสถานีตำรวจ: ${station.name}`)
  }

  useEffect(() => {
    if (visible) {
      // ดึงข้อมูลชื่อเจ้าของบัญชีธนาคาร
      fetchBankAccountNames()
      
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
          document_date: dayjs(), // ตั้งค่าวันที่ปัจจุบัน
          appointment_time: '09:00 น.', // ตั้งค่าเวลานัดหมายเริ่มต้น
        })
      }
    }
  }, [visible, editingRecord, criminalCaseId, form])

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()

      // แปลง dates เป็น string และสร้างวันที่ไทย
      const formatThaiDate = (date: any) => {
        if (!date) return null;
        const thaiMonths = [
          'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
          'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ];
        const day = date.date();
        const month = thaiMonths[date.month()];
        const year = date.year() + 543; // แปลงเป็น พ.ศ.
        return `${day} ${month} ${year}`;
      };

      const payload = {
        ...values,
        criminal_case_id: criminalCaseId,
        status: 'pending', // ตั้งค่า default status
        document_date: values.document_date
          ? values.document_date.format('YYYY-MM-DD')
          : null,
        document_date_thai: formatThaiDate(values.document_date),
        appointment_date: values.appointment_date
          ? values.appointment_date.format('YYYY-MM-DD')
          : null,
        appointment_date_thai: formatThaiDate(values.appointment_date),
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
              label="เลขที่หนังสือ"
              name="document_number"
              tooltip="ระบบจะสร้างอัตโนมัติถ้าไม่ระบุ"
            >
              <Input placeholder="เช่น ตช. 0039.52/....." />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item label="ลงวันที่" name="document_date">
              <DatePicker 
                style={{ width: '100%' }} 
                format="DD/MM/YYYY" 
                defaultValue={dayjs()}
              />
            </Form.Item>
          </Col>

          {/* ข้อมูลผู้ต้องหา */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              ข้อมูลผู้ต้องหา (บังคับ)
            </h4>
          </Col>

          {/* Upload PDF ทร.14 */}
          <Col span={24}>
            <div style={{ marginBottom: 16, padding: 12, backgroundColor: '#f0f8ff', borderRadius: 6, border: '1px solid #d9d9d9' }}>
              <div style={{ marginBottom: 8, fontWeight: 'bold', color: '#1890ff' }}>
                <FileTextOutlined style={{ marginRight: 8 }} />
                อัปโหลดไฟล์ ทร.14 (PDF) เพื่อแกะข้อมูลอัตโนมัติ
              </div>
              <Upload
                accept=".pdf"
                beforeUpload={handlePDFUpload}
                showUploadList={false}
                disabled={uploading}
              >
                <Button 
                  icon={<UploadOutlined />} 
                  loading={uploading}
                  disabled={uploading}
                >
                  {uploading ? 'กำลังแกะข้อมูล...' : 'เลือกไฟล์ ทร.14 (PDF)'}
                </Button>
              </Upload>
              <div style={{ marginTop: 8, fontSize: 12, color: '#666' }}>
                ระบบจะแกะข้อมูล ชื่อ-นามสกุล, เลขบัตรประชาชน, และที่อยู่ จากไฟล์ PDF อัตโนมัติ
              </div>
            </div>
          </Col>

          <Col span={12}>
            <Form.Item
              label="ชื่อผู้ต้องหา"
              name="suspect_name"
              rules={[{ required: true, message: 'กรุณาระบุชื่อผู้ต้องหา' }]}
            >
              <AutoComplete
                placeholder="ชื่อ-นามสกุล หรือเลือกจากรายการ"
                options={bankAccountNames.map(name => ({ value: name }))}
                filterOption={(inputValue, option) =>
                  option?.value?.toLowerCase().includes(inputValue.toLowerCase()) ?? false
                }
                allowClear
              />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="เลขบัตรประชาชน/เลขที่หนังสือเดินทาง"
              name="suspect_id_card"
              rules={[
                {
                  pattern: /^[0-9]{13}$|^[A-Z]{2}[0-9]{7}$/,
                  message: 'กรุณากรอกเลขบัตรประชาชน 13 หลัก หรือเลขที่หนังสือเดินทาง',
                },
              ]}
            >
              <Input placeholder="1234567890123 หรือ A1234567" maxLength={13} />
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

          <Col span={24}>
            <div style={{ marginBottom: 16, textAlign: 'right' }}>
              <Button
                type="default"
                icon={<SearchOutlined />}
                onClick={() => setPoliceStationModalVisible(true)}
                disabled={!form.getFieldValue('suspect_address')?.trim()}
              >
                ค้นหาสถานีตำรวจ
              </Button>
            </div>
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
              <Input placeholder="เช่น 09:00" defaultValue="09:00 น." />
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
              label="สถานะผลหมายเรียก"
              name="reply_status"
              valuePropName="checked"
            >
              <Switch checkedChildren="ตอบกลับแล้ว" unCheckedChildren="ยังไม่ตอบกลับ" />
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

      {/* Modal ค้นหาสถานีตำรวจ */}
      <PoliceStationSearchModal
        visible={policeStationModalVisible}
        onCancel={() => setPoliceStationModalVisible(false)}
        onSelect={handleSelectPoliceStation}
        suspectAddress={form.getFieldValue('suspect_address') || ''}
      />
    </Modal>
  )
}
