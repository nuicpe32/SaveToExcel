import { Modal, Form, Input, Button, Space, Typography, Alert, Spin, Checkbox } from 'antd'
import { MailOutlined, FileTextOutlined, BankOutlined, PhoneOutlined, GlobalOutlined } from '@ant-design/icons'
import { useState } from 'react'

const { Text } = Typography

interface EmailConfirmationModalProps {
  visible: boolean
  onCancel: () => void
  onConfirm: (recipientEmail: string, freezeAccount: boolean) => Promise<void>
  accountType: 'non_bank' | 'payment_gateway' | 'telco_mobile' | 'telco_internet' | 'bank'
  providerName: string
  documentNumber: string
  defaultEmail?: string
  accountNumber?: string
  phoneNumber?: string
  ipAddress?: string
}

const EmailConfirmationModal: React.FC<EmailConfirmationModalProps> = ({
  visible,
  onCancel,
  onConfirm,
  accountType,
  providerName,
  documentNumber,
  defaultEmail,
  accountNumber,
  phoneNumber,
  ipAddress
}) => {
  const [form] = Form.useForm()
  const [sending, setSending] = useState(false)

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      setSending(true)
      await onConfirm(values.recipientEmail, values.freezeAccount || false)
      form.resetFields()
      setSending(false)
    } catch (error) {
      setSending(false)
      console.error('Email sending failed:', error)
    }
  }

  const getAccountTypeLabel = () => {
    switch (accountType) {
      case 'non_bank':
        return 'บริษัทนอกธนาคาร'
      case 'payment_gateway':
        return 'ผู้ให้บริการชำระเงิน'
      case 'telco_mobile':
        return 'ผู้ให้บริการโทรศัพท์'
      case 'telco_internet':
        return 'ผู้ให้บริการอินเทอร์เน็ต'
      case 'bank':
        return 'ธนาคาร'
      default:
        return ''
    }
  }

  const getAccountTypeIcon = () => {
    switch (accountType) {
      case 'non_bank':
      case 'payment_gateway':
      case 'bank':
        return <BankOutlined style={{ fontSize: 20, color: '#1890ff' }} />
      case 'telco_mobile':
        return <PhoneOutlined style={{ fontSize: 20, color: '#52c41a' }} />
      case 'telco_internet':
        return <GlobalOutlined style={{ fontSize: 20, color: '#722ed1' }} />
      default:
        return <FileTextOutlined style={{ fontSize: 20 }} />
    }
  }

  const getAccountDetail = () => {
    if (phoneNumber) return phoneNumber
    if (ipAddress) return ipAddress
    if (accountNumber) return accountNumber
    return '-'
  }

  return (
    <Modal
      title={
        <Space>
          <MailOutlined style={{ color: '#1890ff' }} />
          <span>ยืนยันการส่งหมายเรียกทางอีเมล์</span>
        </Space>
      }
      open={visible}
      onCancel={onCancel}
      footer={[
        <Button key="cancel" onClick={onCancel} disabled={sending}>
          ยกเลิก
        </Button>,
        <Button
          key="submit"
          type="primary"
          onClick={handleSubmit}
          loading={sending}
          icon={<MailOutlined />}
        >
          ส่งอีเมล์
        </Button>,
      ]}
      width={600}
    >
      <Spin spinning={sending} tip="กำลังส่งอีเมล์...">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <Alert
            message="ระบบจะสร้างไฟล์ PDF และส่งหมายเรียกพยานเอกสารไปยังอีเมล์ที่ระบุ"
            type="info"
            showIcon
          />

          <div style={{ padding: '16px', background: '#fafafa', borderRadius: '8px' }}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Space>
                {getAccountTypeIcon()}
                <div>
                  <Text type="secondary" style={{ fontSize: '12px', display: 'block' }}>
                    {getAccountTypeLabel()}
                  </Text>
                  <Text strong style={{ fontSize: '16px' }}>
                    {providerName}
                  </Text>
                </div>
              </Space>

              {(phoneNumber || ipAddress || accountNumber) && (
                <div>
                  <Text type="secondary" style={{ fontSize: '12px', display: 'block' }}>
                    {phoneNumber ? 'หมายเลขโทรศัพท์' : ipAddress ? 'IP Address' : 'เลขบัญชี'}
                  </Text>
                  <Text style={{ fontSize: '14px' }}>{getAccountDetail()}</Text>
                </div>
              )}

              <div>
                <Text type="secondary" style={{ fontSize: '12px', display: 'block' }}>
                  เลขที่หมายเรียก
                </Text>
                <Text style={{ fontSize: '14px' }}>{documentNumber || '-'}</Text>
              </div>
            </Space>
          </div>

          <Form
            form={form}
            layout="vertical"
            initialValues={{
              recipientEmail: defaultEmail || ''
            }}
          >
            <Form.Item
              label="อีเมล์ผู้รับ"
              name="recipientEmail"
              rules={[
                { required: true, message: 'กรุณากรอกอีเมล์ผู้รับ' },
                { type: 'email', message: 'กรุณากรอกอีเมล์ให้ถูกต้อง' }
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="example@company.com"
                size="large"
                disabled={sending}
              />
            </Form.Item>

            {/* แสดงตัวเลือกอายัดบัญชีเฉพาะ Non-Bank */}
            {accountType === 'non_bank' && (
              <Form.Item
                name="freezeAccount"
                valuePropName="checked"
                style={{ marginBottom: 0 }}
              >
                <Checkbox disabled={sending}>
                  อายัดบัญชี (เพิ่มข้อความให้อายัดบัญชีในหมายเรียก)
                </Checkbox>
              </Form.Item>
            )}
          </Form>

          <Alert
            message={
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <Text strong>อีเมล์จะประกอบด้วย:</Text>
                </div>
                <ul style={{ margin: 0, paddingLeft: '20px' }}>
                  <li>เนื้อหาอีเมล์พร้อมรายละเอียดหมายเรียก</li>
                  <li>ไฟล์ PDF หมายเรียกพยานเอกสารแนบ</li>
                  <li>ข้อมูลติดต่อกลับ (โทร, อีเมล์)</li>
                </ul>
              </div>
            }
            type="warning"
            showIcon
          />
        </Space>
      </Spin>
    </Modal>
  )
}

export default EmailConfirmationModal
