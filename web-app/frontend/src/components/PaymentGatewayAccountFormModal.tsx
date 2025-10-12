import { useEffect, useState } from 'react'
import { Modal, Form, Input, DatePicker, Select, Switch, Row, Col, message, Button, Table, Popconfirm } from 'antd'
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import 'dayjs/locale/th'
import api from '../services/api'

const { TextArea } = Input
const { Option } = Select
const { RangePicker } = DatePicker

interface TransferDetail {
  key: string
  source_bank_id?: number
  source_bank_name?: string
  source_account_number?: string
  source_account_name?: string
  transfer_date?: string
  transfer_time?: string
  transfer_amount?: string
  note?: string
  _existing_id?: number  // ID ของรายการที่มีอยู่แล้วในฐานข้อมูล
}

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
    // รูปแบบ: "4 ส.ค. 68 - 6 ส.ค. 68"
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

interface PaymentGatewayAccountFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function PaymentGatewayAccountFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: PaymentGatewayAccountFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord && !editingRecord._is_new_from_cfr
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null)
  const isFromCfr = !!editingRecord && editingRecord._is_new_from_cfr
  const [paymentGateways, setPaymentGateways] = useState<any[]>([])
  const [banks, setBanks] = useState<any[]>([])
  const [transferDetails, setTransferDetails] = useState<TransferDetail[]>([])
  const MAX_TRANSFERS = 5
  const MIN_TRANSFERS = 1  // ต้องมีอย่างน้อย 1 รายการ

  // Helper function: หาชื่อธนาคารจาก ID
  const getBankNameById = (bankId?: number): string => {
    if (!bankId) return ''
    const bank = banks.find(b => b.id === bankId)
    return bank?.bank_name || ''
  }

  // ดึงรายการโอนที่มีอยู่แล้วในฐานข้อมูล
  const fetchExistingTransactions = async (paymentGatewayAccountId: number) => {
    try {
      const response = await api.get(`/payment-gateway-transactions/?payment_gateway_account_id=${paymentGatewayAccountId}`)
      const transactions = response.data
      
      console.log('📦 Fetched existing transactions:', transactions)
      
      if (transactions && transactions.length > 0) {
        // แปลงข้อมูลเป็น TransferDetail format
        const formattedTransactions: TransferDetail[] = transactions.map((t: any) => ({
          key: `existing-${t.id}`,
          source_bank_id: t.source_bank_id,
          source_bank_name: getBankNameById(t.source_bank_id) || t.source_bank_name,
          source_account_number: t.source_account_number,
          source_account_name: t.source_account_name,
          transfer_date: t.transfer_date,
          transfer_time: t.transfer_time,
          transfer_amount: t.transfer_amount?.toString(),
          note: t.note,
          _existing_id: t.id,
        }))
        
        console.log('✅ Formatted transactions:', formattedTransactions)
        setTransferDetails(formattedTransactions)
        
        message.info(`พบรายการโอนที่บันทึกไว้แล้ว ${formattedTransactions.length} รายการ`)
      }
    } catch (error) {
      console.error('Error fetching transactions:', error)
    }
  }

  // ดึงรายชื่อ Payment Gateway Payment Gateway
  useEffect(() => {
    const fetchPaymentGateways = async () => {
      try {
        const response = await api.get('/payment-gateways/')
        setPaymentGateways(response.data)
      } catch (error) {
        console.error('Error fetching payment gateways:', error)
      }
    }
    if (visible) {
      fetchPaymentGateways()
    }
  }, [visible])

  // ดึงรายชื่อธนาคาร
  useEffect(() => {
    const fetchBanks = async () => {
      try {
        const response = await api.get('/banks/')
        setBanks(response.data)
      } catch (error) {
        console.error('Error fetching banks:', error)
      }
    }
    if (visible) {
      fetchBanks()
    }
  }, [visible])

  useEffect(() => {
    if (visible) {
      if (editingRecord) {
        // แก้ไข - ใส่ค่าเดิม
        console.log('🔍 Editing record:', editingRecord)
        console.log('🏦 Bank ID from record:', editingRecord.bank_id)
        console.log('💳 Payment Gateway ID from record:', editingRecord.payment_gateway_id)
        
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
          const parsedDateRange = parseThaiDateRange(editingRecord.time_period)
          if (parsedDateRange) {
            setDateRange(parsedDateRange)
          } else {
            setDateRange(null)
          }
        } else {
          setDateRange(null)
        }
        
        // ดึงรายการโอนที่มีอยู่แล้ว (ถ้ามี)
        if (editingRecord.id) {
          fetchExistingTransactions(editingRecord.id)
        }
      } else {
        // เพิ่มใหม่ - reset form
        form.resetFields()
        setDateRange(null) // reset date range
        setTransferDetails([]) // reset transfer list
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
    } else {
      // เมื่อปิด modal ให้ reset
      setTransferDetails([])
    }
  }, [visible, editingRecord, criminalCaseId, form])

  const handleSubmit = async () => {
    try {
      // Validate: ต้องมีรายการโอนอย่างน้อย 1 รายการ
      if (transferDetails.length < MIN_TRANSFERS) {
        message.error(`กรุณาเพิ่มรายละเอียดการโอนอย่างน้อย ${MIN_TRANSFERS} รายการ`)
        return
      }

      const values = await form.validateFields()

      console.log('📝 Form values:', values)
      console.log('🏦 Bank ID:', values.bank_id)
      console.log('💳 Payment Gateway ID:', values.payment_gateway_id)

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

      console.log('📤 Payload:', payload)

      let paymentGatewayAccountId = editingRecord?.id

      try {
        if (isEdit) {
          const response = await api.put(`/payment-gateway-accounts/${editingRecord.id}`, payload)
          console.log('✅ Updated account:', response.data)
          message.success('แก้ไขบัญชี Payment Gateway สำเร็จ')
        } else {
          const response = await api.post('/payment-gateway-accounts/', payload)
          paymentGatewayAccountId = response.data.id
          console.log('✅ Created account:', response.data)
          message.success('เพิ่มบัญชี Payment Gateway สำเร็จ')
        }
      } catch (err: any) {
        // ถ้า token หมดอายุ (401) จะถูก handle โดย interceptor
        // แต่ถ้าเป็น error อื่นๆ ให้แสดง error
        if (err.message === 'Session หมดอายุ กรุณา login ใหม่') {
          message.error('Session หมดอายุ กรุณา login ใหม่อีกครั้ง')
          // interceptor จะ redirect ไป login อัตโนมัติ
          return
        }
        throw err // ส่งต่อไปให้ catch block นอกจัดการ
      }

      // ถ้ามีรายการโอน ให้บันทึกเฉพาะรายการใหม่
      if (transferDetails.length > 0 && paymentGatewayAccountId) {
        let successCount = 0
        let failCount = 0

        for (const transfer of transferDetails) {
          // ตรวจสอบว่าเป็นรายการเดิมหรือรายการใหม่
          if (transfer._existing_id) {
            // รายการเดิม - ข้ามไป (ไม่ต้อง POST ซ้ำ)
            console.log('⏭️ Skipping existing transaction:', transfer._existing_id)
            continue
          }
          
          // รายการใหม่ - ให้ POST
          const transactionPayload = {
            criminal_case_id: criminalCaseId,
            payment_gateway_account_id: paymentGatewayAccountId,
            source_bank_id: transfer.source_bank_id,
            source_account_number: transfer.source_account_number,
            source_account_name: transfer.source_account_name,
            destination_bank_id: values.bank_id,
            destination_account_number: values.account_number,
            destination_account_name: values.account_name,
            transfer_date: transfer.transfer_date,
            transfer_time: transfer.transfer_time,
            transfer_amount: transfer.transfer_amount,
            note: transfer.note,
          }

          try {
            console.log('➕ Adding new transaction:', transactionPayload)
            await api.post('/payment-gateway-transactions/', transactionPayload)
            successCount++
          } catch (err: any) {
            if (err.message === 'Session หมดอายุ กรุณา login ใหม่') {
              message.error('Session หมดอายุ กรุณา login ใหม่อีกครั้ง')
              return
            }
            failCount++
            console.error('Error saving transaction:', err)
          }
        }

        if (successCount > 0) {
          message.success(`เพิ่มรายละเอียดการโอน ${successCount} รายการใหม่สำเร็จ`)
        } else if (successCount === 0 && failCount === 0) {
          // ไม่มีรายการใหม่ (ทุกรายการเป็นรายการเดิม)
          console.log('ℹ️ No new transactions to add')
        }
        if (failCount > 0) {
          message.warning(`ไม่สามารถบันทึกรายการโอน ${failCount} รายการได้`)
        }
      }

      form.resetFields()
      setTransferDetails([])
      onClose(true)
    } catch (err: any) {
      if (err.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else if (err.message && err.message.includes('Session หมดอายุ')) {
        // Token หมดอายุ - interceptor จะ redirect
        return
      } else {
        const errorMsg = err.response?.data?.detail || (isEdit ? 'ไม่สามารถแก้ไขบัญชี Payment Gatewayได้' : 'ไม่สามารถเพิ่มบัญชี Payment Gatewayได้')
        message.error(errorMsg)
        console.error('Error:', err)
      }
    }
  }

  const handleAddTransfer = () => {
    // ตรวจสอบจำนวนรายการ
    if (transferDetails.length >= MAX_TRANSFERS) {
      message.warning(`สามารถเพิ่มรายการโอนได้สูงสุด ${MAX_TRANSFERS} รายการเท่านั้น`)
      return
    }

    const values = form.getFieldsValue()
    
    // Validate ข้อมูลการโอน
    if (!values.source_bank_id) {
      message.error('กรุณาเลือกธนาคารต้นทาง')
      return
    }
    if (!values.transfer_date || !values.transfer_amount) {
      message.error('กรุณากรอกวันที่โอนและจำนวนเงิน')
      return
    }

    // หาชื่อธนาคาร
    const selectedBank = banks.find(b => b.id === values.source_bank_id)
    
    const newTransfer: TransferDetail = {
      key: `${Date.now()}`,
      source_bank_id: values.source_bank_id,
      source_bank_name: selectedBank?.bank_name,
      source_account_number: values.source_account_number,
      source_account_name: values.source_account_name,
      transfer_date: values.transfer_date ? values.transfer_date.format('YYYY-MM-DD') : undefined,
      transfer_time: values.transfer_time,
      transfer_amount: values.transfer_amount,
      note: values.transfer_note,
    }

    setTransferDetails([...transferDetails, newTransfer])
    
    // Reset ฟิลด์การโอน
    form.setFieldsValue({
      source_bank_id: undefined,
      source_account_number: '',
      source_account_name: '',
      transfer_date: null,
      transfer_time: '',
      transfer_amount: '',
      transfer_note: '',
    })
    
    message.success('เพิ่มรายการโอนเรียบร้อย')
  }

  const handleDeleteTransfer = async (key: string) => {
    const transfer = transferDetails.find(item => item.key === key)
    
    // ถ้าเป็นรายการเดิมที่บันทึกในฐานข้อมูลแล้ว ต้องลบจากฐานข้อมูลด้วย
    if (transfer?._existing_id) {
      try {
        await api.delete(`/payment-gateway-transactions/${transfer._existing_id}`)
        console.log('🗑️ Deleted existing transaction from database:', transfer._existing_id)
        message.success('ลบรายการโอนจากฐานข้อมูลเรียบร้อย')
      } catch (err) {
        message.error('ไม่สามารถลบรายการโอนจากฐานข้อมูลได้')
        console.error('Error deleting transaction:', err)
        return // ถ้าลบไม่สำเร็จ ไม่ต้องลบจาก UI
      }
    } else {
      message.success('ลบรายการโอนเรียบร้อย')
    }
    
    // ลบจาก UI
    setTransferDetails(transferDetails.filter(item => item.key !== key))
  }

  const handleCancel = () => {
    form.resetFields()
    setDateRange(null)
    setTransferDetails([])
    onClose(false)
  }

  return (
    <Modal
      title={isEdit ? 'แก้ไขบัญชี Payment Gateway' : 'เพิ่มบัญชี Payment Gateway'}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      width={1200}
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

          <Col span={12}>
            <Form.Item
              label="ชื่อ Payment Gateway"
              name="payment_gateway_id"
              rules={[{ required: true, message: 'กรุณาเลือก Payment Gateway' }]}
            >
              <Select
                placeholder="เลือก Payment Gateway"
                showSearch
                filterOption={(input, option) =>
                  (option?.children?.toString() || '')
                    .toLowerCase()
                    .includes(input.toLowerCase())
                }
              >
                {paymentGateways.map((pg) => (
                  <Option key={pg.id} value={pg.id}>
                    {pg.company_name}
                  </Option>
                ))}
              </Select>
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              label="ธนาคาร"
              name="bank_id"
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
                {banks.map((bank) => (
                  <Option key={bank.id} value={bank.id}>
                    {bank.bank_name}
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

          {/* รายละเอียดการโอนเงิน (บังคับ) */}
          <Col span={24}>
            <h4 style={{ marginTop: 16, marginBottom: 12, color: '#1890ff' }}>
              รายละเอียดการโอนเงิน (บังคับ อย่างน้อย 1 รายการ)
            </h4>
          </Col>

          <>
              {/* บัญชีต้นทาง */}
              <Col span={24}>
                <h4 style={{ marginTop: 8, marginBottom: 8, color: '#52c41a' }}>
                  1. บัญชีต้นทาง (Source Account)
                </h4>
              </Col>

              <Col span={8}>
                <Form.Item label="ธนาคาร" name="source_bank_id">
                  <Select
                    placeholder="เลือกธนาคาร"
                    showSearch
                    filterOption={(input, option) =>
                      (option?.children?.toString() || '')
                        .toLowerCase()
                        .includes(input.toLowerCase())
                    }
                  >
                    {banks.map((bank) => (
                      <Option key={bank.id} value={bank.id}>
                        {bank.bank_name}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
              </Col>

              <Col span={8}>
                <Form.Item label="เลขที่บัญชี" name="source_account_number">
                  <Input placeholder="เลขที่บัญชีต้นทาง" />
                </Form.Item>
              </Col>

              <Col span={8}>
                <Form.Item label="ชื่อบัญชี" name="source_account_name">
                  <Input placeholder="ชื่อบัญชีต้นทาง" />
                </Form.Item>
              </Col>

              {/* บัญชีปลายทาง */}
              <Col span={24}>
                <h4 style={{ marginTop: 8, marginBottom: 8, color: '#ff4d4f' }}>
                  2. บัญชีปลายทาง (Destination Account)
                </h4>
                <p style={{ fontSize: '13px', color: '#888', marginTop: -4, marginBottom: 8 }}>
                  ข้อมูลจะถูกดึงจากข้อมูลด้านบนโดยอัตโนมัติ
                </p>
              </Col>

              <Col span={8}>
                <Form.Item label="ธนาคาร">
                  <Input 
                    disabled 
                    value={
                      form.getFieldValue('bank_id')
                        ? banks.find(b => b.id === form.getFieldValue('bank_id'))?.bank_name || '-'
                        : '-'
                    } 
                  />
                </Form.Item>
              </Col>

              <Col span={8}>
                <Form.Item label="เลขที่บัญชี">
                  <Input disabled value={form.getFieldValue('account_number') || '-'} />
                </Form.Item>
              </Col>

              <Col span={8}>
                <Form.Item label="ชื่อบัญชี">
                  <Input disabled value={form.getFieldValue('account_name') || '-'} />
                </Form.Item>
              </Col>

              {/* ข้อมูลการโอน */}
              <Col span={24}>
                <h4 style={{ marginTop: 8, marginBottom: 8, color: '#1890ff' }}>
                  3. ข้อมูลการโอนเงิน
                </h4>
              </Col>

              <Col span={8}>
                <Form.Item label="วันที่โอน" name="transfer_date">
                  <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
                </Form.Item>
              </Col>

              <Col span={8}>
                <Form.Item label="เวลาที่โอน" name="transfer_time">
                  <Input placeholder="เช่น 14:30" />
                </Form.Item>
              </Col>

              <Col span={8}>
                <Form.Item label="จำนวนเงิน (บาท)" name="transfer_amount">
                  <Input type="number" placeholder="เช่น 50000" />
                </Form.Item>
              </Col>

              <Col span={24}>
                <Form.Item label="หมายเหตุการโอน" name="transfer_note">
                  <TextArea rows={2} placeholder="หมายเหตุเพิ่มเติมเกี่ยวกับการโอนเงิน..." />
                </Form.Item>
              </Col>

              {/* ปุ่มเพิ่มรายการโอน */}
              <Col span={24} style={{ textAlign: 'center', marginTop: 16 }}>
                <Button
                  type="dashed"
                  icon={<PlusOutlined />}
                  onClick={handleAddTransfer}
                  disabled={transferDetails.length >= MAX_TRANSFERS}
                  block
                  size="large"
                  style={{
                    borderColor: transferDetails.length >= MAX_TRANSFERS ? '#d9d9d9' : '#1890ff',
                    color: transferDetails.length >= MAX_TRANSFERS ? '#999' : '#1890ff',
                  }}
                >
                  เพิ่มรายการโอนนี้ ({transferDetails.length}/{MAX_TRANSFERS})
                </Button>
                {transferDetails.length >= MAX_TRANSFERS && (
                  <p style={{ color: '#ff4d4f', fontSize: '13px', marginTop: 8 }}>
                    เพิ่มรายการโอนได้สูงสุด {MAX_TRANSFERS} รายการเท่านั้น
                  </p>
                )}
              </Col>

              {/* ตารางแสดงรายการโอนที่เพิ่มแล้ว */}
              {transferDetails.length > 0 && (
                <Col span={24} style={{ marginTop: 16 }}>
                  <h4 style={{ marginBottom: 8, color: '#52c41a' }}>
                    รายการโอนที่เพิ่มแล้ว ({transferDetails.length} รายการ)
                  </h4>
                  <Table
                    dataSource={transferDetails}
                    size="small"
                    pagination={false}
                    bordered
                    columns={[
                      {
                        title: '#',
                        key: 'index',
                        width: 50,
                        render: (_, __, index) => index + 1,
                      },
                      {
                        title: 'ธนาคารต้นทาง',
                        dataIndex: 'source_bank_name',
                        key: 'source_bank_name',
                        width: 200,
                      },
                      {
                        title: 'เลขบัญชีต้นทาง',
                        dataIndex: 'source_account_number',
                        key: 'source_account_number',
                        width: 150,
                      },
                      {
                        title: 'วันที่โอน',
                        dataIndex: 'transfer_date',
                        key: 'transfer_date',
                        width: 120,
                        render: (date) => date ? dayjs(date).format('DD/MM/YYYY') : '-',
                      },
                      {
                        title: 'เวลา',
                        dataIndex: 'transfer_time',
                        key: 'transfer_time',
                        width: 80,
                      },
                      {
                        title: 'จำนวนเงิน',
                        dataIndex: 'transfer_amount',
                        key: 'transfer_amount',
                        width: 120,
                        render: (amount) => amount ? `${parseFloat(amount).toLocaleString()} บาท` : '-',
                      },
                      {
                        title: 'การจัดการ',
                        key: 'action',
                        width: 80,
                        render: (_, record) => (
                          <Popconfirm
                            title="ยืนยันการลบรายการนี้?"
                            onConfirm={() => handleDeleteTransfer(record.key)}
                            okText="ลบ"
                            cancelText="ยกเลิก"
                          >
                            <Button
                              danger
                              size="small"
                              icon={<DeleteOutlined />}
                            >
                              ลบ
                            </Button>
                          </Popconfirm>
                        ),
                      },
                    ]}
                  />
                </Col>
              )}
            </>

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

          {/* บันทึกเพิ่มเติม */}
          <Col span={24}>
            <Form.Item label="บันทึกเพิ่มเติม" name="notes">
              <TextArea rows={3} placeholder="บันทึกข้อมูลเพิ่มเติม..." />
            </Form.Item>
          </Col>

          {/* หมายเหตุที่อยู่ */}
          <Col span={24}>
            <p style={{ marginTop: 8, color: '#888', fontSize: '13px' }}>
              📍 หมายเหตุ: ที่อยู่จะดึงจากข้อมูลสำนักงานของผู้ให้บริการโดยอัตโนมัติ
            </p>
          </Col>
        </Row>
      </Form>
    </Modal>
  )
}
